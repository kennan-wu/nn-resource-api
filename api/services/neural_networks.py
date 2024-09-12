import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from tensorflow import keras

def create_neural_network(layers, input_shape):
    model = keras.Sequential()

    for i, layer in enumerate(layers):
        if i == 0:
            model.add(keras.layers.Dense(units=layer['units'], activation=layer['activation'], input_shape=input_shape))
        else:
            model.add(keras.layers.Dense(units=layer['units'], activation=layer['activation']))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.build(input_shape=(None,) + input_shape)

    return model

layers = [
    {'units': 64, 'activation': 'relu'},
    {'units': 32, 'activation': 'relu'},
    {'units': 10, 'activation': 'softmax'}
]
input_shape = (100,)

model = create_neural_network(layers, input_shape)

model.summary()