from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import Optional

class Category:
    def __init__(
        self,
        _id: Optional[ObjectId] = None,
        name: str = "",
        createdAt: Optional[datetime] = None,
        updatedAt: Optional[datetime] = None
    ):
        self._id = _id
        self.name = name
        self.createdAt = createdAt or datetime.utcnow()
        self.updatedAt = updatedAt or datetime.utcnow()

    def save_to_db(self, db):
        """Save the Category document to MongoDB."""
        if not self.name:
            raise ValueError("Category name cannot be empty.")
        
        category_data = {
            "name": self.name,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
        if self._id:
            db.update_one({"_id": self._id}, {"$set": category_data})
        else:
            result = db.insert_one(category_data)
            self._id = result.inserted_id

    @classmethod
    def from_db(cls, db, _id: ObjectId):
        """Retrieve a Category document from MongoDB and create an instance."""
        data = db.find_one({"_id": _id})
        if data:
            return cls(
                _id=data["_id"],
                name=data["name"],
                createdAt=data["createdAt"],
                updatedAt=data["updatedAt"]
            )
        return None

    def update(self, db, name: str):
        """Update the category details."""
        if not name:
            raise ValueError("Category name cannot be empty.")
        
        self.name = name
        self.updatedAt = datetime.utcnow()
        self.save_to_db(db)

    def delete(self, db):
        """Delete the Category document from MongoDB."""
        if self._id:
            db.delete_one({"_id": self._id})
            self._id = None
