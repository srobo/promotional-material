#!/bin/pyhton3

import sys
import re
import lxml.etree as ET
import subprocess
#from cairosvg import svg2png

namesfile = sys.argv[1]

names=open(namesfile).readlines()

def altersvg(file,name,role):
    svg = open(file, mode="rb").read()
    root = ET.fromstring(svg)
    print(root)
    root.findall(".//text[@inkscape:label='Name']",root.nsmap)[0][0].text=name
    root.findall(".//text[@inkscape:label='Role']",root.nsmap)[0][0].text=role
    return(ET.tostring(root, encoding='UTF-8'))



subprocess.call(["mkdir", "tmp"])
subprocess.call(["mkdir", "out"])
for name in names:
    parts = name.strip().split(":")
    print(parts)
    customsvg = altersvg("badge.svg",parts[0],parts[1])
    #svg2png(bytestring=customsvg,write_t0='tmp.png')

    name = parts[0]
    writesvg = open("tmp/"+name+".svg","wb")
    writesvg.write(customsvg)
    writesvg.close()
    subprocess.call(["c://Program Files/Inkscape/inkscape.exe", "-f", "tmp/"+name+".svg", "-e", "out/"+name+".png", "-d", "600"])
