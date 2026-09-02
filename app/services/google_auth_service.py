from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.core.security import create_access_token


class GoogleAuthService:

    @staticmethod
    def login_with_google(db: Session, credential: str):

        # Verify the Google ID token
        try:
            claims = id_token.verify_oauth2_token(
                credential,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
        except ValueError:
            raise ValueError("Invalid Google token.")

        # Make sure the token belongs to Google
        if claims.get("iss") not in [
            "accounts.google.com",
            "https://accounts.google.com",
        ]:
            raise ValueError("Invalid Google token issuer.")

        # Google must have verified the email
        if not claims.get("email_verified"):
            raise ValueError("Google email is not verified.")

        email = claims.get("email")
        google_subject = claims.get("sub")
        full_name = claims.get("name") or email.split("@")[0]

        if not email or not google_subject:
            raise ValueError("Invalid Google account information.")

        # Check whether the user already exists
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        # Create a new ForgeIQ account if necessary
        if not user:

            base_username = email.split("@")[0]
            username = base_username
            counter = 1

            while db.query(User).filter(
                User.username == username
            ).first():
                username = f"{base_username}_{counter}"
                counter += 1

            user = User(
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=None,
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        # Generate the same ForgeIQ JWT used by normal login
        access_token = create_access_token(
            data={"sub": user.email}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }