from pymongo import MongoClient

def delete_databases():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["FreelancerManagement"]
        collections_to_drop = [
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
        if db.name in client.list_database_names():
            print(f"Database '{db.name}' found. Proceeding to drop collections.")
            for collection_name in collections_to_drop:
                if collection_name in db.list_collection_names():
                    try:
                        db.drop_collection(collection_name)
                        print(f"Collection '{collection_name}' dropped successfully!")
                    except Exception as e:
                        print(f"Error dropping collection '{collection_name}': {e}")
                else:
                    print(f"Collection '{collection_name}' does not exist.")
        else:
            print(f"Database '{db.name}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
