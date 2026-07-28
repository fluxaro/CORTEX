"""Authentication REST API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.oauth.providers import OAuthProviderFactory
from app.dependencies.db import get_db
from app.schemas.enterprise import (
    RefreshTokenRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
async def register(req: UserRegisterRequest, db: AsyncSession = Depends(get_db)) -> Any:
    """Register new user account."""
    service = AuthService(db)
    try:
        user, access, refresh = await service.register_user(req)
        return TokenResponse(access_token=access, refresh_token=refresh)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/login", response_model=TokenResponse)
async def login(req: UserLoginRequest, db: AsyncSession = Depends(get_db)) -> Any:
    """Authenticate user with email & password."""
    service = AuthService(db)
    try:
        user, access, refresh = await service.authenticate_user(req)
        return TokenResponse(access_token=access, refresh_token=refresh)
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=401, detail=str(e)) from e


@router.post("/refresh", response_model=TokenResponse)
async def refresh(req: RefreshTokenRequest, db: AsyncSession = Depends(get_db)) -> Any:
    """Refresh JWT access token."""
    service = AuthService(db)
    try:
        access, refresh_token = await service.refresh_tokens(req.refresh_token)
        return TokenResponse(access_token=access, refresh_token=refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e


@router.get("/oauth/{provider}")
async def get_oauth_url(provider: str, redirect_uri: str = Query(...)) -> Any:
    """Get OAuth authorization URL for GitHub, GitLab, or Bitbucket."""
    try:
        oauth = OAuthProviderFactory.get_provider(provider)
        url = oauth.get_authorization_url(redirect_uri, state="state-123")
        return {"authorization_url": url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/oauth/{provider}/callback", response_model=TokenResponse)
async def oauth_callback(
    provider: str,
    code: str = Query(...),
    redirect_uri: str = Query(...),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Handle OAuth callback exchange."""
    try:
        oauth = OAuthProviderFactory.get_provider(provider)
        user_info = await oauth.exchange_code_for_user(code, redirect_uri)
        service = AuthService(db)
        # Register or retrieve OAuth user
        reg_req = UserRegisterRequest(
            email=user_info["email"],
            password="OAuthGeneratedPassword123!",
            full_name=user_info["name"],
        )
        try:
            _, access, refresh_token = await service.register_user(reg_req)
        except ValueError:
            login_req = UserLoginRequest(
                email=user_info["email"], password="OAuthGeneratedPassword123!"
            )
            _, access, refresh_token = await service.authenticate_user(login_req)

        return TokenResponse(access_token=access, refresh_token=refresh_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
