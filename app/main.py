from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from .api import auth, views
from .core.config import settings
from .core.db import Base, engine
from .core.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Setup global HTTP client
    app.state.http_client = httpx.AsyncClient(timeout=30.0)
    yield
    # Cleanup
    await app.state.http_client.aclose()
    await redis_client.close()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Add session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Register routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(views.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
