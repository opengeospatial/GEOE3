"""This module contains functions to load input data into the model"""
from xml_ import *
from xml_ import ns
from lxml import etree as ET
import os
import urllib.request
import tempfile
import json
import dicttoxml
import tempfile
import shutil
from datetime import datetime
import xml.dom.minidom
import csv

''' Loads data from a metadata file
def load_dataset_metadata(filename):
    """Read metadata file and return the MD_Metadata etree element"""
    tree = ET.parse(filename)
    root = tree.getroot()

    return root.xpath('//gmd:MD_Metadata', namespaces=ns)[0]'''



def load_dataset_metadata(xml_file):
    """
    Loads metadata from an XML file and returns an lxml Element object representing the root element.
    
    Args:
        xml_file (str): Path to the XML file containing metadata.
    
    Returns:
        lxml.etree.Element: Root element of the parsed XML tree.
    """
    with open(xml_file, 'rb') as response:
        xml = response.read()
    parser = ET.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = ET.fromstring(xml, parser)
    return root

# Loads data from an API through a url, turns the JSON format into XML to be the same as the metadata files, saves it as a temp file (.xml) and returns the path
def load_API(url, serviceId):
    with urllib.request.urlopen(url) as response:
        json_data = json.loads(response.read().decode('utf-8'))
        # Save the JSON data to a temporary file
        fd, tmp_filename = tempfile.mkstemp(suffix='.xml')
        with os.fdopen(fd, 'wb') as tmp_file:
            # Convert the JSON data to XML and write it to the file
            xml_data = dicttoxml.dicttoxml(json_data, root=False, attr_type=False)
            root = "root"
            xml_data = f"<{root}>{xml_data.decode()}</{root}>"
            tmp_file.write(xml_data.encode())
            dom = xml.dom.minidom.parseString(xml_data)
            pretty_tmp_file = dom.toprettyxml()
            

        # Move the file to your desired directory
        program_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(program_dir, 'temp', serviceId)
        os.makedirs(temp_dir, exist_ok=True)
        now_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        new_filename = os.path.join(temp_dir, f'temp{now_str}.xml')
        shutil.move(tmp_filename, new_filename)
    return new_filename

def load_cvs(cvs_file):
    with open(cvs_file, newline='',encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        rows = [row for row in reader]
    # split each row into a list of values
    rows = [row[0].split(',') for row in rows]
    return rows
