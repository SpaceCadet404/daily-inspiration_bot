import requests
import schedule
import time
import telegram
import os

botID = os.environ.get('BOT_TOKEN')
bot = telegram.Bot(token=botID)

roomID = os.environ.get('ROOMID')

def goodmorning():
    r = requests.get('https://inspirobot.me/api?generate=true')
    bot.sendMessage(chat_id=roomID, text = f'Good morning!\n {r.text}')

def flushot():
    bot.sendMessage(chat_id=roomID, text="Have you received your flu shot?\
    \n\nFind a location near you: https://vaccinefinder.org/find-vaccine\
    \n\nHave questions or concerns about the flu vaccine? Find more information here: https://www.cdc.gov/flu/season/faq-flu-season-2020-2021.htm")


schedule.every().day.at('04:20').do(goodmorning)
schedule.every().day.at('12:00').do(flushot)

while True:
    schedule.run_pending()
    time.sleep(1)
