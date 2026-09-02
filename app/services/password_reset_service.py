import hashlib
import secrets
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.password_reset_otp import PasswordResetOTP
from app.models.user import User
from app.services.email_service import EmailService
from app.core.security import hash_password


class PasswordResetService:

    OTP_EXPIRY_MINUTES = 3
    MAX_ATTEMPTS = 5

    @staticmethod
    def _hash_otp(otp: str) -> str:
        """
        Hash the OTP before storing it in the database.
        """
        return hashlib.sha256(otp.encode()).hexdigest()

    @staticmethod
    def _generate_otp() -> str:
        """
        Generate a secure 6-digit OTP.
        """
        return f"{secrets.randbelow(1_000_000):06d}"

    @staticmethod
    def request_otp(db: Session, email: str):
        """
        Generate and send a password-reset OTP.
        """

        # Find user by email
        user = db.query(User).filter(User.email == email).first()

        # Do not reveal whether an email exists
        if not user:
            return

        # Invalidate all previous unused OTPs
        db.query(PasswordResetOTP).filter(
            PasswordResetOTP.user_id == user.id,
            PasswordResetOTP.used == False,
        ).update(
            {
                PasswordResetOTP.used: True
            },
            synchronize_session=False,
        )

        # Generate new OTP
        otp = PasswordResetService._generate_otp()

        # Hash OTP before storing
        otp_hash = PasswordResetService._hash_otp(otp)

        # Create expiry time
        expires_at = datetime.utcnow() + timedelta(
            minutes=PasswordResetService.OTP_EXPIRY_MINUTES
        )

        # Store OTP
        reset_otp = PasswordResetOTP(
            user_id=user.id,
            otp_hash=otp_hash,
            expires_at=expires_at,
            attempts=0,
            used=False,
        )

        db.add(reset_otp)
        db.commit()

        # Send OTP email
        EmailService.send_password_reset_otp(
            user.email,
            user.full_name,
            otp,
        )

    @staticmethod
    def verify_otp(
        db: Session,
        email: str,
        otp: str,
    ) -> bool:
        """
        Verify whether the supplied OTP is valid.
        """

        user = db.query(User).filter(User.email == email).first()

        if not user:
            return False

        # Get latest unused OTP
        reset_otp = (
            db.query(PasswordResetOTP)
            .filter(
                PasswordResetOTP.user_id == user.id,
                PasswordResetOTP.used == False,
            )
            .order_by(PasswordResetOTP.created_at.desc())
            .first()
        )

        if not reset_otp:
            return False

        # Check expiry
        if datetime.utcnow() > reset_otp.expires_at:
            reset_otp.used = True
            db.commit()
            return False

        # Check attempts
        if reset_otp.attempts >= PasswordResetService.MAX_ATTEMPTS:
            reset_otp.used = True
            db.commit()
            return False

        # Count this verification attempt
        reset_otp.attempts += 1

        # Hash submitted OTP
        submitted_hash = PasswordResetService._hash_otp(otp)

        # Compare hashes
        if submitted_hash != reset_otp.otp_hash:
            db.commit()
            return False

        db.commit()

        return True

    @staticmethod
    def reset_password(
        db: Session,
        email: str,
        otp: str,
        new_password: str,
    ) -> bool:
        """
        Verify OTP and reset the user's password.
        """

        user = db.query(User).filter(User.email == email).first()

        if not user:
            return False

        # Get latest unused OTP
        reset_otp = (
            db.query(PasswordResetOTP)
            .filter(
                PasswordResetOTP.user_id == user.id,
                PasswordResetOTP.used == False,
            )
            .order_by(PasswordResetOTP.created_at.desc())
            .first()
        )

        if not reset_otp:
            return False

        # Check expiry
        if datetime.utcnow() > reset_otp.expires_at:
            reset_otp.used = True
            db.commit()
            return False

        # Check attempts
        if reset_otp.attempts >= PasswordResetService.MAX_ATTEMPTS:
            reset_otp.used = True
            db.commit()
            return False

        # Count attempt
        reset_otp.attempts += 1

        # Compare OTP
        submitted_hash = PasswordResetService._hash_otp(otp)

        if submitted_hash != reset_otp.otp_hash:
            db.commit()
            return False

        # Update password
        user.hashed_password = hash_password(new_password)

        # Invalidate OTP
        reset_otp.used = True

        db.commit()

        return True