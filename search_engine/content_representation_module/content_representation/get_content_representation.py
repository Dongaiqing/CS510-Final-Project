import torch
from model import EncoderRNN
from academic_parser import AcademicParser
from doc_parser import DocParser, Document
import os
import pickle
from cr_trainer import indexesFromSentence, variableFromSentence, variablesFromPair, getSentenceEmbedding
from embedder import Embedder
import json

embedding_path = "pickles/word_embeddings.pickle"
model_param_path = "model_parameters/crmodel.pt"
grobid_path = "../../grobid_processed"

def main():
    embedder = Embedder()
    parser = DocParser()
    # iterate through grobid
    with open('grobid_data.pkl', 'wb') as output:
        for subdir, dirs, files in os.walk(grobid_path):
            print(len(files))
            count = 0
            for file in files:
                print(count)
                count += 1
                # print(os.path.join(subdir, file))
                doc = parser.parseXML(os.path.join(subdir, file))
                if len(doc.abstract) == 0:
                    continue
                doc.embedding = embedder.embed(doc.abstract)
                # pair = variablesFromPair((doc.abstract, doc.title), word_index, embedding_map)
                # if (len(pair[0]) == 0 or len(pair[1]) == 0):
                #     continue
                # doc.embedding = encode(encoder, pair[0])
                pickle.dump(doc, output, pickle.HIGHEST_PROTOCOL)
                # doc_embedding = encode(encode, )
                # exit()

    # iterate throught academic dataset
    with open("academic_data.pkl", "wb") as output:
        parser = AcademicParser("../train_data/Academic_papers/docs.json")
        docs = parser.get_documents()
        count = 0
        for doc in docs:
            count += 1
            print(count)
            if len(doc["paperAbstract"][0]) > 0 and len(doc["title"][0]) > 0:
                new_doc_object = Document()
                new_doc_object.id = doc["docno"][0]
                new_doc_object.embedding = embedder.embed(doc["paperAbstract"][0])
                new_doc_object.abstract = doc["paperAbstract"][0]
                new_doc_object.title = doc["title"][0]
                pickle.dump(new_doc_object, output, pickle.HIGHEST_PROTOCOL)
        assert(count == len(docs))

    # iterate through query
    with open("query_data.pkl", "wb") as output:
        with open("train_queries.json", "r") as json_file:
            count = 0
            for line in json_file:
                count += 1
                print(count)
                q = json.loads(line)
                new_query_object = Document()
                new_query_object.id = q["qid"]
                new_query_object.embedding = embedder.embed(q["query"])
                new_query_object.abstarct = q["query"]
                pickle.dump(new_query_object, output, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
