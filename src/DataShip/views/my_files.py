from DataShip.db_management.db_manager import DB_manager
from sqlite3 import Connection
import streamlit as st
from DataShip.db_management.db_models import User_file
from DataShip.data_analysis_modules import user_files_reader_writer as ufrw
from datetime import date


def files(DB_MAN: DB_manager, DB_CONN: Connection) -> None:
    """This function represents a view to the my files page.

    Args:
        DB_MAN (DB_manager): database manager.
        DB_CONN (Connection): database connection.
    """
    
    st.subheader("Upload a new file")
    # let the user upload multiple files to store in the server
    new_files = st.file_uploader("", type=["csv", "txt", "json", "xlsx"], accept_multiple_files=True)

    if new_files is not None:
        # iterate over the uploaded files to store them in the database
        for n_file in new_files:
            f = User_file(
                id=1,
                user_id=st.session_state["user"].id,
                file_name=n_file.name,
                file_type=n_file.name.split(".")[-1],
                created_at=date.today(),
            )
            f = DB_MAN.link_file_to_user(DB_CONN, f)
            df = ufrw.save_file_in_server(n_file, f.file_type, str(f.id))

            st.success(f"Succesfully uploaded file {n_file.name}")
            st.session_state["current_file"] = df

    # get the user files from the database
    user_files = DB_MAN.get_files_from_user(DB_CONN, st.session_state["user"].id)

    # show the file info in 3 columns
    st.subheader("My Files")
    st.write("----")
    n = 3
    columns = st.columns(n)
    for i, file in enumerate(user_files):
        with columns[i % n]:
            st.subheader(file.file_name)
            st.write(f"{file.file_type} - {file.created_at}")
            if st.button("Load File", key=file.id):
                df = ufrw.read_file(f"{file.id}.{file.file_type}", file.file_type, True)
                st.success(f"Succesfully loaded file {file.file_name}")
                st.session_state["current_file"] = df

            if st.button("Delete File", key=file.id):
                DB_MAN.delete_file_link(DB_CONN, file.id)
                ufrw.delete_file_from_server(f"{file.id}.{file.file_type}", file.file_type, True)
                st.error("Succesfully deleted the file")

            st.write("----")
