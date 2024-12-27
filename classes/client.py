from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import List, Dict, Optional
import logging

class Client:
    def __init__(
        self,
        _id: Optional[ObjectId] = None,
        user: Optional[ObjectId] = None,
        email: Optional[str] = None,
        hiredFreelancers: Optional[List[ObjectId]] = None,
        reviewsGiven: Optional[List[Dict[str, str]]] = None,
        createdAt: Optional[datetime] = None,
        updatedAt: Optional[datetime] = None,
    ):
        self._id = _id
        self.user = user
        self.email = email
        self.hiredFreelancers = hiredFreelancers or []
        self.reviewsGiven = reviewsGiven or []
        self.createdAt = createdAt or datetime.utcnow()
        self.updatedAt = updatedAt or datetime.utcnow()

    def save_to_db(self, db):
        client_data = {
            "user": self.user,
            "email": self.email,
            "hiredFreelancers": self.hiredFreelancers,
            "reviewsGiven": self.reviewsGiven,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
        try:
            if self._id:
                db.update_one({"_id": self._id}, {"$set": client_data})
                logging.info(f"Client with ID {self._id} updated successfully.")
            else:
                result = db.insert_one(client_data)
                self._id = result.inserted_id
                logging.info(f"Client inserted with ID {self._id}.")
        except Exception as e:
            logging.error(f"Error saving client: {e}")
            raise RuntimeError(f"Failed to save client: {e}")

    @classmethod
    def from_db(cls, db, _id: ObjectId):
        try:
            data = db.find_one({"_id": _id})
            if data:
                logging.info(f"Client with ID {data['_id']} found.")
                return cls(
                    _id=data["_id"],
                    user=data.get("user"),
                    email=data.get("email"),
                    hiredFreelancers=data.get("hiredFreelancers", []),
                    reviewsGiven=data.get("reviewsGiven", []),
                    createdAt=data.get("createdAt"),
                    updatedAt=data.get("updatedAt"),
                )
            logging.warning(f"No client found with ID {_id}.")
            return None
        except Exception as e:
            logging.error(f"Error fetching client with ID {_id}: {e}")
            raise RuntimeError(f"Failed to fetch client: {e}")

    def update(self, db, **kwargs):
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.updatedAt = datetime.utcnow()
            self.save_to_db(db)
            logging.info(f"Client with ID {self._id} updated successfully.")
        except Exception as e:
            logging.error(f"Error updating client with ID {self._id}: {e}")
            raise RuntimeError(f"Failed to update client: {e}")

    def delete(self, db):
        try:
            if self._id:
                db.delete_one({"_id": self._id})
                self._id = None
                logging.info(f"Client with ID {self._id} deleted successfully.")
            else:
                logging.warning("No client ID to delete.")
        except Exception as e:
            logging.error(f"Error deleting client with ID {self._id}: {e}")
            raise RuntimeError(f"Failed to delete client: {e}")

    def __repr__(self):
        return f"Client(user={self.user}, email={self.email}, hiredFreelancers={self.hiredFreelancers}, reviewsGiven={self.reviewsGiven})"
