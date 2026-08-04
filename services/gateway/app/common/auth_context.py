from dataclasses import dataclass

from app.auth.models import User


@dataclass
class AuthContext:
    user: User
    organization_id: int
    role: str