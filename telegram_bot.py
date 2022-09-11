from telegram.ext import Updater, CommandHandler
import logging
import requests
from bs4 import BeautifulSoup
import os, sys

# environment variables
bot_token = os.environ.get('BOT_TOKEN')
reply_banned = "I don't like you, "

# bot setup
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# assign admins
try:
    admins_file = open('admins.txt','r')
    admins = admins_file.read().split('\n')
    admins_file.close()
# Creates file if missing
except OSError:
    admins_file = open('admins.txt','w+')
    admins = admins_file.read().split('\n')
    admins_file.close()
    print("Created admins.txt")

# assign banlist
try:
    banlist_file = open('banlist.txt','r')
    banlist = banlist_file.read().split('\n')
    banlist_file.close()
# Creates file if missing
except OSError:
    banlist_file = open('banlist.txt','w+')
    banlist = banlist_file.read().split('\n')
    banlist_file.close()
    print("Created banlist.txt")


# Writes data in list to file
def list_write(data, file):
    with open(file,'w') as active_file:
        for line in data:
            active_file.write(f'{line}\n')
        active_file.close()


# Standard reply. Easier to type this way.
def reply(update, context, message):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def verified(user):
    return user in admins

def banned(user):
    return user in banlist


# Refuse user's command because they are on banlist
def deny(update, context):
        user = update.message.from_user.username
        if user not in banlist:
            banlist.append(update.message.from_user.username)
            list_write(banlist, 'banlist.txt')
            reply(update, context, f'{user} is not an admin.\n{user} added to banlist.')
        else:
            reply(update, context, f"{reply_banned}{user}")


# ----- Moderation tools -----

# Adds user specified in message to banlist. If requester is not admin, adds requester to banlist.
def ban(update, context):
    if verified(update.message.from_user.username) and not banned(update.message.from_user.username):
        if update.message.text.split()[1] not in banlist:
            banlist.append(update.message.text.split()[1])
            list_write(banlist, 'banlist.txt')
            reply(update, context, f"{banlist[-1]} added to banlist.")
        else:
            reply(update, context, f"Error: {update.message.text.split()[1]} is already on banlist!")
    else:
        deny(update, context)

# Removes user specified in message from banlist. If requester is not admin, adds requester to banlist.
def unban(update, context):
    if verified(update.message.from_user.username) and not banned(update.message.from_user.username):
        if update.message.text.split()[1] in banlist:
            banlist.remove(update.message.text.split()[1])
            list_write(banlist, 'banlist.txt')
            reply(update, context, f'{update.message.text.split()[1]} has been unbanned.')
        else:
            reply(update, context, f'Error: {update.message.text.split()[1]} is not currently banned!')
    else:
        deny(update, context)

def op(update, context):
    if verified(update.message.from_user.username) and not banned(update.message.from_user.username):
        if update.message.text.split()[1] not in admins:
            admins.append(update.message.text.split()[1])
            list_write(admins, 'admins.txt')
            reply(update, context, f'{admins[-1]} has been granted admin rights.')
        else:
            reply(update, context, f'Error: {update.message.text.split()[1]} is already an admin!')
    else:
        deny(update, context)

def deop(update,context):
    if verified(update.message.from_user.username) and not banned(update.message.from_user.username):
        if update.message.text.split()[1] in admins:
            admins.remove(update.message.text.split()[1])
            list_write(admins, 'admins.txt')
            reply(update, context, f'{update.message.text.split()[1]} admin rights revoked.')
        else:
            reply(update, context, f'Error: {update.message.text.split()[1]} is not an admin!')
    else:
        deny(update, context)


# ----- Fun things -----

def hello(update, context):
    reply(update, context, "HELLO WORLD. I AM INSPIRATION DELIVERY BOT.")


def inspire(update, context):
    if banned(update.message.from_user.username):
        deny(update, context)
    else:
        r = requests.get('https://inspirobot.me/api?generate=true')
        reply(update, context, r.text)


def insult(update, context):
    if banned(update.message.from_user.username):
        deny(update, context)
    else:
        r = requests.get('https://generatorfun.com/code/model/generatorcontent.php?recordtable=generator&recordkey=3&gen=Y&itemnumber=1&randomoption=undefined&genimage=No&nsfw=No&keyword=undefined&tone=Normal')
        soup = BeautifulSoup(r.content, 'html.parser')
        text = soup.find_all('p')[0].get_text()
        reply(update, context, text)


start_handler = CommandHandler('hello', hello)
inspire_handler = CommandHandler('inspire', inspire)
insult_handler = CommandHandler('insult', insult)
ban_handler = CommandHandler('ban', ban)
unban_handler = CommandHandler('unban', unban)
op_handler = CommandHandler('op', op)
deop_handler = CommandHandler('deop', deop)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(inspire_handler)
dispatcher.add_handler(insult_handler)
dispatcher.add_handler(ban_handler)
dispatcher.add_handler(unban_handler)
dispatcher.add_handler(op_handler)
dispatcher.add_handler(deop_handler)

# running
updater.start_polling()
