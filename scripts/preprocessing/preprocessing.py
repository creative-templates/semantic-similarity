import re
import string

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
lemmatize = np.vectorize(lambda x: lemmatizer.lemmatize(x))


def preprocess(text: str) -> str:
    # remove stackoverflow tags
    text = re.sub('(\[[a-z]+\])$', '', text)
    # remove urls
    text = re.sub(r'http\S+', '', text)
    # tokenize word
    tokens = word_tokenize(text)

    tokens = lemmatize(tokens)

    text = " ".join(tokens)

    return text


print(preprocess("This is a test. Remove [python] and http://stackoverflow.com is a website."))
