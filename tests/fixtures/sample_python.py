"""Sample Python fixture for QA testing."""

from dataclasses import dataclass
from typing import Protocol


class Logger(Protocol):
    def log(self, message: str) -> None: ...


@dataclass
class User:
    name: str
    email: str
    active: bool = True

    def deactivate(self) -> None:
        self.active = False


def find_active_users(users: list[User]) -> list[User]:
    return [u for u in users if u.active]


async def fetch_user_data(user_id: int) -> dict:
    """Simulates an async API call."""
    import asyncio

    await asyncio.sleep(0.1)
    return {"id": user_id, "status": "ok"}
