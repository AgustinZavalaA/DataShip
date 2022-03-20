import sqlite3
from sqlite3 import Connection
import streamlit as st
import hashlib
from typing import Optional

from DataShip.db_management.db_models import User, Feedback_post, Feedback_type, Module


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class DB_manager:
    def __init__(self, db_uri: str):
        self.URI = db_uri

    def get_all_users(self, con: Connection):
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

    def get_username_by_id(self, con: Connection, user_id: str) -> str:
        if user_id == "nan" or user_id == "" or user_id is None:
            return "Anonymous"
        cur = con.cursor()
        cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        return str(cur.fetchone()[0])

    def check_user_password(self, con: Connection, username_or_emal: str, password: str) -> Optional[User]:
        cur = con.cursor()
        if username_or_emal.find("@") != -1:
            cur.execute("SELECT * FROM users WHERE email = ?", (username_or_emal,))
        else:
            cur.execute("SELECT * FROM users WHERE username = ?", (username_or_emal,))
        user = cur.fetchone()
        if user is None:
            return None

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

        return None

    def get_modules_from_user(self, con: Connection, user_id: int) -> list[Module]:
        cur = con.cursor()
        cur.execute("SELECT module_id FROM users_modules WHERE user_id = ?", (user_id,))
        modules = []
        for row in cur.fetchall():
            modules.append(self.get_module_by_id(con, row[0]))
        return modules

    def get_module_by_id(self, con: Connection, module_id: int) -> Module:
        cur = con.cursor()
        cur.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
        row = cur.fetchone()
        module = Module(id=row[0], name=row[1], description=row[2], created_at=row[3])
        return module

    def get_all_modules(self, con: Connection) -> list[Module]:
        cur = con.cursor()
        cur.execute("SELECT * FROM modules")
        modules = []
        for row in cur.fetchall():
            modules.append(Module(id=row[0], name=row[1], description=row[2], created_at=row[3]))
        return modules

    def add_module_to_user(self, con: Connection, user_id: int, module_id: int) -> bool:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users_modules (user_id, module_id) VALUES (?, ?)",
            (user_id, module_id),
        )
        con.commit()
        return True

    def create_user(self, con: Connection, user: User) -> bool:
        cur = con.cursor()

        user.password = hash_password(user.password)
        cur.execute(
            "INSERT INTO users (name, username, email, password, color_scheme, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (
                user.name,
                user.username,
                user.email,
                user.password,
                user.color_scheme,
                user.created_at,
            ),
        )
        con.commit()
        return True

    def get_feedback_posts(self, con: Connection) -> list[Feedback_post]:
        cur = con.cursor()
        cur.execute("SELECT * FROM Feedback_post")
        return [
            Feedback_post(
                id=row[0], type_id=row[1], title=row[2], post=row[3], created_at=row[4], done=row[5], user_id=row[6]
            )
            for row in cur.fetchall()
        ]

    def create_feedback_post(self, con: Connection, feedback_post: Feedback_post) -> bool:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Feedback_post (type_id, title, post, created_at, done, user_id) VALUES (?, ?, ?, ?, ?, ?)",
            (
                feedback_post.type_id,
                feedback_post.title,
                feedback_post.post,
                feedback_post.created_at,
                feedback_post.done,
                feedback_post.user_id,
            ),
        )
        con.commit()
        return True

    def get_all_feedback_types(self, con: Connection) -> list[Feedback_type]:
        cur = con.cursor()
        cur.execute("SELECT * FROM Feedback_type")
        return [Feedback_type(id=row[0], name=row[1], created_at=row[2]) for row in cur.fetchall()]

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
            sys.argv[1:],
            "cps",
            ["create_base_database", "populate_base_database", "show_database"],
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
    """Prints all data in database including all table names, column names and data."""
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

        # print the data
        for row in cur.execute(f"SELECT * FROM {table_name[0]}"):
            print(row)
        print("-" * 50)

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
