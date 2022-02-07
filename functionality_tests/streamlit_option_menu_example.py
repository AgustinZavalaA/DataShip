import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "Settings"],
        icons=["house", "gear"],
        menu_icon="bar-chart-steps",
        default_index=1,
    )
    st.write(selected)

# horizontal menu
selected2 = option_menu(
    None,
    ["Home  ", "Upload", "Tasks", "Settings"],
    icons=["house", "cloud-upload", "list-task", "gear"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)
st.write(selected2)
