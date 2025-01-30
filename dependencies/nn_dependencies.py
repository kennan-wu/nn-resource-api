from typing import Annotated

from fastapi import Depends
from services.keras_service import KerasService
from services.nn_service import NNService

nn_service_dep = Annotated[NNService, Depends(lambda: NNService())]
keras_service_dep = Annotated[KerasService, Depends(lambda: KerasService())]
