from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.models import User
from app.common.repositories.user_repository import UserRepository
from app.core.config import settings
from app.db.database import get_db
from app.common.auth_context import AuthContext
from app.common.repositories.organization_member_repository import (
    OrganizationMemberRepository,
)

security = HTTPBearer()
def get_auth_context(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> AuthContext:

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
    )

    user_id = payload["sub"]

    user_repo = UserRepository(db)
    member_repo = OrganizationMemberRepository(db)

    user = user_repo.get_by_id(user_id)
    membership = member_repo.get_by_user_id(user_id)

    if not user or not membership:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed",
        )

    return AuthContext(
        user=user,
        organization_id=membership.organization_id,
        role=membership.role,
    )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    repo = UserRepository(db)
    user = repo.get_by_id(int(user_id))

    if user is None:
        raise credentials_exception

    return user