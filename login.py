import streamlit as st
from database_1 import verify_login

def login():
    st.title("Login Page")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    logged_in = False  # Default login status
    username_value = None  # Default username

    if st.button("Login"):
        if verify_login(username, password):
            st.success("Login successful!")
            logged_in = True
            username_value = username  # Set the username on successful login
            
        else:
            st.error("Invalid username or password.")


    return logged_in, username_value  # Return login status and username
