from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..core.security import (
    User,
    Token,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
    check_permissions
)
from typing import List

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# Mock user database - in production, this would be a real database
users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "disabled": False,
        "roles": ["admin"]
    }
}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = User(**user_dict)
    
    # Generate tokens
    access_token = create_access_token(
        data={"sub": user.username, "roles": user.roles}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "roles": user.roles}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/protected")
async def protected_route(current_user: User = Depends(check_permissions(["admin"]))):
    return {"message": "You have access to this protected route", "user": current_user.username}

@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    # Generate new tokens
    access_token = create_access_token(
        data={"sub": current_user.username, "roles": current_user.roles}
    )
    refresh_token = create_refresh_token(
        data={"sub": current_user.username, "roles": current_user.roles}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
