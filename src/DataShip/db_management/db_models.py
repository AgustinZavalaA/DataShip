from dataclasses import dataclass
from datetime import date
from typing import Optional

""" This module describes the database models used by the DataShip application."""


@dataclass
class User:
    """This class represent an user of the DataShip application."""

    id: int
    name: str
    username: str
    password: str
    created_at: date
    email: Optional[str] = None


@dataclass
class Feedback_post:
    """This class represent a feedback post of the DataShip application."""

    id: int
    type_id: int
    title: str
    post: str
    created_at: date
    done: bool
    user_id: Optional[int] = None


@dataclass
class Feedback_type:
    """This class represent a feedback type of the DataShip application."""

    id: int
    name: str
    created_at: date


@dataclass
class Module:
    """This class represent a module of the DataShip application."""

    id: int
    name: str
    description: str
    created_at: date


@dataclass
class User_file:
    """This class represent a user file of the DataShip application."""

    id: int
    user_id: int
    file_name: str
    file_type: str
    created_at: date
