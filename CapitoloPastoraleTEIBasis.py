import xml.etree.ElementTree as ET
from xml.dom import minidom

# Open txt file with CP text and read all lines
with open('CapitoloPastorale.txt', encoding='utf8') as f:
    linesCP = f.readlines()

# Build main structure for XML document
# For information about etree see: https://docs.python.org/3/library/xml.etree.elementtree.html
root = ET.Element("root")
doc = ET.SubElement(root, "div2")
start = ET.SubElement(doc, "lg")

# Create container for terzina data
terzinaList = list()
terzinaSingle = list()

counter = 0

# Go through all lines that have been read from TXT and manage terzinas
for line in linesCP:
    if counter < 3:
        terzinaSingle.append(line)
        counter += 1
    if counter == 3:
        terzinaList.append(terzinaSingle)
        counter = 0
        terzinaSingle = list()

# Go through all terzina built beforehands and wirte them into XML tree
for terzina in terzinaList:
    lg = ET.SubElement(doc, "lg")
    for terzLine in terzina:
        ET.SubElement(lg, "l").text = terzLine

# Write XML structure to file
tree = ET.ElementTree(root)
# Parse XML tree into pretty string, using this hint:
# https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file
xmlstr = minidom.parseString(ET.tostring(
    tree.getroot(), encoding='utf-8')).toprettyxml(indent="   ")
file = open("CapitoloPastorale.xml", "w", encoding="utf-8")
file.write(xmlstr)
