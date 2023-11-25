import pandas as pd
import streamlit as st
from database_1 import view_stock,add_to_watchlist,add_to_portfolio,call_sql_function

def display_company_data(username):
    
    st.subheader("Company Data")
    company_data=view_stock()
    columns = ["comp_name", "industry", "curr_price", "open_price"]
    company_df = pd.DataFrame(company_data, columns=columns)
    st.dataframe(company_df)
    comp_name=st.text_input("Stock name:")
    if st.button("add to watchlist"):
        if add_to_watchlist(comp_name,username):
            st.success("Added Successfully")
        else:
            st.error("Already exists")  
    quant=st.text_input("Enter quantity")        
    if st.button("add to Portfolio"):
        
        if add_to_portfolio(comp_name,username,quant):
            st.success("Added Successfully")
        else:
            st.error("Already exists")
    if st.button("update prices"):
        call_sql_function()  
 