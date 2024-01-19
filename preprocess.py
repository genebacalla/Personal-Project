from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np




def purge(text):
    

    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalpha() and word.lower() not in stop_words]

    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]

    # cleaned_text = ' '.join(tokens)

    stemmed_tokens = ' '.join(tokens)
    return stemmed_tokens

def tokenize_data(data_list):
    tokenized_data = [word_tokenize(text.lower()) for text in data_list]
    return tokenized_data


def generate_feature_vectors(tokenized_data, model):
    feature_vector=[]
    for token in (tokenized_data):
        # print(token)
        vector = np.mean([model.wv[word] for word in token if word in model.wv], axis=0)
        feature_vector.append(vector)
  

    return feature_vector