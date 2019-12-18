import json
import re

class AcademicParser():
    def __init__(self, fname):
        self.academic_doc = []
        self.paperAbstract = []
        self.title = []
        self.valid_docno = []
        self.document_id_to_num = {}

         # Punctuation list
        self.punctuations = re.escape('!"#%\'()*+,./:;<=>?@[\\]^_`{|}~')

        self.re_remove_brackets = re.compile(r'\{.*\}')
        self.re_remove_html = re.compile(r'<(\/|\\)?.+?>', re.UNICODE)
        self.re_transform_numbers = re.compile(r'\d', re.UNICODE)
        self.re_transform_emails = re.compile(r'[^\s]+@[^\s]+', re.UNICODE)
        self.re_transform_url = re.compile(r'(http|https)://[^\s]+', re.UNICODE)
        # Different quotes are used.
        self.re_quotes_1 = re.compile(r"(?u)(^|\W)[‘’′`']", re.UNICODE)
        self.re_quotes_2 = re.compile(r"(?u)[‘’`′'](\W|$)", re.UNICODE)
        self.re_quotes_3 = re.compile(r'(?u)[‘’`′“”]', re.UNICODE)
        self.re_dots = re.compile(r'(?<!\.)\.\.(?!\.)', re.UNICODE)
        self.re_punctuation = re.compile(r'([,";:]){2},', re.UNICODE)
        self.re_hiphen = re.compile(r' -(?=[^\W\d_])', re.UNICODE)
        self.re_tree_dots = re.compile(u'…', re.UNICODE)
        # Differents punctuation patterns are used.
        self.re_punkts = re.compile(r'(\w+)([%s])([ %s])' %
                            (self.punctuations, self.punctuations), re.UNICODE)
        self.re_punkts_b = re.compile(r'([ %s])([%s])(\w+)' %
                                (self.punctuations, self.punctuations), re.UNICODE)
        self.re_punkts_c = re.compile(r'(\w+)([%s])$' % (self.punctuations), re.UNICODE)
        self.re_changehyphen = re.compile(u'–')
        self.re_doublequotes_1 = re.compile(r'(\"\")')
        self.re_doublequotes_2 = re.compile(r'(\'\')')
        self.re_trim = re.compile(r' +', re.UNICODE)

        # self.document_ids()
        self.load_files(fname)
        
       

    def document_ids(self):
        with open('../document_id_mapping.txt', 'r') as infile:
            for line in infile:
                doc_num, doc_id = line.strip().split(' ')
                self.document_id_to_num[doc_id] = int(doc_num)

    def load_files(self, fname):
        '''
        self.academic_doc is a dictionary with doc_num as keys.
        The value of each (key, value) pair is a json dictionary with keys: 
        ['keyPhrases', 'paperAbstract', 'numKeyReferences', 'title', 'venue', 'numCitedBy', 'numKeyCitations', 'docno', 'ana']]
        keyPhrases might be absent
        '''
        with open(fname, "r") as json_file:
            for line in json_file:
                f = json.loads(line)
                # doc_num = self.document_id_to_num[f["docno"]]
                if self.check_if_valid(f):
                    self.academic_doc.append(f)
                    self.valid_docno.append(f["docno"])
                    self.title.append(self.clean_str(f["title"][0]))
                    self.paperAbstract.append(self.clean_str(f["paperAbstract"][0]))

    def check_if_valid(self, doc):
        if len(doc["paperAbstract"][0]) > 0 and len(doc["title"][0]) > 0:
            return True

    def get_documents(self):
        return self.academic_doc

    def get_paperAbstract(self):
        return self.paperAbstract
    
    def get_title(self):
        return self.title

    def clean_str(self, string):
        string = string.replace('\n', ' ')
        """Apply all regex above to a given string."""
        string = string.lower()
        string = self.re_tree_dots.sub('...', string)
        string = re.sub('\.\.\.', '', string)
        string = self.re_remove_brackets.sub('', string)
        string = self.re_changehyphen.sub('-', string)
        string = self.re_remove_html.sub(' ', string)
        string = self.re_transform_numbers.sub('0', string)
        string = self.re_transform_url.sub('URL', string)
        string = self.re_transform_emails.sub('EMAIL', string)
        string = self.re_quotes_1.sub(r'\1"', string)
        string = self.re_quotes_2.sub(r'"\1', string)
        string = self.re_quotes_3.sub('"', string)
        string = re.sub('"', '', string)
        string = self.re_dots.sub('.', string)
        string = self.re_punctuation.sub(r'\1', string)
        string = self.re_hiphen.sub(' - ', string)
        string = self.re_punkts.sub(r'\1 \2 \3', string)
        string = self.re_punkts_b.sub(r'\1 \2 \3', string)
        string = self.re_punkts_c.sub(r'\1 \2', string)
        string = self.re_doublequotes_1.sub('\"', string)
        string = self.re_doublequotes_2.sub('\'', string)
        string = self.re_trim.sub(' ', string)

        return string.strip()

'''

def main():
    parser = AcademicParser("../train_data/Academic_papers/docs.json")
    docs = parser.get_documents()
    valid_count = 0
    for doc in docs:
        if len(doc["paperAbstract"][0]) > 0 and len(doc["title"][0]) > 0:
            valid_count += 1
        
    print("total datapoints: ", len(docs))
    print("total valid datapoints:", valid_count)

if __name__ == '__main__':  
    main()
'''