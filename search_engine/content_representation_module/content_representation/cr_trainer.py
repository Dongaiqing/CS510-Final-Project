import logging
import os
import time
import torch
import numpy as np
import pickle
from torch.autograd import Variable
from academic_parser import AcademicParser
from model import EncoderRNN, DecoderRNN
from torch import optim, nn
import random
import math 

embedding_path = "pickles/word_embeddings.pickle"
parameter_path = "model_parameters/crmodel.pt"

def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))

def indexesFromSentence(word_dict, sentence):
    res = [] 
    for word in sentence.split(' '):
        if word not in word_dict:
            res.append(1)
        else:
            res.append(word_dict[word])
    return res

def variableFromSentence(word_dict, sentence):
    indexes = indexesFromSentence(word_dict, sentence)
    # indexes.append(EOS_token)
    result = Variable(torch.LongTensor(indexes).view(-1, 1))
    return result

def variablesFromPair(pair, word_dict, embedding_map):
    input_variable = variableFromSentence(word_dict, pair[0])
    input_variable = getSentenceEmbedding(input_variable, embedding_map)
    target_variable = variableFromSentence(word_dict, pair[1])
    # target_variable = getSentenceEmbedding(target_variable, embedding_map)
    return (input_variable, target_variable)

def getSentenceEmbedding(indices, embedding_map):
    res = []
    for index in indices:
        res.append(embedding_map[index])
    return res

def train(input_variable, target_variable, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion):
    encoder_hidden = encoder.initHidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()
    
    input_variable = [torch.from_numpy(input_variable[i]).float() for i in range(len(input_variable))]

    input_length = len(input_variable)
    target_length = len(target_variable)
    # print(target_length)

    encoder_output = []

    loss = 0
    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_variable[ei], encoder_hidden)

    decoder_input = Variable(torch.LongTensor([[0]]))

    decoder_hidden = encoder_hidden

    # Without teacher forcing: use its own predictions as the next input
    assert(target_length > 0)
    for di in range(target_length):
#             decoder_output, decoder_hidden, decoder_attention = decoder(
#                 decoder_input, decoder_hidden, encoder_outputs)
        decoder_output, decoder_hidden = decoder(
            decoder_input, decoder_hidden)
        topv, topi = decoder_output.data.topk(1)
        ni = topi[0][0]

        decoder_input = Variable(torch.LongTensor([[ni]]))

        loss += criterion(decoder_output, target_variable[di])
        # if ni == EOS_token:
        #     break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.data[0] / target_length


def trainIters(encoder, decoder, n_iters, train_set, print_every=500, plot_every=100, learning_rate=0.01):
    start = time.time()
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
    training_pairs = [random.choice(train_set)
                      for i in range(n_iters)]
    criterion = nn.NLLLoss()

    for iter in range(1, n_iters + 1):
        training_pair = training_pairs[iter - 1]
        input_variable = training_pair[0]
        target_variable = training_pair[1]

        loss = train(input_variable, target_variable, encoder,
                     decoder, encoder_optimizer, decoder_optimizer, criterion)
        print_loss_total += loss
        plot_loss_total += loss

        if iter % print_every == 0:
            print_loss_avg = print_loss_total / print_every
            print_loss_total = 0
            print('%s (%d %d%%) %.4f' % (timeSince(start, iter / n_iters),
                                         iter, iter / n_iters * 100, print_loss_avg))
            print("Saving model...")
            torch.save(encoder, parameter_path)

        if iter % plot_every == 0:
            plot_loss_avg = plot_loss_total / plot_every
            plot_losses.append(plot_loss_avg)
            plot_loss_total = 0

def main():
    ### load word embedding
    pickle_file = open(embedding_path, "rb")
    word_embedding = pickle.load(pickle_file)
    pickle_file.close()

    word_index = word_embedding[0]
    embedding_map = word_embedding[1]
    output_size = len(word_index)

    ### initialize model
    hidden_size = 100
    encoder = EncoderRNN(hidden_size)
    decoder = DecoderRNN(hidden_size, output_size)
    
    ### load train data
    parser = AcademicParser("../train_data/Academic_papers/docs.json")
    abstracts = parser.get_paperAbstract()
    titles = parser.get_title() 
    assert(len(abstracts) == len(titles))

    ### prepare train data
    train_set = []
    for i in range(len(abstracts)):
        abstract = abstracts[i]
        title = titles[i]
        new_pair = variablesFromPair((abstract, title), word_index, embedding_map)    
        if (len(new_pair[1]) > 0):
            train_set.append(new_pair)

    trainIters(encoder, decoder, 20000, train_set)
    
    

if __name__ == '__main__':
    main()