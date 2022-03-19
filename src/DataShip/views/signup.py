from DataShip.db_management.db_models import User
from DataShip.db_management.db_manager import DB_manager
import streamlit as st
from datetime import date
from sqlite3 import Connection


def signup(DB_MAN: DB_manager, DB_CONN: Connection) -> None:
    st.subheader("Signup")
    with st.form("signup"):
        name = st.text_input("Full name *")
        email = st.text_input("Email")
        username = st.text_input("Username *")
        password = st.text_input("Password *", type="password")
        color1 = st.color_picker("Primary color")
        color2 = st.color_picker("Secondary color")
        submit = st.form_submit_button("signup")
        if submit:
            user = User(
                id=1,
                name=name,
                username=username,
                password=password,
                color_scheme=f"{color1}:{color2}",
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
