from DataShip.db_management.db_models import Feedback_post
from DataShip.db_management.db_manager import DB_manager
from sqlite3 import Connection
import streamlit as st
from datetime import date


def feedback(DB_MAN: DB_manager, DB_CONN: Connection) -> None:
    """ This function represent a view for viewing feedback posts.

    Args:
        DB_MAN (DB_manager): database manager.
        DB_CONN (Connection): database connection.
    """
    
    st.subheader("Feedback")
    with st.form("Feedback"):
        all_feedback_types = DB_MAN.get_all_feedback_types(DB_CONN)

        title = st.text_input("Title* ")
        post = st.text_area("Post description* ")
        feedback_type = st.selectbox("Select an option", [x.name for x in all_feedback_types])

        confirm = st.form_submit_button("submit")
        if confirm:
            if st.session_state["user"] is not None:
                user_id = st.session_state["user"].id
            else:
                user_id = None

            feedback_type = next(x.id for x in all_feedback_types if x.name == feedback_type)
            fp = Feedback_post(
                id=1,
                type_id=feedback_type,
                title=title,
                post=post,
                created_at=date.today(),
                done=False,
                user_id=user_id,
            )
            if DB_MAN.create_feedback_post(DB_CONN, fp):
                st.success("Feedback post submited correctly")
            else:
                st.error("Feedback post wasn't submited correctly :(")
