from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import (
    Token,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.auth.service import AuthService
from app.common.responses import success_response
from app.core.security import create_access_token
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_role
from app.common.auth_context import AuthContext


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.get("/owner-only")
def owner_only(
    ctx: AuthContext = Depends(require_role("owner")),
):
    return {
        "message": f"Welcome {ctx.user.full_name}",
        "organization": ctx.organization_id,
        "role": ctx.role,
    }

@router.post("/register", status_code=201)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    created_user = service.register_user(user)

    return success_response(
        data=UserResponse.model_validate(created_user).model_dump(),
        message="User registered successfully",
        status_code=201,
    )


@router.post("/login")
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    result = service.authenticate_user(
        credentials.email,
        credentials.password,
    )

    user = result["user"]
    membership = result["membership"]

    token = create_access_token(
        {
            "sub": user.id,
            "organization_id": membership.organization_id,
            "role": membership.role,
        }
    )

    return success_response(
        data=Token(
            access_token=token,
            token_type="bearer",
        ).model_dump(),
        message="Login successful",
    )


@router.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    return success_response(
        data={
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
        },
        message="User profile fetched successfully",
    )