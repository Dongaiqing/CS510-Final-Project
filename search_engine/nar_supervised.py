import torch
import pickle
import random
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from embedder import Embedder
import os
import json
import numpy as np
from doc_parser import Document


class NARModel:
    def __init__(self, train_data_path, article_size, query_size, num_user, sample_size):
        self.embedder = Embedder()
        self.train_data_path = train_data_path
        self.train_label = None
        self.article_sz = article_size
        self.query_sz = query_size
        self.user_sz = num_user
        self.sample_size = sample_size

    def pickle_to_embeddings(self, file_path):
        # create mappings from id to embeddings
        id_to_eb = {}

        with open(file_path, 'rb') as input:
            while True:
                try:
                    doc = pickle.load(input)
                    id_to_eb[doc.id] = [doc.embedding[0][0]]

                except EOFError:
                    break

        return id_to_eb

    def generate_train_data(self):
        sample_size = self.sample_size
        academic_sample_size = 3782
        num_features = 3
        len_ebd = 100
        train_data = np.zeros((sample_size, num_features, len_ebd))
        train_labels = []
        a_id_to_eb, _ = pickle_to_embeddings("data/academic_data.pkl")
        q_id_to_eb, _ = pickle_to_embeddings("data/query_data.pkl")
        u_id_to_eb, _ = pickle_to_embeddings("data/user_data.pkl")
        i = 0
        with open(self.train_data_path[0], 'r') as f:

            for line in f:
                qid, doc_id, uid, score = line.strip().split(' ')
                if int(score) >= 3:
                    label = 1
                else:
                    label = 0
                train_labels.append(label)
                train_data[i, 0, :] = np.asarray(q_id_to_eb[qid])
                train_data[i, 2, :] = np.asarray(u_id_to_eb[uid])
                try:
                    train_data[i, 1, :] = np.asarray(a_id_to_eb[doc_id])
                except KeyError:
                    train_data[i, 0, :] = np.zeros(
                        train_data[i, 0, :].shape, dtype=np.float32)
                    train_data[i, 1, :] = np.zeros(
                        train_data[i, 0, :].shape, dtype=np.float32)
                    train_data[i, 2, :] = np.zeros(
                        train_data[i, 0, :].shape, dtype=np.float32)
                i += 1
        if(sample_size > academic_sample_size):
            with open(self.train_data_path[1], 'r') as fp:
                for line in fp:
                    qid, doc_id, uid, score = line.strip().split(' ')
                    if int(score) >= 3:
                        label = 1
                    else:
                        label = 0
                    train_labels.append(label)
                    train_data[i, 0, :] = np.asarray(q_id_to_eb[qid])
                    train_data[i, 2, :] = np.asarray(u_id_to_eb[uid])
                    try:
                        train_data[i, 1, :] = np.asarray(a_id_to_eb[doc_id])
                    except KeyError:
                        train_data[i, 0, :] = np.zeros(
                            train_data[i, 0, :].shape, dtype=np.float32)
                        train_data[i, 1, :] = np.zeros(
                            train_data[i, 0, :].shape, dtype=np.float32)
                        train_data[i, 2, :] = np.zeros(
                            train_data[i, 0, :].shape, dtype=np.float32)
                    i += 1

        train_labels = np.asarray(train_labels)
        return train_data, train_labels

    def train(self):
        clf = MLPClassifier(
            alpha=1e-05, hidden_layer_sizes=(5, 3), random_state=1)

        scaler = StandardScaler()
        train_data, train_labels = self.generate_train_data()
        train_data = train_data.reshape(train_data.shape[0], -1)
        scaler.fit(train_data)
        clf.fit(train_data, train_labels)
        return clf


def pickle_to_embeddings(file_path):
    id_to_eb = {}
    id_to_contents = {}

    with open(file_path, 'rb') as input:
        while True:
            try:
                doc = pickle.load(input)
                id_to_eb[doc.id] = [doc.embedding[0][0]]
                id_to_contents[doc.id] = [doc.title, doc.abstract]

            except EOFError:
                break

    return id_to_eb, id_to_contents


def embeddings_to_pickle(file_path, dic_embedding):

    with open(file_path, 'wb') as output:
        for key, value in dic_embedding.items():
            embedding = np.zeros((1, 1, 100), dtype=np.float32)

            embedding[0, 0, :] = np.array(value)
            doc_obj = Document()
            doc_obj.id = key
            doc_obj.embedding = embedding
            pickle.dump(doc_obj, output, pickle.HIGHEST_PROTOCOL)


