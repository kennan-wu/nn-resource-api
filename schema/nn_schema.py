from models.layer import Layer
from models.neural_network import NeuralNetwork, NeuralNetworkMetadata


def individual_nn_metadata_serial(nn_metadata) -> NeuralNetworkMetadata:
    return NeuralNetworkMetadata(
        id=str(nn_metadata["_id"]),
        name=nn_metadata["name"],
        description=nn_metadata["description"],
        url=nn_metadata["url"],
        createdAt=nn_metadata["createdAt"],
        lastUpdated=nn_metadata["lastUpdated"]
    )

def list_nn_metadata_serial(nn_metadata_list) -> list[NeuralNetworkMetadata]:
    return [individual_nn_metadata_serial(nn) for nn in nn_metadata_list]

def individual_nn_serial(nn) -> NeuralNetwork:
    return NeuralNetwork(
        id=str(nn["_id"]),
        name=nn["name"],
        description=nn["description"],
        url=nn["url"],
        createdAt=nn["createdAt"],
        lastUpdated=nn["lastUpdated"],
        layers=[individual_layer_serial(layer) for layer in nn["layers"]]
    )

def list_nn_serial(nn_list) -> list[NeuralNetwork]:
    return [individual_nn_serial(nn) for nn in nn_list]

def individual_layer_serial(layer) -> Layer:
    return Layer(
        layerIndex=layer["layerIndex"],
        activation=layer["activation"],
        biases=layer["biases"],
        weights=layer["weights"]
    )

def list_layer_serial(layer_list) -> list[Layer]:
    return [individual_layer_serial(layer) for layer in layer_list]
