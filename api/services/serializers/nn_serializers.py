from rest_framework import serializers
from keras import layers

class LayerSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['Dense'], default='Dense')
    neurons = serializers.IntegerField()
    activation = serializers.ChoiceField(choices=['relu', 'sigmoid', 'softmax', 'tanh'])

    def validate_type(self, value):
        if value != 'Dense':
            raise serializers.ValidationError(f"{value} is not allowed. Only 'Dense' layer is accepted.")
        return value


class NeuralNetworkSerializer(serializers.Serializer):
    layers = LayerSerializer(many=True)

    def validateLength(self, data):
        layers = data.get('layers', [])
        if len(layers) < 2:
            message = "The neural network must have more than a single layer"
            raise serializers.ValidationError(message)
