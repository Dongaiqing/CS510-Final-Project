import re

class Document():
    def __init__(self):
        self.id = None
        self.link = None
        self.title = None
        self.abstract = None
        self.authors = None
        self.text = None
        self.embedding = None

class DocParser():
    def __init__(self):
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

    def parseXML(self, xmlfile):
        '''
        ignore all tags
        '''
        doc = Document()

        f = open(xmlfile, "r")
        f_list = f.read().splitlines()
        abstract_idx = f_list.index("<abstract>")
        doc.abstract = self.clean_str(f_list[abstract_idx+1])
        title_idx = f_list.index("<title>")
        doc.title = self.clean_str(f_list[title_idx+1])
        
        # f_list = [elem.lower() for elem in f_list if len(elem) > 0 and elem[0] != '<']

        return doc

