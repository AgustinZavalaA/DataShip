import sqlite3
from sqlite3 import Connection
import streamlit as st
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class db_management:
    def __init__(self, db_uri):
        self.URI = db_uri

    def get_all_users(self, con: Connection):
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

    def check_user_password(self, con: Connection, username, password):
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        if user is None:
            return False

        hashed_password = user[3]
        if hash_password(password) == hashed_password:
            return {
                "id": user[0],
                "name": user[1],
                "username": user[2],
            }

        return False

    def create_user(self, con: Connection, username, password, name):
        cur = con.cursor()

        cur.execute(
            "INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
            (username, hash_password(password), name),
        )
        con.commit()
        return {
            "id": cur.lastrowid,
            "name": name,
            "username": username,
        }

    @st.cache(hash_funcs={Connection: id})
    def get_connection(self):
        """Put the connection in cache to reuse if path does not change between Streamlit reruns.
        NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
        """
        return sqlite3.connect(self.URI, check_same_thread=False)
