from telegram.ext import Updater, CommandHandler
import logging
import requests
from bs4 import BeautifulSoup


updater = Updater(token='TOKEN', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


# define commands
def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I AM INSPIRATION DELIVERY BOT.")

def inspire(update, context):
    r = requests.get('https://inspirobot.me/api?generate=true')
    context.bot.send_message(chat_id=update.effective_chat.id, text=r.text)

def insult(update, context):
    r = requests.get('https://generatorfun.com/code/model/generatorcontent.php?recordtable=generator&recordkey=3&gen=Y&itemnumber=1&randomoption=undefined&genimage=No&nsfw=No&keyword=undefined&tone=Normal')
    soup = BeautifulSoup(r.content, 'html.parser')
    reply = soup.find_all('p')[0].get_text()
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)


start_handler = CommandHandler('hello', hello)
inspire_handler = CommandHandler('inspire', inspire)
insult_handler = CommandHandler('insult', insult)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(inspire_handler)
dispatcher.add_handler(insult_handler)

# running
updater.start_polling()
