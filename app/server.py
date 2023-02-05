"""
    Copyright (C) 2023 MiranDaniel

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


from flask import Flask, render_template, request, flash
from flask_compress import Compress
import pickle
import requests
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from .scrape import scrape
import threading
import secrets

compress = Compress()
app = Flask(__name__, template_folder=".")
app.secret_key = secrets.token_hex(256)
compress.init_app(app)

tailwind = requests.get("https://cdn.tailwindcss.com").text

lock = False


@app.route("/tailwind.css")
@compress.compressed()
def lazy_tailwind():
    return tailwind


@app.route('/')
@compress.compressed()
def hello_world():
    global lock
    try:
        with open(".cache.pickle", "rb+") as f:
            disks = pickle.load(f)
    except FileNotFoundError:
        disks = []
        if not lock:
            p = threading.Thread(target=scrape)
            p.start()
            lock = True
            flash("No data scraped yet, this can take a minute...")
        else:
            flash("Scraping data, please wait...")

    disks = sorted(disks, key=lambda x: x.price[0] / x.capacity)

    interfaces = set([i.interface for i in disks if not i.interface is None])
    interfaces = sorted(list(interfaces))

    speed = set([i.rpm for i in disks if not i.rpm is None])
    speed = sorted(list(speed))

    filterIf = request.args.get("if")
    if not filterIf in ["", None]:
        filterIf = filterIf.split(",")
    else:
        filterIf = interfaces.copy()
        filterIf.append(None)

    filterRpm = request.args.get("rpm")
    if not filterRpm in ["", None]:
        filterRpm = filterRpm.split(",")
    else:
        filterRpm = speed.copy()
        filterRpm.append(None)

    filterMin = request.args.get("min")
    if filterMin in ["", None]:
        filterMin = 0
    else:
        filterMin = int(filterMin)
    filterMax = request.args.get("max")
    if filterMax in ["", None]:
        filterMax = 1024
    else:
        filterMax = int(filterMax)

    filterSearch = request.args.get("search")

    newDisks = []
    for i in disks:
        if not i.interface in filterIf:
            continue
        if not i.rpm in filterRpm:
            continue
        if not (i.capacityTb >= filterMin and i.capacityTb <= filterMax):
            continue
        if not filterSearch is None:
            if not filterSearch.lower() in i.name.lower():
                continue
        newDisks.append(i)

    lastScrape = "Unknown"
    try:
        with open(".time", "rt") as f:
            lastScrape = f.read()
    except FileNotFoundError:
        print("No .time file")

    return render_template("template.html", disks=newDisks, interfaces=interfaces, speed=speed, results=len(newDisks), totalResults=len(disks), lastUpdate=datetime.datetime.utcnow().isoformat(), lastScrape=lastScrape)


try:
    with open(".cache.pickle", "rb+") as f:
        disks = pickle.load(f)
except FileNotFoundError:
    if not lock:
        p = threading.Thread(target=scrape)
        p.start()
        lock = True


scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape, trigger="interval", minutes=30, id="scrape")
scheduler.start()

atexit.register(lambda: scheduler.shutdown())
