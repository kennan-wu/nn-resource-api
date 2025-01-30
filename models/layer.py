from pydantic import BaseModel, Field, field_validator
from typing import List

class Layer(BaseModel):
    layerIndex: int
    activation: str
    biases: List[float] = Field(max_items = 16)
    weights: List[List[float]]

    @field_validator("weights")
    def checkWeights(cls, v):
        max_rows = 16
        max_cols = 16

        if len(v) > max_rows:
            raise ValueError(f"weights must have at most {max_rows} rows")

        for row in v:
            if len(row) > max_cols:
                raise ValueError(f"Each row in weights must have at most {max_cols} columns")
        
        return v