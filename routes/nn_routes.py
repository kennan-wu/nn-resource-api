from fastapi import APIRouter
from dependencies.nn_dependencies import nn_service_dep, keras_service_dep
from dependencies.user_dependencies import user_service_dep
from dependencies.general_dependencies import s3_service_dep
from models.request.create_nn_request import CreateNNRequest

nn_router = APIRouter(prefix="/user/{user_id}/nn")


@nn_router.get("/")
async def get_all_neural_networks(
    user_id: str, nn_service: nn_service_dep, user_service: user_service_dep
):
    user = user_service.get_user(user_id)
    return nn_service.getAllNN(user)


@nn_router.get("/{nn_id}")
async def get_nn_with_id(nn_id: str, nn_service: nn_service_dep):
    return nn_service.getNN(nn_id)


@nn_router.post("/")
async def create_neural_network(
    user_id: str,
    nn_data: CreateNNRequest,
    nn_service: nn_service_dep,
    user_service: user_service_dep,
    keras_service: keras_service_dep,
    s3_service: s3_service_dep,
):
    user = user_service.get_user(user_id)
    return nn_service.createNN(user, nn_data, user_service, keras_service, s3_service)


@nn_router.delete("/delete/{nn_id}")
async def delete_neural_network(
    nn_id: str,
    user_id: str,
    nn_service: nn_service_dep,
    s3_service: s3_service_dep,
    user_service: user_service_dep,
):
    removed_id = nn_service.deleteNN(nn_id, user_id, user_service, s3_service)
    return removed_id
