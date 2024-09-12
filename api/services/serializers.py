from rest_framework import serializers

class LayerSerializer(serializers.Serializer):
    neurons = serializers.IntegerField()
    activation = serializers.ChoiceField(choices=['relu', 'sigmoid', 'softmax', 'tanh'])

class NeuralNetworkSerializer(serializers.Serializer):
    layers = LayerSerializer(many=True)