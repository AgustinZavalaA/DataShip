import sqlite3
from sqlite3 import Connection
import streamlit as st
import hashlib
from typing import Optional

# import the models from the db_models.py file. This helps to add abstraction to the application.
from DataShip.db_management.db_models import (
    User,
    Feedback_post,
    Feedback_type,
    Module,
    User_file,
)


def hash_password(password: str) -> str:
    """This method returns a hashed password using the SHA-256 algorithm.

    Args:
        password (str): un-hashed password.

    Returns:
        str: hashed password.
    """

    return hashlib.sha256(password.encode()).hexdigest()


class DB_manager:
    def __init__(self, db_uri: str) -> None:
        """This method initializes the database manager.

        Args:
            db_uri (str): un-hashed password.
        """

        self.URI = db_uri

    def get_all_users(self, con: Connection) -> list[User]:
        """This method returns a list of all users in the database.

        Args:
            con (Connection): database connection.

        Returns:
            list[User]: list of all users in the database.
        """

        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

    def get_username_by_id(self, con: Connection, user_id: str) -> str:
        """This method returns the username of a user by their id.

        Args:
            con (Connection): database connection.
            user_id (str): id of the user.

        Returns:
            str: username of the user.
        """

        # if user is not found, return "Anonymous"
        if user_id is None or user_id == "nan" or user_id == "" or user_id == "None":
            return "Anonymous"
        # else fetch the username from the database
        cur = con.cursor()
        cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        return str(cur.fetchone()[0])

    def check_user_password(
        self, con: Connection, username_or_emal: str, password: str
    ) -> Optional[User]:
        """This method checks if the password is correct for a user.

        Args:
            con (Connection): database connection.
            username_or_emal (str): username or email of the user.
            password (str): password of the user.

        Returns:
            Optional[User]: user object if the password is correct.
        """

        cur = con.cursor()
        # check if the username is an email or a username and fetch the user
        if username_or_emal.find("@") != -1:
            cur.execute("SELECT * FROM users WHERE email = ?", (username_or_emal,))
        else:
            cur.execute("SELECT * FROM users WHERE username = ?", (username_or_emal,))
        user = cur.fetchone()
        if user is None:
            return None

        # check if the password is correct and return the user object if it is
        hashed_password = user[4]
        if hash_password(password) == hashed_password:
            return User(
                id=user[0],
                name=user[1],
                username=user[2],
                email=user[3],
                password=user[4],
                created_at=user[5],
            )

        # default return None
        return None

    def get_modules_from_user(self, con: Connection, user_id: int) -> list[Module]:
        """This method returns a list of all modules a user is subscribed to.

        Args:
            con (Connection): database connection.
            user_id (int): id of the user.

        Returns:
            list[Module]: list of all modules a user is subscribed to.
        """

        cur = con.cursor()
        cur.execute("SELECT module_id FROM users_modules WHERE user_id = ?", (user_id,))
        modules = []
        # convert the fetched data to a list of modules
        for row in cur.fetchall():
            modules.append(self.get_module_by_id(con, row[0]))
        return modules

    def get_module_by_id(self, con: Connection, module_id: int) -> Module:
        """This method returns a module object by its id.

        Args:
            con (Connection): database connection.
            module_id (int): id of the module.

        Returns:
            Module: module object.
        """

        cur = con.cursor()
        cur.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
        row = cur.fetchone()
        module = Module(id=row[0], name=row[1], description=row[2], created_at=row[3])
        return module

    def get_all_modules(self, con: Connection) -> list[Module]:
        """This method returns a list of all modules in the database.

        Args:
            con (Connection): database connection.

        Returns:
            list[Module]: list of all modules in the database.
        """

        cur = con.cursor()
        cur.execute("SELECT * FROM modules")
        modules = []
        # convert the fetched data to a list of modules
        for row in cur.fetchall():
            modules.append(
                Module(id=row[0], name=row[1], description=row[2], created_at=row[3])
            )
        return modules

    def add_module_to_user(self, con: Connection, user_id: int, module_id: int) -> bool:
        """This method adds a module to a user.

        Args:
            con (Connection): database connection.
            user_id (int): id of the user.
            module_id (int): id of the module.

        Returns:
            bool: True if the module was added to the user.
        """

        cur = con.cursor()
        cur.execute(
            "INSERT INTO users_modules (user_id, module_id) VALUES (?, ?)",
            (user_id, module_id),
        )
        con.commit()
        return True

    def create_user(self, con: Connection, user: User) -> bool:
        """This method creates a user in the database.

        Args:
            con (Connection): database connection.
            user (User): user object.

        Returns:
            bool: True if the user was created.
        """

        cur = con.cursor()

        user.password = hash_password(user.password)
        cur.execute(
            "INSERT INTO users (name, username, email, password, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                user.name,
                user.username,
                user.email,
                user.password,
                user.created_at,
            ),
        )
        con.commit()
        return True

    def update_user(self, con: Connection, user: User) -> User:
        """This method updates a user in the database.

        Args:
            con (Connection): database connection.
            user (User): user object.

        Returns:
            User: user object.
        """

        cur = con.cursor()
        cur.execute(
            "UPDATE users SET name = ?, username = ?, email = ?, password = ? WHERE id = ?",
            (
                user.name,
                user.username,
                user.email,
                hash_password(user.password),
                user.id,
            ),
        )
        con.commit()
        user.password = hash_password(user.password)
        return user

    def link_file_to_user(self, con: Connection, file: User_file) -> User_file:
        """This method links a file to a user.

        Args:
            con (Connection): database connection.
            file (User_file): file object.

        Returns:
            User_file: file object.
        """

        cur = con.cursor()
        cur.execute(
            "INSERT INTO users_files (user_id, filename, file_type, created_at) VALUES (?, ?, ?, ?)",
            (file.user_id, file.file_name, file.file_type, file.created_at),
        )
        cur.execute("SELECT last_insert_rowid()")
        file.id = cur.fetchone()[0]
        con.commit()
        return file

    def delete_file_link(self, con: Connection, file_id: int) -> bool:
        """This method deletes a file link from the database.

        Args:
            con (Connection): database connection.
            file_id (int): id of the file.

        Returns:
            bool: True if the file link was deleted.
        """

        cur = con.cursor()
        cur.execute("DELETE FROM users_files WHERE id = ?", (file_id,))
        con.commit()
        return True

    def get_files_from_user(self, con: Connection, user_id: int) -> list[User_file]:
        """This method returns a list of all files a user has uploaded.

        Args:
            con (Connection): database connection.
            user_id (int): id of the user.

        Returns:
            list[User_file]: list of all files a user has uploaded.
        """

        cur = con.cursor()
        cur.execute("SELECT * FROM users_files WHERE user_id = ?", (user_id,))
        return [
            User_file(row[0], row[1], row[2], row[3], row[4]) for row in cur.fetchall()
        ]

    def get_feedback_posts(self, con: Connection) -> list[Feedback_post]:
        """This method returns a list of all feedback posts.

        Args:
            con (Connection): database connection.

        Returns:
            list[Feedback_post]: list of all feedback posts.
        """

        cur = con.cursor()
        cur.execute("SELECT * FROM Feedback_post")
        return [
            Feedback_post(
                id=row[0],
                type_id=row[1],
                title=row[2],
                post=row[3],
                created_at=row[4],
                done=row[5],
                user_id=row[6],
            )
            for row in cur.fetchall()
        ]

    def create_feedback_post(
        self, con: Connection, feedback_post: Feedback_post
    ) -> bool:
        """This method creates a feedback post in the database.

        Args:
            con (Connection): database connection.
            feedback_post (Feedback_post): feedback post object.

        Returns:
            bool: True if the feedback post was created.
        """

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
        """This method returns a list of all feedback types.

        Args:
            con (Connection): database connection.

        Returns:
            list[Feedback_type]: list of all feedback types.
        """

        cur = con.cursor()
        cur.execute("SELECT * FROM Feedback_type")
        return [
            Feedback_type(id=row[0], name=row[1], created_at=row[2])
            for row in cur.fetchall()
        ]

    @st.cache(hash_funcs={Connection: id})
    def get_connection(self) -> Connection:
        """Put the connection in cache to reuse if path does not change between Streamlit reruns.
            NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa

        Returns:
            Connection: database connection.
        """

        return sqlite3.connect(self.URI, check_same_thread=False)


