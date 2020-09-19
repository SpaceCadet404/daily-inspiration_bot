import requests
import schedule
import time
import telegram

def goodmorning():
    r = requests.get('https://inspirobot.me/api?generate=true')
    bot = telegram.Bot(token = 'TOKEN')
    bot.sendMessage(chat_id = 'CHAT_ID', text = f'Good morning!\n {r.text}')

schedule.every().day.at('04:20').do(goodmorning)

while True:
    schedule.run_pending()
    time.sleep(1)
