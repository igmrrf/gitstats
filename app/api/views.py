from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..core.db import get_db
from ..models.user import User
from ..core.security import decrypt_token
from ..services.github import GitHubService
from ..services.ai import AIService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os

router = APIRouter(tags=["views"])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = request.session.get('user')
    return templates.TemplateResponse(
        request=request, name="index.html", context={
            "user": user, 
            "title": "Engineering High Fidelity",
            "repo_url": "https://github.com/igmrrf/gitstat-next"
        }
    )

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    username = request.session.get('user')
    if not username:
        return RedirectResponse(url="/?error=unauthorized")

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user:
        request.session.pop('user', None)
        return RedirectResponse(url="/?error=not_found")

    gh = GitHubService(decrypt_token(user.access_token), request.app.state.http_client)
    stats = await gh.get_user_stats()
    top_langs = await gh.get_top_languages()
    expertise = AIService.calculate_expertise_rating(top_langs)
    resume = await AIService.generate_resume(stats, top_langs, request.app.state.http_client)

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={
            "user": user.username,
            "stats": stats,
            "top_langs": top_langs,
            "expertise": expertise,
            "resume": resume,
            "title": f"{user.username}'s Dashboard"
        }
    )
