import re
import string

import contractions
import numpy as np
from autocorrect import Speller
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

spell = Speller("en")
lemmatizer = WordNetLemmatizer()
stopwords = set(stopwords.words("english"))
stopwords.remove("not")
no_punctuation = str.maketrans('', '', string.punctuation)

expand_contractions = np.vectorize(lambda x: contractions.fix(x))
change_not = np.vectorize(lambda x: "not" if x == "n't" else x)
remove_non_alphanumeric = np.vectorize(lambda x: re.sub('[^A-Za-z]+', '', x))
remove_stopwords = np.vectorize(lambda x: x if x not in stopwords else "")
lemmatize = np.vectorize(lambda x: lemmatizer.lemmatize(x))
correct_spelling = np.vectorize(lambda x: spell(x) if not x.isupper() else x)


def preprocess(text: str) -> str:
    # remove stackoverflow tags
    text = re.sub('(\[[a-z]+\])$', '', text)
    # remove urls
    text = re.sub(r'http\S+', '', text)
    # tokenize word
    tokens = word_tokenize(text)
    # expand contractions
    tokens = expand_contractions(tokens)
    # Change n't to not
    tokens = change_not(tokens)
    # remove non-alphabetic characters
    tokens = remove_non_alphanumeric(tokens)
    # removing stopwords
    tokens = remove_stopwords(tokens)
    # Remove empty strings
    tokens = list(filter(None, tokens))
    # lemmatize words
    tokens = lemmatize(tokens)
    # correct spelling
    tokens = correct_spelling(tokens)
    # convert to lower case
    text = " ".join(tokens).lower()

    return text
