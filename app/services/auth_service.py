from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        user: UserCreate,
    ) -> User:

        existing_user = (
            db.query(User)
            .filter(
                (User.email == user.email)
                | (User.username == user.username)
            )
            .first()
        )

        if existing_user:
            raise ValueError("User already exists.")

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            full_name=user.full_name,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def login_user(
        db: Session,
        email: str,
        password: str,
    ):

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password.")

        token = create_access_token(
            {"sub": user.email}
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }