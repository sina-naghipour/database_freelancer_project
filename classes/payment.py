from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import Optional

class Payment:
    def __init__(
        self,
        _id: Optional[ObjectId] = None,
        projectId: ObjectId = None,
        clientId: ObjectId = None,
        freelancerId: ObjectId = None,
        amount: float = 0.0,
        paymentStatus: str = "Pending",  # Default to "Pending"
        timestamp: Optional[datetime] = None
    ):
        self._id = _id
        self.projectId = projectId
        self.clientId = clientId
        self.freelancerId = freelancerId
        self.amount = amount
        self.paymentStatus = paymentStatus
        # Ensure timestamp is always a datetime object
        self.timestamp = timestamp or datetime.utcnow()

    def save_to_db(self, db):
        """Save the Payment document to MongoDB."""
        payment_data = {
            "projectId": self.projectId,
            "clientId": self.clientId,
            "freelancerId": self.freelancerId,
            "amount": self.amount,
            "paymentStatus": self.paymentStatus,
            "timestamp": self.timestamp  # Ensure this is always a datetime object
        }
        if self._id:
            db.update_one({"_id": self._id}, {"$set": payment_data})
        else:
            result = db.insert_one(payment_data)
            self._id = result.inserted_id

    @classmethod
    def from_db(cls, db, _id: ObjectId):
        """Retrieve a Payment document from MongoDB and create an instance."""
        data = db.find_one({"_id": _id})
        if data:
            # Ensure the timestamp is correctly formatted as a datetime
            timestamp = data["timestamp"] if isinstance(data["timestamp"], datetime) else datetime.utcnow()
            return cls(
                _id=data["_id"],
                projectId=data["projectId"],
                clientId=data["clientId"],
                freelancerId=data["freelancerId"],
                amount=data["amount"],
                paymentStatus=data["paymentStatus"],
                timestamp=timestamp  # Corrected to ensure proper datetime type
            )
        return None

    def update_status(self, db, status: str):
        """Update the payment status."""
        self.paymentStatus = status
        self.timestamp = datetime.utcnow()  # Ensure timestamp is updated to current time
        self.save_to_db(db)

    def delete(self, db):
        """Delete the Payment document from MongoDB."""
        if self._id:
            db.delete_one({"_id": self._id})
            self._id = None
