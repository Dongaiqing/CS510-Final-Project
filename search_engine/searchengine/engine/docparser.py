import gzip
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

class DocParser():
    def parse_html(self, path):
        with gzip.open(path, 'rt') as raw_doc:
            content = raw_doc.read()
            html_parser = DocHTMLParser()
            html_parser.feed(content)
            docs = html_parser.doc_list
            return docs
    def parse_xml(self, path):
        xml_parser = DocXMLParser()
        xml_parser.parse(path)
        return xml_parser.doc

class Document():
    def __init__(self):
        self.id = None
        self.link = None
        self.title = None
        self.abstract = None
        self.authors = None
        self.text = None

class DocHTMLParser(HTMLParser):
    doc_list = []
    tag = None
    doc = None
    def handle_starttag(self, tag, attrs):
        self.tag = tag
    def handle_endtag(self, tag):
        if tag == "doc" and self.doc is not None:
            self.doc_list.append(self.doc)
            self.doc = None
            self.doc = None
        self.tag = None
    def handle_data(self, data):
        if self.tag == "doc":
            self.doc = Document()
        if self.tag == "docno":
            self.doc.id = data.strip()
        if self.tag == "ti":
            self.doc.title = data.strip()
        if self.tag == "text":
            self.doc.text = data.strip()

class DocXMLParser():
    def __init__(self):
        self.prefix = "{http://www.tei-c.org/ns/1.0}"
        self.doc = Document()
        self.doc.authors = []
        self.doc.text = ""

    def parse(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        regx = re.compile(r'.*(?<=/)(.*)\.tei*' )
        self.doc.id = regx.search(path).group(1)

        for node in root.getiterator():
            if node.tag == self.prefix + "title":
                self.doc.title = node.text
            if node.tag == self.prefix + "author":
                name = node.find("./*/" + self.prefix + "forename").text + " " + node.find("./*/" + self.prefix + "surname").text
                self.doc.authors.append(name)
            if node.tag == self.prefix + "abstract":
                self.doc.abstract = node.find("./*/" + self.prefix + "p").text
            if node.tag == self.prefix + "body":
                for txt in node.findall("./*/*"):
                    if txt.text is not None:
                        self.doc.text = self.doc.text + " " + txt.text
                break

# def main():
#     parser = DocParser()
#     docs = parser.parse_xml("/output/A00-1001.tei.xml")

# if __name__ == "__main__":
#     main()