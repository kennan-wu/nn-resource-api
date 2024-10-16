from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .services.serializers.nn_serializers import NeuralNetworkSerializer
from .services.neural_network_services.neural_networks import createNeuralNetwork

class NeuralNetworkViewSet(viewsets.ViewSet):
    """
    ViewSet for Neural Network Operations
    """
    def create(self, request):
        # Validate API input data
        serializer = NeuralNetworkSerializer(data=request.data)

        if serializer.is_valid():
            # Create neural network
            layers = serializer.validated_data['layers']
            model = createNeuralNetwork(layers)

            message = 'Neural Network created successfully'
            return Response({'message': message}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve_network_info(self, request, pk=None):
        """
        Retrieve information about the neural network for frontend rendering
        """
        