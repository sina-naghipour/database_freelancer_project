from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, date
from typing import Optional

class Notification:
    def __init__(
        self,
        _id: Optional[ObjectId] = None,
        userId: ObjectId = None,
        type: str = '',
        content: str = '',
        link: Optional[str] = None,
        read: bool = False,
        timestamp: Optional[datetime] = None
    ):
        self._id = _id
        self.userId = userId
        self.type = type
        self.content = content
        self.link = link
        self.read = read
        self.timestamp = timestamp or datetime.utcnow()

    def save_to_db(self, db):
        """Save the Notification document to MongoDB."""
        notification_data = {
            "userId": self.userId,
            "type": self.type,
            "content": self.content,
            "link": self.link,
            "read": self.read,
            "timestamp": self.timestamp  # Ensure it's a datetime object
        }
        if self._id:
            db.update_one({"_id": self._id}, {"$set": notification_data})
        else:
            result = db.insert_one(notification_data)
            self._id = result.inserted_id

    @classmethod
    def from_db(cls, db, _id: ObjectId):
        """Retrieve a Notification document from MongoDB and create an instance."""
        data = db.find_one({"_id": _id})
        if data:
            # Ensure timestamp is a datetime object, not a date
            timestamp = data.get("timestamp")
            if isinstance(timestamp, date):  # If it's a datetime.date object
                timestamp = datetime.combine(timestamp, datetime.min.time())  # Convert to datetime.datetime
            return cls(
                _id=data["_id"],
                userId=data.get("userId"),
                type=data.get("type", ""),
                content=data.get("content", ""),
                link=data.get("link"),
                read=data.get("read", False),
                timestamp=timestamp
            )
        return None

    def mark_as_read(self, db):
        """Mark the notification as read."""
        self.read = True
        self.save_to_db(db)

    def update(self, db, **kwargs):
        """Update specific fields of the Notification document."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save_to_db(db)

    def delete(self, db):
        """Delete the Notification document from MongoDB."""
        if self._id:
            db.delete_one({"_id": self._id})
            self._id = None

    def __repr__(self):
        return f"Notification(userId={self.userId}, type={self.type}, read={self.read})"