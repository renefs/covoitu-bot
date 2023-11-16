from flask import request
from app import app


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return "<h1>Welcome your server is running!</h1>"
