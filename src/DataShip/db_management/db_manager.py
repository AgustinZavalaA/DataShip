import sqlite3
from sqlite3 import Connection
import streamlit as st
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class DB_manager:
    def __init__(self, db_uri: str):
        self.URI = db_uri

    def get_all_users(self, con: Connection):
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

    def check_user_password(self, con: Connection, username_or_emal: str, password: str):
        cur = con.cursor()
        if username_or_emal.find("@"):
            cur.execute("SELECT * FROM users WHERE email = ?", (username_or_emal,))
        else:
            cur.execute("SELECT * FROM users WHERE username = ?", (username_or_emal,))
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

    # TODO actualizar este metodo
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
    def get_connection(self) -> Connection:
        """Put the connection in cache to reuse if path does not change between Streamlit reruns.
        NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
        """
        return sqlite3.connect(self.URI, check_same_thread=False)


def main():
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "cps", ["create_base_database", "populate_base_database", "show_database"]
        )

    except getopt.GetoptError:
        print("Usage: db_manager.py -c|--create_base_database|-p|--populate_base_database|-s|--show_database")
        sys.exit(2)

    DB_URI = "dataship.db"

    db_man = DB_manager(DB_URI)

    for opt, arg in opts:
        if opt in ("-c", "--create_base_database"):
            execute_script(db_man, "src/DataShip/db_management/scripts/create_dataship_db.sql")
        elif opt in ("-p", "--populate_base_database"):
            execute_script(db_man, "src/DataShip/db_management/scripts/populate_dataship_db.sql")
        elif opt in ("-s", "--show_database"):
            show_db()
        else:
            print("Usage: db_manager.py -c|--create_base_database|-p|--populate_base_database")
            sys.exit(2)


def show_db():
    conn = sqlite3.connect("dataship.db")
    cur = conn.cursor()
    for row in cur.execute("SELECT * FROM users"):
        print(row)
    conn.close()


def execute_script(db_man: DB_manager, script_filepath: str):
    conn = sqlite3.connect(db_man.URI)

    cur = conn.cursor()

    with open(script_filepath, "r") as f:
        script = f.read()
    cur.executescript(script)


if __name__ == "__main__":
    main()
