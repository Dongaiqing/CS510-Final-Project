import pickle
import random
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import torch
from embedder import Embedder
import os
import pickle
import json
import numpy as np

class NARModel:
    def __init__(self,train_data_path,article_size,query_size, num_user):
        self.embedder = Embedder()
        self.train_data_path = train_data_path
        self.train_label = None
        self.article_sz  = article_size
        self.query_sz = query_size
        self.user_sz = num_user


    def pickle_to_embeddings(self,file_path):
        #create mappings from id to embeddings
        id_to_eb = {}

        with open(file_path, 'rb') as input:
            while True:
                try:
                    doc = pickle.load(input)
                    id_to_eb[doc.id] = doc.embedding[0][0]

                except EOFError:
                    break

        return id_to_eb

    def generate_train_data(self):
        sample_size = 3782
        num_features = 3
        len_ebd = 100
        train_data = np.zeros((sample_size, num_features, len_ebd))
        train_labels = []
        a_id_to_eb = pickle_to_embeddings("data/academic_data.pkl")
        q_id_to_eb = pickle_to_embeddings("data/query_data.pkl")
        u_id_to_eb = pickle_to_embeddings("data/user_data.pkl")

        with open(self.train_data_path, 'r') as f:
            i = 0
            for line in f:
                qid, doc_id, uid, score = line.strip().split(' ')
                if int(score) >= 3:
                    label = 1
                else:
                    label = 0
                train_labels.append(label)
                train_data[i,0,:] = np.asarray(q_id_to_eb[qid][0])
                try:
                    train_data[i,1,:] = np.asarray(a_id_to_eb[doc_id][0])
                except KeyError:
                    train_data[i,1,:] = np.zeros(train_data[i,0,:].shape,dtype = np.float32)
                train_data[i,2,:] = np.asarray(u_id_to_eb[uid][0])
                i+=1
        train_labels = np.asarray(train_labels)
        print(train_data.shape)
        return train_data, train_labels





    def train(self):
        clf = MLPClassifier(alpha=1e-05, hidden_layer_sizes=(5, 3), random_state=1)

        scaler = StandardScaler()
        train_data, train_labels = self.generate_train_data()
        train_data = train_data.reshape(train_data.shape[0], -1)
        scaler.fit(train_data)
        clf.fit(train_data, train_labels)
        return clf
        #MLPClassifier(alpha=1e-05, hidden_layer_sizes=(5, 2), random_state=1, solver='lbfgs')


def pickle_to_embeddings(file_path):
    id_to_eb = {}

    with open(file_path, 'rb') as input:
        while True:
            try:
                doc = pickle.load(input)
                id_to_eb[doc.id] = [doc.embedding[0][0], doc.title, doc.abstract]

            except EOFError:
                break

    return id_to_eb

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



def recommend(top_k, clf, query, user_id, academic_data):
    '''
    Parameters:
    -top_k: the num of returned article ids
    -clf: model trained by Multi Layer Perceptron Classifier
    -query: string
    -user_id: String
    -academic_data: pickle file with doc embedding and doc id
    '''
    #return a ordered 2d list, [article id, scores]
    embedder = Embedder()


    results = {}
    #a_eb_to_id = embedding2id("data/academic_data.pkl" )
    u_id_to_eb = pickle_to_embeddings("data/user_data.pkl")
    a_id_to_eb = pickle_to_embeddings(academic_data)

    q_emb = embedder.embed(query)
    u_emb = u_id_to_eb[user_id][0]
    input = np.zeros((len(a_id_to_eb), 3, 100))
    i = 0
    for key,value in a_id_to_eb.items():
        a_emb = [value[0]]
        a_id = key
        input[i,0,:] = np.asarray(q_emb)
        input[i,1,:] = np.asarray(a_emb)
        input[i,2,:] = np.asarray(u_emb)
        i+=1


    input = input.reshape(input.shape[0], -1)
    prediction = clf.predict_proba(input)
    print(prediction.shape)
    results = {}
    j = 0
    for key, value in a_id_to_eb.items():
        results[key] = prediction[j][1]
        j += 1
    recommendation = []
    # store article id into recommendtaion
    sorted_result = sorted(results.items(), key=lambda x: x[1],reverse = True)[:top_k]
    recommendation = [(a_id_to_eb[result[0]][1], a_id_to_eb[result[0]][2], result[0]) for result in sorted_result]

    return recommendation

def create_NAR_model():

    train_data_path = "data/train_data.txt"
    train_pair_count = 80
    article_size = 7152
    query_size = train_pair_count
    num_user = 20

    model = NARModel(train_data_path,article_size,query_size, num_user)
    clf = model.train()

    return clf

    '''
    article_path = "/search_engine/searchengine/engine/grobid_data.pkl"
    query_path = "/project/search_engine/searchengine/engine/query_data.pkl"
    model = NARModel()
    model.generate_train_label()
    train_label = model.train_label

    # sample test data
    user_id = 1 # test user id
    user_ids, user_embeddings, user_cluster_map, cluster_embedding_map = bootstrap() # get userid, cluster id map from clustering
    user_cluster = user_cluster_map[user_id] # which cluster this user belongs to
    article_embedding = [[0., 0.], [1., 1.], [0., 0.], [1., 1.]]
    query_embedding = [[0., 1.], [0., 2.], [1., 1.]]
    model.generate_train_data(article_embedding, query_embedding, user_cluster)
    train_data = model.train_data

    # use the next untrained query as current query
    model.generate_test_data(article_embedding, query_embedding[model.query_count], user_cluster)
    test_data = model.test_data

    top_k = 1 # how many articles we return based on the score
    recommendation = model.recommend(train_data, train_label, test_data, user_cluster, top_k)
    print(recommendation)
    '''
if __name__ == "__main__":
    main()
