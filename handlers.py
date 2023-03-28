from os import path
from json import load
from typing import Any
from random import choice

with open(path.join('data', 'questions.json'), encoding='utf-8') as file:
    questions = load(file)['questions']

with open(path.join('data', 'books.json'), encoding='utf-8') as file:
    books_descriptions = load(file)

with open(path.join('data', 'commands.json'), encoding='utf-8') as file:
    commands = load(file)

SUPERGAME = {
    2: ['Теперь у Вас 2 жизни.', 'Не переживайте, у Вас ещё целых две жизни.', 'С этого момента у Вас 2 жизни.'],
    1: ['С этого момента у Вас нет права на ошибку!', 'Последняя жизнь! Ошибаться больше нельзя!',
        'Права на ошибку больше нет!'],
    0: ['Поражение..', 'Всё кончено!', 'Игра окончена...', 'Это конец!']
}
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
TRUEANS = ["Правильно!", "Верно!", "Абсолютно точно!", "Ты молодец! Всё правильно.", "Вы великолепны, правильно!", "Как неожиданно, Вы правы!"]

IMAGES_FOR_QUESTIONS = ["1652229/3513b2e092b536a1db35", "997614/66778b95cc6e1a7b76f2",
                        "937455/75c64f8e40145a270655", "1533899/cdadf2f29b7b85d2d438",
                        "1652229/3513b2e092b536a1db35", "937455/71b1d565fa686b3b7978",
                        "1030494/aa243b85eca4b09a020e", "997614/b9e8cc1ef284a07802d4",
                        "1533899/bc2102cdbf2869e23fda", "997614/a450012a2984faff527d",
                        "997614/40952917bdd4d9049aaa", "1652229/05d59c2e8b762967069f",
                        "1540737/297189116bd10b6250f9", "1652229/a343bbc8d1cc61d4e3af",
                        "1533899/ce772f731eef74e04a94"]

