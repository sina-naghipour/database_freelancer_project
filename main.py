import streamlit as st
import pandas as pd
from pymongo import MongoClient
import streamlit_elements
import fake_data
from bson import ObjectId
import json
# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['FreelancerManagement']
collections = ['Users', 'Freelancers', 'Clients', 'Messages', 'Projects', 'Payments', 'Categories']

st.title('MongoDB Data Viewer')

# Button to generate fake data with user input
st.write("### Generate Fake Data")
n = st.number_input("Enter the number of fake data entries:", min_value=1, step=1, value=1)
if st.button('Generate Fake Data'):
    fake_data.main(n)

# Create two columns for the side-by-side layout
col1, col2 = st.columns(2)

# Place the two sections inside the columns
with col1:
    streamlit_elements.show_create_database_section()

with col2:
    streamlit_elements.show_deletion_expander()

st.write('### MongoDB Records')
# Use Streamlit to display the dataframe
streamlit_elements.display_collection_selector(db, collections)

# Custom CSS to make the whole page wider
st.markdown("""
    <style>
        /* Increase the width of the whole Streamlit page */
        .block-container {
            max-width: 90%;  /* Adjust the percentage for desired width */
            padding-left: 3rem;
            padding-right: 3rem;
        }

        /* Make the dataframe container wider */
        .stDataFrame {
            width: 100%;
        }

        /* Adjust the sidebar width as well (optional) */
        .css-1v3fvcr {
            width: 300px;  /* Increase the width of the sidebar */
        }
    </style>
""", unsafe_allow_html=True)
