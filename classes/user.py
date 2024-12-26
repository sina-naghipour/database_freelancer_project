from datetime import datetime
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
import logging


class User:
    """A class representing a user entity."""

    def __init__(
        self,
        _id: ObjectId = None,
        name: str = "",
        email: str = "",
        password_hash: str = "",
        profile_picture: str = "",
        bio: str = "",
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self._id = _id or ObjectId()
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.profile_picture = profile_picture
        self.bio = bio
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self) -> dict:
        """Converts the object to a dictionary for MongoDB storage."""
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "passwordHash": self.password_hash,
            "profilePicture": self.profile_picture,
            "bio": self.bio,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a User instance from a dictionary."""
        if not data:
            raise ValueError("Cannot create User from empty data.")
        return cls(
            _id=data["_id"],
            name=data["name"],
            email=data["email"],
            password_hash=data["passwordHash"],
            profile_picture=data["profilePicture"],
            bio=data["bio"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"],
        )

    def save_to_db(self, collection: Collection) -> ObjectId:
        """
        Saves the user object to the database.

        Parameters:
            collection (Collection): The MongoDB collection.

        Returns:
            ObjectId: The ID of the saved user.
        """
        try:
            self.updated_at = datetime.utcnow()  # Update timestamp
            collection.update_one(
                {"_id": self._id}, {"$set": self.to_dict()}, upsert=True
            )
            logging.info(f"User {self.name} saved/updated successfully.")
            return self._id
        except PyMongoError as e:
            logging.error(f"Failed to save user {self.name}: {e}")
            raise RuntimeError(f"Failed to save user: {e}")

    @classmethod
    def find_by_id(cls, collection: Collection, user_id: ObjectId):
        """
        Finds a user by their ID.

        Parameters:
            collection (Collection): The MongoDB collection.
            user_id (ObjectId): The user's ID.

        Returns:
            User: The found user instance, or None if not found.
        """
        try:
            data = collection.find_one({"_id": user_id})
            if data:
                logging.info(f"User found with ID {user_id}.")
                return cls.from_dict(data)
            logging.warning(f"No user found with ID {user_id}.")
            return None
        except PyMongoError as e:
            logging.error(f"Failed to fetch user by ID {user_id}: {e}")
            raise RuntimeError(f"Failed to fetch user: {e}")

    @classmethod
    def find_by_email(cls, collection: Collection, email: str):
        """
        Finds a user by their email.

        Parameters:
            collection (Collection): The MongoDB collection.
            email (str): The user's email.

        Returns:
            User: The found user instance, or None if not found.
        """
        try:
            data = collection.find_one({"email": email})
            if data:
                logging.info(f"User found with email {email}.")
                return cls.from_dict(data)
            logging.warning(f"No user found with email {email}.")
            return None
        except PyMongoError as e:
            logging.error(f"Failed to fetch user by email {email}: {e}")
            raise RuntimeError(f"Failed to fetch user by email: {e}")

    def delete(self, collection: Collection) -> bool:
        """
        Deletes the user from the database.

        Parameters:
            collection (Collection): The MongoDB collection.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            result = collection.delete_one({"_id": self._id})
            if result.deleted_count > 0:
                logging.info(f"User {self.name} deleted successfully.")
                return True
            logging.warning(f"No user found with ID {self._id} to delete.")
            return False
        except PyMongoError as e:
            logging.error(f"Failed to delete user {self.name}: {e}")
            raise RuntimeError(f"Failed to delete user: {e}")

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, bio={self.bio})"
