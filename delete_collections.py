from pymongo import MongoClient

# Prompt user for confirmation
confirmation = input("Type 'delete_collections' to confirm deletion of collections: ")

if confirmation == 'delete_collections':
    try:
        # Connect to the MongoDB server (adjust the URI if needed)
        client = MongoClient("mongodb://localhost:27017/")  # Default MongoDB URI

        # Access the FreelancerManagement database
        db = client["FreelancerManagement"]

        # List of collections to drop based on the new schema
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

        # Check if database exists
        if db.name in client.list_database_names():
            print(f"Database '{db.name}' found. Proceeding to drop collections.")
            # Drop each collection
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
else:
    print("Operation aborted. Collections were not deleted.")
