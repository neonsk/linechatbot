from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os
import requests
import pprint
import pya3rt
import scraper_ainow

app=Flask(__name__)
#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN="+1wc60N4p4u3ZAR26GRHfK/B+scc4cp4QPxQhV2dWe3ngWTDaj7lq9BZtvH8tPCbrheywXkdf+uvPNrGUYQIRfnAzcpWW53hYlatwBWwhd/gAxzGo2NspesMQFTb8V5buWvAResxWYCLAZPq+vpBJgdB04t89/1O/w1cDnyilFU="
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

    #=========返答タイプの設定==========================
    #天気APIにより応答
    #reply_text = weatherapi_response(push_text)
    
    #A3RTのTalkAPIにより応答
    # reply_text = talkapi_response(push_text)

    # 記事を取得し返答
    scraping = scraper_ainow.ScrapingAinow()
    article_urls, article_titles = scraping.execute
    #===================================
    
    #リプライ部分の記述
    for num in article_urls:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=article_titles[0]))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=article_urls[0]))


#天気APIにより応答
def weatherapi_response(push_text):
    if push_text == "天気":
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=130010'
        api_data = requests.get(url).json()
        for weather in api_data['forecasts']:
            weather_date = weather['dateLabel']
            weather_forecasts = weather['telop']
            print(weather_date + ':' + weather_forecasts)
        return api_data["description"]["text"]
    else:
        return push_text

#A3RTのTalkAPIにより応答
def talkapi_response(text):
    apikey = "DZZTN8HTduABGoAd8GPaM3QCvapddGU7"
    client = pya3rt.TalkClient(apikey)
    response = client.talk(text)
    return ((response['results'])[0])['reply']

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)