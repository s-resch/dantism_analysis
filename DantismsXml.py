from lxml import etree
import xml.etree.ElementTree as ET
from xml.dom import minidom
import csv


def searchDantsims(filename):

    # Read TEI XML file using parameter of function and get lemma attributes of all w tags
    # For information about etree see: https://docs.python.org/3/library/xml.etree.elementtree.html
    treeAnalyze = etree.parse("AnnotationLemma/" + filename + "Lemma.xml")
    listLemmaAnalyze = treeAnalyze.findall('//w')
    listLemmaOnlyAnalyze = [l.attrib.get('lemma') for l in listLemmaAnalyze]

    # Read 3 corpora with dantisms
    with open('Dantisms_Viel_Ortho_Inferno.csv', newline='') as f:
        reader = csv.reader(f)
        dantismInferno = list(reader)
        dantismInferno = [x[0] for x in dantismInferno]

    with open('Dantisms_Viel_Ortho_Purgatorio.csv', newline='') as f:
        reader = csv.reader(f)
        dantismPurgatorio = list(reader)
        dantismPurgatorio = [x[0] for x in dantismPurgatorio]

    with open('Dantisms_Viel_Ortho_Paradiso.csv', newline='') as f:
        reader = csv.reader(f)
        dantismParadiso = list(reader)
        dantismParadiso = [x[0] for x in dantismParadiso]

    # Build result lists: Look for intersections between corpora and lemma
    # list o four text. Save position of lemma as extra information
    listPosLemmaInferno = [[x, i] for i, x in enumerate(
        listLemmaOnlyAnalyze) if x in dantismInferno]
    listPosLemmaPurgatorio = [[x, i] for i, x in enumerate(
        listLemmaOnlyAnalyze) if x in dantismPurgatorio]
    listPosLemmaParadiso = [[x, i] for i, x in enumerate(
        listLemmaOnlyAnalyze) if x in dantismParadiso]

    # Build lists that don’t contain duplicates: Use conversion via set as ‘workaround’ to eliminate duplicates
    uniqueListDantInferno = list(set([x[0] for x in listPosLemmaInferno]))
    uniqueListDantPurgatorio = list(
        set([x[0] for x in listPosLemmaPurgatorio]))
    uniqueListDantParadiso = list(set([x[0] for x in listPosLemmaParadiso]))

    # Build XML structure to be saved to result XML-file
    rootXml = ET.Element("dantisms")

    # Create main tags indicating cantiche
    infernoXml = ET.SubElement(rootXml, "inferno")
    infernoXml.set("number", str(len(listPosLemmaInferno)))
    infernoXml.set("numberUnique", str(len(uniqueListDantInferno)))

    purgatorioXml = ET.SubElement(rootXml, "purgatorio")
    purgatorioXml.set("number", str(len(listPosLemmaPurgatorio)))
    purgatorioXml.set("numberUnique", str(len(uniqueListDantPurgatorio)))

    paradisoXml = ET.SubElement(rootXml, "paradiso")
    paradisoXml.set("number", str(len(listPosLemmaParadiso)))
    paradisoXml.set("numberUnique", str(len(uniqueListDantParadiso)))

    # Add information about dantisms found to each cantica-section
    for i in range(len(listPosLemmaInferno)):
        dantism = ET.SubElement(infernoXml, "dantism")
        dantism.set("position", str(listPosLemmaInferno[i][1]))
        dantism.text = listPosLemmaInferno[i][0]

    for i in range(len(listPosLemmaPurgatorio)):
        dantism = ET.SubElement(purgatorioXml, "dantism")
        dantism.set("position", str(listPosLemmaPurgatorio[i][1]))
        dantism.text = listPosLemmaPurgatorio[i][0]

    for i in range(len(listPosLemmaParadiso)):
        dantism = ET.SubElement(paradisoXml, "dantism")
        dantism.set("position", str(listPosLemmaParadiso[i][1]))
        dantism.text = listPosLemmaParadiso[i][0]

    # Write XML structure to file
    treeResult = ET.ElementTree(rootXml)
    # Parse XML tree into pretty string, using this hint:
    # https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file
    xmlstr = minidom.parseString(ET.tostring(
        treeResult.getroot(), encoding='utf-8')).toprettyxml(indent="   ")
    file = open("Results/Dantisms/" + filename +
                "_Dantisms.xml", "w", encoding="utf-8")
    file.write(xmlstr)
