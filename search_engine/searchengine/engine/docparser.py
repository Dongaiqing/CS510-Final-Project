import gzip
from html.parser import HTMLParser

class DocParser():
    def parse(self, path):
        with gzip.open(path, 'rt') as raw_doc:
            content = raw_doc.read()
            html_parser = DocHTMLParser()
            html_parser.feed(content)
            docs = html_parser.doc_list
            return docs

class Document():
    def __init__(self):
        self.id = None
        self.title = None
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

# def main():
#     parser = DocParser()
#     docs = parser.parse("search_engine/searchengine/static/fb396001.gz")

# if __name__ == "__main__":
#     main()