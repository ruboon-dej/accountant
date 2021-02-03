from flask import Flask, request, abort
from flask_caching import Cache

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from user import User

cache = Cache()
app = Flask(__name__)

cache_servers = os.environ.get('MEMCACHIER_SERVERS')
cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
cache.init_app(app,
    config={'CACHE_TYPE': 'saslmemcached',
            'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
            'CACHE_MEMCACHED_USERNAME': cache_user,
            'CACHE_MEMCACHED_PASSWORD': cache_pass,
            'CACHE_OPTIONS': { 'behaviors': {
                # Faster IO
                'tcp_nodelay': True,
                # Keep connection alive
                'tcp_keepalive': True,
                # Timeout for set/get requests
                'connect_timeout': 2000, # ms
                'send_timeout': 750 * 1000, # us
                'receive_timeout': 750 * 1000, # us
                '_poll_timeout': 2000, # ms
                # Better failover
                'ketama': True,
                'remove_failed': 1,
                'retry_timeout': 2,
                'dead_timeout': 30}}})

line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id

    user = cache.get(user_id)
    if user is None:
        user = User()
        cache.set(user_id, user)

    text = user.get_response(event.message.text)
    cache.set(user_id, user)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))


if __name__ == "__main__":
    app.run()