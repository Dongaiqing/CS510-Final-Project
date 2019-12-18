import numpy
import math
from sklearn.cluster import AgglomerativeClustering, DBSCAN
from collections import defaultdict
from utils import data_loader


def create_clusters(user_ids, user_embedding_vectors):
    '''takes a list of user ids and user embeddings.
    returns a mapping of user_ids -> cluster_ids, as well as a mapping of cluster_ids -> cluster_embeddings.
    Uses Agglomerative (hierarchical) clustering method to find blobs inside a mostly-even distribution.
    * Hierarchical clustering seems most promising, though many clustering methods struggle with sparse data like this.
    DBSCAN seems most theoretically valuable, assuming that the embedding patterns of viewed documents
    provides a discernable structure, but without that data, experimentation is difficult.'''
    num_clusters = math.floor(len(user_ids) / 100)
    #clustering = DBSCAN().fit(user_embedding_vectors)  # struggles with sparse data
    clustering = AgglomerativeClustering(n_clusters=num_clusters, affinity='cosine', linkage='complete').fit(user_embedding_vectors)
    # investigate different linkages, affinities?
    labels = clustering.labels_

    # initialize cluster_midpoints return structure
    cluster_midpoints = {}
    for i in range(num_clusters):
        cluster_midpoints[i] = numpy.zeros(len(user_embedding_vectors[0]))

    # create user->cluster mapping
    user_clusters = {}
    for i in range(len(user_ids)):
        user_clusters[user_ids[i]] = labels[i]

    # determine popularity of different clusters
    cluster_counts = defaultdict(int)
    for cluster in range(math.floor(len(user_ids) / 100)):
        for user in user_clusters:
            if user_clusters[user] == cluster:
                cluster_counts[cluster] += 1

    # create cluster_midpoint values - this probably needs to be improved
    for i in range(len(user_embedding_vectors)):  # iterate over index shared between user_id and user_embedding_vectors
        cluster_midpoints[user_clusters[user_ids[i]]] = numpy.add(cluster_midpoints[user_clusters[user_ids[i]]], user_embedding_vectors[i])

    for i in range(len(cluster_midpoints)):  # iterate over cluster_id
        cluster_midpoints[i] = numpy.divide(cluster_midpoints[i], cluster_counts[i])

    return user_clusters, cluster_midpoints


def create_test_data(n):
    '''Produces a dummy set of user data'''
    return list(range(1000, 1000+n)), numpy.random.rand(n, 250)


def bootstrap():
    '''Generates dummy data, runs clustering, prints the results of the clustering algorithm'''
    user_ids, user_embeddings = create_test_data(1000)
    user_cluster_map, cluster_embedding_map = create_clusters(user_ids, user_embeddings)

    return user_ids, user_embeddings, user_cluster_map, cluster_embedding_map


def generate_user_embedding_vector(user_id, user_embedding, user_cluster_map, cluster_embedding_map, beta=0.3, use_average_cluster=False):
    '''Returns the modified user embedding vector combined with the cluster embedding vector that the user belongs to
    Weighted as such: combined_embedding = (user_embedding * beta) + (cluster_embedding * (1-beta))
    If the user has not been added to a cluster yet, uses 'use_average_cluster' to decide whether to use
    the average of all clusters for the cluster_embedding value, or just to return user_embedding
    * This is something that would be a good candidate for further extension - needs to be mentioned in report'''
    cluster_embedding = numpy.zeros(len(user_embedding))

    if user_id not in user_cluster_map:
        if not use_average_cluster:
            return user_embedding
        # use average cluster value for embedding
        ids = 0
        for cluster_id in cluster_embedding_map:
            ids += 1
            cluster_embedding = numpy.add(cluster_embedding, cluster_embedding_map[cluster_id])
        cluster_embedding = numpy.divide(cluster_embedding, ids)
        pass
    else:
        cluster_embedding = cluster_embedding_map[user_cluster_map[user_id]]

    return numpy.add(numpy.multiply(user_embedding, beta), numpy.multiply(cluster_embedding, (1.0 - beta)))


if __name__ == "__main__":
    user_ids, user_embeddings, user_cluster_map, cluster_embedding_map = bootstrap()

    loader = data_loader.KaggleLoader(unzip=False)
    loader.output_cluster_files(user_cluster_map, cluster_embedding_map)
    del user_cluster_map, cluster_embedding_map  # shows that we've actually loaded the data correctly
    user_cluster_map, cluster_embedding_map = loader.load_cluster_files()

    point_seven = generate_user_embedding_vector(user_ids[0], user_embeddings[0], user_cluster_map, cluster_embedding_map, beta=0.7)
    point_three = generate_user_embedding_vector(user_ids[0], user_embeddings[0], user_cluster_map, cluster_embedding_map, beta=0.3)
    print(numpy.subtract(point_seven, point_three))
