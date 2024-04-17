import os
from flask import Flask, request, jsonify
from ultrabot import ultraChatBot
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return "<h1>Hello, World!</h1>"
    if request.method == 'POST':
        bot = ultraChatBot(request.json)
        return bot.Processingـincomingـmessages()


if (__name__) == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
