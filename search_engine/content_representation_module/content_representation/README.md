# Content Representation module
This module is to train an embedder that embeds both the paper and the query. The way we train the embedder is as follows:

We first use a vanilla autoencoder to train a vector-based language model. This autoencoder takes as inputs the abstracts of the articles, generates a vector representation, and reconstructs the paper title from the vector. During training, the autoencoder tries to minimize the loss between the generated title and the original title. The encoder part of the trained autoencoder is then used as the embedder.

We use pretrained word2vec embedding on the Wikipedia corpus from [here](https://wikipedia2vec.github.io/wikipedia2vec/) as the initial word embedding. 

The parameters of the embedder is stored in `content_reprentation_module/content_representation/model_parameters/crmodel.pt`. To use the model, 
```
embedder = torch.load(PATH)
```
To embed any string, simply call
```
embedder.embed(STRING)
```
You can get the embedding for the entire ACL corpus by running
```
python3 get_content_representation.py
```
Each document will be stored as a `Doc` object (defined in `doc_parser.py`) in the resulting `grobid_data.pkl`. You can load these documents from the pickle file as described in `load_grobid_pkl.py`.
