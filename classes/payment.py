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
        paymentStatus: str = "Pending",
        timestamp: Optional[datetime] = None
    ):
        self._id = _id
        self.projectId = projectId
        self.clientId = clientId
        self.freelancerId = freelancerId
        self.amount = amount
        self.paymentStatus = paymentStatus
        self.timestamp = timestamp or datetime.utcnow()

    def save_to_db(self, db):
        payment_data = {
            "projectId": self.projectId,
            "clientId": self.clientId,
            "freelancerId": self.freelancerId,
            "amount": self.amount,
            "paymentStatus": self.paymentStatus,
            "timestamp": self.timestamp
        }
        if self._id:
            db.update_one({"_id": self._id}, {"$set": payment_data})
        else:
            result = db.insert_one(payment_data)
            self._id = result.inserted_id

    @classmethod
    def from_db(cls, db, _id: ObjectId):
        data = db.find_one({"_id": _id})
        if data:
            timestamp = data["timestamp"] if isinstance(data["timestamp"], datetime) else datetime.utcnow()
            return cls(
                _id=data["_id"],
                projectId=data["projectId"],
                clientId=data["clientId"],
                freelancerId=data["freelancerId"],
                amount=data["amount"],
                paymentStatus=data["paymentStatus"],
                timestamp=timestamp
            )
        return None

    def update_status(self, db, status: str):
        self.paymentStatus = status
        self.timestamp = datetime.utcnow()
        self.save_to_db(db)

    def delete(self, db):
        if self._id:
            db.delete_one({"_id": self._id})
            self._id = None
