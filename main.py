from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os
import requests
import pprint

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
    #入力された文字列を格納
    push_text = event.message.text

    #リプライする文字列
    if push_text == "天気":
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=130010'
        api_data = requests.get(url).json()
        for weather in api_data['forecasts']:
            weather_date = weather['dateLabel']
            weather_forecasts = weather['telop']
            print(weather_date + ':' + weather_forecasts)
        reply_text = api_data["description"]["text"]
    else:
        reply_text = push_text

    #リプライ部分の記述
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text+"。でもなおに会いたいな"))

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)