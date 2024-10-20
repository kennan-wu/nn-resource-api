from rest_framework import viewsets, status
from rest_framework.response import Response
from .services.serializers.nn_serializers import CreateNNRequestSerializer, NeuralNetworkSerializer
from .services.neural_network_services.neural_networks import NeuralNetworkFactory
from .services.aws_services.S3_file_manager import S3FileManager
from dotenv import load_dotenv
from .models import NeuralNetwork
import os

load_dotenv()
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, 'test.txt')

bucket_name = os.getenv('NN_BUCKET_NAME')
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')

s3_manager = S3FileManager(bucket_name, aws_access_key, aws_secret_key, region_name)

def index(request):
    return Response("Hello, world. You're at the api index.")

class NeuralNetworkViewSet(viewsets.ViewSet):
    """
    ViewSet for Neural Network Operations
    """
    s3_manager = s3_manager

    def create(self, request):
        """
        Creates a Neural Network, posts metadata of the NN to the database, 
        and uploads the model to S3.
        """
        requestSerializer = CreateNNRequestSerializer(data=request.data)

        if not requestSerializer.is_valid():
            return Response(requestSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        layers = requestSerializer.validated_data['layers']
        input_shape = requestSerializer.validated_data['input_shape']
        description = requestSerializer.validated_data.get('description')
        name = requestSerializer.validated_data['name']
        
        nn_model = NeuralNetworkFactory(layers, input_shape, name, description)

        try:
            nn_metadata = NeuralNetwork.objects.create(**nn_model.db_representation)
        except Exception as e:
            return Response(
                {"error": f"Failed to save neural network metadata to the database: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        keras_model_stream = nn_model.get_keras_file_stream()
        json_model_stream = nn_model.get_json_file_stream()
        s3_keras_key = f'keras-neural-networks/{nn_metadata.id}.keras'
        s3_json_key = f'json-neural-networks/{nn_metadata.id}.json'

        message = 'Neural Network created successfully'

        try:
            self.s3_manager.upload_stream(keras_model_stream, s3_keras_key)
            self.s3_manager.upload_stream(json_model_stream, s3_json_key)
        except Exception as e:
            message = f'Neural Network created but failed to upload to S3: {str(e)}'

        serialized_nn_metadata = NeuralNetworkSerializer(nn_metadata)
        
        return Response(
            {
                'status': 'success',
                'message': message,
                'data': serialized_nn_metadata.data
            },
            status=status.HTTP_201_CREATED)
            

    def retrieve_network_info(self, request, pk=None):
        """
        Retrieve information about the neural network for frontend rendering
        """
        pass  