from rest_framework import serializers
from ...models import NeuralNetwork

class LayerSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['Dense'], default='Dense')
    neurons = serializers.IntegerField()
    activation = serializers.ChoiceField(choices=['relu', 'sigmoid', 'softmax', 'tanh'])

    def validate_type(self, value):
        if value != 'Dense':
            raise serializers.ValidationError(f"{value} is not allowed. Only 'Dense' layer is accepted.")
        return value


class CreateNNRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(required=False, max_length=255)
    layers = LayerSerializer(many=True)
    input_shape = serializers.ListField(child=serializers.IntegerField(), min_length=1)

    def validate(self, data):
        layers = data.get('layers', [])
        if len(layers) < 2:
            raise serializers.ValidationError("The neural network must have more than a single layer.")
        
        return data

class NeuralNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeuralNetwork
        fields = '__all__'
