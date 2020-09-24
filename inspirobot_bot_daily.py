import requests
import schedule
import time
import telegram
import os

def goodmorning():
    r = requests.get('https://inspirobot.me/api?generate=true')
    bot = telegram.Bot(token=os.environ.get('ROOMID'))
    bot.sendMessage(chat_id =os.environ.get('BOT_TOKEN'), text = f'Good morning!\n {r.text}')

schedule.every().day.at('04:20').do(goodmorning)

while True:
    schedule.run_pending()
    time.sleep(1)
