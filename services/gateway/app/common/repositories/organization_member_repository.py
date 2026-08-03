from sqlalchemy.orm import Session

from app.organizations.models import OrganizationMember


class OrganizationMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return (
            self.db.query(OrganizationMember)
            .filter(OrganizationMember.user_id == user_id)
            .first()
        )