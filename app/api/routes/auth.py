from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token,
)
from app.schemas.password_reset import (
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest,
    GoogleLoginRequest,
)
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.services.password_reset_service import PasswordResetService

from app.services.google_auth_service import GoogleAuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):

    try:
        created_user = AuthService.register_user(
            db,
            user,
        )

        # Send the welcome email after the HTTP response is prepared
        # so SMTP latency does not block account creation.
        background_tasks.add_task(
            EmailService.send_welcome_email,
            created_user.email,
            created_user.full_name,
        )

        return created_user

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    try:
        return AuthService.login_user(
            db,
            form_data.username,
            form_data.password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )

@router.post(
    "/forgot-password",
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a password-reset OTP and send it to the user's email.
    """

    PasswordResetService.request_otp(
        db,
        request.email,
    )

    # Always return the same response.
    # This prevents revealing whether an email is registered.
    return {
        "message": "If an account exists with this email, "
                   "a password reset OTP has been sent."
    }

@router.post(
    "/verify-otp",
)
def verify_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db),
):
    """
    Verify the OTP supplied by the user.
    """

    is_valid = PasswordResetService.verify_otp(
        db,
        request.email,
        request.otp,
    )

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP.",
        )

    return {
        "message": "OTP verified successfully."
    }

@router.post(
    "/reset-password",
)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Verify the OTP and reset the user's password.
    """

    success = PasswordResetService.reset_password(
        db,
        request.email,
        request.otp,
        request.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP.",
        )

    return {
        "message": "Password reset successfully."
    }

@router.post("/google", response_model=Token)
def google_login(
    request: GoogleLoginRequest,
    db: Session = Depends(get_db),
):
    try:
        return GoogleAuthService.login_with_google(
            db,
            request.credential,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )