import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from tensorflow import keras

def createNeuralNetwork(layers, inputShape):
    model = keras.Sequential()

    for i, layer in enumerate(layers):
        layerType = getattr(keras.layers, layer['type'])
        
        if layer['type'] == 'Embedding':
            model.add(layerType(input_dim=layer.get('inputDim', 1000),
                                output_dim=layer.get('outputDim', 64),
                                input_length=inputShape[0]))
        else:
            if i == 0:
                model.add(layerType(units=layer['neurons'], activation=layer['activation'], input_shape=inputShape))
            else:
                model.add(layerType(units=layer['neurons'], activation=layer['activation']))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

layers = [
    {'type': 'Embedding', 'inputDim': 1000, 'outputDim': 64}, 
    {'type': 'Dense', 'neurons': 32, 'activation': 'relu'},
    {'type': 'Dense', 'neurons': 10, 'activation': 'softmax'}
]

inputShape = (100,)

model = createNeuralNetwork(layers, inputShape)

model.summary()