AUTHORS = {"Л.Н. Толстой": "Лев Никол+аевич Толст+ой",
           "А.С. Пушкин": "Александр Сергеевич П+ушкин",
           "Ф.М. Достоевский": "Фёдор Михайлович Достоевский",
           "М.М. Горький": "Максим Максимович Г+орький",
           "А.Н. Островский": "Александр Николаевич Остр+овский",
           "И.А. Гончаров": "Иван Александрович Гончар+ов",
           "Н.А. Некрасов": "Николай Алексеевич Некр+асов",
           "М.Ф. Шолохов": "Михаил Александрович Ш+олохов",
           "Н.В. Гоголь": "Николай Васильевич Г+оголь",
           "И.С. Тургенев": "Иван Сергеевич Тург+енев",
           "М.Ю. Лермонтов": "Михаил Юрьевич Л+ермонтов",
           "А.П. Чехов": "Антон Павлович Ч+ехов",
           "А.С. Грибоедов": "Александр Сергеевич Грибоедов",
           "Г.К. Андерсен": "Ганс Кр+истиан Андерсен"}


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
        # собираем стейты для нового пользователя и возвращаем приветственное сообщение
        res['user_state_update'] = {
            'name': '',
            'mode': 'menu',
            'books': [],
            'questions': [],
            'points': 0,
            'hearts': 3,
            'station': False,
            'last_response': {}
        }
        res = save_response(
            res=res,
            text=commands['start']['text'],
            tts=commands['start']['tts'],
            buttons=commands['start']['buttons'],
            card=commands['start']['card']
        )
        return res
    else:
        res['user_state_update'] = event['state']['user'].copy()

    if event['session']['message_id'] == 0:
        res['user_state_update'] = {
            'name': res['user_state_update']['name'],
            'mode': 'menu',
            'books': [],
            'questions': [],
            'points': 0,
            'hearts': 3,
            'station': res['user_state_update']['station'],
            'last_response': {}
        }
        res = save_response(
            res=res,
            text=commands['menu']['text'],
            tts=commands['menu']['tts'],
            buttons=commands['menu']['buttons'],
            card=commands['menu']['card']
        )
        return res

    mode = res['user_state_update']['mode']

    if 'YANDEX.HELP' in list(event['request']['nlu']['intents'].keys()):
        # обработчик фразы "помощь"
        if mode in ('quiz', 'super_quiz', 'library'):
            res = save_response(
                res=res,
                text=commands[mode]['text'],
                tts=commands[mode]['tts'],
                buttons=commands[mode]['buttons'],
                card=commands[mode]['card']
            )
        else:
            res = save_response(
                res=res,
                text=commands['help']['text'],
                tts=commands['help']['tts'],
                buttons=commands['help']['buttons'],
                card=commands['help']['card']
            )
        return res

    if 'YANDEX.WHAT_CAN_YOU_DO' in list(event['request']['nlu']['intents'].keys()):
        # обработчик фразы "что ты умеешь?"
        res = save_response(
            res=res,
            text=commands['help']['text'],
            tts=commands['help']['tts'],
            buttons=commands['help']['buttons'],
            card=commands['help']['card']
        )
        return res

    if 'YANDEX.REPEAT' in list(event['request']['nlu']['intents'].keys()):
        # если пользователь просит повторить сообщение
        for key, item in res['user_state_update']['last_response'].items():
            res['response'][key] = item
        return res

    if 'menu' in list(event['request']['nlu']['intents'].keys()):
        if mode in ('quiz', 'super_quiz'):
            res['user_state_update']['mode'] = 'restart' + mode[0]
            res = save_response(
                res=res,
                text=commands['restart']['text'],
                tts=commands['restart']['tts'],
                buttons=commands['restart']['buttons']
            )
            return res
        else:
            res['user_state_update']['mode'] = 'menu'
            res = save_response(
                res=res,
                text=commands['menu']['text'],
                tts=commands['menu']['tts'],
                buttons=commands['menu']['buttons'],
                card=commands['menu']['card']
            )
            return res

    if 'restart' in mode:
        if 'YANDEX.CONFIRM' in list(event['request']['nlu']['intents'].keys()):
            res['user_state_update'] = {
                'name': res['user_state_update']['name'],
                'mode': 'menu',
                'books': [],
                'questions': [],
                'points': 0,
                'hearts': 3,
                'station': res['user_state_update']['station'],
                'last_response': {}
            }
            res = save_response(
                res=res,
                text=commands['menu']['text'],
                tts=commands['menu']['tts'],
                buttons=commands['menu']['buttons'],
                card=commands['menu']['card']
            )
            return res
        elif 'YANDEX.REJECT' in list(event['request']['nlu']['intents'].keys()):
            if mode[-1] == 'q':
                res['user_state_update']['mode'] = 'quiz'
            else:
                res['user_state_update']['mode'] = 'super_quiz'
            question = res['user_state_update']['questions'][-1]
            res = return_question(res, question)
            return res
        else:
            return error_handler(res, choice(MISUNDERSTANDING))

    if 'finish_game' in mode:
        res['user_state_update'] = {
            'name': res['user_state_update']['name'],
            'mode': 'menu',
            'books': [],
            'questions': [],
            'points': 0,
            'hearts': 3,
            'station': res['user_state_update']['station'],
            'last_response': {}
        }
        if 'YANDEX.CONFIRM' in list(event['request']['nlu']['intents'].keys()):
            if mode[-1] == 'q':
                res['user_state_update']['mode'] = 'quiz'
            else:
                res['user_state_update']['mode'] = 'super_quiz'
            res = get_questions(res)
            question = res['user_state_update']['questions'][-1]
            res = return_question(res, question)
            return res
        elif 'YANDEX.REJECT' in list(event['request']['nlu']['intents'].keys()):
            res['user_state_update']['mode'] = 'menu'
            res = save_response(
                res=res,
                text=commands['menu']['text'],
                tts=commands['menu']['tts'],
                buttons=commands['menu']['buttons'],
                card=commands['menu']['card']
            )
            return res
        else:
            return error_handler(res, choice(MISUNDERSTANDING))

    if mode == 'menu':
        # если пользователь вызывает меню
        return menu_handler(event, res)

    if mode == 'quiz' or mode == 'super_quiz':
        if not res['user_state_update']['questions']:
            if 'YANDEX.CONFIRM' in list(event['request']['nlu']['intents'].keys()):
                res = get_questions(res)
                question = res['user_state_update']['questions'][-1]
                res = return_question(res, question)
                return res
            elif 'YANDEX.REJECT' in list(event['request']['nlu']['intents'].keys()):
                res['user_state_update']['mode'] = 'menu'
                res = save_response(
                    res=res,
                    text=commands['menu']['text'],
                    tts=commands['menu']['tts'],
                    buttons=commands['menu']['buttons'],
                    card=commands['menu']['card']
                )
                return res
            else:
                return error_handler(res, choice(MISUNDERSTANDING))
        elif 'Чтобы повторить вопрос, скажите "Повтори".' in res['user_state_update']['last_response']['card'][
            'description']:
            question = res['user_state_update']['questions'][-1]
            res = return_question(res, question)
            return res
        else:
            question = res['user_state_update']['questions'][-1]
            flag = True
            if event['request']['type'] == "ButtonPressed":
                if event['request']['payload']['title'] in question['answers']:
                    flag = False
            else:
                if event['request']['original_utterance'].lower() in question['answers']:
                    flag = False
                for t in event['request']['nlu']['tokens']:
                    if t.lower() in question['answers']:
                        flag = False
                        break
            if flag:
                if mode == 'super_quiz':
                    res['user_state_update']['hearts'] -= 1
                    answer = choice(WRONGANS) + ' ' + choice(SUPERGAME[res['user_state_update']['hearts']]) + '\n'
                    if res['user_state_update']['hearts'] == 0:
                        res['user_state_update']['mode'] = 'finish_game' + mode[0]
                        answer += f' Ваш результат: {res["user_state_update"]["points"]}. ' + commands['finish_game'][
                            'text']
                        res = save_response(
                            res=res,
                            text=answer,
                            tts=answer,
                            buttons=commands['finish_game']['buttons']
                        )
                        return res
                elif mode == 'quiz':
                    answer = choice(WRONGANS) + '\n'
            else:
                res['user_state_update']['points'] += 1
                answer = choice(TRUEANS) + '\n'
            question, res['user_state_update']['questions'] = None, res['user_state_update']['questions'][:-1]
            if res['user_state_update']['questions']:
                question = res['user_state_update']['questions'][-1]
                res = return_question(res, question)
                res['response']['tts'] = answer + res['response']['tts']
                res['response']['card']['description'] = answer + res['response']['card']['description']
                res['user_state_update']['last_response']['tts'] = res['response']['tts']
                res['user_state_update']['last_response']['card'] = res['response']['card']
                return res
            else:
                if mode == 'super_quiz':
                    res = get_questions(res)
                    question = res['user_state_update']['questions'][-1]
                    res = return_question(res, question)
                    return res
                else:
                    res['user_state_update']['mode'] = 'finish_game' + mode[0]
                    answer = f'{answer} Викторина окончена! Ваш результат: ' \
                             f'{res["user_state_update"]["points"]}. {commands["finish_game"]["text"]}"'
                    res = save_response(
                        res=res,
                        text=answer,
                        tts=answer,
                        buttons=commands['finish_game']['buttons']
                    )
                    return res

    raise Exception


