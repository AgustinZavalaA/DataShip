from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    username: str
    password: str
    color_scheme: str
    created_at: date
    email: Optional[str] = None
    
@dataclass
class Feedback_post:
    id: int
    type_id: int
    title: str
    post: str
    created_at: date
    done: bool
    user_id: Optional[int] = None
    
@dataclass
class Feedback_type:
    id: int
    name: str
    created_at: date


def main():
    user = User(
        id=1,
        name="Juan",
        username="juan",
        password="1234",
        color_scheme="dark",
        created_at=date.today(),
    )
    print(user)


if __name__ == "__main__":
    main()
