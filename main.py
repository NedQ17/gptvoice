import speech_recognition as sr
from gtts import gTTS
import os
import requests
import json

# API-ключ ChatGPT
api_key = "your_api"


# Функция отправки запроса к API ChatGPT
def send_request(prompt):
    data = {
        "inputs": prompt,
        "parameters": {
            "model": "text-generation"
        },
        "options": {
            "use_cache": False,
            "wait_for_model": True
        }
    }
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.openai.com/v1/engines/davinci-codex/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["text"]

# Функция для генерации и воспроизведения речи
def generate_and_play_voice(text):
    # Синтез речи с помощью gTTS и сохранение в файл
    tts = gTTS(text=text, lang='ru')
    tts.save("output.mp3")

    # Воспроизведение синтезированной речи
    os.system("mpg321 output.mp3")

# Создание объекта Recognizer из библиотеки speech_recognition
r = sr.Recognizer()

# Определение устройства для записи звука
with sr.Microphone() as source:
    print("Говорите...")
    audio = r.listen(source)

    try:
        # Преобразование голосового ввода в текст
        text = r.recognize_google(audio, language='ru-RU')
        print("Вы сказали: ", text)

        # Отправка запроса к API ChatGPT
        response_text = send_request(text)

        # Генерация и воспроизведение синтезированной речи
        generate_and_play_voice(response_text)
    except sr.UnknownValueError:
        print("Речь не распознана")
    except sr.RequestError as e:
        print("Ошибка сервиса распознавания речи; {0}".format(e))
    except requests.exceptions.HTTPError as err:
        print(f"Ошибка HTTP: {err}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
