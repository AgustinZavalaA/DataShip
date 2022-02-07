import streamlit as st
import streamlit_authenticator as stauth

names = ["John Smith", "Rebecca Briggs"]
usernames = ["jsmith", "rbriggs"]
passwords = ["123", "456"]

hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(
    names, usernames, hashed_passwords, "some_cookie_name", "some_signature_key", cookie_expiry_days=30
)

name, authentication_status = authenticator.login("Login", "main")

if authentication_status:
    st.write("Welcome *%s*" % (name))
    st.title("Some content")
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")

if st.session_state["authentication_status"]:
    st.write("Welcome *%s*" % (st.session_state["name"]))
    st.title("Some content")
elif st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] == None:
    st.warning("Please enter your username and password")
