import os

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.python.keras.optimizer_v1 import Adam

from utils import one_hot_cards, translate_cards_to_str, translate_games_to_str, one_hot_encode_game

# get the pandas dataframe
store = pd.HDFStore('data/process_data/bidding-no-pos-700k-incl-all-pass.h5') # take bidding-no-pos-700k-incl-all-pass.h5 for real process_data
games_data = store['games_data']

# sanity check of process_data - for new process_data batch useful
sanity_check_sample = games_data.sample(n=10)
sample = []
for i in range(sanity_check_sample.shape[0]):
    sample.append([translate_cards_to_str(sanity_check_sample.games.iloc[i]), translate_games_to_str(sanity_check_sample.labels.iloc[i])])
print(sample)

msk = np.random.rand(len(games_data)) < 0.8
train = games_data[msk]
test = games_data[~msk]

train_examples = []
train_labels = []
test_examples = []
test_labels = []

for cards in train.games:
    train_examples.append(one_hot_cards(cards))
for game in train.labels:
    train_labels.append(one_hot_encode_game(game))
for cards in test.games:
    test_examples.append(one_hot_cards(cards))
for game in test.labels:
    test_labels.append(one_hot_encode_game(game))

train_dataset = tf.data.Dataset.from_tensor_slices((train_examples, train_labels)).batch(100)
test_dataset = tf.data.Dataset.from_tensor_slices((test_examples, test_labels)).batch(100)

# compile and build NN
bidding_nn = tf.keras.Sequential([
    tf.keras.layers.Dense(units=128, activation='elu', kernel_initializer='he_uniform'),
    tf.keras.layers.Dense(units=128, activation='elu', kernel_initializer='he_uniform'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=9, activation='softmax', kernel_initializer='he_uniform'),
])
adam = Adam(lr=0.02, decay=0.01)
bidding_nn.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])

checkpoint_path = "training/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

bidding_nn.fit(train_dataset, epochs=10, callbacks=[cp_callback]) # add validation data?
test_loss, test_acc = bidding_nn.evaluate(test_dataset, verbose=2)

print('\nTest accuracy:', test_acc)

bidding_nn.save('/home/pirate/PycharmProjects/SchafkopfAI/models/trained_models/bidding-nn-no-pos-700k')

# # Recreate the exact same model, including its weights and the optimizer
# new_model = tf.keras.models.load_model('my_model.h5')