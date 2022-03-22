# test for thwe file db_manager.py
import DataShip.db_management.db_manager as db_manager
from DataShip.db_management.db_models import User, Feedback_post
import pytest
from sqlite3 import Connection
from datetime import date


@pytest.fixture
def db_conn_man():
    DB_URI_SQLITE = "dataship.db_test"
    DB_MAN = db_manager.DB_manager(DB_URI_SQLITE)
    DB_CONN = DB_MAN.get_connection()

    db_manager.execute_script(DB_MAN, "src/DataShip/db_management/scripts/create_dataship_db.sql")
    db_manager.execute_script(DB_MAN, "src/DataShip/db_management/scripts/populate_dataship_db.sql")

    return DB_CONN, DB_MAN


# test insertion in database
def test_insert_user(db_conn_man: tuple[Connection, db_manager.DB_manager]) -> None:
    db_conn, db_man = db_conn_man
    user = User(
        id=1,
        name="test name",
        username="test username",
        password="test password",
        created_at=date.today(),
        email="test email",
    )
    # test that the new user is created in the database
    assert db_man.create_user(db_conn, user) is True
    # test that the lenght of all users in the database is 4, because in the begining there are 3
    assert len(db_man.get_all_users(db_conn)) == 4


def test_update_user(db_conn_man: tuple[Connection, db_manager.DB_manager]) -> None:
    db_conn, db_man = db_conn_man
    user = User(
        id=4,
        name="test name",
        username="test username",
        password="test password",
        created_at=date.today(),
        email="test email",
    )
    # test that the new user is created in the database
    assert db_man.create_user(db_conn, user) is True
    # test that the lenght of all users in the database is 4, because in the begining there are 3
    assert len(db_man.get_all_users(db_conn)) == 4
    # test update an user
    user2 = db_man.check_user_password(db_conn, "test username", "test password")
    user2.name = "changed name"
    user2.username = "changed username"
    user2.password = "changed password"
    user2.email = "changed email"
    modified_user = db_man.update_user(db_conn, user2)
    print(user, user2, modified_user)

    assert user.id == modified_user.id
    assert str(user.created_at) == modified_user.created_at
    assert user.name != modified_user.name
    assert user.username != modified_user.username
    assert user.password != modified_user.password
    assert user.email != modified_user.email


def test_get_all_users(db_conn_man: tuple[Connection, db_manager.DB_manager]) -> None:
    db_conn, db_man = db_conn_man

    all_users = db_man.get_all_users(db_conn)
    # test getting the correct amount of users when the db is created
    assert len(all_users) == 3
    # testing for the first user created in the sql file (ADMIN)
    assert all_users[0][1] == "Admin"


def test_get_user_by_id(db_conn_man: tuple[Connection, db_manager.DB_manager]) -> None:
    db_conn, db_man = db_conn_man

    # testing for the first user created in the sql file (ADMIN)
    assert db_man.get_username_by_id(db_conn, "1") == "admin"
    assert db_man.get_username_by_id(db_conn, "2") == "agus"
    assert db_man.get_username_by_id(db_conn, "3") == "daniel"


def test_check_pass_user(db_conn_man: tuple[Connection, db_manager.DB_manager]) -> None:
    db_conn, db_man = db_conn_man
    user = User(
        id=4,
        name="test name",
        username="test username",
        password="test password",
        created_at=date.today(),
        email="test@email",
    )
    # test that the new user is created in the database
    assert db_man.create_user(db_conn, user) is True
    # test that the lenght of all users in the database is 4, because in the begining there are 3
    assert len(db_man.get_all_users(db_conn)) == 4

    # test the new user password by name
    assert db_man.check_user_password(db_conn, "test username", "test password").name == user.name
    # test the new user password by email
    assert db_man.check_user_password(db_conn, "test@email", "test password").name == user.name

    # test with an invalid password
    assert db_man.check_user_password(db_conn, "test@email", "bad password") is None


def test_modules_table(db_conn_man: tuple[Connection, db_manager.DB_manager]) -> None:
    db_conn, db_man = db_conn_man

    all_modules = db_man.get_all_modules(db_conn)
    # test the number of modules in database, at start there are 8
    assert len(all_modules) == 8
    # test the first name of the module (mean)
    assert all_modules[0].name == "Mean"
    # test get the first module and comparing the name
    assert db_man.get_module_by_id(db_conn, 2).name == "Median"
    # test linking the first module to the first user
    assert db_man.add_module_to_user(db_conn, user_id=1, module_id=3) is True
    # test len of modules from user
    assert len(db_man.get_modules_from_user(db_conn, user_id=1)) == 1
    # test the name of the first module of the user
    assert db_man.get_modules_from_user(db_conn, user_id=1)[0].name == "Mode"


def test_feedback_and_types_table(db_conn_man: tuple[Connection, db_manager.DB_manager]) -> None:
    db_conn, db_man = db_conn_man

    # test the number of feedback types as start of program
    assert len(db_man.get_all_feedback_types(db_conn)) == 3
    # test the number of feedback posts as start of program
    assert len(db_man.get_feedback_posts(db_conn)) == 17
    # test the insertion of a new feedback post
    feebback_post = Feedback_post(
        id=1,
        type_id=1,
        title="test title",
        post="test post",
        created_at=date.today(),
        done=False,
        user_id=1,
    )
    assert db_man.create_feedback_post(db_conn, feebback_post) is True
    assert len(db_man.get_feedback_posts(db_conn)) == 18
