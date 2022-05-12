import random
import urllib.parse
import bs4
import requests
import telebot
from telebot import types
import SECRET
from io import BytesIO

import B_J
import BotGames
from menuBot import Menu

bot = telebot.TeleBot(SECRET.TGBot)  # Полуновский Максимилиан 1-МД-19
game21 = None
game_B_J = None
game_words = None

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
    global game_words
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

        elif ms_text == "Тянуть новую!" :
            if game_B_J == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return
            text_game = game_B_J.get_cards(1)
            bot.send_message(chat_id, text=text_game)

            if game_B_J.status != None:  # выход, если игра закончена
                goto_menu(chat_id, "Выход")
                return
        elif ms_text == "Пас!" :
            game_B_J = None
            goto_menu(chat_id, "Выход")
            return

        elif ms_text == "Цитату":  # .....................................................
            bot.send_message(chat_id, text=quotes())

        elif ms_text == "Начать" and game_words == None:  # .....................................................
            game_words = True
            print("Начали")
            # goto_menu(chat_id, "Закончить")
        elif ms_text == "Закончить":
            game_words = None
            goto_menu(chat_id, "Выход")

        elif ms_text == "Тян":  # .........................................................
            bot.send_message(chat_id, tyan())

        elif ms_text == "Угадай кто?":
            get_ManOrNot(chat_id)

        elif ms_text == "Связь":  # ..........................................................
            send_link(chat_id)

        elif ms_text == "Отключиться":  # .................................................................
            goto_menu(chat_id, "Пока :3 ")
        elif ms_text == "Вернуться":
            bot.send_message(chat_id, text="C Возвращением) ")
            goto_menu(chat_id, "Главное меню")

    else:  # ......................................................................................................
        if game_words != None:
            if ms_text[-1].upper() != ("Ь" or "Ъ" or "Ы"):
                a = ms_text[-1].upper()
            else:
                a = ms_text[-2].upper()
            bot.send_message(chat_id, text=WordGame(a))
            goto_menu(chat_id, "Закончить")
        else:
            bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
            goto_menu(chat_id, "Главное меню")

# -----------------------------------------------------------------------
def quotes():
    quotes = []
    avtor = []
    req_quo = requests.get("https://citaty.info/random")
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

# ----------------------------------------------------------------------
def WordGame(a):
    TheWorde = ""
    Word_precent = str(urllib.parse.quote(a))  # Преобр UTF-8 в %
    count_page = random.randint(1, 11)
    url = (f"https://slovopoisk.ru/type-1/begin-{Word_precent}?page={count_page}")  # Определенная стр. с буквой
    word_req = requests.get(url)
    soup = bs4.BeautifulSoup(word_req.text, "html.parser")
    print(url)
    strongs = str(((count_page - 1)*100) + random.randint(1, 100)) + "."  # Позиция слова на стр.
    print(strongs)
    Words_html = soup.find("span", class_="word-num", string=strongs)
    if Words_html != None:
        Words_html = Words_html.next_sibling  # Переход к слову
        if Words_html != None:
            for z in range(1, len(Words_html)):
                if Words_html[z].isalpha(): TheWorde += (Words_html[z])
        else:
            Words_html = Words_html.previous_sibling
            Words_html = Words_html.next_element
            print(Words_html)
    else:
        print(Words_html)
        TheWorde = "Я проиграл, покончи со мной..."
    return TheWorde

# я - 7 ю-3
# -----------------------------------------------------------------------
def get_ManOrNot(chat_id):
    global bot

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить", url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")

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
        if target_menu.name == "21":
            global game21

            game21 = BotGames.Game21()  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif target_menu.name == "Black Jack":
            global game_B_J
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
