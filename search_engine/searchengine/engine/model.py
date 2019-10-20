import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from os import listdir
from os.path import dirname, abspath
import os
from searchengine.engine.parse_xml import parseXML
from utils import os_directory
from utils.data_loader import DataLoader
import string
import math
import numpy as np

class UnigramLM:
    def __init__(self, data_dir, data_size, lam):
        # lam stands for lamda
        self.data_dir = data_dir
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
            try:
                self.str_list[i], self.title_list[i], self.abstract_list[i] = parseXML(self.data_dir + xml_list[i])
            except UnicodeDecodeError:
                continue
    
    def convert_all_to_unigram(self):     
        '''
        convert all document string to unigram counter
        '''
        if not self.load_model("model.npy"):
            for i in range(self.data_size):
                print(i)
                self.unigram_list[i] = self.convert_to_unigram(self.str_list[i], i)
            self.save_model("model.npy")
    
    def save_model(self, fname):
        '''
        saves model parameters for faster loading
        '''
        save_lst = []
        save_lst.append(self.doc_length)
        save_lst.append(self.total_words)
        save_lst.append(self.reference_counter)
        save_lst.append(self.unigram_list)
        np.save(fname, np.asarray(save_lst))
    
    def load_model(self, fname):
        '''
        loads model parameters from existing saves
        '''
        if os.path.exists(fname):
            lst = np.load(fname, allow_pickle=True).tolist()
            self.doc_length = lst[0]
            self.total_words = lst[1]
            self.reference_counter = lst[2]
            self.unigram_list = lst[3]
            return True
        else:
            return False
    
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
        '''
        return a list of [title, abstract]
        '''
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
        # scores can be proportional values: log used to prevent underflow
        for w in words:
            if self.unigram_list[doc_idx][w] != 0:
                n = 1 + (self.lam / (1 - self.lam)) * (self.unigram_list[doc_idx][w] / (self.doc_length[doc_idx] * (self.reference_counter[w] / self.total_words)))
                score += math.log(n, 2)
        return score

def main():
    loader = DataLoader()
    num_files = loader.load_data()

    # use xml parser here, pass data into UnigramLM?

    LM = UnigramLM(loader.destination_dir, num_files, 0.1)
    counter = LM.get_Counter(11)
    print(LM.query("translation", 10))

if __name__ == '__main__':
    main()