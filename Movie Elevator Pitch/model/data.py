import numpy
import re
import gensim
import string
from nltk.tokenize.treebank import TreebankWordDetokenizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import regularizers



def cleanse_data(data):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    data = url_pattern.sub(r'', data)

    data = re.sub('\S*@\S*\s?', '', data)

    data = re.sub('\s+', ' ', data)

    data = re.sub("\'", "", data)
    data = str(data).lower()  # Lowercase words
    data = re.sub(r"\[(.*?)\]", "", data)  # Remove [+XYZ chars] in content
    data = re.sub(r"\s+", " ", data)  # Remove multiple spaces in content
    data = re.sub(r"\w+…|…", "", data)  # Remove ellipsis (and last word)
    data = re.sub(r"(?<=\w)-(?=\w)", " ", data)  # Replace dash between words
    data = re.sub(
        f"[{re.escape(string.punctuation)}]", "", data
    )  # Remove punctuation

    return data

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def detokenize(text):
    return TreebankWordDetokenizer().detokenize(text)

def processText(data, max_words):
    # max_len = 900

    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(data)
    sequences = tokenizer.texts_to_sequences(data)
    texts = pad_sequences(sequences)
    return texts
