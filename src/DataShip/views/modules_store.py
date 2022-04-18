from DataShip.db_management.db_manager import DB_manager
from sqlite3 import Connection
import streamlit as st


def modules(DB_MAN: DB_manager, DB_CONN: Connection) -> None:
    """ This function represent a view for viewing all .

    Args:
        DB_MAN (DB_manager): database manager.
        DB_CONN (Connection): database connection.
    """

    # Shows the user the current user modules
    user_modules = []
    if st.session_state["user"] is None:
        st.warning("You aren't logged in yet, all changes you make won't take effect. ")
    else:
        user_modules = DB_MAN.get_modules_from_user(DB_CONN, st.session_state["user"].id)
        st.subheader("My modules")
        for module in user_modules:
            st.markdown(f"- **{module.name}**")

    with st.spinner("Loading modules..."):
        all_modules = DB_MAN.get_all_modules(DB_CONN)

    # Show the user the available modules to get
    st.subheader("Modules store")
    st.write("----")
    n = 3
    columns = st.columns(n)
    for i, module in enumerate(all_modules):
        with columns[i % n]:
            st.subheader(module.name)
            st.write(module.description)
            if (
                st.button(
                    "I want it!",
                    key=module.name,
                    disabled=module.name in [m.name for m in user_modules] or st.session_state["user"] is None,
                )
                and st.session_state["user"] is not None
                and DB_MAN.add_module_to_user(DB_CONN, st.session_state["user"].id, module.id)
            ):
                st.success("Module added to your workspace!")

            st.write("----")
