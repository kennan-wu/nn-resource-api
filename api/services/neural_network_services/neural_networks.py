import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import json
import tensorflow as tf
from tensorflow import keras
import io
import tempfile
import shutil

class NeuralNetworkFactory:
    def __init__(self, layers, input_shape, name, description=None):
        self.layers = layers
        self.input_shape = tuple(input_shape)
        self.name = name
        self.description = description
        self.model = self.create_neural_network()
        self.db_representation = self.serialize_for_db()
        
    def create_neural_network(self):
        model = keras.Sequential()
        model.add(keras.layers.Input(shape=self.input_shape))
        
        for layer in self.layers:
            layer_type = getattr(keras.layers, layer['type'])
            model.add(layer_type(units=layer['neurons'], activation=layer['activation']))
        
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.build(input_shape=(None,) + self.input_shape)
        return model

    def get_keras_file_stream(self):
        """
        Serializes the model to an in-memory buffer.
        Returns a BytesIO object containing the serialized model data.
        """
        temp_dir = tempfile.mkdtemp()

        try:
            keras_file_path = os.path.join(temp_dir, 'model.keras')
            self.model.save(keras_file_path, overwrite=True)
            model_stream = io.BytesIO()
            with open(keras_file_path, 'rb') as f:
                model_stream.write(f.read())
            
            model_stream.seek(0)
            return model_stream

        finally:
            shutil.rmtree(temp_dir)

    def serialize_for_db(self):
        model_info = {
            'name': self.name,
            'description': self.description,
            'input_shape': list(self.input_shape),
            'layers': [
                {
                    'type': layer.__class__.__name__,
                    'neurons': layer.get_config().get('units') if 'units' in layer.get_config() else None,
                    'activation': layer.get_config().get('activation')
                } for layer in self.model.layers
            ]
        }
        return model_info

    def get_json_file_stream(self):
        model_data = []

        for i, layer in enumerate(self.model.layers):
            layer_info = {
                'weights': None,
                'biases': None,
                'activation_values': [None] * (layer.get_config().get('units') if 'units' in layer.get_config() else 0)
            }

            weights_biases = layer.get_weights()
            if weights_biases:
                weights, biases = weights_biases if len(weights_biases) == 2 else (weights_biases[0], None)
                layer_info['weights'] = weights.tolist() if weights is not None else None
                layer_info['biases'] = biases.tolist() if biases is not None else None

            model_data.append(layer_info)

        json_data = json.dumps(model_data)
        return io.BytesIO(json_data.encode('utf-8'))

# layers = [
#     {'type': 'Dense', 'neurons': 5, 'activation': 'sigmoid'},
#     {'type': 'Dense', 'neurons': 1, 'activation': 'sigmoid'}
# ]
# input_shape = [2,]
# name = "test"

# nn_model = NeuralNetworkFactory(layers, input_shape, name)