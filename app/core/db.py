from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

raw_url = settings.DATABASE_URL

# 1. Handle driver prefix
if raw_url.startswith("postgresql://"):
    raw_url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# 2. Parse URL and clean up query params
parsed = urlparse(raw_url)
query = parse_qs(parsed.query)

# Detect SSL requirement before stripping
ssl_required = "require" in query.get("sslmode", []) or "sslmode=require" in raw_url

# Strip problematic params for asyncpg
query.pop("sslmode", None)
query.pop("channel_binding", None) # Also not supported by asyncpg

# Reconstruct URL
new_query = urlencode(query, doseq=True)
clean_url = urlunparse(parsed._replace(query=new_query))

# 3. Configure Engine
connect_args = {}
if ssl_required:
    connect_args["ssl"] = True

engine = create_async_engine(
    clean_url, 
    echo=False,
    connect_args=connect_args
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
