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

        # Email is the primary registration identifier.
        # Username remains in the database for compatibility with the
        # existing schema, but it is generated automatically when the
        # frontend does not provide one.
        existing_user = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_user:
            raise ValueError("An account with this email already exists.")

        username = user.username

        if not username:
            base_username = user.email.split("@")[0]
            base_username = "".join(
                character
                for character in base_username
                if character.isalnum() or character == "_"
            )[:40] or "user"

            username = base_username
            suffix = 1

            while db.query(User).filter(User.username == username).first():
                suffix_text = f"_{suffix}"
                username = f"{base_username[:50 - len(suffix_text)]}{suffix_text}"
                suffix += 1

        else:
            existing_username = (
                db.query(User)
                .filter(User.username == username)
                .first()
            )

            if existing_username:
                raise ValueError("That username is already in use.")

        db_user = User(
            username=username,
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