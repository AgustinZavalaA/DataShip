import sqlite3
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def main():
    # create a database connection (dataship db)
    con = sqlite3.connect("dataship.db")
    cur = con.cursor()

    # create users table with name, username and password
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, username TEXT, password TEXT)"
    )
    print("users table created")

    # generate sample users
    names = ["Agustin Zavala", "Julian Barron", "Rangel Turrubiates"]
    usernames = ["agustin", "kapsu", "rangel"]
    passwords = ["123", "456", "789"]

    for user in zip(names, usernames, passwords):
        cur.execute(
            "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
            (user[0], user[1], hash_password(user[2])),
        )

    # commit changes
    con.commit()

    # show all users
    for user in cur.execute("SELECT * FROM users"):
        print(user)

    # show users with a password
    p = "123"
    print(f"Users with password {p}")
    for row in cur.execute("SELECT * FROM users WHERE password = ?", (hash_password(p),)):
        print(row)

    # close connection
    con.close()


def show_db():
    conn = sqlite3.connect("dataship.db")
    cur = conn.cursor()
    for row in cur.execute("SELECT * FROM users"):
        print(row)
    conn.close()


if __name__ == "__main__":
    # main()
    show_db()
