import pickle
import torch
from model import EncoderRNN
from cr_trainer import indexesFromSentence, variableFromSentence, variablesFromPair, getSentenceEmbedding

class Embedder():
    def __init__(self):
        self.embedding_path = "../train_data/Academic_papers/pickles/word_embeddings.pickle"
        self.model_param_path = "model_parameters/crmodel.pt"
        self.hidden_size = 100

        pickle_file = open(self.embedding_path, "rb")
        word_embedding = pickle.load(pickle_file)
        pickle_file.close()
        self.word_index = word_embedding[0]
        self.embedding_map = word_embedding[1]
        self.encoder = torch.load(self.model_param_path)

    def embed(self, text):
        input_variable = variableFromSentence(self.word_index, text)
        input_variable = getSentenceEmbedding(input_variable, self.embedding_map)
        input_variable = [torch.from_numpy(input_variable[i]).float() for i in range(len(input_variable))]
        assert(len(input_variable) > 0) # the input content might not contain any word in dictionary
        input_length = len(input_variable)
        encoder_output = []
        encoder_hidden = self.encoder.initHidden()
        
        for ei in range(input_length):
            encoder_output, encoder_hidden = self.encoder(
                input_variable[ei], encoder_hidden)

        return encoder_output
        
        
