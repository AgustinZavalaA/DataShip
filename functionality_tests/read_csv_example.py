# DataShip main archive using Streamlit
import streamlit as st
import pandas as pd


def main():
    st.title("DataShip")

    with st.form("my_form"):
        st.write("Inside the form")
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)

    st.write("Outside the form")

    link = "[Google](https://google.com)"
    st.markdown(link, True)

    uploaded_file = st.file_uploader("Choose a file")

    # st button for redirecting to github
    st.button("Github")

    if uploaded_file is not None:

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)

        select_columns = st.multiselect("Select columns", dataframe.columns)

        graph_data = dataframe[select_columns]
        try:
            st.line_chart(graph_data)
            st.write(graph_data.mean().rename("Mean"))
            st.write(graph_data.median().rename("Median"))
            st.write(graph_data.mode(axis=0))

        except Exception as e:
            st.error("You have selected an invalid column")
            st.write(e)
    else:
        st.warning("Upload a file to continue")


if __name__ == "__main__":
    main()
