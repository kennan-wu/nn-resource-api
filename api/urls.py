from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Index route
    path("create/", views.NeuralNetworkViewSet.as_view({'post': 'create'}), name='create_neural_network'),  # Create route
    path("test-download/", views.NeuralNetworkViewSet.as_view({'get': 'test_download'}), name='test_download'),  # Test download route
    # path("download/<str:pk>/", views.NeuralNetworkViewSet.as_view({'get': 'download'}), name='download_neural_network')  # Dynamic download route
]
