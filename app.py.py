import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Приветствую! В этом чате вы можете получить информацию по конвертации валюты. \n"
                                      "Для этого необходимо ввести данные в формате: \n"
                                      "<имя валюты > <в какую валюту перевести> <количество валюты> \n"
                                      "Пример ввода данных:  Евро Рубль 100 \n"
                                      "Бот выдаст информацию о переводе 100 Евро в Рубли по текущему курсу \n"
                                      "Доступную валюту для конвертации можно узнать с помощью '/values'")
    pass

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
    pass

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введите три параметра, где первое исходная валюта, второе валюта в которую переводим, третье количество переводимой валюты')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка.\n{e}')
    except Exception as e:
        bot.reply_to(f'Не удалось выполнить команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)