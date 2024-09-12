from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .services.serializers import NeuralNetworkSerializer
from .services.neural_networks import create_neural_network

@api_view(["POST"])
def initialize(request):
    # validate api input data
    serializer = NeuralNetworkSerializer(data=request.data)

    if serializer.is_valid():
        # Create neural network
        layers = serializer.validated_data['layers']
        model = create_neural_network(layers)

        message = 'Neural Network created successfully'
        return message