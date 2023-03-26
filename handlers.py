from os import path
from json import load

with open(path.join('data', 'questions.json'), encoding='utf-8') as file:
    books_n_questions = load(file)
__all_questions = []
for book in books_n_questions.keys():
    for question in books_n_questions[book]:
        __all_questions.append(question)

with open(path.join('data', 'books.json'), encoding='utf-8') as file:
    books_descriptions = load(file)

with open(path.join('data', 'commands.json'), encoding='utf-8') as file:
    start = load(file)

with open(path.join('data', 'commands.json'), encoding='utf-8') as file:
    commands = load(file)

MISUNDERSTANDING = [
    "Прошу прощения, ответьте конкретнее.",
    "Я Вас совсем не понимаю. Пожалуйста, ответьте точнее.",
    "Простите, не расслышал. Повторите, пожалуйста.",
    "Ошибка! Ваш запрос оказался недостаточно полным. Попробуйте ещё раз.",
    "Даже не знаю, что сказать... Попробуйте ответить ещё раз."
]


def dialog_handler(event: dict, res: dict) -> dict:
    """Основной обработчик запросов пользователя и ответов сервера, принимает на вход request и возвращает response"""

    if not event['state']['user']:
        # собираем стейты для нового пользователя
        res['user_state_update'] = {
            'name': '',
            'mode': 'start',
            'books': [],
            'questions': [],
            'station': False,
            'last_state': {'mode': 'start',
                           'books': [],
                           'questions': [],
                           'station': False}
        }
    else:
        res['user_state_update'] = event['state']['user'].copy()

    mode = res['user_state_update']['mode']

    if 'YANDEX.REPEAT' in list(event['request']['nlu']['intents'].keys()):
        # если пользователь просит повторить сообщение
        repeat_handler(res)

    elif mode in start.keys():
        # если пользователь только знакомится с навыком
        start_handler(res)

    elif mode in commands.keys():
        # если пользователь вызывает команду
        commands_handler(event, res)

    return res


def start_handler(res: dict):
    mode = res['user_state_update']['mode']
    res['response']['text'] = start[mode]['text']
    res['response']['tts'] = start[mode]['tts']
    res['response']['buttons'] = start[mode]['buttons']
    if start[mode]['card']:
        res['response']['card'] = start[mode]['card']
    save_state(res)
    res['user_state_update']['mode'] = start[mode]['next_mode']


def commands_handler(event: dict, res: dict):
    mode = res['user_state_update']['mode']
    if res['user_state_update']['last_state']['mode'] == 'register':
        if 'YANDEX.FIO' in list(event['request']['nlu']['intents'].keys()):
            res['user_state_update']['name'] = event['request']['original_utterance'].capitalize()
        else:
            res['response']['text'] = 'Пожалуйста, введите настоящее имя!'
            res['response']['tts'] = 'Пожалуйста, введите настоящее имя!'
            res['response']['buttons'] = []
            return
    res['response']['text'] = commands[mode]['text']
    res['response']['tts'] = commands[mode]['tts']
    res['response']['buttons'] = commands[mode]['buttons']
    if commands[mode]['card']:
        res['response']['card'] = commands[mode]['card']
    save_state(res)


def repeat_handler(res: dict, data: dict = None):
    pass


def save_state(res: dict):
    copy_res = res['user_state_update'].copy()
    res['user_state_update']['last_state'] = {
        'mode': copy_res['mode'],
        'books': copy_res['books'],
        'questions': copy_res['questions'],
        'station': copy_res['station']
    }
