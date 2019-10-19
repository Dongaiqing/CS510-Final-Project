from xml.dom import minidom
import os
from os.path import dirname, abspath

def parseXML(xmlfile):
    '''
    ignore all tags
    '''
    f = open(xmlfile, "r")
    f_list = f.read().splitlines()
    abstract_idx = f_list.index("<abstract>")
    abstract = f_list[abstract_idx+1]
    title_idx = f_list.index("<title>")
    title = f_list[title_idx+1]
    f_list = [elem.lower() for elem in f_list if len(elem) > 0 and elem[0] != '<']

    return " ".join(f_list), title, abstract


dir_path = dirname(dirname(abspath(__file__)))
if os.name == 'nt':
    dir_path += "\\"
else:
    dir_path += "/grobid_processed/A00-1012.tei.xml"

parseXML(dir_path)