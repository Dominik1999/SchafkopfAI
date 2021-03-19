import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.optimizer_v1 import Adam

from utils import one_hot_encode_cards, translate_cards_to_str, translate_games_to_str, one_hot_encode_game, \
    one_hot_encode_position, one_hot_encode_protocol, one_hot_encode_game_chosen


def compile_bidding_model():
    # bidding neural net
    input1 = Input(shape=(8, 32), dtype=tf.float64, name='x1')
    input2 = Input(shape=(4,), dtype=tf.float64, name='x2')
    input3 = Input(shape=(4, 10), dtype=tf.float64, name='x3')
    y1 = tf.keras.layers.Dense(units=128, activation='elu', kernel_initializer='he_uniform')(input1)
    y1 = tf.keras.layers.Flatten()(y1)
    y2 = tf.keras.layers.Concatenate(axis=1)([y1, input2])
    y2 = tf.keras.layers.Dense(units=128, activation='elu', kernel_initializer='he_uniform')(y2)
    y2 = tf.keras.layers.Flatten()(y2)
    y3 = tf.keras.layers.Dense(units=128, activation='elu', kernel_initializer='he_uniform')(input3)
    y3 = tf.keras.layers.Flatten()(y3)
    y4 = tf.keras.layers.Concatenate(axis=1)([y2, y3])
    y4 = tf.keras.layers.Dense(units=128, activation='elu', kernel_initializer='he_uniform')(y4)
    y = tf.keras.layers.Dense(units=9, activation='softmax', kernel_initializer='he_uniform')(y4)
    model = Model(inputs=[input1, input2, input3], outputs=y)

    # compile and build NN
    adam = Adam(lr=0.02, decay=0.01)
    model.compile(optimizer='adam',
                          loss=tf.keras.losses.CategoricalCrossentropy(),
                          metrics=['accuracy'])

    return model


# get the pandas dataframe
store = pd.HDFStore('/models/training_data/data/bidding-pos-101000001-102000070.h5')
games_data = store['games_data']

games_data = games_data.dropna()
# sanity check of process_data - for new process_data batch useful
#sanity_check_sample = games_data.sample(n=10)
#sample = []
#for i in range(sanity_check_sample.shape[0]):
#    sample.append(
#        [translate_cards_to_str(sanity_check_sample.cards.iloc[i]),
#         sanity_check_sample.position.iloc[i],
#         translate_games_to_str(sanity_check_sample.label.iloc[i]),
#         sanity_check_sample.points.iloc[i]])
#print(sample)

# Split data into training and test data

msk = np.random.rand(len(games_data)) < 0.8
train = games_data[msk]
test = games_data[~msk]

# now prepare training data
X1 = tf.data.Dataset.from_tensor_slices([one_hot_encode_cards(cards) for cards in train.cards]).batch(100)
X2 = tf.data.Dataset.from_tensor_slices([one_hot_encode_position(position) for position in train.position]).batch(100)
X3 = tf.data.Dataset.from_tensor_slices([one_hot_encode_protocol(protocol) for protocol in train.protocol]).batch(100)
X12 = tf.data.Dataset.zip((X1, X2))
X = tf.data.Dataset.zip((X12, X3))
Y = tf.data.Dataset.from_tensor_slices([one_hot_encode_game_chosen(label) for label in train.label]).batch(100)
XY = tf.data.Dataset.zip((X, Y))

print("Training Data Created")

# now prepare testing data
X1t = tf.data.Dataset.from_tensor_slices([one_hot_encode_cards(cards) for cards in test.cards]).batch(100)
X2t = tf.data.Dataset.from_tensor_slices([one_hot_encode_position(position) for position in test.position]).batch(100)
X3t = tf.data.Dataset.from_tensor_slices([one_hot_encode_protocol(protocol) for protocol in test.protocol]).batch(100)
X12t = tf.data.Dataset.zip((X1t, X2t))
Xt = tf.data.Dataset.zip((X12t, X3t))
Yt = tf.data.Dataset.from_tensor_slices([one_hot_encode_game_chosen(label) for label in test.label]).batch(100)
XYt = tf.data.Dataset.zip((Xt, Yt))

print("Test Data Created")

#bidding_model = compile_bidding_model()
bidding_model = tf.keras.models.load_model('/home/pirate/PycharmProjects/SchafkopfAI/models/trained_models/bidding-pos-nn')

checkpoint_path = "training/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

bidding_model.fit(XY, epochs=10, callbacks=[cp_callback]) # add validation training_data?
test_loss, test_acc = bidding_model.evaluate(XYt, verbose=2)

print('\nTest accuracy:', test_acc)

bidding_model.save('/home/pirate/PycharmProjects/SchafkopfAI/models/trained_models/bidding-pos-nn')
