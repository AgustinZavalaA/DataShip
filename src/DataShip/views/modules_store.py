from DataShip.db_management.db_manager import DB_manager
from DataShip.db_management.db_models import User
from sqlite3 import Connection
import streamlit as st


def modules(DB_MAN: DB_manager, DB_CONN: Connection) -> None:
    user_modules = []
    if st.session_state["user"] is None:
        st.warning("You aren't logged in yet, all changes you make won't take effect. ")
    else:
        user_modules = DB_MAN.get_modules_from_user(
            DB_CONN, st.session_state["user"].id
        )
        st.subheader("My modules")
        user_modules = [x.name for x in user_modules]
        for module_name in user_modules:
            st.markdown(f"- **{module_name}**")

    with st.spinner("Loading modules..."):
        all_modules = DB_MAN.get_all_modules(DB_CONN)

    st.subheader("Modules store")
    st.write("----")
    n = 3
    columns = st.columns(n)
    for i, module in enumerate(all_modules):
        with columns[i % n]:
            st.subheader(module.name)
            st.write(module.description)
            if st.button(
                "I want it!",
                key=module.name,
                disabled=module.name in user_modules
                or st.session_state["user"] is None,
            ):
                if DB_MAN.add_module_to_user(
                    DB_CONN, st.session_state["user"].id, module.id
                ):
                    st.success("Module added to your workspace!")

            st.write("----")

    st.write(user_modules)
