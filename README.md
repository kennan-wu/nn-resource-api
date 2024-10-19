# nnframework-backend

## Overview

This is the backend application for an ongoing project where users will eventually be able to create and view Neural networks through a GUI. This backend uses Django, SQLite, and Tensorflow.
The created and saved NNs will be saved in a S3 bucket as a JSON file.

## Getting Started

1. Download the dependancies: `pip install -r requirements.txt`
2. Create a `.env` file in the root directory. You will need:
   1. `NN_BUCKET_NAME`
   2. `AWS_ACCESS_KEY_ID`
   3. `AWS_SECRET_ACCESS_KEY`
   4. `AWS_REGION`
3. To start the project run: `python manage.py runserver`

### Admin Page

There is an admin endpoint that allows you to work with database items through a GUI. To do so, you need to create an admin account: `python manage.py createsuperuser`. Follow the prompts to create your account. Afterwards, run the server and visit `http://127.0.0.1:8000/admin/`.

## Endpoints

### Creating and modifying neural networks

**Enpoint:** `POST /api/nn/start`

- Creates a Neural Network whose metadata is posted to the SQLite database, and the file of the neural net is uploaded to S3

Sample request body:

```json
{
  "name": "test_nn",
  "layers": [
    { "type": "Dense", "neurons": 5, "activation": "sigmoid" },
    { "type": "Dense", "neurons": 1, "activation": "sigmoid" }
  ],
  "input_shape": [2]
}
```

Sample response:

```json
{
  "status": "success",
  "message": "Neural Network created successfully",
  "data": {
    "id": "0afb3dc8-9a4e-41ee-88b7-d8f83da64228",
    "name": "test_nn",
    "created_on": "2024-10-19T00:56:57.869215-05:00",
    "last_updated": "2024-10-19T00:56:57.869215-05:00"
  }
}
```
