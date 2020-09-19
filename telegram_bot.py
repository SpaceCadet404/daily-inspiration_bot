from telegram.ext import Updater, CommandHandler
import logging
import requests


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


start_handler = CommandHandler('hello', hello)
inspire_handler = CommandHandler('inspire', inspire)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(inspire_handler)

# running
updater.start_polling()
