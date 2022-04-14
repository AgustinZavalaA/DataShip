from DataShip.db_management.db_manager import DB_manager
import streamlit as st
from sqlite3 import Connection


def login(DB_MAN: DB_manager, DB_CONN: Connection):
    """This function represent a view for validating users logging in.

    Args:
        DB_MAN (DB_manager): database manager.
        DB_CONN (Connection): database connection.
    """

    st.subheader("Login")
    st.write("Don't have an account yet? Signup")
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("login")
        if submit:
            user = DB_MAN.check_user_password(DB_CONN, username, password)
            if user:
                st.success(f"Welcome {user.name}")
                st.session_state["user"] = user
                st.experimental_rerun()
            else:
                st.error("Username/password is incorrect")
