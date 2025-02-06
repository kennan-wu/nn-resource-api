from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException
from models.request.create_nn_request import CreateNNRequest
from models.user import User
from schema.nn_schema import individual_nn_serial, list_nn_serial, list_nn_metadata_serial
from config.database import nn_collection, client
from services.keras_service import KerasService
from services.s3_service import S3Service
from services.user_service import UserService


class NNService:
    def getAllNN(self, user: User):
        return user.neural_network_metadatas

    def getNN(self, nn_id: str):
        nn = nn_collection.find_one({"_id": ObjectId(nn_id)})

        if nn:
            return individual_nn_serial(nn)
        else:
            raise HTTPException(status_code=404, detail="Neural network not found")
        
    def createNN(self, user: User, 
                 nn_data: CreateNNRequest,
                 user_service: UserService,
                 keras_service: KerasService,
                 s3_service: S3Service
    ):
        model_id = str(ObjectId())
        model = keras_service.create_neural_network(nn_data)

        session = client.start_session()
        try:
            with session.start_transaction():
                nn_url = self._uploadModelToBucket(model, keras_service, s3_service, user.id, model_id)
                self._uploadModelToDB(nn_data, model, model_id, nn_url, keras_service, session)
                user = self._uploadMetadataModelToDB(nn_data, model_id, nn_url, user.id, user_service, session)
                session.commit_transaction()
                return model_id
        except Exception as e:
            session.abort_transaction()
            raise Exception(f"Transaction failed: {str(e)}")
        finally:
            session.end_session()

    def _uploadMetadataModelToDB(self, nn_data, model_id, nn_url, user_id, user_service, session):
        nn_metadata_dict = self._createNNMetadataDict(nn_data, model_id, nn_url)
        user = user_service.update_field("neural_network_metadatas", user_id, "$push", nn_metadata_dict, session)
        return user

    def _uploadModelToBucket(self, model, keras_service: KerasService, s3_service: S3Service, user_id, model_id):
        model_file_stream = keras_service.get_keras_file_stream(model)
        nn_url = s3_service.upload_stream(model_file_stream, f"{user_id}/{model_id}.keras")
        return nn_url

    def _uploadModelToDB(self, nn_data, model, model_id, nn_url, keras_service, session):
        nn_dict = self._createNNDict(nn_data, model, model_id, nn_url, keras_service)
        return nn_collection.insert_one(nn_dict, session=session)

    def _createNNMetadataDict(self, nn_data: CreateNNRequest,
                      model_id,
                      model_url,
    ):
        return {
            "_id": ObjectId(model_id),
            "name": nn_data.name,
            "description": nn_data.description,
            "url": model_url,
            "createdAt": datetime.now(timezone.utc),
            "lastUpdated": datetime.now(timezone.utc),
        }

    def _createNNDict(self, nn_data: CreateNNRequest,
                      model, 
                      model_id,
                      model_url,
                      keras_service: KerasService
    ):
        serialized_layers = keras_service.serialize_for_db(model)
        return {
            "_id": ObjectId(model_id),
            "name": nn_data.name,
            "description": nn_data.description,
            "url": model_url,
            "createdAt": datetime.now(timezone.utc),
            "lastUpdated": datetime.now(timezone.utc),
            "layers": serialized_layers
        }