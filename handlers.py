from os import path
from json import load
from typing import Any

with open(path.join('data', 'questions.json'), encoding='utf-8') as file:
    books_n_questions = load(file)
__all_questions = []
for book in books_n_questions.keys():
    for question in books_n_questions[book]:
        __all_questions.append(question)

with open(path.join('data', 'books.json'), encoding='utf-8') as file:
    books_descriptions = load(file)

with open(path.join('data', 'commands.json'), encoding='utf-8') as file:
    commands = load(file)

MISUNDERSTANDING = [
    "Прошу прощения, ответьте конкретнее.",
    "Я Вас совсем не понимаю. Пожалуйста, ответьте точнее.",
    "Простите, не расслышал. Повторите, пожалуйста.",
    "Ошибка! Ваш запрос оказался недостаточно полным. Попробуйте ещё раз.",
    "Даже не знаю, что сказать... Попробуйте ответить ещё раз.",
    "Если вам что-то непонятно, то скажите \"Меню\" или \"Помощь\"."
]
WRONGANS = [
    "Упс! Вы ответили неверно...",
    "Неверный ответ.",
    "Вы ошиблись.",
    "Не хотел я этого говорить, но Вы ошиблись.",
    "Ошибка!",
    "Как бы вам сказать, что Вы ошиблись..."
]
TRUEANS = ["Правильно!", "Верно!", "Абсолютно точно", "Ты молодец! Всё правильно", "Вы великолепны, правильно!"]


def dialog_handler(event: dict, context: Any) -> dict:
    """Основной обработчик запросов пользователя и ответов сервера, принимает на вход request и возвращает response"""

    res = {
        'session': event['session'],
        'version': event['version'],
        'response': {
            'end_session': False
        }
    }

    if not event['state']['user']:
        # собираем стейты для нового пользователя
        res['user_state_update'] = {
            'name': '',
            'mode': 'menu',
            'books': [],
            'questions': [],
            'points': 0,
            'station': False,
            'last_state': {'mode': 'start',
                           'books': [],
                           'questions': [],
                           'station': False},
            'last_response': {}
        }
        res['response']['text'] = commands['start']['text']
        res['response']['tts'] = commands['start']['tts']
        res['response']['buttons'] = commands['start']['buttons']
        res['response']['card'] = commands['start']['card']
        return res
    else:
        res['user_state_update'] = event['state']['user'].copy()

    mode = res['user_state_update']['mode']

    if 'YANDEX.HELP' in list(event['request']['nlu']['intents'].keys()):
        if mode == 'quiz' or mode == 'super_quiz' or mode == 'library':
            res = save_response(
                text=commands[mode]['text'],
                tts=commands[mode]['tts'],
                buttons=commands[mode]['buttons'],
                card=commands[mode]['card']
            )
        else:
            res = save_response(
                text=commands['help']['text'],
                tts=commands['help']['tts'],
                buttons=commands['help']['buttons'],
                card=commands['help']['card']
            )
        return res

    if 'YANDEX.WHAT_CAN_YOU_DO' in list(event['request']['nlu']['intents'].keys()):
        res = save_response(
            text=commands['help']['text'],
            tts=commands['help']['tts'],
            buttons=commands['help']['buttons'],
            card=commands['help']['card']
        )
        return res

    if 'YANDEX.REPEAT' in list(event['request']['nlu']['intents'].keys()):
        # если пользователь просит повторить сообщение
        repeat_handler(res)

    if mode in commands.keys():
        # если пользователь вызывает команду
        return commands_handler(event, res)

    raise Exception


def commands_handler(event: dict, res: dict) -> dict:
    mode = res['user_state_update']['mode']
    if res['user_state_update']['last_state']['mode'] == 'start':
        if event['request']['nlu']['entities'] and 'YANDEX.FIO' == event['request']['nlu']['entities'][0]['type']:
            res['user_state_update']['name'] = event['request']['nlu']['entities'][0]['value'][
                'first_name'].capitalize()
        else:
            res['response']['text'] = 'Пожалуйста, введите настоящее имя!'
            res['response']['tts'] = 'Пожалуйста, введите настоящее имя!'
            res['response']['buttons'] = []
            return res
    res['response']['text'] = commands[mode]['text']
    res['response']['tts'] = commands[mode]['tts']
    res['response']['buttons'] = commands[mode]['buttons']
    if commands[mode]['card']:
        res['response']['card'] = commands[mode]['card']
    res = save_state(res)
    return res


def repeat_handler(res: dict, data: dict = None):
    pass


def save_state(res: dict) -> dict:
    copy_res = res['user_state_update'].copy()
    res['user_state_update']['last_state'] = {
        'mode': copy_res['mode'],
        'books': copy_res['books'],
        'questions': copy_res['questions'],
        'station': copy_res['station']
    }
    return res


def save_response(res: dict, text: str, tts: str, buttons: list, card: dict = None) -> dict:
    res['response']['text'] = text
    res['response']['tts'] = tts
    res['response']['buttons'] = buttons
    if card:
        res['response']['card'] = card
    res['last_response'] = {
        'text': text,
        'tts': tts,
        'buttons': buttons,
        'card': card
    }
    return res