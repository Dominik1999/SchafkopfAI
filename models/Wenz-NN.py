import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.optimizer_v1 import Adam

from utils import one_hot_encode_cards, translate_cards_to_str, translate_games_to_str, one_hot_encode_game, \
    one_hot_encode_position, one_hot_encode_result

# get the pandas dataframe
store = pd.HDFStore('/home/pirate/PycharmProjects/SchafkopfAI/models/training_data/data/Wenz-hands-with-pos.h5')
games_data = store['games_data']

# sanity check of process_data - for new process_data batch useful
#sanity_check_sample = games_data.sample(n=10)
#sample = []
#for i in range(sanity_check_sample.shape[0]):
#    sample.append([translate_cards_to_str(sanity_check_sample.cards.iloc[i]), sanity_check_sample.position.iloc[i], sanity_check_sample.result.iloc[i]])

msk = np.random.rand(len(games_data)) < 0.8
train = games_data[msk]
test = games_data[~msk]

train_examples_cards = []
train_examples_pos = []
train_labels = []
test_examples_cards = []
test_examples_pos = []
test_labels = []

#np.array((1,4),(8,32))
for cards in train.cards:
    train_examples_cards.append(one_hot_encode_cards(cards))
for pos in train.position:
    train_examples_pos.append(one_hot_encode_position(pos))
for result in train.result:
    train_labels.append(one_hot_encode_result(result[0]))
for cards in test.cards:
    test_examples_cards.append(one_hot_encode_cards(cards))
for pos in test.position:
    test_examples_pos.append(one_hot_encode_position(pos))
for result in test.result:
    test_labels.append(one_hot_encode_result(result[0]))

X1 = tf.data.Dataset.from_tensor_slices(train_examples_cards).batch(32)
X2 = tf.data.Dataset.from_tensor_slices(train_examples_pos).batch(32)
X = tf.data.Dataset.zip((X1,X2))
Y = tf.data.Dataset.from_tensor_slices(train_labels).batch(32)
XY = tf.data.Dataset.zip((X,Y))

X1t = tf.data.Dataset.from_tensor_slices(test_examples_cards).batch(32)
X2t = tf.data.Dataset.from_tensor_slices(test_examples_pos).batch(32)
Xt = tf.data.Dataset.zip((X1t,X2t))
Yt = tf.data.Dataset.from_tensor_slices(test_labels).batch(32)
XYt = tf.data.Dataset.zip((Xt,Yt))


input1 = Input(shape=(8,32), dtype=tf.float64, name='x1')
input2 = Input(shape=(4,), dtype=tf.float64, name='x2')
y1 = tf.keras.layers.Dense(units=64, activation='elu', kernel_initializer='he_uniform')(input1)
y1 = tf.keras.layers.Flatten()(y1)
y = tf.keras.layers.Concatenate(axis=1)([y1, input2])
y = tf.keras.layers.Dense(units=32, activation='elu', kernel_initializer='he_uniform')(y)
y = tf.keras.layers.Dense(units=2, activation='softmax', kernel_initializer='he_uniform')(y)
wenz_model = Model(inputs=[input1, input2], outputs=y)

adam = Adam(lr=0.02, decay=0.01)
wenz_model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=['accuracy'])

checkpoint_path = "training/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

wenz_model.fit(XY, epochs=10, callbacks=[cp_callback]) # add validation training_data?
test_loss, test_acc = wenz_model.evaluate(XYt, verbose=2)

print('\nTest accuracy:', test_acc)

wenz_model.save('/home/pirate/PycharmProjects/SchafkopfAI/models/trained_models/test-wenz-prediction6')
store.close()