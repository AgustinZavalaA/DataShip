from DataShip.db_management.db_models import User
from DataShip.db_management.db_manager import DB_manager
from DataShip.views import signup, login, feed_post_admin
import streamlit as st
from streamlit_option_menu import option_menu

DB_URI_SQLITE = "dataship.db"
DB_MAN = DB_manager(DB_URI_SQLITE)
DB_CONN = DB_MAN.get_connection()


def home(DB_MAN, DB_CONN):
    st.subheader("Home")


def settings(DB_MAN, DB_CONN):
    st.subheader("Settings")


def feedback(DB_MAN, DB_CONN):
    st.subheader("Feedback")


def modules(DB_MAN, DB_CONN):
    st.subheader("Modules")


def files_saved(DB_MAN, DB_CONN):
    st.subheader("Files saved")
    st.write("Files saved")

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
            self.apps["Login"] = [login.login, "bi-person"]
            self.apps["Signup"] = [signup.signup, "bi-person-plus"]
        else:
            self.apps["My files"] = [files_saved, "bi-files"]
            if st.session_state["user"].username == "admin":
                self.apps["VIEW FEEDBACK"] = [feed_post_admin.feedback_post, "bi-cog"]

    def serve(self):
        with st.sidebar:
            if st.session_state["user"] is not None:
                st.subheader(f"Welcome back {st.session_state['user'].name}!")
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
        self.apps[navigation][0](DB_MAN, DB_CONN)


def main():
    page = DataShip()
    page.serve()


if __name__ == "__main__":
    main()
