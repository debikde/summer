import json
import random
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

class SpellingBee:
    def __init__(self, dictionary_path):
        with open(dictionary_path, "r", encoding="utf-8") as f:
            self.word_score_dict = json.load(f)
        self.letters = []
        self.main_letter = ''
        self.valid_words = {}
        self.used_words = set()
        self.score = 0

    def generate_letters(self):
        all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        while True:
            self.main_letter = random.choice(all_letters)
            other_letters = random.sample([l for l in all_letters if l != self.main_letter], 6)
            self.letters = [self.main_letter] + other_letters
            has_vowel = False
            for letter in self.letters:
                if letter in "AEIOUY":
                    has_vowel = True
                    break
            if has_vowel:
                break

    def filter_words(self):
        self.valid_words = {}
        allowed_letters = set(self.letters)
        for word, score in self.word_score_dict.items():
            word_upper = word.upper()
            if len(word_upper) < 4:
                continue
            if self.main_letter not in word_upper:
                continue
            if not all(c in allowed_letters for c in word_upper):
                continue
            if any(word_upper.count(c) > self.letters.count(c) for c in set(word_upper)):
                continue
            self.valid_words[word] = score

    def is_valid_word(self, word):
        word = word.lower()
        if len(word) < 4:
            return False, "Слишком короткое слово (меньше 4 букв)."
        if self.main_letter.lower() not in word:
            return False, "Слово не содержит главную букву."
        if word in self.used_words:
            return False, "Слово уже использовано."
        if word not in self.valid_words:
            return False, "Такого слова не существует или его пока нет в базе(("
        return True, ""

    def start_game(self):
        print("Привет! Добро пожаловать в игру со словами")
        self.generate_letters()
        print(f"Ваши буквы: {' '.join(self.letters)} (главная буква: {self.main_letter})")
        self.filter_words()
        print(f"Всего возможных слов: {len(self.valid_words)}")

        while True:
            user_word = input("Введите слово (или XXXXX для выхода): ").strip().lower()
            if user_word.upper() == "XXXXX":
                break
            if not user_word.isalpha():
                print("Ошибка: вводите только буквы.")
                continue
            valid, msg = self.is_valid_word(user_word)
            if not valid:
                print(f"Неверное слово: {msg}")
                continue
            score = self.valid_words[user_word]
            self.score += score
            self.used_words.add(user_word)
            print(f"Слово принято! Очки за слово: {score}. Текущий счёт: {self.score} \n Осталось найти слов: {len(self.valid_words) - len(self.used_words)}")
            if len(self.used_words) == len(self.valid_words):
                print("Поздравляем, все слова найдены!")
                break
        print(f"Игра окончена. Ваш итоговый счёт: {self.score}")
