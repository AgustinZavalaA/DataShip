import sqlite3
from sqlite3 import Connection
import streamlit as st
import hashlib

from DataShip.db_management.db_models import User


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class DB_manager:
    def __init__(self, db_uri: str):
        self.URI = db_uri

    def get_all_users(self, con: Connection):
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

    def check_user_password(self, con: Connection, username_or_emal: str, password: str) ->  User:
        cur = con.cursor()
        if username_or_emal.find("@") != -1:
            cur.execute("SELECT * FROM users WHERE email = ?", (username_or_emal,))
        else:
            cur.execute("SELECT * FROM users WHERE username = ?", (username_or_emal,))
        user = cur.fetchone()
        if user is None:
            return False

        hashed_password = user[4]
        if hash_password(password) == hashed_password:
            return User(
                id=user[0],
                name=user[1],
                username=user[2],
                email=user[3],
                password=user[4],
                color_scheme=user[5],
                created_at=user[6],
            )

        return False

    def create_user(self, con: Connection, user: User) -> bool:
        cur = con.cursor()

        user.password = hash_password(user.password)
        cur.execute(
            "INSERT INTO users (name, username, email, password, color_scheme, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user.name, user.username, user.email, user.password, user.color_scheme, user.created_at),
        )
        con.commit()
        return True
    
    def get_feedback_posts(self, con: Connection) -> list:
        cur = con.cursor()
        cur.execute("SELECT * FROM Feedback_post")
        return cur.fetchall()

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
    """ Prints all data in database including all table names, column names and data."""
    conn = sqlite3.connect("dataship.db")
    cur = conn.cursor()
    
    # Get all table names
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall()
    tables.remove(("sqlite_sequence",))
    
    # Iterate over all tables
    print("PRINTING ALL TABLES")
    for table_name in tables:
        # print table name and column names
        print(f"NAME : {table_name[0]}")
        print("COLUMNS :", end="")
        for col in cur.execute(f"PRAGMA table_info({table_name[0]})").fetchall():
            print(f" {col[1]}", end="")
        print()
        
        #print data
        for row in cur.execute(f"SELECT * FROM {table_name[0]}"):
            print(row)
        print("-"*50)
        
    # close connection to database
    conn.close()


def execute_script(db_man: DB_manager, script_filepath: str):
    conn = sqlite3.connect(db_man.URI)

    cur = conn.cursor()

    with open(script_filepath, "r") as f:
        script = f.read()
    cur.executescript(script)


if __name__ == "__main__":
    main()
