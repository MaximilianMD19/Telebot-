import requests


# -----------------------------------------------------------------------
class Card:
    emo_SPADES = "U0002660"  # Unicod эмоджи Пики
    emo_CLUBS = "U0002663"  # Unicod эмоджи Крести
    emo_HEARTS = "U0002665"  # Unicod эмоджи Черви
    emo_DIAMONDS = "U0002666"  # Unicod эмоджи Буби

    def __init__(self, card):
        if isinstance(card, dict):  # если передали словарь
            self.__card_JSON = card
            self.code = card["code"]
            self.suit = card["suit"]
            self.value = card["value"]
            self.cost = self.get_cost_card()
            self.cost_enemy = self.get_cost_card_enemy()

        elif isinstance(card, str):  # карту передали строкой, в формате "2S"
            self.__card_JSON = None
            self.code = card

            value = card[0]
            if value == "J":
                self.value = "JACK"
            elif value == "Q":
                self.value = "QUEEN"
            elif value == "K":
                self.value = "KING"
            elif value == "A":
                self.value = "ACE"
            elif value == "J":
                self.value = "JACK"
            else:
                self.value = value

            suit = card[1]
            if suit == "S":
                self.suit = "♠️"  # Пики
            elif suit == "C":
                self.suit = "♣️"  # Крести
            elif suit == "H":
                self.suit = "♥️"  # Черви
            elif suit == "D":
                self.suit = "♦️"  # Буби

            self.cost = self.get_cost_card()
            self.cost_enemy = self.get_cost_card_enemy()

    def get_cost_card(self):
        if self.value == "JACK":
            return 2
        elif self.value == "QUEEN":
            return 3
        elif self.value == "KING":
            return 4
        elif self.value == "ACE":
            return 11
        elif self.value == "JOKER":
            return 1
        else:
            return int(self.value)

    def get_cost_card_enemy(self):
        if self.value == "JACK":
            return 3
        elif self.value == "QUEEN":
            return 2
        elif self.value == "KING":
            return 1
        elif self.value == "ACE":
            return 4
        elif self.value == "JOKER":
            return 1
        else:
            return (int(self.value)+1)


# -----------------------------------------------------------------------
class Game_B_J:
    def __init__(self, deck_count=1):
        new_pack = self.new_pack(deck_count)  # в конструкторе создаём новую пачку из deck_count-колод
        if new_pack is not None:
            self.pack_card = new_pack  # сформированная колода
            self.remaining = new_pack["remaining"],  # количество оставшихся карт в колоде
            self.card_in_game = []  # карты в игре
            self.arr_cards_URL = []  # URL карт игрока
            self.score = 0 # очки игрока
            self.enemy_score = 0  # очки уже не игрока
            self.status = None  # статус игры: True - Игра окончена, False - Игрок пасовал, None - Игра продолжается
            self.enemy_status = None # статус игры: True - Враг спасовал, None - Игра продолжается

    # ---------------------------------------------------------------------
    def new_pack(self, deck_count):
        response = requests.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={deck_count}")
        # создание стопки карт из "deck_count" колод по 52 карты
        if response.status_code != 200:
            return None
        pack_card = response.json()
        return pack_card

    # ---------------------------------------------------------------------
    def get_cards(self, card_count=1):
        if self.pack_card == None:
            return None
        if self.status != None:  # игра закончена
            return None

        deck_id = self.pack_card["deck_id"]
        response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={card_count}")
        # достать из deck_id-колоды card_count-карт
        if response.status_code != 200:
            return False
# ------------- PLAYER
        new_cards = response.json()
        if new_cards["success"] != True:
            return False
        self.remaining = new_cards["remaining"]  # обновим в классе количество оставшихся карт в колоде

        arr_newCards = []
        for card in new_cards["cards"]:
            card_obj = Card(card)  # создаем объекты класса Card и добавляем их в список карт у игрока
            arr_newCards.append(card_obj)
            self.card_in_game.append(card_obj)
            self.score = self.score + card_obj.cost

# -------------- BOT

        arr_en_newCards = []
        for card in new_cards["cards"]:
            card_obj = Card(card)  # создаем объекты класса Card и добавляем их в список карт у игрока
            arr_en_newCards.append(card_obj)
            self.card_in_game.append(card_obj)
            self.enemy_score = self.enemy_score + card_obj.cost_enemy
        if self.enemy_status == None:
            if self.enemy_score >= 17:
                self.enemy_status = True
            elif self.score > 21:
                self.enemy_status = True

# -------------  Result
        if self.score > 21 :
            if self.score > self.enemy_score:
                self.status = True
                text_game = "Ваши очки: " + str(self.score) + "\nОчки врага: " + str(self.enemy_score) + \
                            "\n\n ВЫ ПРОИГРАЛИ!"
            elif self.score < self.enemy_score:
                self.status = True
                text_game = "Ваши очки: " + str(self.score) + "\nОчки врага: " + str(self.enemy_score) + \
                            "\n\n ВЫ ВЫИГРАЛИ!"
            else:
                self.status = True
                text_game = "НиЧья"
        elif self.score == 21:
            if self.score != self.enemy_score:
                self.status = True
                text_game = "Ваши очки: " + str(self.score) + "\nОчки врага: " + str(self.enemy_score) + \
                            "\n\n ВЫ ВЫИГРАЛИ!"
            else:
                self.status = True
                text_game = "НиЧья"
        elif self.score < 21 and self.status == False:
            if self.score < self.enemy_score:
                self.status = True
                text_game = "Ваши очки: " + str(self.score) + "\nОчки врага: " + str(self.enemy_score) + \
                            "\n\n ВЫ ПРОИГРАЛИ!"
            elif self.score > self.enemy_score:
                text_game = "Ваши очки: " + str(self.score) + "\nОчки врага: " + str(self.enemy_score) + \
                            "\n\n ВЫ ВЫИГРАЛИ!"
                self.status = True
            else:
                self.status = True
                text_game = "НиЧья"
        else:
            self.status = None
            text_game = "Ваши очки: " + str(self.score) + "\nОчки врага: " + str(self.enemy_score) +\
                        "\n\nВ колоде осталось карт: " + str(self.remaining)

        return text_game


# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("Этот код должен использоваться ТОЛЬКО в качестве модуля!")
