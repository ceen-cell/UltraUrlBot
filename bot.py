import os
from telebot import TeleBot
from keyboards import Keyboards
from url_component import UrlService, QRCodeMaker
from bot_messages import greeting, commands, nxt_step_msg
from databaser import Users

# getting the key from the environment variables
bot = TeleBot(os.environ["api_key"]) 
url_service = UrlService()
database = Users(os.environ['db_name'], os.environ['db_pass'], 'users')


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id, 
        text=greeting, 
        reply_markup=Keyboards.contact_keyboard()
    )
    # Send bot commands to user.
    bot.send_message(message.chat.id, commands)
    database.add_user(message.chat.username, message.chat.id)


""""
Below are the new ways of shortening and expanding the URLS
These just require the user to use the command /s {URL here} 
when shortening a URL and /e {URL here when expanding a URL}
The old method required two separate functions, one to handle the command and the other to
handle the shortening or expanding feature.
Currently, these two methods will be used at the same time, so that the user can adapt to the new way.
"""


@bot.message_handler(commands=['s'])
def shorten_url(message):
    bot.send_chat_action(message.chat.id, 'typing')
    # Replaces the /s with nothing which leaves only the URL
    url = message.text.replace('/s', '').strip()
    new_url = url_service.shorten_url(url)  # returns Shortened URL
    bot.send_message(
        message.chat.id, new_url, disable_web_page_preview=True
    )
    bot.send_message(1425477245, "New method used // Sortener") 

@bot.message_handler(commands=['e'])
def expand(message):
    """Expand the url that was sent by the user
    The message arrives in the form /e {url}. As such the command (/e)
    is being stripped from the message text to leave only thr url that
    was sent.
    """
    bot.send_chat_action(message.chat.id, 'typing')
    url = message.text.replace('/e', '').strip() 
    expanded_url = url_service.expand_url(url)
    bot.send_message(
        message.chat.id, 
        expanded_url,
        disable_web_page_preview=True,
    )
# The new methods end here.


# Support for the old method
@bot.message_handler(commands=['shorten'])
def handle_command(message):
    bot.send_chat_action(message.chat.id, 'typing')
    msg_to_user = bot.send_message(message.chat.id, nxt_step_msg+'shorten')
    bot.register_next_step_handler(msg_to_user, short_url)


def short_url(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id, 
        url_service.shorten_url(message.text), 
        disable_web_page_preview=True
    )
    bot.send_message(1425477245, "old method used")


@bot.message_handler(commands=['expand'])
def handle_unshorten(message):
    bot.send_chat_action(message.chat.id, 'typing')
    msg_to_user = bot.send_message(message.chat.id, nxt_step_msg+'expand')
    bot.register_next_step_handler(msg_to_user, expand_url)


def expand_url(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id, 
        url_service.expand_url(message.text), 
        disable_web_page_preview=True
    )


# Sending message to users function starts here.
@bot.message_handler(commands=['update'])
def check_user(message):
    # Check whether I'm the user sending this command
    # otherwise send a 404 message to the person trying to access this command
    if message.chat.id == 1425477245: 
        msg = bot.send_message(message.chat.id, 'Go on')
        bot.register_next_step_handler(msg, send_messages)
    else:
        bot.reply_to(message, '404 Error')


def send_messages(message):
    update_info = message.text # This represents the message i want to send to the users
    for user in database.get_chat_id_of_all_users():
        try:
            bot.send_message(user, update_info, parse_mode='Markdown')
        except:
            # if the user cannot be reached, delete the user from the database
            database.delete_user(user) 


# QRCode generator function
@bot.message_handler(func=lambda x: True)  # Accepts all input forms
def create_qr(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    qr_maker = QRCodeMaker(version=8)
    qr_maker.create_qr(message.text)
    bot.send_photo(
        message.chat.id, photo=open(QRCodeMaker.file_name, 'rb')
    )
    qr_maker.delete_qr()
    bot.send_message(1425477245, "Qr generated")

bot.polling(non_stop=True)
