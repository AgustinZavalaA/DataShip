# test for the file db_models.py
import DataShip.db_management.db_models as models
from datetime import date


def test_user_model():
    user = models.User(
        id=1,
        name="test name",
        username="test username",
        password="test password",
        created_at=date.today(),
        email="test email",
    )
    assert user.id == 1
    assert user.name == "test name"
    assert user.username == "test username"
    assert user.password == "test password"
    assert user.created_at == date.today()
    assert user.email == "test email"


def test_feedback_type_model():
    feedback_type = models.Feedback_type(id=1, name="test name", created_at=date.today())
    assert feedback_type.id == 1
    assert feedback_type.name == "test name"
    assert feedback_type.created_at == date.today()


def test_feedback_post_model():
    feedback_post = models.Feedback_post(
        id=1,
        type_id=1,
        title="test title",
        post="test post",
        created_at=date.today(),
        done=False,
        user_id=1,
    )
    assert feedback_post.id == 1
    assert feedback_post.type_id == 1
    assert feedback_post.title == "test title"
    assert feedback_post.post == "test post"
    assert feedback_post.created_at == date.today()
    assert feedback_post.done is False
    assert feedback_post.user_id == 1
