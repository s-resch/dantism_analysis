import treetaggerwrapper
import xml.etree.ElementTree as ET
from xml.dom import minidom
from string import punctuation

# Read text file, e.g. Asino and prepare tagger – change file name to address text needed
# For information about etree see: https://docs.python.org/3/library/xml.etree.elementtree.html
treeMachiavelli = ET.parse("Material/Decennali.xml")
tagger = treetaggerwrapper.TreeTagger(TAGLANG='it')

# Get all <l> elements representing lines
elems = treeMachiavelli.findall('//l')

# Prepare set to check for punctuation
punctuationSet = set(punctuation)

# Loop through all lines to extract text and run treetagger on this text
# Annotate lemma information using XML-attribute “lemma” in <w> tag
# Write punctuation into <pc> tag according to TEI
# Maintain complete verse in <l> tag, so we can easily perform a manual review
for elem in elems:
    if elem.text == None:
        continue
    # Call tagger for element and get tags
    tags = tagger.tag_text(elem.text)
    # Loop through all tags obtained by tagger and write lemma information into our XML tree
    for tag in tags:
        elements = tag.split('\t')
        if elements[0] in punctuationSet:
            punct = ET.SubElement(elem, 'pc')
            punct.text = elements[0]
        else:
            lemma = ET.SubElement(elem, 'w')
            lemma.set('lemma', elements[2])
            lemma.text = elements[0]

# Parse XML tree into pretty string, using this hint:
# https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file
xmlstr = minidom.parseString(ET.tostring(
    treeMachiavelli.getroot(), encoding='utf-8')).toprettyxml(indent="   ")
file = open("DecennaliLemma.xml", "w", encoding="utf-8")
file.write(xmlstr)
