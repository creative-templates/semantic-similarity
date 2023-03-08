import numpy as np
import tensorflow as tf
from batch_generator import BatchGenerator

model = tf.keras.models.load_model("model")
labels = ["contradiction", "entailment", "neutral"]


def similarity(sentence1, sentence2):
    sentence_pairs = np.array([[str(sentence1), str(sentence2)]])
    test_data = BatchGenerator(sentence_pairs, labels=None, batch_size=1, shuffle=False, include_targets=False,)
    proba = model.predict(test_data[0])[0]
    idx = np.argmax(proba)
    proba = f"{proba[idx]: .2f}%"
    pred = labels[idx]
    return pred, proba
