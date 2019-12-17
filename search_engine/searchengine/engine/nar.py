import pickle
import random
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from clustering import *

class NARModel:
    def __init__(self):
        self.train_articles = []
        self.train_query = []
        self.train_data = []
        self.train_label = []
        self.test_data = []
        self.query_count = 1 # number of queries that have already been queried by this user in this active session
        self.article_count = 2 # number of articles read by this user in this active session, the remaining articles will be used for recommendation

    def generate_train_data(self, article_embedding, query_embedding, user_cluster):
        """
        Assume top 100 documents and are read by this user in this session, and top 5 queries are used in this session.
        """
        # To-Do: parse input, input embedding should be a two dimentaional array, each row represent an article or query
        for i in range(self.article_count):
            self.train_articles.append(article_embedding[i])

        for i in range(self.query_count):
            self.train_query.append(query_embedding[i])
        
        # generate training data
        for i in range(self.query_count):
            for j in range(self.article_count):
                self.train_data.append([user_cluster] + self.train_query[i] + self.train_articles[j])

    # label is generated randomly since we have no ideas on article id and query id
    def generate_train_label(self):
        for i in range(self.query_count*self.article_count):
            self.train_label.append(random.randint(0, 1))

    def generate_test_data(self, article_embedding, query, user_cluster):
        # we can make an assumption that we are only predicting for one query, this will make life easier
        for i in range(self.article_count, len(article_embedding)):
            self.test_data.append([user_cluster] + query + article_embedding[i])
    
    def train(self, train_data, train_label):
        clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 2), random_state=1)

        scaler = StandardScaler()
        scaler.fit(train_data)
        clf.fit(train_data, train_label)
        MLPClassifier(alpha=1e-05, hidden_layer_sizes=(5, 2), random_state=1,
                    solver='lbfgs')
        return clf

    def recommend(self, train_data, train_label, embedding, user_cluster, top_k):
        """
        A multi-layer neural network model

        Prameters:
        train_data -- dataset that have articles user cluster clicked, and skipped
        train_label -- to simplify, use 1 or 0 to classify: 0 not clicked, 1 clicked
        embedding -- article embedding: numpy matrix, the output of ACR model
        user_cluster -- the cluster current user is in

        Output:
        recommendation: list of top k <article id, score> that might be clicked by this class of user

        """
        clf = self.train(train_data, train_label)

        result = clf.predict(embedding)
        result_prob = clf.predict_proba(embedding)
        recommendation = []
        # store article id into recommendtaion
        for i in range(len(result)):
            if result[i] == 1:
                recommendation.append([i, max(result_prob[i])])
        recommendation.sort(key=lambda tup: tup[1])
        return recommendation[:top_k]

def main():
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

if __name__ == "__main__":
    main()
