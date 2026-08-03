from sqlalchemy.orm import Session

from app.organizations.models import (
    Organization,
    OrganizationMember,
)


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        name: str,
        slug: str,
    ) -> Organization:
        organization = Organization(
            name=name,
            slug=slug,
        )

        self.db.add(organization)
        self.db.flush()

        return organization

    def add_member(
        self,
        *,
        organization_id: int,
        user_id: int,
        role: str = "owner",
    ) -> OrganizationMember:
        membership = OrganizationMember(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )

        self.db.add(membership)

        return membership