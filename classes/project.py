from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

class Bid:
    def __init__(self, freelancerId: ObjectId, bidAmount: float, message: str, date: Optional[datetime] = None):
        self.freelancerId = freelancerId
        self.bidAmount = bidAmount
        self.message = message
        self.date = date or datetime.utcnow()

    def to_dict(self):
        return {
            "freelancerId": self.freelancerId,
            "bidAmount": self.bidAmount,
            "message": self.message,
            "date": self.date
        }

class Review:
    def __init__(self, rating: int, comment: str, date: Optional[datetime] = None):
        self.rating = rating
        self.comment = comment
        self.date = date or datetime.utcnow()

    def to_dict(self):
        return {
            "rating": self.rating,
            "comment": self.comment,
            "date": self.date
        }

class Status:
    def __init__(self, type: str, lastUpdated: Optional[datetime] = None):
        self.type = type
        self.lastUpdated = lastUpdated or datetime.utcnow()

    def to_dict(self):
        return {
            "type": self.type,
            "lastUpdated": self.lastUpdated
        }

class Project:
    def __init__(
        self,
        _id: Optional[ObjectId] = None,
        title: str = '',
        description: str = '',
        clientId: ObjectId = None,
        freelancerId: Optional[ObjectId] = None,
        budget: float = 0.0,
        bids: List[Bid] = None,
        status: Status = None,
        reviews: dict = None,
        createdAt: Optional[datetime] = None,
        updatedAt: Optional[datetime] = None
    ):
        self._id = _id
        self.title = title
        self.description = description
        self.clientId = clientId
        self.freelancerId = freelancerId
        self.budget = budget
        self.bids = bids or []
        self.status = status or Status(type='Open')
        self.reviews = reviews or {
            "clientReview": None,
            "freelancerReview": None
        }
        self.createdAt = createdAt or datetime.utcnow()
        self.updatedAt = updatedAt or datetime.utcnow()

    def save_to_db(self, db):
        """Save the Project document to MongoDB."""
        project_data = {
            "title": self.title,
            "description": self.description,
            "clientId": self.clientId,
            "freelancerId": self.freelancerId,
            "budget": self.budget,
            "bids": [bid.to_dict() for bid in self.bids],
            "status": self.status.to_dict(),
            "reviews": self.reviews,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
        if self._id:
            db.update_one({"_id": self._id}, {"$set": project_data})
        else:
            result = db.insert_one(project_data)
            self._id = result.inserted_id

    @classmethod
    def from_db(cls, db, _id: ObjectId):
        """Retrieve a Project document from MongoDB and create an instance."""
        data = db.find_one({"_id": _id})
        if data:
            bids = [Bid(**bid) for bid in data.get("bids", [])]
            status = Status(**data.get("status", {}))
            return cls(
                _id=data["_id"],
                title=data["title"],
                description=data["description"],
                clientId=data["clientId"],
                freelancerId=data.get("freelancerId"),
                budget=data["budget"],
                bids=bids,
                status=status,
                reviews=data.get("reviews", {}),
                createdAt=data["createdAt"],
                updatedAt=data["updatedAt"]
            )
        return None

    def add_bid(self, db, freelancerId: ObjectId, bidAmount: float, message: str):
        """Add a new bid to the project."""
        bid = Bid(freelancerId=freelancerId, bidAmount=bidAmount, message=message)
        self.bids.append(bid)
        self.save_to_db(db)

    def update_status(self, db, status_type: str):
        """Update the project status."""
        self.status = Status(type=status_type)
        self.updatedAt = datetime.utcnow()
        self.save_to_db(db)

    def add_review(self, db, review_type: str, rating: int, comment: str):
        """Add a review for the client or freelancer."""
        review = Review(rating=rating, comment=comment)
        if review_type == 'client':
            self.reviews['clientReview'] = review.to_dict()
        elif review_type == 'freelancer':
            self.reviews['freelancerReview'] = review.to_dict()
        self.updatedAt = datetime.utcnow()
        self.save_to_db(db)

    def delete(self, db):
        """Delete the Project document from MongoDB."""
        if self._id:
            db.delete_one({"_id": self._id})
            self._id = None
