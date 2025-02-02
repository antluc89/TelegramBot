import telebot
from configuration import currency, TOKEN
from extensions import ConversionException, ValueConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_bot(message: telebot.types.Message):
    text = 'Чтобы запустить бота, введите команду в следующем формате: \n<название валюты, цену которой вы хотите узнать> \
<название валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты> \nУвидеть список всех доступных валют для конверсии: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in currency.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversionException('Неверное количество параметров. Введите три параметра')

        quote, base, amount = values
        total_base = ValueConverter.get_price(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Oшибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос:\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} составляет {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)


