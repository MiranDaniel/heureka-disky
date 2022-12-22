"""
    Copyright (C) 2022 MiranDaniel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import requests_cache
from datetime import timedelta
from bs4 import BeautifulSoup
from disk import Disk
import pickle
from datasize import DataSize
import time


internal = "https://pevne-disky.heureka.cz/"
external = "https://pevne-disky-externi.heureka.cz/"

pageQuery = "?f="
sleep = 1 # seconds

session = requests_cache.CachedSession(".cache", expire_after=timedelta(hours=0.1))


def humanReadable(size, precision=2):
    suffixes = [" B", " KB", " MB", " GB", " TB"]
    suffixIndex = 0
    while size > 1000 and suffixIndex < 4:
        suffixIndex += 1
        size = size / 1000.0
    return "%.*f%s" % (precision, size, suffixes[suffixIndex])


def getPage(endpoint, index):
    r = session.get(f"{endpoint}{pageQuery}{index}")
    print(f"{r.url=}")

    if r.status_code == 410:
        return None
    elif r.status_code == 429:
        print("Ratelimit hit.")
        quit(429)

    time.sleep(sleep)

    return r.text


def parsePage(page):
    soup = BeautifulSoup(page, features="html.parser")
    items = soup.find_all("section", class_="c-product")

    disks = []

    for item in items:
        disk = Disk()

        name = item.find_all("h3", class_="c-product__title")
        if len(name) > 0:
            name = name[0].text
        else:
            name = None

        rating = item.find("span", class_="c-star-rating__rating-value")
        if rating is not None:
            rating = rating.text

        url = item.find("a", class_="c-product__link")
        if url is not None:
            url = url.get("href")

        price = item.find_all("a", class_="c-product__price")
        if price == None:
            continue
        if len(price) > 0:
            price = price[0].text
        else:
            price = None

        ul = item.find_all(
            "li",
            class_="u-base c-product__attributes-list__item c-product__attributes-list__item--has-following",
        )
        ul += item.find_all("li", class_="u-base c-product__attributes-list__item")
        for li in ul:
            setTable = {
                "Rozhraní": "interface",
                "Kapacita": "capacity",
                "Formát disku": "size",
                "Otáčky": "rpm",
                "Max. rychlost čtení [MB/s]": "rspeed",
                "Max. rychlost zápisu [MB/s]": "wspeed",
            }
            title = li.get("title")
            if title in setTable:
                disk.__setattr__(setTable[title], li.text)

        disk.name = name
        disk.rating = rating
        disk.price = price
        disk.url = url

        if not disk.isValid():
            continue

        disk.capacity = DataSize(disk.capacity.replace(" ", ""))
        disk.capacityRaw = str(round(disk.capacity / 1_000_000_000_000, 2)) + " TB"

        if not disk.rspeed is None:
            disk.rspeed = humanReadable(
                DataSize(disk.rspeed.replace(" ", "").replace("/s", ""))
            )

        if not disk.wspeed is None:
            disk.wspeed = humanReadable(
                DataSize(disk.wspeed.replace(" ", "").replace("/s", ""))
            )

        if not disk.rpm is None:
            disk.rpm = disk.rpm.replace(" ot/min", "").replace(" ", "")

        disk.price = (
            price.replace("\xa0", "").replace("Kč", "").split(" – ")
        )  # stupid character
        disk.price = [round(float(i)) for i in disk.price]

        disks.append(disk)

    print(f"Found {len(disks)} disks!")
    return disks


disks = []

print("Tento program je rozšiřován v naději, že bude užitečný, avšak BEZ JAKÉKOLIV ZÁRUKY. Neposkytují se ani odvozené záruky PRODEJNOSTI anebo VHODNOSTI PRO URČITÝ ÚČEL. Další podrobnosti hledejte v Obecné veřejné licenci GNU.")

for i in range(1, 1000):
    page = getPage(internal, i)
    if page == None:
        break

    result = parsePage(page)
    if len(result) == 0:
        break
    disks += result


for i in range(1, 1000):
    page = getPage(external, i)
    if page == None:
        break

    result = parsePage(page)
    if len(result) == 0:
        break
    disks += result

with open(".cache.pickle", "wb+") as f:
    pickle.dump(disks, f)
