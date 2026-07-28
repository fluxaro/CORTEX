"""Authentication & User service."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.security.password import hash_password, verify_password
from app.models.enterprise import User, UserPreference
from app.schemas.enterprise import UserLoginRequest, UserRegisterRequest


class AuthService:
    """Service handling User registration, login, and JWT tokens."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_user(self, req: UserRegisterRequest) -> tuple[User, str, str]:
        """Register new user account."""
        stmt = select(User).where(User.email == req.email)
        res = await self.session.execute(stmt)
        existing = res.scalars().first()
        if existing:
            raise ValueError(f"User with email '{req.email}' already exists.")

        user = User(
            email=req.email,
            hashed_password=hash_password(req.password),
            full_name=req.full_name,
            role="DEVELOPER",
            is_active=True,
            is_verified=False,
        )
        self.session.add(user)
        await self.session.flush()

        pref = UserPreference(user_id=user.id)
        self.session.add(pref)
        await self.session.commit()
        await self.session.refresh(user)

        access_token = create_access_token(
            {"sub": user.id, "email": user.email, "role": user.role}
        )
        refresh_token = create_refresh_token({"sub": user.id})
        return user, access_token, refresh_token

    async def authenticate_user(self, req: UserLoginRequest) -> tuple[User, str, str]:
        """Authenticate user with email and password."""
        stmt = select(User).where(User.email == req.email)
        res = await self.session.execute(stmt)
        user = res.scalars().first()

        if not user or not verify_password(req.password, user.hashed_password):
            raise ValueError("Invalid email or password.")

        if not user.is_active:
            raise PermissionError("User account is deactivated.")

        access_token = create_access_token(
            {"sub": user.id, "email": user.email, "role": user.role}
        )
        refresh_token = create_refresh_token({"sub": user.id})
        return user, access_token, refresh_token

    async def refresh_tokens(self, refresh_token: str) -> tuple[str, str]:
        """Generate new access/refresh token pair from valid refresh token."""
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type for refresh.")

        user_id = payload.get("sub")
        stmt = select(User).where(User.id == user_id)
        res = await self.session.execute(stmt)
        user = res.scalars().first()

        if not user or not user.is_active:
            raise ValueError("User not found or inactive.")

        new_access = create_access_token(
            {"sub": user.id, "email": user.email, "role": user.role}
        )
        new_refresh = create_refresh_token({"sub": user.id})
        return new_access, new_refresh

    async def get_user_by_id(self, user_id: str) -> User | None:
        """Retrieve user by ID."""
        stmt = select(User).where(User.id == user_id)
        res = await self.session.execute(stmt)
        return res.scalars().first()
