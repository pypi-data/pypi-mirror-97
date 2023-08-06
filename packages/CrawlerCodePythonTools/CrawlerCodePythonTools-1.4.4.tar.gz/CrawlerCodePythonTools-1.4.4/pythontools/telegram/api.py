import requests

TELEGRAM_TOKEN = None
TELEGRAM_CHAT_ID = None

def setToken(TOKEN):
    global TELEGRAM_TOKEN
    TELEGRAM_TOKEN = TOKEN

def setChatID(CHAT_ID):
    global TELEGRAM_CHAT_ID
    TELEGRAM_CHAT_ID = CHAT_ID

def sendMessage(message, chat_id=None):
    global TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    requests.post('https://api.telegram.org/bot' + str(TELEGRAM_TOKEN) + '/sendMessage', data={'chat_id': chat_id if chat_id is not None else TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': "Markdown"})