def menu_handler(event: dict, res: dict) -> dict:
    if not res['user_state_update']['name']:
        if event['request']['nlu']['entities'] and 'YANDEX.FIO' == event['request']['nlu']['entities'][0]['type']:
            res['user_state_update']['name'] = event['request']['nlu']['entities'][0]['value'][
                'first_name'].capitalize()
            res = save_response(
                res=res,
                text=commands['menu']['text'],
                tts=commands['menu']['tts'],
                buttons=commands['menu']['buttons'],
                card=commands['menu']['card']
            )
        else:
            res = error_handler(res, 'Пожалуйста, введите настоящее имя!')
        return res
    if event['request']['type'] == "ButtonPressed":
        text = [event['request']['payload']['title'].lower()]
    else:
        text = event['request']['nlu']['tokens']
        text.append(event['request']['original_utterance'].lower().strip().strip('.'))
    if 'викторина' in text:
        mode = 'quiz'
    elif 'супер-игра' in text or 'супер игра' in text:
        mode = 'super_quiz'
    elif 'библиотека' in text:
        # mode = 'library'
        text = 'В разработке... Скажите \"Меню\", чтобы вернуться обратно.'
        res = save_response(
            res=res,
            text=text,
            tts=text,
            buttons=[
                {
                    "title": "Меню",
                    "payload": {},
                    "hide": True
                }
            ]
        )
        return res
    else:
        return error_handler(res, choice(MISUNDERSTANDING))
    res['user_state_update']['mode'] = mode
    card = commands[mode]['card'].copy()
    card['description'] += ' Вы готовы начать?'
    res = save_response(
        res=res,
        text=commands[mode]['text'] + ' Вы готовы начать?',
        tts=commands[mode]['tts'] + ' Вы готовы начать?',
        buttons=[
            {
                "title": "Да",
                "payload": {},
                "hide": True
            },
            {
                "title": "Нет",
                "payload": {},
                "hide": True
            }
        ],
        card=card
    )
    return res


def save_response(res: dict, text: str, tts: str, buttons: list, card: dict = None) -> dict:
    res['response']['text'] = text
    res['response']['tts'] = tts
    res['response']['buttons'] = buttons
    res['user_state_update']['last_response'] = {
        'text': text,
        'tts': tts,
        'buttons': buttons
    }
    if card:
        res['response']['card'] = card
        res['user_state_update']['last_response']['card'] = card
    return res


def error_handler(res: dict, err_message: str) -> dict:
    res = save_response(
        res=res,
        text=err_message,
        tts=err_message,
        buttons=[]
    )
    return res


def get_questions(res: dict) -> dict:
    deck = []
    while len(deck) < 20:
        question = choice(questions)
        if question not in deck:
            deck.append(question)
    res['user_state_update']['questions'] = deck
    return res


def return_question(res: dict, question_original: dict) -> dict:
    question = question_original.copy()
    question['card']['image_id'] = choice(IMAGES_FOR_QUESTIONS)
    question['card']['title'] = question['book']
    question['tts'] += ' ' + question['book']
    res = save_response(
        res=res,
        text=question['text'],
        tts=question['tts'],
        buttons=question['buttons'] + [
            {
                "title": "Помощь",
                "payload": {},
                "hide": True
            },
            {
                "title": "Меню",
                "payload": {},
                "hide": True
            },
            {
                "title": "Повтори",
                "payload": {},
                "hide": True
            }
        ],
        card=question['card']
    )
    return res
