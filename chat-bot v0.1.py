import telebot

bot = telebot.TeleBot('5107250105:AAGmEXjY-JZIEO9lJPToN2M4GI_ikwmU9Z0')

@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я тестовый бот для курса программирования на языке ПаЙтон".format(
                         message.from_user))

@bot.message_handler(commands=["text"])
def get_text_message(message):
    chat_id = message.chat.id
    ms_text = message.text
    bot.send_message(chat_id, text="Ага! сооб.:"+ ms_text)

bot.polling(none_stop=True, interval=0)
