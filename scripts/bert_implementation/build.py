import tensorflow as tf
import transformers

MAXLENGTH = 32
strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    input_ids = tf.keras.layers.Input(
        shape=(MAXLENGTH,), dtype=tf.int32, name="input_ids"
    )
    attention_masks = tf.keras.layers.Input(
        shape=(MAXLENGTH,), dtype=tf.int32, name="attention_masks"
    )
    token_type_ids = tf.keras.layers.Input(
        shape=(MAXLENGTH,), dtype=tf.int32, name="token_type_ids"
    )

    tf_bert_model = transformers.TFBertModel.from_pretrained("bert-base-uncased")
    tf_bert_model.trainable = False

    bert_output = tf_bert_model.bert(
        input_ids, attention_mask=attention_masks, token_type_ids=token_type_ids
    )
    last_h_state = bert_output.last_hidden_state
    pool_output = bert_output.pooler_output
    lstm = tf.keras.layers.LSTM(64, return_sequences=True)
    bi_lstm = tf.keras.layers.Bidirectional(lstm)(last_h_state)
    avg_pool = tf.keras.layers.GlobalAveragePooling1D()(bi_lstm)
    max_pool = tf.keras.layers.GlobalMaxPooling1D()(bi_lstm)
    concated = tf.keras.layers.concatenate([avg_pool, max_pool])
    dropedout = tf.keras.layers.Dropout(0.3)(concated)

    inputs = [input_ids, attention_masks, token_type_ids]
    output = tf.keras.layers.Dense(3, activation="softmax")(dropedout)
    model = tf.keras.models.Model(inputs=inputs, outputs=output)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss="categorical_crossentropy",
        metrics=["acc"],
    )
