#!/bin/pyhton3

import sys
import re
import lxml.etree as etree
import subprocess

namesfile = sys.argv[1]

names=open(namesfile).readlines()

def altersvg(file,name,role):
    svg = open(file, mode="rb").read()
    root = etree.fromstring(svg)
    print(root)
    root.findall(".//text[@inkscape:label='Name']",root.nsmap)[0][0].text=name
    root.findall(".//text[@inkscape:label='Role']",root.nsmap)[0][0].text=role
    return(etree.tostring(root, encoding='UTF-8'))



os.mkdir("tmp")
os.mkdir("tmp")
for name in names:
    parts = name.split(":")
    print(parts)
    name = parts[0].strip()
    role = parts[1].strip()
    customsvg = altersvg("badge.svg",name,role)
    #svg2png(bytestring=customsvg,write_t0='tmp.png')

    if os.name == 'nt':
        inkscape="c://Program Files/Inkscape/inkscape.exe"
    else:
        inkscape="inkscape"

    writesvg = open("tmp/"+name+".svg","wb")
    writesvg.write(customsvg)
    writesvg.close()
    subprocess.call([inkscape, "-f", "tmp/"+name+".svg", "-e", "out/"+name+".png", "-d", "600"])
