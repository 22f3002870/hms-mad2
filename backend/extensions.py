from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import redis

db = SQLAlchemy()

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


