import logging
import os
import random


from logging.handlers import RotatingFileHandler
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup


from dotenv import load_dotenv


load_dotenv()

token = os.getenv('TOKEN')

MULTIPLICATION = {
    '2*2': 4, '3*2': 6, '3*3': 9, '4*2': 8, '4*3': 12, '4*4': 16,
    '5*2': 10, '5*3': 15, '5*4': 20, '5*5': 25, '6*2': 12, '6*3': 18,
    '6*4': 24, '6*5': 30, '6*6': 36, '7*2': 14, '7*3': 21, '7*4': 28,
    '7*5': 35, '7*6': 42, '7*7': 49, '8*2': 16, '8*3': 24, '8*4': 32,
    '8*5': 40, '8*6': 48, '8*7': 56, '8*8': 64, '9*2': 18, '9*3': 27,
    '9*4': 36, '9*5': 45, '9*6': 54, '9*7': 63, '9*8': 72, '9*9': 81
}

REACTION_FALSE = [
    'Неправильно! Попробуйте еще раз',
    'Ну, конечно нет!',
    'Ай-ай-ай! Ответ неверный',
    'Нет'
]
REACTION_TRUE = [
    'Правильно!',
    'Молодец!',
    'Так держать!',
    'Ну ладно. Угадал',
    'На этот раз зассчитано. Так уж и быть',
    'Где ответы подсматриваешь? '
]

REACTION_REPEAT = [
    'Еще раз: сколько будет ', 'Так сколько будет ',
    'Ну и? ', 'Может уже вспомнил? '
]

MESSAGE_ERROR = ('Что-то пошло не так :( '
                 'Попробуйте начать все сначала или приходите позже, '
                 'когда меня починят. '
                 'Для начала работы наберите /start. '
                 'Если надоело учить таблицу умножения наберите /stop.')
questions = {}

handler = logging.FileHandler(filename='main.log', encoding='utf-8')
logging.basicConfig(
    handlers=(handler,),
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'my_logger.log',
    maxBytes=50000000,
    backupCount=5
)
logger.addHandler(handler)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


def generate_question(update, context):
    try:
        chat = update.effective_chat
        name = update.message.chat.first_name
        questions[chat.id] = random.choice(list(MULTIPLICATION.keys()))
        logger.info(f'{chat.id}: {questions[chat.id]}')
        context.bot.send_message(
                chat_id=chat.id,
                text='{}, cколько будет {}?'.format(name, questions[chat.id]),
        )
    except Exception as error:
        context.bot.send_message(chat.id, MESSAGE_ERROR)
        log_message = f'Сбой в работе программы: {error}'
        logger.error(log_message)


def wake_up(update, context):
    try:
        chat = update.effective_chat
        name = update.message.chat.first_name
        button = ReplyKeyboardMarkup([['/stop']], resize_keyboard=True)
        message = (f'Привет! {name} Я бот, '
                   f'который поможет тебе выучить таблицу умножения. '
                   f'Я сварганен на скорую руку, поэтому ломаюсь, '
                   f'когда получаю неподходящие команды. '
                   f'Если вы сделали что-то не так, '
                   f'могу немного нагрубить, но не сильно. '
                   f'Для начала работы наберите /start. '
                   f'Если надоело учить таблицу умножения наберите /stop.')
        context.bot.send_message(
                chat_id=chat.id,
                text=message,
                reply_markup=button
        )
        generate_question(update, context)
    except Exception as error:
        context.bot.send_message(chat.id, MESSAGE_ERROR)
        log_message = f'Сбой в работе программы: {error}'
        logger.error(log_message)


def stop_questions(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)
    message = ('Все-все. Уже отстал. '
               'Если захотите еще потренироваться, наберите /start')
    context.bot.send_message(
            chat_id=chat.id,
            text=message,
            reply_markup=button
    )
    del questions[chat.id]


def check_answer(update, context):
    global questions
    try:
        chat = update.effective_chat
        info = update.message.text
        if chat.id not in questions:
            message = 'Включи меня. Я не активен. Набери /start'
            context.bot.send_message(chat.id, message)
        else:
            if info.isdigit():
                if update.message.text == str(
                    MULTIPLICATION[questions[chat.id]]
                ):
                    message = random.choice(REACTION_TRUE)
                    context.bot.send_message(chat.id, message)
                    generate_question(update, context)
                else:
                    message1 = random.choice(REACTION_FALSE)
                    message2 = (f'{random.choice(REACTION_REPEAT)}'
                                f'{questions[chat.id]}?')
                    context.bot.send_message(chat.id, message1)
                    context.bot.send_message(chat.id, message2)
            elif info[-1] == '?':
                message = 'Ввопросы здесь задаю я, а вы - отвечаете.'
                context.bot.send_message(chat.id, message)
                context.bot.send_message(chat.id, questions[chat.id])
            elif len(info) > 10:
                message = ('Поболтаем как-нибудь в другой раз. '
                           'А сейчас главное - таблица умножения!')
                context.bot.send_message(chat.id, message)
                context.bot.send_message(chat.id, questions[chat.id])
            else:
                message = ('Введите только число!! '
                           'Я не понимаю ваш ответ, я немного туповат')
                context.bot.send_message(chat.id, message)
                context.bot.send_message(chat.id, questions[chat.id])
    except Exception as error:
        context.bot.send_message(chat.id, MESSAGE_ERROR)
        log_message = f'Сбой в работе программы: {error}'
        logger.error(log_message)


def main():
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('stop', stop_questions))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, check_answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
