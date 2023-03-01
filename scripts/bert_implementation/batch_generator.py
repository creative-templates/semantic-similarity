import numpy as np
import transformers
from tensorflow import keras


class BatchGenertor(keras.utils.Sequence):
    def __init__(self, sentences, classes, batch_size=32, randomize=True, targets_in_output=True):
        self.sentences = sentences
        self.classes = classes
        self.randomize = randomize
        self.batch_size = batch_size
        self.targets_in_output = targets_in_output
        self.indexes = np.arange(len(self.sentences))
        self.tokenizer = transformers.BertTokenizer.from_pretrained("bert-base-uncased")
        self.on_epoch_end()

    def __len__(self):
        return len(self.sentences) // self.batch_size

    def __getitem__(self, idx):
        indexes = self.indexes[idx * self.batch_size: (idx + 1) * self.batch_size]
        sentences = self.sentences[indexes]

        encoded = self.tokenizer.batch_encode_plus(sentences.tolist(), add_special_tokens=True, max_length=128,
                                                   return_attention_mask=True, return_token_type_ids=True,
                                                   pad_to_max_length=True, return_tensors="tf", truncation=True)

        input_ids = np.array(encoded["input_ids"], dtype="int32")
        attention_masks = np.array(encoded["attention_mask"], dtype="int32")
        token_type_ids = np.array(encoded["token_type_ids"], dtype="int32")

        if self.targets_in_output:
            labels = np.array(self.classes[indexes], dtype="int32")
            return [input_ids, attention_masks, token_type_ids], labels
        else:
            return [input_ids, attention_masks, token_type_ids]

    def on_epoch_end(self):
        if self.randomize:
            np.random.RandomState(42).shuffle(self.indexes)
