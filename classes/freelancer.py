from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict
import logging

class Freelancer:
    def __init__(
        self,
        _id: Optional[ObjectId] = None,
        user: Optional[ObjectId] = None,
        email: Optional[str] = None,
        skills: Optional[List[str]] = None,
        services: Optional[List[Dict[str, str]]] = None,
        portfolio: Optional[List[Dict[str, str]]] = None,
        reviews: Optional[List[Dict[str, str]]] = None,
        averageRating: Optional[float] = None,
        createdAt: Optional[datetime] = None,
        updatedAt: Optional[datetime] = None,
    ):
        self._id = _id
        self.user = user
        self.email = email
        self.skills = skills or []
        self.services = services or []
        self.portfolio = portfolio or []
        self.reviews = reviews or []
        self.averageRating = averageRating
        self.createdAt = createdAt or datetime.utcnow()
        self.updatedAt = updatedAt or datetime.utcnow()

    def save_to_db(self, db):
        """Save the Freelancer document to MongoDB."""
        freelancer_data = {
            "user": self.user,
            "email": self.email,
            "skills": self.skills,
            "services": self.services,
            "portfolio": self.portfolio,
            "reviews": self.reviews,
            "averageRating": self.averageRating,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
        try:
            if self._id:
                db.update_one({"_id": self._id}, {"$set": freelancer_data})
                logging.info(f"Freelancer with ID {self._id} updated successfully.")
            else:
                result = db.insert_one(freelancer_data)
                self._id = result.inserted_id
                logging.info(f"Freelancer inserted with ID {self._id}.")
        except Exception as e:
            logging.error(f"Error saving freelancer: {e}")
            raise RuntimeError(f"Failed to save freelancer: {e}")

    @classmethod
    def from_db(cls, db, _id: ObjectId):
        """Retrieve a Freelancer document from MongoDB and create an instance."""
        try:
            data = db.find_one({"_id": _id})
            if data:
                logging.info(f"Freelancer with ID {data['_id']} found.")
                return cls(
                    _id=data["_id"],
                    user=data.get("user"),
                    email=data.get("email"),
                    skills=data.get("skills", []),
                    services=data.get("services", []),
                    portfolio=data.get("portfolio", []),
                    reviews=data.get("reviews", []),
                    averageRating=data.get("averageRating"),
                    createdAt=data.get("createdAt"),
                    updatedAt=data.get("updatedAt"),
                )
            logging.warning(f"No freelancer found with ID {_id}.")
            return None
        except Exception as e:
            logging.error(f"Error fetching freelancer with ID {_id}: {e}")
            raise RuntimeError(f"Failed to fetch freelancer: {e}")

    def update(self, db, **kwargs):
        """Update specific fields of the Freelancer document."""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.updatedAt = datetime.utcnow()
            self.save_to_db(db)
            logging.info(f"Freelancer with ID {self._id} updated successfully.")
        except Exception as e:
            logging.error(f"Error updating freelancer with ID {self._id}: {e}")
            raise RuntimeError(f"Failed to update freelancer: {e}")

    def delete(self, db):
        """Delete the Freelancer document from MongoDB."""
        try:
            if self._id:
                db.delete_one({"_id": self._id})
                self._id = None
                logging.info(f"Freelancer with ID {self._id} deleted successfully.")
            else:
                logging.warning("No freelancer ID to delete.")
        except Exception as e:
            logging.error(f"Error deleting freelancer with ID {self._id}: {e}")
            raise RuntimeError(f"Failed to delete freelancer: {e}")

    def __repr__(self):
        return f"Freelancer(user={self.user}, email={self.email}, skills={self.skills}, averageRating={self.averageRating})"
