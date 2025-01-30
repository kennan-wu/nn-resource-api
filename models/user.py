from pydantic import BaseModel
from bson import ObjectId
from models.neural_network import NeuralNetworkMetadata
from typing import List

class User(BaseModel):
    id: str
    name: str
    email: str
    neural_network_metadatas: List[NeuralNetworkMetadata]