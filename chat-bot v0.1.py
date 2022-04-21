import random

import bs4
import requests
import telebot
from telebot import types

import B_J
import BotGames
from menuBot import Menu

bot = telebot.TeleBot('5107250105:AAGmEXjY-JZIEO9lJPToN2M4GI_ikwmU9Z0') # Полуновский Максимилиан 1-МД-19
game21 = None
game_B_J = None

# /start
@bot.message_handler(commands="start")
def command(message, res=False):
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(message.chat.id, text=txt_message, reply_markup=Menu.getMenu("Главное меню").markup)
# -----



# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global game21
    global game_B_J
    chat_id = message.chat.id
    ms_text = message.text

    result = goto_menu(chat_id, ms_text)
    if result == True:
        return

    if Menu.cur_menu != None and ms_text in Menu.cur_menu.buttons:

        if ms_text == "🤚":
            c = ["🤚", "✌ ️", "✊"]
            random.shuffle(c)
            if c[0] == "✌ ️":
                answer = "Я победил, а ты нет))"
            elif c[0] == "✊":
                answer = "Я проиграл(("
            else:
                answer = "Ничья. Тебе просто повезло."
            bot.send_message(chat_id, text=f"    {c[0]}\n...{answer}")
            goto_menu(chat_id, "Игры")
        elif ms_text == "✌ ️":
            c = ["🤚", "✌ ️", "✊"]
            random.shuffle(c)
            if c[0] == "✊":
                answer = "Я победил, а ты нет))"
            elif c[0] == "🤚":
                answer = "Я проиграл(("
            else:
                answer = "Ничья. Тебе просто повезло."
            bot.send_message(chat_id, text=f"    {c[0]}\n...{answer}")
            goto_menu(chat_id, "Игры")
        elif ms_text == "✊":
            c = ["🤚", "✌ ️", "✊"]
            random.shuffle(c)
            if c[0] == "🤚":
                answer = "Я победил, а ты нет))"
            elif c[0] == "✌ ️":
                answer = "Я проиграл(("
            else:
                answer = "Ничья. Тебе просто повезло."
            bot.send_message(chat_id, text=f"    {c[0]}\n...{answer}")
            goto_menu(chat_id, "Игры")

        elif ms_text == "Карту!" :
            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                goto_menu(chat_id, "Выход")
                return
        elif ms_text == "Стоп!" :
            game21 = None
            goto_menu(chat_id, "Выход")
            return

        elif ms_text == "Цитату":  # .....................................................
            bot.send_message(chat_id, text=quotes())

        elif ms_text == "Тян" or ms_text == "Ещё тян":  # .........................................................
            bot.send_message(chat_id, tyan())

        elif ms_text == "WEB-камера":  # ..............................................................................
            bot.send_message(chat_id, text="еще не готово...")
            goto_menu(chat_id, "Главное меню")

        elif ms_text == "Связь":  # ..........................................................
            send_link(chat_id)

        elif ms_text == "Отключиться":  # .................................................................
            goto_menu(chat_id, "Пока :3 ")
        elif ms_text == "Вернуться":
            bot.send_message(chat_id, text="C Возвращением) ")
            goto_menu(chat_id, "Главное меню")
        else:  # ......................................................................................................
            bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
            goto_menu(chat_id, "Главное меню")

# -----------------------------------------------------------------------
def quotes():
    quotes = []
    avtor = []
    req_quo = requests.get("https://citaty.info/random",)
    soup = bs4.BeautifulSoup(req_quo.text, "html.parser")
    res = soup.find_all(class_='field-item even last')
    avt = soup.find_all(class_="field-item even")
    for res4 in res:
        quotes.append(res4.getText().strip())
    for avt4 in avt:
        avtor.append(avt4.getText())
    quotes = quotes[0]
    wh = ""
    try:
        for i in range(0, len(avtor)):
            if wh == "":
                wh += avtor[i]
            elif avtor[i] == avtor[i].lower():
                break
            else:
                wh += ", " + avtor[i]
        avtors = "\n\n" + wh
    except IndexError:
        avtors = ''
    quotes = '" '+quotes.replace("\xa0", " ")+' "' + avtors
    return quotes


# -----------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    if name_menu == "Выход" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            global game21
            game21 = BotGames.Game21()  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif target_menu.name == "Игра в Black Jack":
            game_B_J = B_J.Game_B_J()  # создаём новый экземпляр игры
            text_game = game_B_J.get_cards(2)  # просим 2 карты в начале игры
            bot.send_message(chat_id, text=text_game)
        return True

    else:
        return False


# -----------------------------------------------------------------------
def tyan():
    req = requests.get("http://randomwaifu.altervista.org/")
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    img = soup.find(class_="center-fit")
    img = "http://randomwaifu.altervista.org/" + img["src"]
    return img


# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias

#  ----------------------------------------------------------------------
def send_link(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Полуновский Максимилиан")
    key1 = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/mBumblebee")
    key1.add(btn1)
    img = open('ddd.png', 'rb')
    bot.send_photo(chat_id, img, reply_markup=key1)

# ----------------------------------------------------------------------

bot.polling(none_stop=True, interval=0)
print()
