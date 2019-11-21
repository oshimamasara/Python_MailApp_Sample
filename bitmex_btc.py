# testmail4.py 連続メール防止措置、 メールしたら一旦お休み 1時間
# sendgrid setup    https://app.sendgrid.com/guide/integrate/langs/python

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import requests
import json
import datetime
from pytz import timezone
import time

sended = 0

def send_mail():
    global message, sended_time, sended

    message = Mail(
        from_email='oshimamasara@yahoo.co.jp',
        to_emails='oshimamasara@gmail.com',
        subject='MyBotからのお知らせ　変動率: ' + str(percent),
        html_content='本文なし')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        sended_time = str(now_time.minute)
        sended = sended + 1
    except Exception as e:
        print(e.message)


def btc_data():
    global symbol,percent, price_now

    response = requests.get("https://www.bitmex.com/api/v1/instrument")
    data = json.loads(response.text)

    symbol = data[88]["symbol"]
    percent = data[88]["lastChangePcnt"]
    price_now = data[88]["midPrice"]

    if percent < -0.003 or percent > 0.003:
        if sended > 0 :
            #print("ifif___")
            #print(type(minute))
            #print(type(sended_time))
            if minute == sended_time:
                print("送信したばっか...")
            else:
                send_mail()
        else:
            send_mail()
            #print("else___")
            #print(sended_time)
    else:
        pass


def print_data():
    global minute
    btc_data()
    month = str(now_time.month)
    day = str(now_time.day)
    hour = str(now_time.hour)
    minute = str(now_time.minute)
    print("TIME: " + month + "月" + day + "日 " + hour + "時" + minute + "分")
    print(symbol + " : "+ str(price_now))
    print("変動率: " + repr(percent))



i = 0
sleep_time = 10

while True:
    try:
        print("\n チェックスタート " + str(i) + "回目")
        now_time = datetime.datetime.now(timezone('Asia/Tokyo'))
        print_data()
        print("メール送信回数:::  " + str(sended))
        time.sleep(sleep_time)
        i = i + 1

    except:
        print("チェックエラー")
        time.sleep(sleep_time)
        i = i + 1

