from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
)
from app.services.auth_service import AuthService

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
    db: Session = Depends(get_db),
):

    try:
        return AuthService.register_user(
            db,
            user,
        )

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
    user: UserLogin,
    db: Session = Depends(get_db),
):

    try:
        return AuthService.login_user(
            db,
            user.email,
            user.password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )