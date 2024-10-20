from django.contrib import admin
from .models import NeuralNetwork

class NeuralNetworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'input_shape', 'layers', 'created_on', 'last_updated')

admin.site.register(NeuralNetwork, NeuralNetworkAdmin)
