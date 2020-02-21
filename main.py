from flask import Flask, request, abort
import os,random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def getImage() : 
    imageList = [
        "https://d1f5hsy4d47upe.cloudfront.net/f3/f36c375c339f1212cceb122fdb9d0808_t.jpeg",
        "https://i.pinimg.com/originals/e8/1d/22/e81d226c27de0167cd4da2682ddfbf16.jpg",
        "https://news.p-mom.net/wp-content/uploads/2018/02/9cfd8c4279f16b3c1fb732b2a205b0bc_t.jpeg",
        "https://d1f5hsy4d47upe.cloudfront.net/6a/6adb9b83ef9f5ebb117aa7e58c5aa761_t.jpeg",
        "https://lh3.googleusercontent.com/proxy/ZBMVLmouvPf7sNX7s8aNSsJpwB4bno_YBPuLZ0rGKbraBguULWpxdhymAytqLkR9-P42Pud8YBvxmGBNNjSi38EL5mI",
        "https://d1f5hsy4d47upe.cloudfront.net/d8/d88c9e6b728d8d84c41aa57269baf85d_t.jpeg",
        "https://www.pakutaso.com/shared/img/thumb/tom190303AISD_TP_V1.jpg",
        "https://d2dcan0armyq93.cloudfront.net/photo/odai/600/e91c5dd8898fe1b30373c6e26779e845_600.jpg",
        "https://lacrima.jp/wordpress/wp-content/uploads/2017/09/kawaii_neko_free.jpg",
        "https://pictkan.com/uploads/cache/4062436776/cat-590684_1920-400x270-MM-100.jpg",
        "https://xn--n8jx07hl4dx2oy5n.net/wp-content/uploads/2016/07/cat.jpg",
        "https://cdn.plus.amanaimages.com/uploads/items/000/486/62/preview/FYI00048662.jpg",
        "https://farm4.static.flickr.com/3644/3648450139_644bbfb746.jpg",
        "https://lh3.googleusercontent.com/proxy/4lC7J1h8hdzT6d12HFO7iEmsELW5o4xt2y0Q9dblmzqsPwYIkOHSptDiEHR-lrjG9Km1vkBgU4TYHn1vIfUi5XgB1CuelO15p6ol0G2k11qzOZJsObB0G84bsk8JiBhsf2PuUbcfuSqguD-kMCrJLzBxSg",
        
    ]
    rand = int(random.uniform(0, 15))
    return imageList[3]

@app.route("/")
def hello_world():
    return "Hello!! world!"

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
    text = event.message.text
    
    # 画像
    imgUrl = getImage()
    imgMessages = ImageSendMessage(imgUrl, imgUrl)
        
    checkNya = False
    checkNyaList = ["にゃ", "猫", "ねこ", "NEKO", "neko", "まただび", "キャット", "きゃっと", "肉球", "にくきゅう", "かわいい"]
    
    for chk in checkNyaList :
        if chk in text : 
            checkNya = True

    if checkNya :
        line_bot_api.reply_message(
            event.reply_token,
            imgMessages)
    else : 
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("猫に関するメッセージを送ると画像を送ってくれます！"))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
