import torch
from model import EncoderRNN
from academic_parser import AcademicParser
from doc_parser import DocParser
import os
import pickle
from cr_trainer import indexesFromSentence, variableFromSentence, variablesFromPair, getSentenceEmbedding
from embedder import Embedder

embedding_path = "../train_data/Academic_papers/pickles/word_embeddings.pickle"
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
        
if __name__ == '__main__':
    main()
