from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    username: str
    password: str
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


@dataclass
class Module:
    id: int
    name: str
    description: str
    created_at: date
