from models.user import User
from schema.nn_schema import individual_nn_metadata_serial

def individual_user_serial(user) -> User:
    return User(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        neural_network_metadatas=[
            individual_nn_metadata_serial(nn) for nn in user.get("neural_network_metadatas", [])
        ]
    )

def list_user_serial(users) -> list[User]:
    return [individual_user_serial(user) for user in users]
