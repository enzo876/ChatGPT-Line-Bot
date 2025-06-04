import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 將 LINE 的憑證寫入環境變數或直接填入
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 允許回覆的使用者 ID 清單
ALLOWED_USERS = {
    'Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  # 範例 userId，可替換成自己的
}

app = Flask(__name__)

@app.route('/callback', methods=['POST'])
def callback():
    """接收並處理 LINE Webhook"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    """處理文字訊息"""
    user_id = event.source.user_id
    if user_id in ALLOWED_USERS:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='哈囉，特定朋友！')
        )
    # 不在清單中則不回覆

# 主動推播訊息的範例
# push_message('Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', '這是一則主動推播訊息')

def push_message(user_id: str, text: str):
    """推送文字訊息給指定的 userId"""
    line_bot_api.push_message(user_id, TextSendMessage(text=text))

if __name__ == '__main__':
    app.run(port=8080)
