from dataclasses import dataclass


@dataclass
class Session:
    user: str
    database: str
    password: str
