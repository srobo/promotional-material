#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

import lxml.etree as etree
from itertools import islice


def chunk(it, size):
    it = iter(it)
    while slice := tuple(islice(it, size)):
        yield slice


namesfile = sys.argv[1]

names = open(namesfile).readlines()


def alter_badge_svg(file, name, role, pronouns):
    svg = open(file, mode="rb").read()
    root = etree.fromstring(svg)
    root.findall(".//text[@id='Name']", root.nsmap)[0][0].text = name
    root.findall(".//text[@id='Role']", root.nsmap)[0][0].text = role
    root.findall(".//text[@id='Pronouns']", root.nsmap)[0][0].text = pronouns
    return(etree.tostring(root, encoding='UTF-8'))


def alter_badge_template(file, badges):
    svg = open(file, mode="rb").read()
    print(svg)
    root = etree.fromstring(svg)
    for i, badge in enumerate(badges):
        print(i + 1, badge)
        embedded_root = etree.parse("tmp/" + badge).getroot()  # load svg
        print(root.findall(f".//rect[@id='Badge{i+1}']", root.nsmap)[0])
        embed_parent = root.findall(f".//rect[@id='Badge{i+1}']/..", root.nsmap)[0]
        embed_child = embed_parent.findall(f".//rect[@id='Badge{i+1}']", root.nsmap)[0]
        embed_index = list(embed_parent).index(embed_child)

        for field in ['x', 'y', 'width', 'height']:  # set x, y, height & width from the placeholder
            embedded_root.set(field, embed_child.get(field))

        embed_parent[embed_index] = embedded_root  # replace element with svg
    return(etree.tostring(root, encoding='UTF-8'))


if not os.path.exists("tmp"):
    os.mkdir("tmp")
if not os.path.exists("out"):
    os.mkdir("out")
for name in names:
    parts = name.split(":")
    print(parts)
    name = parts[0].strip()
    role = parts[1].strip()
    pronouns = parts[2].strip()
    customsvg = alter_badge_svg("badge-plain.svg", name, role, pronouns)
    # svg2png(bytestring=customsvg,write_t0='tmp.png')

    if os.name == 'nt':
        inkscape = "c://Program Files/Inkscape/bin/inkscape.exe"
    else:
        inkscape = "inkscape"

    writesvg = open(f"tmp/{name}.svg", "wb")
    writesvg.write(customsvg)
    writesvg.close()
    subprocess.call([
        inkscape,
        "-p",
        f"tmp/{name}.svg",
        "-o",
        f"out/{name}.png",
        "-d",
        "600",
    ])


# split names into chunks with max size of 8
for i, badge_group in enumerate(chunk(names, 8)):
    # place badges into 'Badgel-Layout-Plain.svg'
    badges = []
    for name in badge_group:
        parts = name.split(":")
        name = parts[0].strip()
        badges.append(f"{name}.svg")
    print(badges)
    custom_svg = alter_badge_template("Badge-Layout-Plain.svg", badges)
    write_svg = open(f"tmp/{i}.svg", "wb")
    write_svg.write(custom_svg)
    write_svg.close()
    subprocess.call([
        inkscape,
        f"tmp/{i}.svg",
        "-o",
        f"out/{i}.pdf",
    ])
