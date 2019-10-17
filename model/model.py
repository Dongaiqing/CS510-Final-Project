import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from os import listdir
from os.path import dirname, abspath
from parse_xml import parseXML
import string
import math
import numpy as np

class UnigramLM:
    def __init__(self, data_size, lam):
        # lam stands for lamda
        self.data_dir = dirname(dirname(abspath(__file__))) + "/grobid_processed/"
        self.data_size = data_size
        self.total_words = 0
        self.lam = lam
        self.doc_length = [0] * data_size
        self.str_list = [""] * data_size
        self.unigram_list = [""] * data_size
        self.title_list = [""] * data_size
        self.abstract_list = [""] * data_size
        self.translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
        self.reference_counter = Counter()
        self.parseAllXML()
        self.convert_all_to_unigram()
        assert(sum(self.doc_length, self.total_words))
        

    def parseAllXML(self):
        xml_list = listdir(self.data_dir)
        for i in range(self.data_size):
            self.str_list[i], self.title_list[i], self.abstract_list[i] = parseXML(self.data_dir + xml_list[i])
    
    def convert_all_to_unigram(self):     
        for i in range(self.data_size):
            self.unigram_list[i] = self.convert_to_unigram(self.str_list[i], i)

    def get_str_list(self):
        return self.str_list
    
    def get_Counter(self, idx):
        assert(idx < self.data_size)
        return self.unigram_list[idx]

    def convert_to_unigram(self, text, idx):
        text = text.translate(self.translator)
        token = nltk.word_tokenize(text)
        self.doc_length[idx] = len(token)
        self.total_words += len(token)
        counter = Counter(token)
        self.reference_counter += counter
        return counter
    
    def query(self, query, k):
        score_list = [0] * self.data_size
        for i in range(self.data_size):
            score_list[i] = self.compute_score(query, i)
        score_list = np.argsort(score_list)[::-1]
        doc_list = []
        for i in range(k):
            print("result %d: %d" % (i, self.unigram_list[score_list[i]]["translation"]))
            doc_list.append([self.title_list[score_list[i]], self.abstract_list[score_list[i]]])
        return doc_list
    
    def compute_score(self, query, doc_idx):
        '''
        Using JM smoothing
        '''
        words = query.split(" ")
        score = 0
        for w in words:
            if self.unigram_list[doc_idx][w] != 0:
                n = 1 + (self.lam / (1 - self.lam)) * (self.unigram_list[doc_idx][w] / (self.doc_length[doc_idx] * (self.reference_counter[w] / self.total_words)))
                score += math.log(n, 2)
        return score

def main():
    LM = UnigramLM(100, 0.1)
    counter = LM.get_Counter(11)
    print(LM.query("translation", 10))

if __name__ == '__main__':
    main()