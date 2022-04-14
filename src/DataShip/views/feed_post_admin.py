import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from dataclasses import asdict

from DataShip.db_management.db_models import Feedback_post


def feedback_post(DB_MAN, DB_CONN) -> None:
    """ This function represent a view for creating feedback posts.

    Args:
        DB_MAN (_type_): database manager.
        DB_CONN (_type_): database connection.
    """
    st.title("Feedback Posts")
    feedback_posts = DB_MAN.get_feedback_posts(DB_CONN)

    df = pd.DataFrame([asdict(post) for post in feedback_posts])

    df["type_id"].replace({1: "BUG", 2: "FEATURE", 3: "VULNERABILITY"}, inplace=True)

    gb = GridOptionsBuilder.from_dataframe(df)

    # gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridOptions = gb.build()

    data = AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme="material",
    )

    if data:
        for row in data["selected_rows"]:
            post = Feedback_post(**row)
            done = "✔️" if post.done else "❌"
            st.markdown(f"## {done} {post.done}: {post.title}")

            post_type = str(post.type_id)
            if post_type == "BUG":
                html_text = "### 🐛 <span style=color:yellow> BUG </span> "
            elif post_type == "FEATURE":
                html_text = "### 📌 <span style=color:green> FEATURE </span> "
            else:
                html_text = "### 🚩 <span style=color:red> VULNERABILITY </span> "
            st.markdown(html_text, unsafe_allow_html=True)

            st.caption(f"{post.created_at} by {DB_MAN.get_username_by_id(DB_CONN, post.user_id)}")
            st.write(post.post)

            st.write("-" * 50)
