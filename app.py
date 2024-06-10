from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    questions_answers = {
        "apple": "蘋果",
        "banana": "香蕉",
        "cat": "貓",
        "dog": "狗",
        "elephant": "大象",
        "flower": "花",
        "guitar": "吉他",
        "house": "房子",
        "ice": "冰",
        "tiger": "虎",
        "jacket": "夾克",
        "keyboard": "鍵盤",
        "lemon": "檸檬",
        "monkey": "猴子",
        "notebook": "筆記本",
        "orange": "橙子",
        "piano": "鋼琴",
        "queen": "女王",
        "rabbit": "兔子",
        "sun": "太陽",
        "tree": "樹",
        "umbrella": "雨傘",
        "violin": "小提琴",
        "whale": "鯨魚",
        "xylophone": "木琴",
        "yacht": "遊艇",
        "zebra": "斑馬",
        "bread": "麵包",
        "car": "車",
        "duck": "鴨子",
        "什麼是中央處理器 (CPU)？": "中央處理器 (CPU) 是電腦的主要運算單元，負責執行指令和處理數據。它是電腦的“腦”，能夠執行計算、邏輯運算和控制其他硬件元件。",
        "RAM 和 ROM 有什麼區別？": "答：RAM（隨機存取記憶體）是電腦的臨時存儲空間，用於存儲正在使用的數據和程式，電腦關機後數據會丟失。ROM（只讀記憶體）是永久存儲空間，用於存儲不會經常更改的數據和程式，如電腦的啟動程式，電腦關機後數據仍然保存。",
        "什麼是作業系統 (OS)？": "作業系統 (OS) 是管理電腦硬體和軟體資源的系統軟體，提供使用者與電腦互動的界面。常見的作業系統包括 Windows、macOS 和 Linux。",
        "硬碟 (HDD) 和固態硬碟 (SSD) 有什麼不同？": "硬碟 (HDD) 使用旋轉磁碟和讀寫磁頭來存儲數據，存取速度較慢但容量大。固態硬碟 (SSD) 使用快閃記憶體晶片來存儲數據，存取速度快但容量相對較小且價格較高。"
    }
    if msg in questions_answers:
        #print(f"{english_word} 的中文翻譯是：{words_dict[english_word]}")
    
        line_bot_api.reply_message(event.reply_token, TextSendMessage(questions_answers[msg]))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))
       
         

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
