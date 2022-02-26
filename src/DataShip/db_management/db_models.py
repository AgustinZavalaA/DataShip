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
