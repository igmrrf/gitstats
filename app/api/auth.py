import httpx
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..core.db import get_db
from ..core.security import encrypt_token
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()
oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    client_kwargs={"scope": "user:email repo"},
)


@router.get("/login")
async def login(request: Request):
    return await oauth.github.authorize_redirect(request, settings.GITHUB_CALLBACK_URL)


@router.get("/callback")
async def callback(request: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.github.authorize_access_token(request)
    access_token = token.get("access_token")

    # Fetch user info from GitHub
    async with httpx.AsyncClient() as client:
        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"},
        )
        user_data = user_resp.json()

        email_resp = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"token {access_token}"},
        )
        emails = email_resp.json()
        primary_email = next(
            (e["email"] for e in emails if e["primary"]), user_data.get("email")
        )

    # Check if user exists
    result = await db.execute(
        select(User).where(User.github_id == str(user_data["id"]))
    )
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            github_id=str(user_data["id"]),
            username=user_data["login"],
            email=primary_email,
            full_name=user_data.get("name"),
            avatar_url=user_data.get("avatar_url"),
            access_token=encrypt_token(access_token),
        )
        db.add(user)
    else:
        user.access_token = encrypt_token(access_token)

    await db.commit()
    await db.refresh(user)

    # Issue session
    request.session["user"] = user.username

    return RedirectResponse(url="/dashboard")


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")
