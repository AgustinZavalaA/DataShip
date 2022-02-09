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


def files_saved():
    st.subheader("Files saved")
    st.write("Files saved")


def signup():
    st.subheader("Signup")
    with st.form("signup"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        name = st.text_input("Name")
        submit = st.form_submit_button("signup")
        if submit:
            user = DB_MANAGER.create_user(DB_CONN, username, password, name)
            if user:
                st.success("Welcome %s" % user["name"])
                st.session_state["user"] = user
                st.experimental_rerun()
            else:
                st.error("Username/password is incorrect")


def login():
    st.subheader("Login")
    st.write("Don't have an account yet? Signup")
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

        self.apps = {
            "Home": [home, "bar-chart-line"],
            "Modules": [modules, "box-seam"],
            "Settings": [settings, "gear"],
            "Feedback": [feedback, "megaphone"],
        }

        if "user" not in st.session_state.keys():
            st.session_state["user"] = None

        if st.session_state["user"] is None:
            self.apps["Login"] = [login, "bi-person"]
            self.apps["Signup"] = [signup, "bi-person-plus"]
        else:
            self.apps["My files"] = [files_saved, "bi-files"]

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
                icons=[app[1] for app in self.apps.values()],
                menu_icon="bar-chart-steps",
                default_index=0,
            )
        self.apps[navigation][0]()


def main():
    page = DataShip()
    page.serve()


if __name__ == "__main__":
    main()
