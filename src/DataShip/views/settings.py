from DataShip.db_management.db_manager import DB_manager
import streamlit as st
from sqlite3 import Connection


def settings(DB_MAN: DB_manager, DB_CONN: Connection) -> None:
    st.subheader("Settings")
    if st.session_state["user"] is None:
        st.error("You must first login to access this page")
        return
    with st.form("reconfigure your account"):
        username = st.text_input("Actual username *")
        actual_password = st.text_input("Actual password *", type="password")
        st.write("-----")
        st.subheader("Change your current user")
        name = st.text_input("Full name *")
        email = st.text_input("Email")
        new_password = st.text_input("New password *", type="password")
        submit = st.form_submit_button("confirm")
        if submit:
            user = DB_MAN.check_user_password(DB_CONN, username, actual_password)
            if not user:
                st.error("Couldn't find the given user :(")
                return
            user.name = name
            user.email = email
            user.password = new_password

            user = DB_MAN.update_user(DB_CONN, user)

            st.success(f"Settings changed for user: {user.name}")
            st.session_state["user"] = user
            st.experimental_rerun()
