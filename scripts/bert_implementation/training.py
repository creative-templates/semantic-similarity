import pandas as pd
import tensorflow as tf
from batch_generator import BatchGenerator
from build import builder

train_df = pd.read_csv("SNLI_Corpus/snli_1.0_train.csv", nrows=100000)
valid_df = pd.read_csv("SNLI_Corpus/snli_1.0_dev.csv")
test_df = pd.read_csv("SNLI_Corpus/snli_1.0_test.csv")

train_df = (train_df[train_df.similarity != "-"].sample(frac=1.0).reset_index(drop=True))
valid_df = (valid_df[valid_df.similarity != "-"].sample(frac=1.0).reset_index(drop=True))


def is_entailment(x):
    return 1 if x == "entailment" else 2


train_df["label"] = train_df["similarity"].apply(lambda x: 0 if x == "contradiction" else is_entailment(x))
y_train = tf.keras.utils.to_categorical(train_df.label, num_classes=3)

valid_df["label"] = valid_df["similarity"].apply(lambda x: 0 if x == "contradiction" else is_entailment(x))
y_val = tf.keras.utils.to_categorical(valid_df.label, num_classes=3)

test_df["label"] = test_df["similarity"].apply(lambda x: 0 if x == "contradiction" else is_entailment(x))
y_test = tf.keras.utils.to_categorical(test_df.label, num_classes=3)

model = builder()

train_data = BatchGenerator(train_df[["sentence1", "sentence2"]].values.astype("str"), y_train, batch_size=32,
                            shuffle=True,)
valid_data = BatchGenerator(valid_df[["sentence1", "sentence2"]].values.astype("str"), y_val, batch_size=32,
                            shuffle=False,)


tf_bert_model, fitted = model.fit(train_data, validation_data=valid_data,
                                  epochs=2, use_multiprocessing=True, workers=-1,)

tf_bert_model.trainable = True
model.compile(optimizer=tf.keras.optimizers.Adam(1e-5), loss="categorical_crossentropy", metrics=["accuracy"],)
full_model = model.fit(train_data, validation_data=valid_data, epochs=2, use_multiprocessing=True, workers=-1,)
full_model.save("model")
