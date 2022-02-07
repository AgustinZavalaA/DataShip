import streamlit as st
from streamlit_option_menu import option_menu
from db_management import db_management

DB_URI_SQLITE = "dataship.db"
DB_MANAGER = db_management(DB_URI_SQLITE)
DB_CONN = DB_MANAGER.get_connection()


def home():
    st.subheader("Home")


def settings():
    st.subheader("Settings")


def feedback():
    st.subheader("Feedback")


def modules():
    st.subheader("Modules")


def login():
    st.subheader("Login")
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("login")
        if submit:
            user = DB_MANAGER.check_user_password(DB_CONN, username, password)
            if user:
                st.success("Welcome %s" % user["name"])
                st.session_state["user"] = user
                st.experimental_rerun()
            else:
                st.error("Username/password is incorrect")


class DataShip:
    def __init__(self):
        st.title("DataShip")

        self.apps = {"Home": home, "Modules": modules, "Settings": settings, "Feedback": feedback}

        if "user" not in st.session_state.keys():
            st.session_state["user"] = None

        if st.session_state["user"] is None:
            self.apps["Login"] = login

    def serve(self):
        with st.sidebar:
            if st.session_state["user"] is not None:
                st.subheader(f"Welcome back {st.session_state['user']['name']}!")
                if st.button("Logout"):
                    st.session_state["user"] = None
                    st.experimental_rerun()
            navigation = option_menu(
                "Navigation",
                list(self.apps.keys()),
                icons=["bar-chart-line", "box-seam", "gear", "megaphone", "bi-person", "bi-files"],
                menu_icon="bar-chart-steps",
                default_index=0,
            )
        self.apps[navigation]()


def main():
    page = DataShip()
    page.serve()


if __name__ == "__main__":
    main()
