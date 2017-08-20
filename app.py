from flask import Flask, request
import antolib
from linebot import (
    LineBotApi, WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError,
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

line_bot_api = LineBotApi('Q9mBh6gIvVPV0WwarYpIJgX2KgaSB8+EVOLQs0ArwbV70v/wy9TSRiDqE5tdWMVBu9f5Hfkhg1IQZo7t75pihBIfiXhf7VSfm4yPB3MzQisRg4pUVXUYgU5ZHhDQP3IoB4Lcw1XntAz8k2Y22GGjCgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2955a4a0afede99d8681691bbfea167f')

app = Flask(__name__)

# username of anto.io account
user = 'Thepwarut'
# key of permission, generated on control panel anto.io
key = 'g6WxzaZHiL344vzOljd6yXN2k0VtC6sJlxhUfsiY'
# your default thing.
thing = 'NodeMCU'

anto = antolib.Anto(user, key, thing)


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text="Turn Off channel1"))

if __name__ == "__main__":
    anto.mqtt.connect()
    app.run(debug=True)
