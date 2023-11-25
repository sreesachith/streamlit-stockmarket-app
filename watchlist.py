import pandas as pd
import streamlit as st
from database_1 import view_watchlist

def display_watchlist(username):
    
    st.subheader("Company Data")
    company_data=view_watchlist(username)
    columns = ["comp_name", "industry", "curr_price", "open_price","member_name"]
    company_df = pd.DataFrame(company_data, columns=columns)
    st.dataframe(company_df)
 