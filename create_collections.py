from pymongo import MongoClient

# Connect to the MongoDB server (adjust the URI if needed)
client = MongoClient("mongodb://localhost:27017/")  # Default MongoDB URI

# Create the FreelancerManagement database
db = client["FreelancerManagement"]

# Define the collections
collections = [
    "Users",
    "Freelancers",
    "Clients",
    "Admins",
    "Messages",
    "Notifications",
    "Projects",
    "Payments",
    "Categories"
]

# Create each collection in the database (if they don't exist already)
for collection in collections:
    if collection not in db.list_collection_names():
        db.create_collection(collection)
        print(f"Collection '{collection}' created!")
    else:
        print(f"Collection '{collection}' already exists.")

# Create indexes if necessary (e.g., on fields like email, etc.)
# Creating a unique index on 'email' for Freelancers and Clients
db.Freelancers.create_index([("email", 1)], unique=True)
db.Clients.create_index([("email", 1)], unique=True)

# Example: Create a compound index on 'clientId' and 'freelancerId' for Projects to optimize queries
db.Projects.create_index([("clientId", 1), ("freelancerId", 1)])

# Example: Index on 'userId' for Notifications
db.Notifications.create_index([("userId", 1)])

print("Collections and indexes created successfully.")
