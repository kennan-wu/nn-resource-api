from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from models.layer import Layer

class NeuralNetworkMetadata(BaseModel):
    id: str
    name: str
    description: str
    url: str
    createdAt: datetime
    lastUpdated: datetime

class NeuralNetwork(NeuralNetworkMetadata):
    id: str
    name: str
    description: str
    url: str
    createdAt: datetime
    lastUpdated: datetime
    layers: List[Layer]