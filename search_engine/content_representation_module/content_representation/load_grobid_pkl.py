import pickle

def main():
    with open('grobid_data.pkl', 'rb') as input:
        while True:
            try:
                doc = pickle.load(input)
                print(doc.title)
                print(doc.embedding.shape)
            except EOFError:
                break
            

if __name__ == '__main__':
    main()