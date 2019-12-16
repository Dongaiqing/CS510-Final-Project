import argparse
from paperloader import Paper_loader
from tokenization import tokenize_articles, nan_to_str, convert_tokens_to_int, get_words_freq
from word_embeddings import load_word_embeddings, process_word_embedding_for_corpus_vocab, save_word_vocab_embeddings

word2vec_path = "/Users/luzijie/Desktop/CS510/project/CS510-Literature-Search-Engine/search_engine/content_representation"

def create_args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
            '--input_word_embeddings_path', default= word2vec_path + '/enwiki_20180420_100d.txt',
            help='Input path of the word2vec embeddings model (word2vec).')    

    parser.add_argument(
            '--output_tf_records_path', default='',
            help='Output path for generated TFRecords with news content.')

    parser.add_argument(
            '--output_word_vocab_embeddings_path', default= word2vec_path + '/train_data/Academic_papers/pickles/word_embeddings.pickle',
            help='Output path for a pickle with words vocabulary and corresponding word embeddings.')

    parser.add_argument(
            '--output_label_encoders', default='',
            help='Output path for a pickle with label encoders (article_id, category_id, publisher_id).')

    parser.add_argument(
        '--articles_by_tfrecord', type=int, default=1000,
        help='Number of articles to be exported in each TFRecords file')

    parser.add_argument(
        '--vocab_most_freq_words', type=int, default=50000,
        help='Most frequent words to keep in vocab')

    return parser

def main():
    parser = create_args_parser()
    args = parser.parse_args()
    
    print("Load papers")
    loader = Paper_loader()

    print("Tokenize papers")
    tokenized_articles = tokenize_articles(loader.get_paper())

    print('Computing word frequencies...')
    words_freq = get_words_freq(tokenized_articles)
    print('Corpus vocabulary size: {}'.format(len(words_freq)))

    print("Loading word2vec model and extracting words of this corpus' vocabulary...")
    w2v_model = load_word_embeddings(args.input_word_embeddings_path, binary=False)
    print("process embeddings")
    word_vocab, word_embeddings_matrix = process_word_embedding_for_corpus_vocab(w2v_model, 
                                                                                words_freq,
                                                                                args.vocab_most_freq_words)

    print('Saving word embeddings and vocab.: {}'.format(args.output_word_vocab_embeddings_path))
    save_word_vocab_embeddings(args.output_word_vocab_embeddings_path, 
                               word_vocab, word_embeddings_matrix)

if __name__ == '__main__':
    main()