'''
def list2Str(s):
    s = list(s)
    s = [str(i) for i in s]
    ret = ""
    return ret.join(s)


def embedding2id( file_path):
    eb_to_id = {}
    with open(file_path, 'rb') as input:
        while True:
            try:
                doc = pickle.load(input)
                hash = list2Str(doc.embedding[0][0])
                eb_to_id[hash] = doc.id
            except EOFError:
                break
    return eb_to_id
'''


def recommend(top_k, clf, query, user_id, academic_data):
    '''
    Parameters:
    -top_k: the num of returned article ids
    -clf: model trained by Multi Layer Perceptron Classifier
    -query: string
    -user_id: String
    -academic_data: pickle file with doc embedding and doc id
    '''
    # return a ordered 2d list, [article id, scores]
    embedder = Embedder()

    results = {}
    #a_eb_to_id = embedding2id("data/academic_data.pkl" )
    u_id_to_eb, _ = pickle_to_embeddings("data/user_data.pkl")
    a_id_to_eb, a_id_to_contents = pickle_to_embeddings(academic_data)

    q_emb = embedder.embed(query)
    u_emb = u_id_to_eb[user_id]
    input = np.zeros((len(a_id_to_eb), 3, 100))
    i = 0
    for key, value in a_id_to_eb.items():
        a_emb = value
        a_id = key
        input[i, 0, :] = np.asarray(q_emb)
        input[i, 1, :] = np.asarray(a_emb)
        input[i, 2, :] = np.asarray(u_emb)
        i += 1

    input = input.reshape(input.shape[0], -1)
    prediction = clf.predict_proba(input)
    results = {}
    j = 0
    for key, value in a_id_to_eb.items():
        results[key] = prediction[j][1]
        j += 1
    recommendation = []
    # store article id into recommendtaion
    sorted_result = sorted(
        results.items(), key=lambda x: x[1], reverse=True)[:top_k]
    recommendation = [(a_id_to_contents[result[0]][0],
                       a_id_to_contents[result[0]][1], result[0]) for result in sorted_result]

    return recommendation


def record(user_id, paper_id_lst, query, score_lst):
    '''
    -user_id: string
    -paper_id_list: string list
    -query: String
    -score_list: int list
    '''
    embedder = Embedder()
    data_len_path = "data/data_len.json"
    query_path = "data/query_data.pkl"
    user_path = "data/user_data.pkl"
    train_path = "data/acl_train_data.txt"
    # update query size
    f = json.load(open(data_len_path, "r"))
    # update query pkl file
    q_id_to_eb = {}
    q_id_to_eb, _ = pickle_to_embeddings(query_path)
    query_embed = embedder.embed(query)
    qid = f['query']
    f["query"] += 1
    json.dump(f, open(data_len_path, "w"))

    q_id_to_eb[str(qid)] = query_embed
    embeddings_to_pickle(query_path, q_id_to_eb)
    # update usesr embedding

    dict = json.load(open("data/user_query_history.json", "r"))
    dict[user_id] += " "
    dict[user_id] += query
    json.dump(dict, open("data/user_query_history.json", 'w'))
    # create new user embedding
    u_id_to_eb, _ = pickle_to_embeddings(user_path)
    u_id_to_eb[user_id] = embedder.embed(dict[user_id])
    embeddings_to_pickle(user_path, u_id_to_eb)

    # update train data
    lines = ""
    with open(train_path, 'r') as fp:
        for line in fp:
            lines += line
    for i in range(len(paper_id_lst)):
        lines += (str(f['query']-1) + " " + paper_id_lst[i] +
                  " " + str(user_id) + " " + str(score_lst[i]) + "\n")
    with open(train_path, 'w') as fx:
        fx.write(lines)
    f['sample_size'] += len(paper_id_lst)
    json.dump(f, open("data/data_len.json", 'w'))


def create_NAR_model():
    train_data_path = ["data/academic_train_data.txt",
                       "data/acl_train_data.txt"]
    data_len_path = "data/data_len.json"
    data_len = {}
    data_len = json.load(open(data_len_path, 'r'))
    article_size = data_len['article']
    query_size = data_len['query']
    num_user = data_len['user']
    sample_size = data_len['sample_size']
    model = NARModel(train_data_path, article_size,
                     query_size, num_user, sample_size)
    clf = model.train()

    return clf