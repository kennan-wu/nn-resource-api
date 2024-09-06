# nnframework-backend

## Overview
This is the backend application for an ongoing project where users will eventually be able to create and view Neural networks through a GUI. This backend uses Django as a backend framework, Tensorflow, and Numpy.
The created and saved NNs will be saved in a S3 bucket as a JSON file.

## Endpoints
### Creating and modifying neural networks to S3
__Enpoint:__ `POST /api/nn/initialize`
__body:__
- `inputLayer: int` the amount of neurons in the input layer
- `hiddenLayers: int[]` length of this arr is the amount of hidden layers, and each element represents the amount of neurons in hiddenLayers[i]
This endpoint initilizes a Neural Network given the structure of the neural network in the body and will push to S3

__Endpoint:__ `GET /api/nn/retrieve`
__body:__ TBD
This endpoint retreives and instantiates the nn stored in S3
