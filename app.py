"""
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

"""
#載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from __future__ import unicode_literals
import os

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('zVkUr0O4yEQo3FyR7rCjOZkH/wHWG8e4tnRW6l3iU6kJ/fJxXQAveMeFYBugrIC4jz1dsvRRYIAa7c2LvTcOL9fbLwodHQl8xSKrj8gvOZ6U0rf1Db0TLEPlmFeZhC6PhElulVEWcbTbrzkg3Sj54AdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('ac5b69f52f6a568c4cb6b8c2db7a834b')

line_bot_api.push_message('U2b030a5933594945dc1ca06a78690cd6', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""

from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('zVkUr0O4yEQo3FyR7rCjOZkH/wHWG8e4tnRW6l3iU6kJ/fJxXQAveMeFYBugrIC4jz1dsvRRYIAa7c2LvTcOL9fbLwodHQl8xSKrj8gvOZ6U0rf1Db0TLEPlmFeZhC6PhElulVEWcbTbrzkg3Sj54AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ac5b69f52f6a568c4cb6b8c2db7a834b')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

if __name__ == "__main__":
    app.run()