def main():
    """This file can be run as a standalone script to create, populate or view the database."""

    import sys
    import getopt
    import os
    import shutil

    # get the args from the command line
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "cps",
            ["create_base_database", "populate_base_database", "show_database"],
        )

    except getopt.GetoptError:
        print(
            "Usage: db_manager.py -c|--create_base_database|-p|--populate_base_database|-s|--show_database"
        )
        sys.exit(2)

    DB_URI = "dataship.db"

    db_man = DB_manager(DB_URI)

    # iterate over the args and do the expected function
    for opt, arg in opts:
        if opt in ("-c", "--create_base_database"):
            # if user_files folder already exists, delete it
            if os.path.exists("user_files/"):
                shutil.rmtree("user_files")
            os.mkdir("user_files")
            # create the database
            execute_script(
                db_man, "src/DataShip/db_management/scripts/create_dataship_db.sql"
            )
        elif opt in ("-p", "--populate_base_database"):
            # populate the database
            execute_script(
                db_man, "src/DataShip/db_management/scripts/populate_dataship_db.sql"
            )
        elif opt in ("-s", "--show_database"):
            # show the database
            show_db()
        else:
            # show the help to the user if the args are not understood and exit
            print(
                "Usage: db_manager.py -c|--create_base_database|-p|--populate_base_database"
            )
            sys.exit(2)


def show_db():
    """Prints all data in database including all table names, column names and data."""
    conn = sqlite3.connect("dataship.db")
    cur = conn.cursor()

    # Get all table names
    tables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    ).fetchall()
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


def execute_script(db_man: DB_manager, script_filepath: str) -> None:
    """This function execute a script in the database.

    Args:
        db_man (DB_manager): a database manager.
        script_filepath (str): file path to the script to execute.
    """
    conn = sqlite3.connect(db_man.URI)

    cur = conn.cursor()

    with open(script_filepath, "r") as f:
        script = f.read()
    cur.executescript(script)


if __name__ == "__main__":
    main()
