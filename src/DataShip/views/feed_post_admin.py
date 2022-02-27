import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def feedback_post(DB_MAN, DB_CONN):
    st.title('Feedback Posts')
    feedback_posts = DB_MAN.get_feedback_posts(DB_CONN)
    
    df = pd.DataFrame(feedback_posts)
    df.rename(columns={0:'ID', 1:'FEEDBACK TYPE', 2:'TITLE', 3:'POST', 4:'SUMBMITTED ON', 5:'DONE', 6:'USER_ID'}, inplace=True)
    df['FEEDBACK TYPE'].replace({1:'BUG', 2:'FEATURE', 3:'VULNERABILITY'}, inplace=True)
    
    gb = GridOptionsBuilder.from_dataframe(df)

    # gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridOptions = gb.build()

    data = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, update_mode=GridUpdateMode.SELECTION_CHANGED, theme="streamlit")
    
    if data:
        for row in data['selected_rows']:
            done = "✔️" if row['DONE'] else "❌"
            st.markdown(f"## {done} {row['ID']}: {row['TITLE']}")
            
            if row['FEEDBACK TYPE'] == 'BUG':
                html_text = f"### 🐛 <span style=color:yellow> BUG </span> "
            elif row['FEEDBACK TYPE'] == 'FEATURE':
                html_text = f"### 📌 <span style=color:green> FEATURE </span> "
            else:
                html_text = f"### 🚩 <span style=color:red> VULNERABILITY </span> "                
            st.markdown (html_text, unsafe_allow_html=True)
            
            st.caption(f"{row['SUMBMITTED ON']} by {row['USER_ID']}")
            st.write(row['POST'])
            
            st.write("-"*50)
        