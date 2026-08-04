from fastapi import Depends, HTTPException, status

from app.common.auth_context import AuthContext
from app.dependencies.auth import get_auth_context


def require_role(*allowed_roles: str):
    def checker(
        ctx: AuthContext = Depends(get_auth_context),
    ):
        if ctx.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return ctx

    return checker