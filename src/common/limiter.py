from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
import os
from .const import redis_url

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv(redis_url),
    default_limits=["200 per day", "50 per hour"],
)
