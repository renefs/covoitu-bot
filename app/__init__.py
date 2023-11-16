import logging
from flask import Flask
from dotenv import load_dotenv
from os import environ
from flask_cors import CORS
import redis

load_dotenv()

app = Flask(__name__)
CORS(app)

# Access environment variables
bot_token = environ.get("BOT_TOKEN")
bot_user_name = environ.get("BOT_USERNAME")

if environ.get("DEBUG", "false"):
    logging_level = logging.INFO
else:
    logging_level = logging.DEBUG

logging.basicConfig(
    level=logging_level,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s | %(filename)s:%(lineno)d",
)

logger = logging.getLogger(__name__)

redis_connection = redis.Redis(
    host=environ.get("REDIS_HOST"),
    port=environ.get("REDIS_PORT"),
    password=environ.get("REDIS_PASSWORD"),
    db=0,
)

from .views import *
