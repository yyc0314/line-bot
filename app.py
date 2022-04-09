# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第一章 Line Bot申請與串接
Line Bot機器人串接與測試
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        confirm_template_message = TemplateSendMessage(
            alt_text='舞蹈00',
            template=ConfirmTemplate(
                text='大學想要選什麼科系?',
                actions=[
                    MessageAction(
                        label='a',
                        text='a：舞蹈藝術相關科系'
                    ),
                    MessageAction(
                        label='b',
                        text='b：非藝術相關科系(例：醫學、電機)'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, confirm_template_message)

#def handle_message(event):
#    message = text=event.message.text
  #  if re.match('告訴我秘密',message):
#        line_bot_api.reply_message(event.reply_token, "（就讀舞蹈藝術相關科系後，學習了大量舞蹈的專業知識，也陸陸續續參加了很多表演）\n（大學生活的美好時光過得飛快......）\n\n友：欸欸啊啊啊你看！我之前去徵選的舞團上了！！比賽也過了！可是我英文很爛欸怎麼辦啦，要去國外很恐怖。\n你：別擔心啦，你能力那麼好，一定可以的！")
#        line_bot_api.reply_message(event.reply_token,"（大學畢業前，同學一些從小學舞、長得好看、底子又好的去了國外的專業舞團）\n（那......接下來畢業後我要去哪呢？啊......想繼續跳舞但是我真的有能力讓自己在舞者這塊發光發熱嗎？）")
#        confirm_template_message = TemplateSendMessage(
#            alt_text='舞蹈1a',
#            template=ConfirmTemplate(
#                text='大學想要選什麼科系?',
#                actions=[
#                    MessageAction(
#                        label='a',
#                        text='a：從事專業舞者'
#                    ),
#                    MessageAction(
#                        label='b',
#                        text='b：轉換跑道，成為一位上班時間固定的上班族'
#                    )
#                ]
#            )
#        )
#        line_bot_api.reply_message(event.reply_token, confirm_template_message)
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)