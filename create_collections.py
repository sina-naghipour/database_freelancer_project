from pymongo import MongoClient
def create_databases():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["FreelancerManagement"]

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
    
    for collection in collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)
            print(f"Collection '{collection}' created!")
        else:
            print(f"Collection '{collection}' already exists.")

    db.Freelancers.create_index([("email", 1)], unique=True)
    db.Clients.create_index([("email", 1)], unique=True)
    db.Projects.create_index([("clientId", 1), ("freelancerId", 1)])
    db.Notifications.create_index([("userId", 1)])

    print("Collections and indexes created successfully.")

    