import streamlit as st
import pandas as pd
import create_collections
import delete_collections
from bson import ObjectId


# Function to show an expandable popup for database deletion
def show_deletion_expander():
    with st.expander("⚠️ Click here to delete the database"):
        st.write("Are you sure you want to delete the database?")
        
        user_confirmation = st.text_input("Type 'delete_database' to confirm:")

        if user_confirmation == "delete_database":
            delete_collections.delete_databases()
            st.success("Database has been deleted successfully.")
        elif user_confirmation:
            st.warning("You need to type 'delete_database' to confirm.")
        else:
            st.info("Please type 'delete_database' to confirm deletion.")

# Function for database creation
def create_database():
    create_collections.create_databases()
    st.success("Database created successfully.")

# Function to display the Create Database expander and button
def show_create_database_section():
    with st.expander("🔨 Create Database"):
        if st.button('Create Database'):
            create_database()
            
            

def clean_mongo_record(record):
    """
    Recursively convert MongoDB-specific types (like ObjectId) to JSON-serializable types,
    with additional checks for specific attributes in ObjectId.

    Args:
        record (dict): A MongoDB record/document.

    Returns:
        dict: The cleaned record with all MongoDB-specific types converted.
    """
    if isinstance(record, dict):
        return {key: clean_mongo_record(value) for key, value in record.items()}
    elif isinstance(record, list):
        return [clean_mongo_record(item) for item in record]
    elif isinstance(record, ObjectId):
        # Check if the ObjectId is "_id" and return it as a string
        if str(record) == "_id":
            return str(record)
        
        # Otherwise, check if the ObjectId has specific attributes
        attributes = {
            "amount": "amount",
            "name": "name",
            "content": "content",
            "title": "title",
            "conversationId": "conversationId",
            "email": "email",
            "role": "role"
        }

        # For each attribute, check if it exists and return the value
        for attribute, key in attributes.items():
            if hasattr(record, key):
                return getattr(record, key)

        # If no attribute matches, return the string representation of the ObjectId
        return str(record)
    else:
        return record


def display_collection_selector(db, collections):
    """
    Displays a dropdown for collection selection and shows the data in a table.
    
    Args:
        db: The MongoDB database object.
        collections (list): List of collection names.
    """
    st.write("### Choose a MongoDB Collection")
    selected_collection = st.selectbox("Select a collection:", collections)
    st.write(f"You selected: {selected_collection}")

    # Access the selected collection
    collection = db[selected_collection]
    data = collection.find()
    
    # Clean and convert the MongoDB data
    data_list = [clean_mongo_record(record) for record in data]

    if data_list:
        # Convert cleaned data to a DataFrame
        df = pd.DataFrame(data_list)
        st.dataframe(df)
    else:
        st.write("No data found in the selected collection.")