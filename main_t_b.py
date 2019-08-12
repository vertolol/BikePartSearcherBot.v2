
import logging

from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)

from spiders.spiders_launcher import run_spiders
from static_data import category_tree, examples_part_name, stores
from TOKEN import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSE_STORES, CHOOSE_CATEGORY, GET_RESULT = range(3)
selected = '🔳 '
not_selected = '⬜️️ '
stores_for_select = dict(zip([selected + store for store in stores.stores], stores.stores))
stores_for_select.update({'done': str(CHOOSE_CATEGORY)})
LAST_SIBLING = '_last_sibling'


def get_keyboard_from_dictionary(dictionary, columns=2):
    buttons = [InlineKeyboardButton(key, callback_data=value) for key, value in dictionary.items()]
    keyboard = []
    for index in range(0, len(buttons), columns):
        keyboard.append(buttons[index:index + columns])

    return keyboard


def get_keyboard_of_selection(data, keyboard):
    buttons = []
    for row in keyboard:
        new_row = []

        for button in row:
            if data in button.text:
                if selected in button.text:
                    button.text = button.text.replace(selected, not_selected)
                else:
                    button.text = button.text.replace(not_selected, selected)

            new_row.append(button)
        buttons.append(new_row)

    return buttons


def get_stores_for_search(keyboard):
    stores_list = []
    for row in keyboard:
        for button in row:
            if selected in button.text:
                stores_list.append(button.text.replace(selected, ''))
    return stores_list


def get_category_choice_dict(data):
    if data == str(CHOOSE_CATEGORY):
        category_choice_dict = category_tree.category_for_select
    else:
        category_choice_dict = category_tree.all_categories[data]

    for i in category_choice_dict:
        if category_choice_dict[i] not in category_tree.all_categories:
            category_choice_dict[i] += LAST_SIBLING

    return category_choice_dict


store_choice_reply_keyboard = get_keyboard_from_dictionary(stores_for_select)


def start(bot, update, user_data):
    query = update

    reply_markup = InlineKeyboardMarkup(store_choice_reply_keyboard)
    user_data['stores_for_search'] = get_stores_for_search(store_choice_reply_keyboard)

    bot.send_message(
        chat_id=query.message.chat_id,
        text=u"Выбор магазинов для поиска",
        reply_markup=reply_markup
    )

    return CHOOSE_STORES


def store_choice(bot, update, user_data):
    query = update.callback_query

    data = update.callback_query.data
    updated_keyboard = get_keyboard_of_selection(data, store_choice_reply_keyboard)
    reply_markup = InlineKeyboardMarkup(updated_keyboard)
    user_data['stores_for_search'] = get_stores_for_search(updated_keyboard)

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup,
    )

    return CHOOSE_STORES


def category_choice(bot, update, user_data):
    query = update.callback_query

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=u"Выбор категории"
    )

    data = query.data
    category_choice_dict = get_category_choice_dict(data)
    category_choice_reply_keyboard = get_keyboard_from_dictionary(category_choice_dict)
    reply_markup = InlineKeyboardMarkup(category_choice_reply_keyboard)

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup,
    )

    return CHOOSE_CATEGORY


def inputting_part_name(bot, update, user_data):
    query = update.callback_query
    user_data['category'] = query.data.replace(LAST_SIBLING, '')
    examples = "\n".join(examples_part_name.examples[user_data['category']])

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=f'''Ведите название детали. \nНапример: \n{examples}'''
    )

    return GET_RESULT


def get_result(bot, update, user_data):
    query = update

    stores_for_search = user_data['stores_for_search']
    category = user_data['category']
    part_name = query.message.text
    user_data.clear()

    bot.send_chat_action(
        chat_id=update.message.chat_id,
        action=ChatAction.TYPING)

    results = run_spiders(stores_for_search, category, part_name)

    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        parse_mode='HTML',
        disable_web_page_preview=True,
        text=f"results <b>{part_name}</b>:\n {results}"
    )

    return ConversationHandler.END


def conversation_error(bot, update, user_data):
    query = update

    user_data.clear()

    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Ошибка, попробуйте еще раз /start"
    )

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    REQUEST_KWARGS = {
        'proxy_url': 'https://144.217.161.149:8080',
    }
    updater = Updater(token=TOKEN, request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],

        states={
            CHOOSE_STORES: [CallbackQueryHandler(category_choice,
                                                 pattern=str(CHOOSE_CATEGORY),
                                                 pass_user_data=True),
                            CallbackQueryHandler(store_choice,
                                                 pass_user_data=True)],

            CHOOSE_CATEGORY: [CallbackQueryHandler(inputting_part_name,
                                                   pattern=f'^(.*{LAST_SIBLING})$',
                                                   pass_user_data=True),
                              CallbackQueryHandler(category_choice,
                                                   pass_user_data=True),
                              ],
            GET_RESULT: [MessageHandler(Filters.text,
                                        get_result,
                                        pass_user_data=True)]
        },

        fallbacks=[MessageHandler(Filters.text, conversation_error, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
