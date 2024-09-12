from django.http import JsonResponse
from rest_framework.decorators import api_view
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential

model = Sequential()

@api_view(["POST"])
def initialize(request):
    data = request.data
    input_neurons = data.get('input_neurons')
    hidden_layers = data.get('hidden_layers', [])
    output_neurons = data.get('output_neurons')