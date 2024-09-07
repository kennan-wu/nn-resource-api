# nnframework-backend

## Overview
This is the backend application for an ongoing project where users will eventually be able to create and view Neural networks through a GUI. This backend uses Django as a backend framework, Tensorflow, and Numpy.
The created and saved NNs will be saved in a S3 bucket as a JSON file.

## Endpoints
### Creating and modifying neural networks to S3
__Enpoint:__ `POST /api/v1/nn/initialize`
- This endpoint initilizes a Neural Network given the structure of the neural network in the body and will push to S3

__Endpoint:__ `GET /api/v1/nn/retrieve`
- This endpoint retreives and instantiates the nn stored in S3
