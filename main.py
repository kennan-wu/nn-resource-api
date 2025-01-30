from fastapi import FastAPI
from routes.user_routes import user_router
from routes.nn_routes import nn_router

app = FastAPI()

app.include_router(user_router)
app.include_router(nn_router)