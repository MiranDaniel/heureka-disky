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


from jinja2 import Environment, FileSystemLoader
import pickle
import htmlmin

with open(".cache.pickle", "rb+") as f:
    disks = pickle.load(f)

disks = sorted(disks, key=lambda x: x.price[0] / x.capacity)

interfaces = set([i.interface for i in disks if not i.interface is None])
interfaces = sorted(list(interfaces))

speed = set([i.rpm for i in disks if not i.rpm is None])
speed = sorted(list(speed))

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.html")
out = template.render(
    disks=disks, interfaces=interfaces, speed=speed
)


f = htmlmin.minify(
    out, remove_comments=True, remove_empty_space=True
)
with open("output.html", "w") as fh:
    fh.write(f)
