from flask import Flask
from dotenv import load_dotenv
from os import environ
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Access environment variables
bot_token = environ.get("BOT_TOKEN")
bot_user_name = environ.get("BOT_USERNAME")

from .views import *
