import redis.asyncio as redis
from .config import settings

# Use a connection pool to avoid "max number of clients reached" errors
pool = redis.ConnectionPool.from_url(
    settings.REDIS_URL, 
    decode_responses=False,
    max_connections=10,
    retry_on_timeout=True,
    health_check_interval=30
)
redis_client = redis.Redis(
    connection_pool=pool,
    socket_timeout=5.0,
    socket_connect_timeout=5.0
)

async def get_redis():
    yield redis_client
