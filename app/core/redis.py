import redis

from app.core.config import config

client = redis.Redis(
    host=config.redis_host,
    port=config.redis_port,
    decode_responses=True # returns str instead of bytes
)