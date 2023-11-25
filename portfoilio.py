import pandas as pd
import streamlit as st
from database_1 import view_portfolio,remove_from_portfolio

def show_portfolio(username):
    portfolio_data=view_portfolio(username)
    st.subheader("Portfolio")
    books_df = pd.DataFrame(portfolio_data, columns=["StockID", "name", "buy_price", "curr_Price","Quantity","member_id","Investment","gain"])
    st.dataframe(books_df)
    sell=st.text_input("stock name")
    if st.button("sell stock"):
        if remove_from_portfolio(sell,username):
            st.success("succesfully sold")
        else:
            st.error("stock not available")