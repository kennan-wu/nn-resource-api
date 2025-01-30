from typing import Annotated

from fastapi import Depends
from services.user_service import UserService

user_service_dep = Annotated[UserService, Depends(lambda: UserService())]

