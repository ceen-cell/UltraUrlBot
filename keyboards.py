"""This contains all the keyboards that will be displayed by the
bot to the user.
Includes the following:
-> Contact Developer Keyboard
Further keyboards will be added later.
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Keyboards:
    @staticmethod
    def contact_keyboard(text:str = "Contact Him Here", url:str = 'https://t.me/a_moaba'):
        board = InlineKeyboardMarkup(row_width=1)
        board.add(InlineKeyboardButton(text, url=url))
        return board