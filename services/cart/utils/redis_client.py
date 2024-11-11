from redis import Redis
from ..config import Config

redis_client = Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT
)
