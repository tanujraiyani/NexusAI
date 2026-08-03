from sqlalchemy.orm import Session

from app.auth.schemas import UserRegister
from app.common.exceptions import (
    AlreadyExistsException,
    UnauthorizedException,
)
from app.common.repositories.organization_member_repository import (
    OrganizationMemberRepository,
)
from app.common.repositories.organization_repository import (
    OrganizationRepository,
)
from app.common.repositories.user_repository import UserRepository
from app.common.utils import slugify
from app.core.security import (
    hash_password,
    verify_password,
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.organizations = OrganizationRepository(db)
        self.memberships = OrganizationMemberRepository(db)

    def get_user_by_email(self, email: str):
        return self.users.get_by_email(email)

    def register_user(self, user_data: UserRegister):
        existing = self.users.get_by_email(user_data.email)

        if existing:
            raise AlreadyExistsException("Email is already registered")

        try:
            user = self.users.create(
                email=user_data.email,
                full_name=user_data.full_name,
                hashed_password=hash_password(user_data.password),
            )

            organization = self.organizations.create(
                name=f"{user.full_name}'s Organization",
                slug=slugify(user.full_name),
            )

            self.organizations.add_member(
                organization_id=organization.id,
                user_id=user.id,
                role="owner",
            )

            self.db.commit()

            self.db.refresh(user)

            return user

        except Exception:
            self.db.rollback()
            raise

    def authenticate_user(self, email: str, password: str):
        user = self.users.get_by_email(email)

        if not user:
            raise UnauthorizedException("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")

        membership = self.memberships.get_by_user_id(user.id)

        if membership is None:
            raise UnauthorizedException(
                "User is not assigned to an organization"
            )

        return {
            "user": user,
            "membership": membership,
        }