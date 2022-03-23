from DataShip.db_management.db_manager import DB_manager
import streamlit as st
from sqlite3 import Connection
import DataShip.data_analysis_modules.user_files_reader_writer as ufrw
import DataShip.data_analysis_modules.data_analysis_modules as modules


def home(DB_MAN: DB_manager, DB_CONN: Connection) -> None:
    st.subheader("Home")

    df = None

    if st.session_state["current_file"] is not None:
        df = st.session_state["current_file"]
    else:
        st.subheader("No file selected")
        st.write("Upload a file to see it here or load the demo file")
        if st.button("Load Demo File"):
            df = ufrw.read_file("demo_data/demo_data.csv", "csv", False)
            st.session_state["current_file"] = df
            st.experimental_rerun()
        if st.button("Load Demo file (coordinates)"):
            df = ufrw.read_file("demo_data/data_coordinates.json", "json", False)
            st.session_state["current_file"] = df
            st.experimental_rerun()
        st.write(
            "You can also can save your own file if you have one account, just **Sign Up** and go to **My Files**"
        )
        file = st.file_uploader("", type=["csv", "txt", "json", "xlsx"])
        if file:
            df = ufrw.read_file(file, file.name.split(".")[-1], False)
            st.session_state["current_file"] = df
            st.experimental_rerun()

    if df is not None:
        st.subheader("Current File Selected")
        if st.button("Unload File"):
            st.session_state["current_file"] = None
            st.experimental_rerun()

        st.write(df)

        active_modules = modules.get_active_modules()

        with st.sidebar:
            if st.session_state["user"] is not None:
                st.subheader("Data Analysis Modules")
                user_modules_bd = DB_MAN.get_modules_from_user(
                    DB_CONN, st.session_state["user"].id
                )
                user_modules = [x.name for x in user_modules_bd]
            else:
                user_modules = ["Mean", "Median", "Mode"]

            st.subheader("Select a data analysis module")
            for module in user_modules:
                if st.checkbox(module):
                    active_modules[module] = (active_modules[module][0], True)

        selected_columns = st.multiselect("Select columns", df.columns)

        analysis_df = df[selected_columns]

        for key, value in active_modules.items():
            if value[1]:
                st.subheader(f"Analysis of {key}")
                result = value[0](analysis_df)
                if not result.empty:
                    st.write(result)
