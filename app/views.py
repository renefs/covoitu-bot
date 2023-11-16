from flask import Response, request
import requests
from app import app, logger, bot_token
from os import environ

from app.bot_actions import (
    get_add,
    get_clear,
    get_help,
    get_kill,
    get_remove,
    get_set,
    get_show,
)


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return "<h1>Welcome, your server is running!</h1>"


@app.route("/", methods=["POST"])
def post_example():
    if request.method == "POST":
        # Access POST data from the request
        msg = request.get_json()
        should_respond = False

        # Trying to parse message
        try:
            logger.debug("Text received")
            chat_id = msg["message"]["chat"]["id"]

            if chat_id != int(environ.get("CHAT_ID")):
                logger.warning(f"Chat id {chat_id} is not allowed")
                return Response("not ok", status=400)

            text = msg["message"]["text"]  # This gets the text from the msg

            username = msg["message"]["from"]["username"]
            user_id = msg["message"]["from"]["id"]
            user_first_name = msg["message"]["from"]["first_name"]

            logger.debug(f"Message received: {text} from chat {chat_id}")
            logger.debug(f"User: {username} ({user_id}): {user_first_name} - {text}")

            if text == "/add":
                payload = get_add(chat_id, username, user_id, user_first_name)
                should_respond = True

            if text == "/remove":
                payload = get_remove(chat_id, username, user_id, user_first_name)
                should_respond = True

            if text == "/show":
                payload = get_show(chat_id)
                should_respond = True

            if text.startswith("/kill"):
                payload = get_kill(chat_id, text)
                should_respond = True

            if text.startswith("/set"):
                payload = get_set(chat_id, text)
                should_respond = True

            if text.startswith("/clear"):
                payload = get_clear(chat_id, text)
                should_respond = True

            if text == "/help":
                payload = get_help(chat_id)
                should_respond = True

            if should_respond:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                # Calling the telegram API to reply the message

                r = requests.post(url, json=payload)

                if r.status_code == 200:
                    return Response("ok", status=200)
                else:
                    logger.error("Failed to send message to Telegram")
                    return Response("Failed to send message to Telegram", status=500)
        except Exception as ex:
            logger.error(ex, exc_info=True)

        return Response("ok", status=200)
