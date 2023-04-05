"""Телеграм бот для проверки курса валют @Shifty_Lickbot"""
# ~ We've got to have... MONEY

import telebot
from config import TOKEN
from extensions import *

bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    text = "Добро пожаловать в мой офис! \n" \
           "Я знаю цену деньгам и могу перевести одну валюту в любую другую\n" \
           "Это один из моих многочисленных талантов\n" \
           "\n" \
           "Чтобы узнать курс валют введите:\n" \
           "<валюта1> <валюта2> <количество>\n" \
           "валюта1 - из какой\n" \
           "валюта2 - в какую\n" \
           "количество - цифра валюта1 (если десятичная, то разделяйте точкой)\n" \
           "Например, чтобы перевести 5 долларов в евро:\n" \
           "доллар евро 5\n" \
           "\n" \
           "Доступные команды:\n" \
           "/help - подсказка\n" \
           "/values - какие валюты знает Ликбот"
    bot.send_message(message.chat.id, text)


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message: telebot.types.Message):
    text = "Чтобы узнать курс валют введите:\n" \
           "<валюта1> <валюта2> <количество>\n" \
           "валюта1 - из какой\n" \
           "валюта2 - в какую\n" \
           "количество - цифра валюта1 (если десятичная, то разделяйте точкой)\n" \
           "Например, чтобы перевести 5 долларов в евро:\n" \
           "доллар евро 5\n" \
           "\n" \
           "Доступные команды:\n" \
           "/help - подсказка\n" \
           "/values - какие валюты знает Ликбот"
    bot.send_message(message.chat.id, text)


# Обработчик команды /values
# Выводит список ключей из CURRENCY_DICT
@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    text = "Я могу работать с валютами:\n" + "\n".join(CURRENCY_DICT.keys())
    bot.send_message(message.chat.id, text)


# Обработчик текстового сообщения
@bot.message_handler(content_types=['text'])
def handle_message(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException("Сообщение должно состоять из трех слов")

        base, quote, amount = values
        converted_amount = Exchange.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f"{e}")
    except Exception as e:
        bot.reply_to(message, f"Что-то пошло не так, денежные духи мне шепчут:\n{e}")
    else:
        bot.reply_to(message, amount + f" {base} = {'%.2f' % converted_amount} {quote}")


bot.polling()
