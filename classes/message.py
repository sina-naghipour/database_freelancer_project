from typing import Optional, List
from bson import ObjectId
from datetime import datetime
import logging

class Message:
    def __init__(
        self,
        _id: Optional[ObjectId] = None,
        conversationId: str = '',
        participants: List[ObjectId] = None,
        messages: List[dict] = None,
        lastUpdated: Optional[datetime] = None
    ):
        self._id = _id
        self.conversationId = conversationId
        self.participants = participants or []
        self.messages = messages or []
        self.lastUpdated = lastUpdated or datetime.utcnow()

    def save_to_db(self, db):
        message_data = {
            "conversationId": self.conversationId,
            "participants": self.participants,
            "messages": self.messages,
            "lastUpdated": self.lastUpdated
        }
        try:
            if self._id:
                db.update_one({"_id": self._id}, {"$set": message_data})
                logging.info(f"Message with ID {self._id} updated successfully.")
            else:
                result = db.insert_one(message_data)
                self._id = result.inserted_id
                logging.info(f"Message inserted with ID {self._id}.")
        except Exception as e:
            logging.error(f"Error saving message: {e}")
            raise RuntimeError(f"Failed to save message: {e}")

    @classmethod
    def from_db(cls, db, _id: ObjectId):
        try:
            data = db.find_one({"_id": _id})
            if data:
                logging.info(f"Message with ID {data['_id']} found.")
                return cls(
                    _id=data["_id"],
                    conversationId=data.get("conversationId"),
                    participants=data.get("participants", []),
                    messages=data.get("messages", []),
                    lastUpdated=data.get("lastUpdated"),
                )
            logging.warning(f"No message found with ID {_id}.")
            return None
        except Exception as e:
            logging.error(f"Error fetching message with ID {_id}: {e}")
            raise RuntimeError(f"Failed to fetch message: {e}")

    def update(self, db, **kwargs):
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.lastUpdated = datetime.utcnow()
            self.save_to_db(db)
            logging.info(f"Message with ID {self._id} updated successfully.")
        except Exception as e:
            logging.error(f"Error updating message with ID {self._id}: {e}")
            raise RuntimeError(f"Failed to update message: {e}")

    def delete(self, db):
        try:
            if self._id:
                db.delete_one({"_id": self._id})
                self._id = None
                logging.info(f"Message with ID {self._id} deleted successfully.")
            else:
                logging.warning("No message ID to delete.")
        except Exception as e:
            logging.error(f"Error deleting message with ID {self._id}: {e}")
            raise RuntimeError(f"Failed to delete message: {e}")

    def __repr__(self):
        return f"Message(conversationId={self.conversationId}, participants={self.participants})"

    def add_reply(self, reply_to_message_id: ObjectId, reply_content: str, sender_id: ObjectId, db):
        reply = {
            "senderId": sender_id,
            "content": reply_content,
            "timestamp": datetime.utcnow(),
            "repliedToMessageId": reply_to_message_id,
            "read": False,
            "replyTo": ReplyTo(
                messageId=reply_to_message_id,
                content=reply_content,
                senderId=sender_id,
                timestamp=datetime.utcnow()
            ).to_dict(),
            "attachments": []
        }
        self.messages.append(reply)
        self.update(db, messages=self.messages)

    def forward_message(self, message_id: ObjectId, db):
        forwarded_message = {
            "senderId": message_id,
            "content": "Forwarded message",
            "timestamp": datetime.utcnow(),
            "forwardedFromMessageId": message_id,
            "attachments": []
        }
        self.messages.append(forwarded_message)
        self.update(db, messages=self.messages)
