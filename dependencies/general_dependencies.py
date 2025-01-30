from typing import Annotated

from fastapi import Depends
from services.s3_service import S3Service

s3_service_dep = Annotated[S3Service, Depends(lambda: S3Service())]

