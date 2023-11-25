import streamlit as st
import sqlite3
from database_1 import is_username_taken
from database_1 import add_user

# Main registration function
def register():
    st.title("Registration Page")

    # Get user input
    new_username = st.text_input("Choose a username:")
    new_password = st.text_input("Choose a password:", type="password")

    # Check if the username is available when the user clicks the "Register" button
    if st.button("Register"):
        if is_username_taken(new_username):
            st.error("Username is already taken. Please choose another.")
        else:
            # Add the new user to the Users table
            add_user(new_username, new_password)
            st.success("Registration successful! You can now log in.")

if __name__ == "__main__":
    register()