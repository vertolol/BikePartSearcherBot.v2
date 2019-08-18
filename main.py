import logging

from format_data import to_caption, to_image
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)

from spiders.spiders_launcher import run_spiders
from static_data import categories, examples_part_name, stores
from TOKEN import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSE_STORES, CHOOSE_CATEGORY, GET_RESULT = range(3)
SELECTED = '🔳 '
NOT_SELECTED = '⬜️️ '
stores_for_select = dict(zip([SELECTED + store for store in stores.stores], stores.stores))
stores_for_select.update({'done': str(CHOOSE_CATEGORY)})
LAST_SIBLING = '_last_sibling'


def get_keyboard_from_dictionary(dictionary: dict, columns=2) -> list:
    """Преобразовывает словарь в список кнопок.
    :param dictionary: принимает словарь, keys - текст кнопки, values - callback data
    :param columns: определяет количество колонок клавиатуры (Default value = 2)
    :returns: список объектов кнопок(InlineKeyboardButton)
    """
    buttons = [InlineKeyboardButton(key, callback_data=value) for key, value in dictionary.items()]
    keyboard = []
    for index in range(0, len(buttons), columns):
        keyboard.append(buttons[index:index + columns])

    return keyboard


def get_keyboard_of_selection(data: str, keyboard: list) -> list:
    """Изменяет текст кнопки.
    :param data: callback data кнопки, текст которой нужно изменить
    :param keyboard: список кнопок(InlineKeyboardButton) клавиатуры, в которой нужно изменить текст кнопки
    :returns: список объектов кнопок(InlineKeyboardButton)
    """
    buttons = []
    for row in keyboard:
        new_row = []

        for button in row:
            if data in button.callback_data:
                if SELECTED in button.text:
                    button.text = button.text.replace(SELECTED, NOT_SELECTED)
                else:
                    button.text = button.text.replace(NOT_SELECTED, SELECTED)

            new_row.append(button)
        buttons.append(new_row)

    return buttons


def get_stores_for_search(keyboard: list) -> list:
    """Возвращает список выбранных кнопок.
    :param keyboard: список кнопок(InlineKeyboardButton) клавиатуры
    :returns: список с текстами кнопок.
    """
    stores_list = []
    for row in keyboard:
        for button in row:
            if SELECTED in button.text:
                stores_list.append(button.text.replace(SELECTED, ''))
    return stores_list


def get_category_choice_dict(data: str) -> dict:
    """Возвращает словарь с категориями.
    Первый вызов, когда data = CHOOSE_CATEGORY, корневой словарь категорий
    Следующие вызовы возвращают категории ниже по дереву
    Если текущий узел не имеет потомков, к ключу добавляется постфикс LAST_SIBLING
    :param data: callback data кнопки
    :returns: словарь категорий для преобразования в клавиатуру
    """
    if data == str(CHOOSE_CATEGORY):
        category_choice_dict = categories.category_for_select
    else:
        category_choice_dict = categories.categories_with_siblings[data]

    for key in category_choice_dict:
        if category_choice_dict[key] not in categories.categories_with_siblings:
            category_choice_dict[key] += LAST_SIBLING

    return category_choice_dict


def start(bot, update, user_data):
    query = update

    user_data['store_choice_keyboard'] = get_keyboard_from_dictionary(stores_for_select)
    user_data['stores_for_search'] = get_stores_for_search(user_data['store_choice_keyboard'])
    reply_markup = InlineKeyboardMarkup(user_data['store_choice_keyboard'])

    bot.send_message(
        chat_id=query.message.chat_id,
        text=u"Выберете магазины, в которых нужно найти деталь.",
        reply_markup=reply_markup
    )

    return CHOOSE_STORES


def store_choice(bot, update, user_data):
    query = update.callback_query

    data = update.callback_query.data
    updated_keyboard = get_keyboard_of_selection(data, user_data['store_choice_keyboard'])
    reply_markup = InlineKeyboardMarkup(updated_keyboard)
    user_data['stores_for_search'] = get_stores_for_search(updated_keyboard)

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup,
    )

    return CHOOSE_STORES


def category_choice(bot, update):
    query = update.callback_query

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=u"Выберете категорию."
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
        text=f'''И ведите название детали. \nНапример: \n{examples}'''
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

    if results:
        res_size = 3

        for index in range(0, len(results), res_size):
            res_for_format = results[index:index+res_size]

            caption = to_caption.get_caption(res_for_format, index+1)
            merge_image = to_image.get_merge_image(res_for_format, index+1)

            bot.send_photo(
                chat_id=query.message.chat_id,
                photo=open(merge_image, 'rb'),
                caption=caption,
                parse_mode = 'HTML'
            )
    else:
        text = 'К сожалению я ничего не нашел. '
        'Если хотите попробовать снова, просто нажмите /start'

        bot.send_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            disable_web_page_preview=True,
            text=text
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


def help_(bot, update):
    query = update

    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Бот для поиска запчастей для велосипеда, '
        'с сортировкой по цене. '
        'В процессе поиска можно выбрать сайты '
        'по которым будет произведен поиск. '
        'Далее выбирается категория для поиска, и ввод названия детали. '
        'Что бы начать нажмите /start'
    )


def error_logging(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    request_kwargs = {
        'proxy_url': 'https://186.103.175.158:3128',
    }
    updater = Updater(token=TOKEN, request_kwargs=request_kwargs)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],

        states={
            CHOOSE_STORES: [CallbackQueryHandler(category_choice,
                                                 pattern=str(CHOOSE_CATEGORY),
                                                 ),
                            CallbackQueryHandler(store_choice,
                                                 pass_user_data=True)],

            CHOOSE_CATEGORY: [CallbackQueryHandler(inputting_part_name,
                                                   pattern=f'^(.*{LAST_SIBLING})$',
                                                   pass_user_data=True),
                              CallbackQueryHandler(category_choice,
                                                   ),
                              ],
            GET_RESULT: [MessageHandler(Filters.text,
                                        get_result,
                                        pass_user_data=True)]
        },

        fallbacks=[MessageHandler(Filters.text, conversation_error, pass_user_data=True)]
    )

    dp.add_handler(CommandHandler("help", help_))
    dp.add_handler(conv_handler)
    dp.add_error_handler(error_logging)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
