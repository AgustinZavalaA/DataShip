import streamlit as st

# mejor seguir este tuto https://github.com/dataprofessor/multi-page-app/blob/main/multiapp.py


def App1page():
    st.write("Showing app 1")
    if st.button("Return to Main Page"):
        st.session_state.runpage = main_page
        st.experimental_rerun()


def App2page():
    st.write("Showing app 2")
    if st.button("Return to Main Page"):
        st.session_state.runpage = main_page
        st.experimental_rerun()


def main_page():
    st.write("This is my main menu page")
    btn2 = st.button("Show App2")
    btn1 = st.button("Show App1")

    if btn1:
        st.session_state.runpage = App1page
        st.session_state.runpage()
        st.experimental_rerun()

    if btn2:
        st.session_state.runpage = App2page
        st.session_state.runpage()
        st.experimental_rerun()


if "runpage" not in st.session_state:
    st.session_state.runpage = main_page
    st.session_state.runpage()
