from typing import List
from models.layer import Layer
from models.request.create_nn_request import CreateNNRequest
from tensorflow import keras
import numpy as np
import io
import tempfile
import shutil
import os

class KerasService:
    def create_neural_network(self, nn_data: CreateNNRequest):
        input_features = (nn_data.neurons_per_layer[0],)
        
        model = keras.Sequential()
        model.add(keras.layers.Input(shape=input_features))
        
        for i in range(1, len(nn_data.activations)):
            model.add(keras.layers.Dense(units=nn_data.neurons_per_layer[i], activation=nn_data.activations[i]))
        
        loss_fn = "binary_crossentropy" if nn_data.neurons_per_layer[-1] == 1 else "categorical_crossentropy"
        model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])
        return model
    
    def serialize_for_db(self, model: keras.Model) -> List[dict]:
        layers = []
        
        for i, layer in enumerate(model.layers):
            if isinstance(layer, keras.layers.Dense):
                weights, biases = layer.get_weights() if layer.get_weights() else ([], [])
                activation = layer.activation.__name__

                num_neurons = len(biases)

                if num_neurons <= 16:
                    selected_biases = biases
                    selected_weights = weights
                else:
                    selected_biases = np.concatenate([biases[:8], biases[-8:]])

                    if weights.shape[0] > 16:
                        selected_weights = np.concatenate([
                            np.concatenate([weights[:8, :8], weights[:8, -8:]], axis=1),
                            np.concatenate([weights[-8:, :8], weights[-8:, -8:]], axis=1)
                        ], axis=0)

                    else:
                        selected_weights = np.concatenate([weights[:, :8], weights[:, -8:]], axis=1)

                layer_dict = {
                    "layerIndex": i,
                    "activation": activation,
                    "biases": selected_biases.tolist(),
                    "weights": selected_weights.tolist()
                }
                layers.append(layer_dict)

        return layers

    def get_keras_file_stream(self, model: keras.Model):
        """
        Serializes the model to an in-memory buffer.
        Returns a BytesIO object containing the serialized model data.
        """
        temp_dir = tempfile.mkdtemp()

        try:
            keras_file_path = os.path.join(temp_dir, 'model.keras')
            model.save(keras_file_path, overwrite=True)
            model_stream = io.BytesIO()
            with open(keras_file_path, 'rb') as f:
                model_stream.write(f.read())
            
            model_stream.seek(0)
            return model_stream

        finally:
            shutil.rmtree(temp_dir)