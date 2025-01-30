from models.user import User
from schema.user_schema import individual_user_serial
from config.database import user_collection
from bson import ObjectId
from fastapi import HTTPException

class UserService:
    def get_user(self, user_id: str) -> User:
        user = user_collection.find_one({"_id": ObjectId(user_id)})

        if user:
            return individual_user_serial(user)
        else:
            raise HTTPException(status_code=404, detail="User not found")
        
    def update_field(self, field: str, user_id: str, action: str, payload, session=None) -> User:        
        update_query = {action: {field: payload}}

        updated_user = user_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            update_query,
            session=session,
            return_document=True,
            upsert=True
        )

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return individual_user_serial(updated_user)