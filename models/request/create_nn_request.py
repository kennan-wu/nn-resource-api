from typing import List
from pydantic import BaseModel


class CreateNNRequest(BaseModel):
    name: str
    description: str
    neurons_per_layer: List[int]
    activations: List[str]