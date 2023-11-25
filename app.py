import streamlit as st
from database_1 import create_tables,create_function,drop_procedure
from login import login
from portfoilio import show_portfolio
from register import register
from stock import display_company_data
from watchlist import display_watchlist
def main():
    create_tables()
    drop_procedure()
    create_function()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        menu_1 = ["LOGIN", "REGISTER"]
        choice_1 = st.sidebar.selectbox("Menu", menu_1)
        if choice_1 == "LOGIN":
            st.session_state.logged_in, st.session_state.username = login()
        elif choice_1 == "REGISTER":
            register()
    
    if st.session_state.logged_in:
        st.sidebar.empty()
        st.title("Online Stock-Portfolio management App")
        menu_2 = ["STOCKS", "PORTFOLIO","WATCHLIST"]
        choice_2 = st.sidebar.selectbox("Menu", menu_2)
        if choice_2 == "STOCKS":
            display_company_data(st.session_state.username)
        elif choice_2 == "PORTFOLIO":
            show_portfolio(st.session_state.username)
        elif choice_2 == "WATCHLIST":
            display_watchlist(st.session_state.username)
                

if __name__ == "__main__":
    main()
