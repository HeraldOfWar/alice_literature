import json
import os

with open(os.path)


def dialog_handler(event: dict, response: dict) -> dict:
    """Основной обработчик запросов пользователя и ответов сервера, принимает на вход request и возвращает response"""
    if not event['state']['user']:
        return start_handler(response)


def start_handler(response: dict) -> dict:
    return response