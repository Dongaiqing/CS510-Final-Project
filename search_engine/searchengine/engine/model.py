import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from os import listdir
from os.path import dirname, abspath, isfile
import os
from searchengine.engine.parse_xml import parseXML
from utils import os_directory
from utils.data_loader import DataLoader, KaggleLoader, csvParse
import string
import math
import numpy as np
import pickle

class UnigramLM:
    def __init__(self, data_dir, data_size, lam):
        # lam stands for lambda
        self.data_dir = data_dir
        self.data_size = data_size
        self.total_words = 0
        self.lam = lam
        self.doc_length = [0] * data_size
        self.str_list = [""] * data_size
        self.unigram_list = [""] * data_size
        self.title_list = [""] * data_size
        self.id_list = [""] * data_size
        self.abstract_list = [""] * data_size
        self.translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
        self.reference_counter = Counter()
        self.parseAllXML()
        self.convert_all_to_unigram()
        assert(sum(self.doc_length, self.total_words))


    def parseAllXML(self):
        xml_list = listdir(self.data_dir)
        exetension = ".tei.xml"
        for i in range(self.data_size):
            try:
                self.str_list[i], self.title_list[i], self.abstract_list[i] = parseXML(self.data_dir + xml_list[i])
                file_name = str(xml_list[i])
                self.id_list[i] = file_name[0: len(file_name)-len(exetension)]
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
        return a list of [title, abstract, id]
        '''
        score_list = [0] * self.data_size
        for i in range(self.data_size):
            score_list[i] = self.compute_score(query, i)
        score_list = np.argsort(score_list)[::-1]
        doc_list = []
        for i in range(k):
            print("result %d: %d" % (i, self.unigram_list[score_list[i]]["translation"]))
            doc_list.append([self.title_list[score_list[i]], self.abstract_list[score_list[i]], self.id_list[score_list[i]]])
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


class KaggleModel:
    def __init__(self, data_dir):
        self.files = []
        for r, d, f in os.walk(data_dir):
            print(r,d,f)
            for file in f:
                if isfile(os.path.join(r, file)):
                    self.files.append(os.path.join(r, file))

    def load_data(self):
        # pickle load kaggle/articles_embeddings.pickle
        embeddings_filename = ''.join([file if "articles_embeddings.pickle" in file else '' for file in self.files])
        self.article_embeddings = pickle.load(open(embeddings_filename, "rb"))
        num_articles = len(self.article_embeddings)                  # 364047
        article_embedding_size = len(self.article_embeddings[0])     # 250

        # csv load kaggle/articles_metadata.csv
        metadata_filename = ''.join([file if "articles_metadata.csv" in file else '' for file in self.files])
        self.article_metadata = csvParse(metadata_filename)[1:]      # article_id, category_id, created_at_ts, publisher_id, words_count

        self.clicks_hour = [None] * 385
        # csv load .../clicks/clicks/clicks_hour_*.csv
        # user_id, session_id, session_start, session_size, click_article_id, click_timestamp, click_environment,
        # click_deviceGroup, click_os, click_country, click_region, click_referrer_type
        for hour in self.files:
            if "clicks_hour" not in hour:
                continue
            self.clicks_hour[int(hour.split('_')[-1].split('.')[0])] = csvParse(hour)[1:]


def main():
    kag = KaggleLoader()
    kag.load_data()

    KagLM = KaggleModel(kag.data_dir)
    KagLM.load_data()


if __name__ == '__main__':
    main()
