from rest_framework import serializers
from tensorflow import keras
from keras import layers

class LayerSerializer(serializers.Serializer):
    type = serializers.CharField(default="")
    neurons = serializers.IntegerField()
    activation = serializers.ChoiceField(choices=['relu', 'sigmoid', 'softmax', 'tanh'])
    inputDim = serializers.IntegerField()
    outputDim = serializers.IntegerField()

    def validate_type(self, value):
        try:
            layer_class = eval(f"layers.{value}")
            
            if not isinstance(layer_class, type) or not issubclass(layer_class, layers.Layer):
                raise serializers.ValidationError(f"{value} is not a valid Keras layer type.")
        except (AttributeError, NameError):
            raise serializers.ValidationError(f"{value} is not a valid Keras layer type.")
        
        return value


class NeuralNetworkSerializer(serializers.Serializer):
    layers = LayerSerializer(many=True)

    def validateLength(self, data):
        layers = data.get('layers', [])
        if len(layers) < 2:
            message = "The neural network must have more than a single layer"
            raise serializers.ValidationError(message)
