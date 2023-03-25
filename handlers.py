import json
import os

with open(os.path.join('data', 'questions.json')) as file:
    book_n_questions = json.load(file)
all_questions = [for question in book_n_questions[book] for book in book_n_questions.keys()]



def dialog_handler(event: dict, response: dict) -> dict:
    """Основной обработчик запросов пользователя и ответов сервера, принимает на вход request и возвращает response"""
    if not event['state']['user']:
        return start_handler(response)


def start_handler(response: dict) -> dict:
    return response