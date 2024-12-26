from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import Optional
import logging

class Admin:
    def __init__(
        self,
        _id: Optional[ObjectId] = None,
        user: Optional[ObjectId] = None,
        role: Optional[str] = None,
        createdAt: Optional[datetime] = None,
        updatedAt: Optional[datetime] = None,
    ):
        self._id = _id
        self.user = user
        self.role = role
        self.createdAt = createdAt or datetime.utcnow()
        self.updatedAt = updatedAt or datetime.utcnow()

    def save_to_db(self, db):
        """Save the Admin document to MongoDB."""
        admin_data = {
            "user": self.user,
            "role": self.role,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
        try:
            if self._id:
                db.update_one({"_id": self._id}, {"$set": admin_data})
                logging.info(f"Admin with ID {self._id} updated successfully.")
            else:
                result = db.insert_one(admin_data)
                self._id = result.inserted_id
                logging.info(f"Admin inserted with ID {self._id}.")
        except Exception as e:
            logging.error(f"Error saving admin: {e}")
            raise RuntimeError(f"Failed to save admin: {e}")

    @classmethod
    def from_db(cls, db, _id: ObjectId):
        """Retrieve an Admin document from MongoDB and create an instance."""
        try:
            data = db.find_one({"_id": _id})
            if data:
                logging.info(f"Admin with ID {data['_id']} found.")
                return cls(
                    _id=data["_id"],
                    user=data.get("user"),
                    role=data.get("role"),
                    createdAt=data.get("createdAt"),
                    updatedAt=data.get("updatedAt"),
                )
            logging.warning(f"No admin found with ID {_id}.")
            return None
        except Exception as e:
            logging.error(f"Error fetching admin with ID {_id}: {e}")
            raise RuntimeError(f"Failed to fetch admin: {e}")

    def update(self, db, **kwargs):
        """Update specific fields of the Admin document."""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.updatedAt = datetime.utcnow()
            self.save_to_db(db)
            logging.info(f"Admin with ID {self._id} updated successfully.")
        except Exception as e:
            logging.error(f"Error updating admin with ID {self._id}: {e}")
            raise RuntimeError(f"Failed to update admin: {e}")

    def delete(self, db):
        """Delete the Admin document from MongoDB."""
        try:
            if self._id:
                db.delete_one({"_id": self._id})
                self._id = None
                logging.info(f"Admin with ID {self._id} deleted successfully.")
            else:
                logging.warning("No admin ID to delete.")
        except Exception as e:
            logging.error(f"Error deleting admin with ID {self._id}: {e}")
            raise RuntimeError(f"Failed to delete admin: {e}")

    def __repr__(self):
        return f"Admin(user={self.user}, role={self.role})"
