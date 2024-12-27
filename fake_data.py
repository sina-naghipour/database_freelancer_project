from pymongo import MongoClient
from bson import ObjectId
from faker import Faker
import random
from datetime import datetime, timezone
import logging
from classes.admin import Admin
from classes.user import User
from classes.freelancer import Freelancer
from classes.client import Client
from classes.payment import Payment
from classes.project import Project, Bid, Review, Status
from classes.notification import Notification
from classes.category import Category
from classes.message import Message

fake = Faker()

def generate_user_data(num_entries):
    users = []
    for _ in range(num_entries):
        user = User(
            name=fake.name(),
            email=fake.email(),
            password_hash=fake.password(),
            profile_picture=fake.image_url(),
            bio=fake.text(),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        users.append(user)
    return users

def generate_freelancer_data(num_entries):
    freelancers = []
    for _ in range(num_entries):
        freelancer = Freelancer(
            user=ObjectId(),
            email=fake.email(),
            skills=[fake.word() for _ in range(random.randint(3, 7))],
            services=[{"service": fake.bs()} for _ in range(random.randint(1, 3))],
            portfolio=[{"project": fake.url(), "description": fake.sentence()} for _ in range(random.randint(1, 3))],
            reviews=[{"reviewer": fake.name(), "rating": random.randint(1, 5), "comment": fake.sentence()} for _ in range(random.randint(1, 5))],
            averageRating=round(random.uniform(1, 5), 2),
            createdAt=datetime.now(timezone.utc),
            updatedAt=datetime.now(timezone.utc)
        )
        freelancers.append(freelancer)
    return freelancers

def generate_client_data(num_entries):
    clients = []
    for _ in range(num_entries):
        client = Client(
            user=ObjectId(),
            email=fake.email(),
            hiredFreelancers=[ObjectId() for _ in range(random.randint(1, 5))],
            reviewsGiven=[{"freelancer": ObjectId(), "rating": random.randint(1, 5), "review": fake.sentence()} for _ in range(random.randint(1, 5))],
            createdAt=datetime.now(timezone.utc),
            updatedAt=datetime.now(timezone.utc)
        )
        clients.append(client)
    return clients

def generate_admin_data(num_entries):
    admins = []
    for _ in range(num_entries):
        admin = Admin(
            user=ObjectId(),
            role=random.choice(["Super Admin", "Admin", "Moderator"]),
            createdAt=datetime.now(timezone.utc),
            updatedAt=datetime.now(timezone.utc)
        )
        admins.append(admin)
    return admins

def generate_message_data(num_entries):
    messages = []
    for _ in range(num_entries):
        message = Message(
            conversationId="some_conversation_id",
            participants=[ObjectId(), ObjectId()],
            messages=[{"senderId": ObjectId(), "content": "Hello, this is a message!"}],
            lastUpdated=datetime.now(timezone.utc)
        )
        messages.append(message)
    return messages

def generate_notification_data(num_entries):
    notifications = []
    for _ in range(num_entries):
        notification = Notification(
            userId=ObjectId(),
            type="Info",
            content="This is a notification.",
            link=None,
            read=False,
            timestamp=datetime.now(timezone.utc)
        )
        notifications.append(notification)
    return notifications

def generate_bid_data(num_entries):
    bids = []
    for _ in range(num_entries):
        bid = Bid(
            freelancerId=ObjectId(),
            bidAmount=100.0,
            message="This is a bid message.",
            date=datetime.now(timezone.utc)
        )
        bids.append(bid)
    return bids

def generate_review_data(num_entries):
    reviews = []
    for _ in range(num_entries):
        review = Review(
            rating=random.randint(1, 5),
            comment=fake.sentence(),
            date=datetime.now(timezone.utc)
        )
        reviews.append(review.to_dict())
    return reviews

def generate_status_data(num_entries):
    statuses = []
    for _ in range(num_entries):
        status = Status(
            type="Active",
            lastUpdated=datetime.now(timezone.utc)
        )
        statuses.append(status)
    return statuses

def generate_project_data(num_entries):
    projects = []
    for _ in range(num_entries):
        project = Project(
            title=fake.bs(),
            description=fake.text(),
            clientId=ObjectId(),
            freelancerId=ObjectId(),
            budget=random.uniform(500, 5000),
            bids=generate_bid_data(random.randint(1, 5)),
            status=random.choice(generate_status_data(1)),
            reviews=[review for review in generate_review_data(1)],
            createdAt=datetime.now(timezone.utc),
            updatedAt=datetime.now(timezone.utc)
        )
        projects.append(project)
    return projects

def generate_payment_data(num_entries):
    payments = []
    for _ in range(num_entries):
        payment = Payment(
            projectId=ObjectId(),
            clientId=ObjectId(),
            freelancerId=ObjectId(),
            amount=random.uniform(50, 2000),
            paymentStatus=random.choice(['Pending', 'Completed', 'Failed']),
            timestamp=datetime.now(timezone.utc)
        )
        payments.append(payment)
    return payments

def generate_category_data(num_entries):
    categories = []
    for _ in range(num_entries):
        category = Category(
            name=fake.bs(),
            createdAt=datetime.now(timezone.utc),
            updatedAt=datetime.now(timezone.utc)
        )
        categories.append(category)
    return categories

def main(n : int):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['FreelancerManagement']

    users = generate_user_data(n)
    freelancers = generate_freelancer_data(n)
    clients = generate_client_data(n)
    admins = generate_admin_data(n)
    messages = generate_message_data(n)
    notifications = generate_notification_data(n)
    bids = generate_bid_data(n)
    reviews = generate_review_data(n)
    statuses = generate_status_data(n)
    projects = generate_project_data(n)
    payments = generate_payment_data(n)
    categories = generate_category_data(n)

    try:
        for user in users:
            user.save_to_db(db['Users'])
        for freelancer in freelancers:
            freelancer.save_to_db(db['Freelancers'])
        for client in clients:
            client.save_to_db(db['Clients'])
        for admin in admins:
            admin.save_to_db(db['Admins'])
        for message in messages:
            message.save_to_db(db['Messages'])
        for notification in notifications:
            notification.save_to_db(db['Notifications'])
        for project in projects:
            project.save_to_db(db['Projects'])
        for payment in payments:
            payment.save_to_db(db['Payments'])
        for category in categories:
            category.save_to_db(db['Categories'])

        logging.info(f"Successfully generated {n} records for each collection.")

    except Exception as e:
        logging.error(f"Error while saving data to the database: {e}")

if __name__ == "__main__":
    main(300)
