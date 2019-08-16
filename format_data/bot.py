import logging

from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def help_(bot, update):
    query = update

    bot.send_photo(
        chat_id=query.message.chat_id,
        photo = open('out.jpg', 'rb'),
        caption=''' 1. 155.46€ SRAM X01 Type 2.1 11-speed Rear Derailleur 
2. 159.62€ SRAM X01 Type 2.1 Rear Derailleur 11-speed long black 
3. 168.06€ SRAM X01 Type 2.1 X-HORIZON Rear Derailleur 11-speed - Red '''
    )


def error_logging(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    TOKEN = '858272646:AAFZzfQabY7BeLU7nm-bIJcn3N2bKdGRyhg'
    request_kwargs = {
        'proxy_url': 'https://144.217.161.149:8080',
    }
    updater = Updater(token=TOKEN, request_kwargs=request_kwargs)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help_))
    dp.add_error_handler(error_logging)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()