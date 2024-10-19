from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.NeuralNetworkViewSet.as_view({'post': 'create'}), name='create_neural_network')
]