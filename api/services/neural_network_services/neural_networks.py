import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow import keras

class NeuralNetworkModel:
    def __init__(self, layers, input_shape):
        self.layers = layers
        self.input_shape = input_shape
        self.model = self._create_neural_network()
    
    def _create_neural_network(self):
        model = keras.Sequential()
        model.add(keras.layers.Input(shape=self.input_shape))
        
        for layer in self.layers:
            layer_type = getattr(keras.layers, layer['type'])
            model.add(layer_type(units=layer['neurons'], activation=layer['activation']))
        
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.build(input_shape=(None,) + self.input_shape)
        model.save('nn.keras')
        return model
    
    def network_information(self):
        network_info = []

        input_layer_info = {
            'layer_index': 0,
            'layer_type': 'InputLayer',
            'neurons': self.input_shape[0], 
            'weights': None,
            'biases': None,
            'activation': None
        }
        network_info.append(input_layer_info)
        
        for i, layer in enumerate(self.model.layers):
            layer_info = {
                'layer_index': i + 1,
                'layer_type': layer.__class__.__name__,
                'neurons': layer.units if hasattr(layer, 'units') else None,
                'weights': layer.get_weights()[0].tolist() if layer.get_weights() else None,
                'biases': layer.get_weights()[1].tolist() if len(layer.get_weights()) > 1 else None,
                'activation': layer.activation.__name__ if hasattr(layer, 'activation') else None
            }
            network_info.append(layer_info)
        
        return network_info

layers = [
    {'type': 'Dense', 'neurons': 5, 'activation': 'sigmoid'},
    {'type': 'Dense', 'neurons': 1, 'activation': 'sigmoid'}
]
input_shape = (2,)

nn_model = NeuralNetworkModel(layers, input_shape)

print(nn_model.network_information())
