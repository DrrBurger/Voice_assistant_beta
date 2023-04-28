import datetime
import random
import time
import webbrowser as wb

import playsound
import speech_recognition as sr
import wikipedia
from gtts import gTTS


def listen_command():
    """Слушает команду через микрофон и распознает её"""

    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        r.adjust_for_ambient_noise(source)
        print("Скажите вашу команду: ")
        audio = r.listen(source)

    # Распознает речь используя Google Speech Recognition
    try:
        our_speech = r.recognize_google(audio, language="ru-RU").lower()
        print("Вы сказали: " + our_speech)
        return our_speech
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError:
        return "ошибка"


def do_this_command(command):
    """Выполняет команду принятую через микрофон"""
    global commands_dict
    for k, v in commands_dict.items():
        if command in v:
            k()


def greeting():
    """Приветствует пользователя при запуске помощника в зависимости от времени"""

    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        say_message("Доброе утро сэр, я ваш голосовой ассистент чем могу помочь?")

    elif 12 <= hour < 18:
        say_message("Добрый день сэр, я ваш голосовой ассистент чем могу помочь?")

    else:
        say_message("Добрый вечер сэр, я ваш голосовой ассистент, чем могу помочь?")


def wiki_search():
    """Поиск по википедии"""
    say_message("Что ищем?")
    query = listen_command()
    wikipedia.set_lang('ru')
    query = query.replace("википедия", "")
    results = wikipedia.summary(query, sentences=2)
    say_message("Согласно википедии")
    print(results)
    say_message(results)


def google_search():  # решить проблему с символами / кодировкой
    """Поиск гугл"""
    say_message("Что ищем?")
    query = listen_command()
    wb.open('https://www.google.com/search?q=' + query)


def open_website():  # решить проблему с символами / кодировкой
    say_message('Какой сайт открыть?')
    query = listen_command()
    wb.open(f"https://www.{query}.com")


def current_time():
    str_time = datetime.datetime.now().strftime("%H:%M:%S")
    say_message(f"Сейчас {str_time} Сэр!")


def unknown_command():
    say_message("Не известная команда")


def goodbye():
    """Выключает прослушивание микрофона в фоне"""
    say_message("Хорошего дня, сэр!")
    exit()


def say_message(message):
    """Записывает сообщение в мр3 файл и воспроизводит его"""

    voice = gTTS(message, lang="ru", slow=False)
    file_voice_name = "_audio_" + str(time.time()) + "_" + str(random.randint(0, 100000)) + ".mp3"
    voice.save(file_voice_name)
    playsound.playsound(file_voice_name)
    print("Голосовой ассистент: " + message)


def create_task():
    """Создает заметку"""

    say_message("Что добавим в список дел?")
    query = listen_command()
    with open("todo_list.txt", "a") as file:
        file.write(f'! {query}\n\n')
    print(f'Задача "{query}" добавлена в todo_list!')


commands_dict = {create_task: ["заметка", "создать заметку", "запиши заметку", "запиши"],
                 greeting: ["привет", "салют", "хай", "здарова"],
                 wiki_search: ["найди в вики", "поищи в вики", "вики", "wiki", 'википедия'],
                 google_search: ["загугли", "чекни в гугл", "поиск гугл", "google"],
                 open_website: ["открой страницу", "открой", "open", "открой веб-сайт", "сайт"],
                 current_time: ["время", "скажи время", "время сейчас", "сколько время", "который час"],
                 goodbye: ["пока", "покеда", "вырубай", "досвидос"]
                 }

if __name__ == '__main__':
    while True:
        command = listen_command()
        do_this_command(command)
