from DataShip.db_management.db_models import User
from DataShip.db_management.db_manager import DB_manager
import streamlit as st
from datetime import date
from sqlite3 import Connection


def signup(DB_MAN: DB_manager, DB_CONN: Connection) -> None:
    """This function represents a view to the signup page.

    Args:
        DB_MAN (DB_manager): database manager.
        DB_CONN (Connection): database connection.
    """

    # signup form to retrieve the information from the user.
    st.subheader("Signup")
    with st.form("signup"):
        name = st.text_input("Full name *")
        email = st.text_input("Email")
        username = st.text_input("Username *")
        password = st.text_input("Password *", type="password")
        submit = st.form_submit_button("signup")
        # if user clicks on the submit button, the information is saved in the database.
        if submit:
            user = User(
                id=1,
                name=name,
                username=username,
                password=password,
                created_at=date.today(),
                email=email if email else None,
            )
            user_created = DB_MAN.create_user(DB_CONN, user)
            if user_created:
                st.success(f"Welcome {user.name}")
                st.session_state["user"] = user
                st.experimental_rerun()
            else:
                st.error("Username/password is incorrect")
