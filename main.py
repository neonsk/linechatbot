from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os

app=Flask(__name__)
#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN="I3b9vUudKz15p7HrL4p/sWYdAUXY4gumr8WM+FGZq62vG84OFdSdfr00K94xvuybrheywXkdf+uvPNrGUYQIRfnAzcpWW53hYlatwBWwhd9b5ryUP7cf4OYYDXzra6Jl/geCFvRarChtKuyqVZgavwdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET="3474fdbe051be518b0d716f4f4c936be"
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="なおに会いたい"))#event.message.text))

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)