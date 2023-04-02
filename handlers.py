from os import path
from json import load
from typing import Any
from random import choice, shuffle, randint

with open(path.join('data', 'questions.json'), encoding='utf-8') as file:
    questions = load(file)['questions']

with open(path.join('data', 'books.json'), encoding='utf-8') as file:
    books_descriptions = load(file)

with open(path.join('data', 'commands.json'), encoding='utf-8') as file:
    commands = load(file)

MISUNDERSTANDING = [
    "Я Вас совсем не понимаю. Пожалуйста, ответьте точнее. Если хотите выйти в меню, скажите \"Меню\" или скажите \"Помощь\"",
    "Если вам что-то непонятно, то скажите \"Меню\" или \"Помощь\".",
    "К сожалению, я не смог понять ваш ответ так же, как героиня романа \"Алиса в Стране Чудес\" не могла "
    "понять бред Шляпника. Скажите \"Меню\", чтобы вернуться в меню, или \"Повтори\" для повтора.",
    "Как и Шерлок Холмс, я не могу понять ваш ответ, потому что мне не хватает информации. "
    "Скажите \"Помощь\" и я попытаюсь Вам помочь.",
    "Как в \"Гарри Поттере\" Роулинг, я не смог понять Ваш вопрос, потому что он находится под сильным "
    "заклинанием. Скажите \"Помощь\", и Я постараюсь вам помочь!"
]
WRONGANS = [
    "Упс! Вы ответили неверно...", "Жаль, но ваш ответ не был верным.",
    "Неверный ответ.", "Увы, ваш ответ оказался мимо кассы.",
    "Вы ошиблись.",
    "Не хотел я этого говорить, но Вы ошиблись.",
    "Как бы вам сказать, что Вы ошиблись...",
    "Ничего страшного, повезёт в следующий раз.",
    "К сожалению, ваш ответ неверный.",
    "Неправильный ответ, но не расстраивайтесь!",
    "Нет, к сожалению, это неверный ответ.",
    "Неправильно, но не переживайте, следующий вопрос будет проще.",
    "Очень близко, но не совсем.", "Ваш ответ был как шерсть на зубах – не совсем то, что нужно.",
    "К сожалению, ваш ответ был настолько неправильным, что Шерлок Холмс."
    "воскликнул бы \"Элементарно, Ватсон, что это неправильно!\"",
    "Хотелось бы, чтобы ваш ответ был верен, но он так же далек от правильного, как Нептун от Меркурия."
]
TRUEANS = [
    "Правильно!", "Верно!", "Абсолютно точно!", "Ты молодец! Всё правильно.", "Вы великолепны, правильно!",
    "Вы правы!", "Как вы это сделали, верно!", "Я удивлён, верно!",
    "Я бы сам не ответил, а вы ответили правильно, поздравляю!", "Вы молодец! Всё правильно!",
    "Отлично! Это правильный ответ.", "Правильно! Вы явно читали много книг.",
    "Вы абсолютно правы! Это был сложный вопрос.", "Верный ответ! Вы уверенно продвигаетесь по викторине.",
    "Верно! Ваше знание литературы впечатляет.", "Ответ верный! Продолжайте в том же духе.",
    "Вы правы! Это действительно было сложно, но вы справились.",
    "Вы абсолютно правы! Этот ответ не оставил сомнений.",
    "Это верный ответ! Вы знакомы с этой темой.", "Именно так! Это был хитрый вопрос, но вы справились.",
    "Именно так! Это было непросто, но вы справились.",
    "Точно! Это был трудный вопрос, но вы сумели ответить верно.",
    "Верный ответ! Вы настоящий знаток литературы.", "Отлично! Вы демонстрируете высокий уровень знаний.",
    "Да, это правильный ответ! Вы действительно знаете свою литературу.",
    "Ваш ответ точен, как рифма в стихотворении Пушкина.",
    "Отлично, вы на правильном пути! Как молодой Холмс, разгадывающий загадки.",
    "Именно так, как Шерлок Холмс, вы нашли ключ к правильному ответу.",
    "Превосходно, вы владеете знаниями, как Дон Кихот владеет мечом."
]

IMAGES_FOR_QUESTIONS = ["1652229/3513b2e092b536a1db35", "997614/66778b95cc6e1a7b76f2",
                        "937455/75c64f8e40145a270655", "1533899/cdadf2f29b7b85d2d438",
                        "1652229/3513b2e092b536a1db35", "937455/71b1d565fa686b3b7978",
                        "1030494/aa243b85eca4b09a020e", "997614/b9e8cc1ef284a07802d4",
                        "1533899/bc2102cdbf2869e23fda", "997614/a450012a2984faff527d",
                        "997614/40952917bdd4d9049aaa", "1652229/05d59c2e8b762967069f",
                        "1540737/297189116bd10b6250f9", "1652229/a343bbc8d1cc61d4e3af",
                        "1533899/ce772f731eef74e04a94"]
IMAGE_GIVE_A_LIVE = [
    '1521359/ae1d5b4c27beec31b7a8',
    '213044/ec19844ed2a539c87757'
]

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
           "Х.К. Андерсен": "Ганс Кр+истиан Андерсен",
           "М.А. Булгаков": "Михаил Афанасьевич Булгаков",
           "Внезапная картинка": "Внезапная картинка",
           "Цитата из": "Цитата из случайной книги"}

BOOKS = list(books_descriptions.keys())

RESULTS = {
    5: 'Потрясающий результат, идеально! Вы настоящий знаток в классической литературе, и вашим знаниям можно '
       'только позавидовать. Надеемся, эта викторина не была для Вас слишком простой!',
    4: 'Поздравляю, отличный результат! Ещё немного, и можно было бы с уверенностью сказать, что в литературе нет '
       'ничего, что Вы могли бы не знать. Продолжайте в том же духе!',
    3: 'Очень неплохой результат! Вам ещё есть куда стремиться, однако уже можно сказать, что Вы владеете '
       'хорошими знаниями в области классической литературы. Не останавливайтесь на достигнутом!',
    2: 'Средненький результат. Похоже, Вы не особо увлекаетесь классической литературой, но всё же обладаете '
       'необходимой базой. Чтобы улучшить её, советуем посетить нашу библиотеку и выбрать интересную для Вас книгу.',
    1: 'Не самый лучший результат. Возможно, Вам просто не повезло с вопросами, однако явно стоит задуматься о '
       'том, чтобы ознакомиться с парочкой произведений. К слову, с этим Вам может помочь наша библиотека!',
    0: 'Откровенно плохой результат. Судя по всему, классическая литература обошла Вас стороной, однако никогда '
       'не поздно что-то начать. Советуем посетить нашу библиотеку и ознакомиться с предложенными книгами!'
}

GIVE_A_LIFE = [
    'Какая удача! Только что у вас стало на одну жизнь больше!',
    'Вжух! Теперь у вас на одну жизнь больше!',
    'Вот это да! Теперь у вас появилась ещё одна жизнь!',
    'Внимание! Только что Вы получили дополнительную жизнь!',
    'Поздравляю! Вам удалось вернуть себе одну жизнь!'
]
LOOSE_A_LIFE = {
    2: ['Теперь у Вас две жизни.', 'Не переживайте, у Вас ещё целых две жизни.', 'С этого момента у Вас две жизни.'],
    1: ['С этого момента у Вас нет права на ошибку!', 'Последняя жизнь! Ошибаться больше нельзя!',
        'Права на ошибку больше нет!'],
    0: ['Поражение...', 'Всё кончено!', 'Игра окончена...', 'Это конец!']
}


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
            'mode': 'station',
            'books': [],
            'questions': [],
            'points': 0,
            'hearts': 3,
            'station': False,
            'last_response': {},
            'help': False
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
            'mode': 'station',
            'books': [],
            'questions': [],
            'points': 0,
            'hearts': 3,
            'station': res['user_state_update']['station'],
            'last_response': {},
            'help': False
        }
        station = commands['station']['card'].copy()
        station['description'] = 'Добро пожаловать в навык "Литературный гений"!' + station['description'][8:]
        res = save_response(
            res=res,
            text='Добро пожаловать в навык "Литературный гений"!' + commands['station']['text'][8:],
            tts='Добро пожаловать в навык "Литературный гений"!' + commands['station']['tts'][8:],
            buttons=commands['station']['buttons'],
            card=station
        )
        return res

    mode = res['user_state_update']['mode']

    if 'YANDEX.HELP' in list(event['request']['nlu']['intents'].keys()):
        # обработчик фразы "помощь"
        res['user_state_update']['help'] = True
        if mode in ('quiz', 'super_quiz', 'library'):
            res = save_response(
                res=res,
                text=commands[mode]['text'],
                tts=commands[mode]['tts'],
                buttons=commands[mode]['buttons'],
                card=commands[mode]['card']
            )
        elif 'restart' in mode or 'finish_game' in mode:
            if mode[-1] == 's':
                res = save_response(
                    res=res,
                    text=commands['super_quiz']['text'],
                    tts=commands['super_quiz']['tts'],
                    buttons=commands['super_quiz']['buttons'],
                    card=commands['super_quiz']['card']
                )
            elif mode[-1] == 'q':
                res = save_response(
                    res=res,
                    text=commands['quiz']['text'],
                    tts=commands['quiz']['tts'],
                    buttons=commands['quiz']['buttons'],
                    card=commands['quiz']['card']
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
        res['user_state_update']['help'] = True
        text = choice(commands['description']['text'])
        card = commands['description']['card'].copy()
        card['description'] = text
        res = save_response(
            res=res,
            text=text,
            tts=text,
            buttons=commands['description']['buttons'],
            card=card
        )
        return res

    if 'YANDEX.REPEAT' in list(event['request']['nlu']['intents'].keys()):
        # если пользователь просит повторить сообщение
        for key, item in res['user_state_update']['last_response'].items():
            res['response'][key] = item
        return res

    if mode == 'station':
        if res['user_state_update']['help']:
            res['user_state_update']['help'] = False
            res = save_response(
                res=res,
                text=commands['station']['text'],
                tts=commands['station']['tts'],
                buttons=commands['station']['buttons'],
                card=commands['station']['card']
            )
            return res
        if 'YANDEX.CONFIRM' in list(event['request']['nlu']['intents'].keys()):
            res['user_state_update']['station'] = True
            res['user_state_update']['mode'] = 'menu'
            res = save_response(
                res=res,
                text=commands['menu']['text'],
                tts=commands['menu']['tts'],
                buttons=commands['menu']['buttons'],
                card=commands['menu']['card']
            )
            return res
        if 'YANDEX.REJECT' in list(event['request']['nlu']['intents'].keys()):
            res['user_state_update']['station'] = False
            res['user_state_update']['mode'] = 'menu'
            res = save_response(
                res=res,
                text=commands['menu']['text'],
                tts=commands['menu']['tts'],
                buttons=commands['menu']['buttons'],
                card=commands['menu']['card']
            )
            return res
        station = commands['station']['card'].copy()
        err_msg = choice(MISUNDERSTANDING)
        station['description'] = err_msg + station['description'][8:]
        res = save_response(
            res=res,
            text=err_msg + commands['station']['text'][8:],
            tts=err_msg + commands['station']['tts'][8:],
            buttons=commands['station']['buttons'],
            card=station
        )
        return res

    if 'menu' in list(event['request']['nlu']['intents'].keys()):
        if mode in ('quiz', 'super_quiz'):
            res['user_state_update']['mode'] = 'restart' + mode[0]
            res['user_state_update']['help'] = False
            res = save_response(
                res=res,
                text=commands['restart']['text'],
                tts=commands['restart']['tts'],
                buttons=commands['restart']['buttons']
            )
            return res
        else:
            res['user_state_update'] = {
                'mode': 'menu',
                'books': [],
                'questions': [],
                'points': 0,
                'hearts': 3,
                'station': res['user_state_update']['station'],
                'last_response': {},
                'help': False
            }
            res = save_response(
                res=res,
                text=commands['menu']['text'],
                tts=commands['menu']['tts'],
                buttons=commands['menu']['buttons'],
                card=commands['menu']['card']
            )
            return res

    if 'restart' in mode:
        res['user_state_update']['help'] = False
        if res['user_state_update']['help']:
            res['user_state_update']['help'] = False
            res = save_response(
                res=res,
                text=commands['restart']['text'],
                tts=commands['restart']['tts'],
                buttons=commands['restart']['buttons']
            )
            return res
        if 'YANDEX.CONFIRM' in list(event['request']['nlu']['intents'].keys()):
            res['user_state_update'] = {
                'name': res['user_state_update']['name'],
                'mode': 'menu',
                'books': [],
                'questions': [],
                'points': 0,
                'hearts': 3,
                'station': res['user_state_update']['station'],
                'last_response': {},
                'help': False
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
            err_msg = choice(MISUNDERSTANDING)
            res = save_response(
                res=res,
                text=err_msg + ' ' + commands['restart']['text'],
                tts=err_msg + ' ' + commands['restart']['tts'],
                buttons=commands['restart']['buttons']
            )
            return res

    if 'finish_game' in mode:
        res['user_state_update'] = {
            'name': res['user_state_update']['name'],
            'mode': 'menu',
            'books': [],
            'questions': [],
            'points': 0,
            'hearts': 3,
            'station': res['user_state_update']['station'],
            'last_response': {},
            'help': False
        }
        if res['user_state_update']['help']:
            if mode[-1] == 'q':
                answer = f'Викторина окончена! Количество правильных ответов: {res["user_state_update"]["points"]}. ' \
                         f'{RESULTS[res["user_state_update"]["points"] // 4]} {commands["finish_game"]["text"]}'
                card = commands['finish_game']['card'].copy()
                card['description'] = answer
                res = save_response(
                    res=res,
                    text=answer,
                    tts=answer,
                    buttons=commands['finish_game']['buttons'],
                    card=card
                )
                return res
            else:
                answer = f'Супер-игра окончена! Количество правильных ответов: {res["user_state_update"]["points"]}. ' \
                          f'{RESULTS[min(5, res["user_state_update"]["points"] // 4)]} ' \
                          f'{commands["finish_game"]["text"]}'
                card = commands['finish_game']['card'].copy()
                card['description'] = answer
                res = save_response(
                    res=res,
                    text=answer,
                    tts=answer,
                    buttons=commands['finish_game']['buttons'],
                    card=card
                )
                return res
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
            res = save_response(
                res=res,
                text=commands['menu']['text'],
                tts=commands['menu']['tts'],
                buttons=commands['menu']['buttons'],
                card=commands['menu']['card']
            )
            return res
        else:
            if mode[-1] == 'q':
                answer = choice(MISUNDERSTANDING) + '\n'
                answer = f'{answer} Викторина окончена! Количество правильных ответов: ' \
                         f'{res["user_state_update"]["points"]}. {RESULTS[res["user_state_update"]["points"] // 4]} ' \
                         f'{commands["finish_game"]["text"]}'
                card = commands['finish_game']['card'].copy()
                card['description'] = answer
                res = save_response(
                    res=res,
                    text=answer,
                    tts=answer,
                    buttons=commands['finish_game']['buttons'],
                    card=card
                )
                return res
            else:
                answer = choice(MISUNDERSTANDING) + ' '
                answer += f'Супер-игра окончена! Количество правильных ответов: {res["user_state_update"]["points"]}.' \
                          f' {RESULTS[min(5, res["user_state_update"]["points"] // 4)]} ' \
                          f'{commands["finish_game"]["text"]}'
                card = commands['finish_game']['card'].copy()
                card['description'] = answer
                res = save_response(
                    res=res,
                    text=answer,
                    tts=answer,
                    buttons=commands['finish_game']['buttons'],
                    card=card
                )
                return res

    if mode == 'quiz' or mode == 'super_quiz':
        # если пользователь запустил викторину
        return quiz_handler(event, res)

    if mode == 'library':
        # если пользователь запустил библиотеку
        return library_handler(event, res)

    if mode == 'menu':
        # если пользователь вызывает меню
        return menu_handler(event, res)

    raise Exception


def menu_handler(event: dict, res: dict) -> dict:
    if res['user_state_update']['help']:
        res['user_state_update']['help'] = False
        res = save_response(
            res=res,
            text=commands['menu']['text'],
            tts=commands['menu']['tts'],
            buttons=commands['menu']['buttons'],
            card=commands['menu']['card']
        )
        return res
    res['user_state_update']['help'] = False
    if event['request']['type'] == "ButtonPressed":
        text = [event['request']['payload']['title'].lower()]
    else:
        text = event['request']['nlu']['tokens']
        text.append(event['request']['original_utterance'].lower().strip().strip('.'))
    mode = ''
    for ans in text:
        if 'викторина' in ans.strip().strip('.') or 'викторину' in ans.strip().strip('.'):
            mode = 'quiz'
            break
        elif 'супер-игра' in ans.strip().strip('.') or 'супер игра' in ans.strip().strip('.') or \
                'супер игру' in ans.strip().strip('.') or 'супер-игру' in ans.strip().strip('.'):
            mode = 'super_quiz'
            break
        elif 'библиотека' in ans.strip().strip('.') or 'библиотеку' in ans.strip().strip('.'):
            mode = 'library'
            break
    if not mode:
        err_msg = choice(MISUNDERSTANDING)
        res['response']['text'] = err_msg + ' ' + commands['menu']['text']
        res['response']['tts'] = err_msg + ' ' + commands['menu']['tts']
        res['response']['buttons'] = commands['menu']['buttons']
        res['response']['card'] = commands['menu']['card']
        return res
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


def quiz_handler(event: dict, res: dict) -> dict:
    mode = res['user_state_update']['mode']

    if not res['user_state_update']['questions']:
        if res['user_state_update']['help']:
            res['user_state_update']['help'] = False
            res = save_response(
                res=res,
                text=commands[mode]['text'],
                tts=commands[mode]['tts'],
                buttons=commands[mode]['buttons'],
                card=commands[mode]['card']
            )
            return res
        res['user_state_update']['help'] = False
        if 'YANDEX.CONFIRM' in list(event['request']['nlu']['intents'].keys()):
            res['user_state_update'] = {
                'mode': mode,
                'books': [],
                'questions': [],
                'points': 0,
                'hearts': 3,
                'station': res['user_state_update']['station'],
                'last_response': {},
                'help': False
            }
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
            card = commands[mode]['card'].copy()
            card['description'] += ' Вы готовы начать?'
            err_msg = choice(MISUNDERSTANDING)
            card['description'] = err_msg + ' ' + card['description']
            res = save_response(
                res=res,
                text=err_msg + ' ' + commands[mode]['text'] + ' Вы готовы начать?',
                tts=err_msg + ' ' + commands[mode]['tts'] + ' Вы готовы начать?',
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

    elif res['user_state_update']['help']:
        res['user_state_update']['help'] = False
        question = res['user_state_update']['questions'][-1]
        res = return_question(res, question)
        return res

    else:
        res['user_state_update']['help'] = False
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
                answer = choice(WRONGANS) + ' ' + choice(LOOSE_A_LIFE[res['user_state_update']['hearts']]) + ' '
                if res['user_state_update']['hearts'] == 0:
                    answer = choice(LOOSE_A_LIFE[res['user_state_update']['hearts']])
                    res['user_state_update']['mode'] = 'finish_game' + mode[0]
                    answer += f' Количество правильных ответов: {res["user_state_update"]["points"]}. ' \
                              f'{RESULTS[min(5, res["user_state_update"]["points"] // 4)]} ' \
                              f'{commands["finish_game"]["text"]}'
                    card = commands['finish_game']['card'].copy()
                    card['description'] = answer
                    res = save_response(
                        res=res,
                        text=answer,
                        tts=answer,
                        buttons=commands['finish_game']['buttons'],
                        card=card
                    )
                    return res
            elif mode == 'quiz':
                answer = choice(WRONGANS) + ' '
        else:
            res['user_state_update']['points'] += 1
            answer = choice(TRUEANS) + ' '
        question, res['user_state_update']['questions'] = None, res['user_state_update']['questions'][:-1]
        if res['user_state_update']['questions']:
            chance = 0
            if mode == 'super_quiz' and res['user_state_update']['hearts'] < 3:
                chance = randint(1, 10)
                if chance == 1:
                    answer += choice(GIVE_A_LIFE)
            question = res['user_state_update']['questions'][-1]
            res = return_question(res, question)
            res['response']['tts'] = answer + res['response']['tts']
            res['response']['card']['description'] = answer + res['response']['card']['description']
            if chance == 1:
                res['response']['card']['image_id'] = choice(IMAGE_GIVE_A_LIVE)
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
                answer = f'{answer} Викторина окончена! Ваш результат: {res["user_state_update"]["points"]}. ' \
                         f'{RESULTS[res["user_state_update"]["points"] // 4]} {commands["finish_game"]["text"]}'
                card = commands['finish_game']['card'].copy()
                card['description'] = answer
                res = save_response(
                    res=res,
                    text=answer,
                    tts=answer,
                    buttons=commands['finish_game']['buttons'],
                    card=card
                )
                return res


def library_handler(event: dict, res: dict) -> dict:
    mode = res['user_state_update']['mode']
    print(event)

    if not res['user_state_update']['books']:
        if res['user_state_update']['help']:
            res['user_state_update']['help'] = False
            res = save_response(
                res=res,
                text=commands[mode]['text'],
                tts=commands[mode]['tts'],
                buttons=commands[mode]['buttons'],
                card=commands[mode]['card']
            )
            return res
        res['user_state_update']['help'] = False
        if 'YANDEX.CONFIRM' in list(event['request']['nlu']['intents'].keys()):
            res['user_state_update'] = {
                'mode': mode,
                'books': [],
                'questions': [],
                'points': 0,
                'hearts': 3,
                'station': res['user_state_update']['station'],
                'last_response': {},
                'help': False
            }
            res = return_books(res)
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
            card = commands[mode]['card'].copy()
            card['description'] += ' Вы готовы начать?'
            err_msg = choice(MISUNDERSTANDING)
            card['description'] = err_msg + ' ' + card['description']
            res = save_response(
                res=res,
                text=err_msg + ' ' + commands[mode]['text'] + ' Вы готовы начать?',
                tts=err_msg + ' ' + commands[mode]['tts'] + ' Вы готовы начать?',
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

    elif res['user_state_update']['help']:
        res['user_state_update']['help'] = False
        if isinstance(res['user_state_update']['books'], list):
            return return_books(res)
        elif isinstance(res['user_state_update']['books'], str):
            return get_book_reference(res, res['user_state_update']['books'])

    elif isinstance(res['user_state_update']['books'], list):
        res['user_state_update']['help'] = False
        if 'next_books' in list(event['request']['nlu']['intents'].keys()):
            return return_books(res)
        book = ''
        if event['request']['type'] == "ButtonPressed":
            book = event['request']['payload']['title']
        else:
            for word in event['request']['nlu']['tokens']:
                for b in BOOKS:
                    if word in b.split():
                        book = b
                        break
                    w = word.replace('ё', 'e')
                    if w in b.split():
                        book = b
                        break
                if book:
                    break
        if book:
            res = get_book_reference(res, book)
            return res
        else:
            err_msg = choice(MISUNDERSTANDING)
            res['response']['text'] = err_msg + ' Возможно, такой книги ещё нет в нашей библиотеке. ' + \
                                      res['user_state_update']['last_response']['text']
            res['response']['tts'] = err_msg + ' Возможно, такой книги ещё нет в нашей библиотеке. ' + \
                                     res['user_state_update']['last_response']['tts']
            res['response']['buttons'] = res['user_state_update']['last_response']['buttons']
            res['response']['card'] = res['user_state_update']['last_response']['card']
            return res

    elif isinstance(res['user_state_update']['books'], str):
        res['user_state_update']['help'] = False
        if 'books_gallery' in list(event['request']['nlu']['intents'].keys()):
            res['user_state_update']['books'] = []
            return return_books(res)
        elif 'main_info_book' in list(event['request']['nlu']['intents'].keys()):
            book_mode = 'main_description'
        elif 'char_info_book' in list(event['request']['nlu']['intents'].keys()):
            book_mode = 'char_description'
        elif 'facts_books' in list(event['request']['nlu']['intents'].keys()):
            book_mode = 'facts'
        elif 'links_books' in list(event['request']['nlu']['intents'].keys()):
            book_mode = 'useful_links'
        else:
            err_msg = choice(MISUNDERSTANDING)
            res['response']['text'] = err_msg + ' Пожалуйста, выберите один из четырёх режимов. ' + \
                                      res['user_state_update']['last_response']['text']
            res['response']['tts'] = err_msg + ' Пожалуйста, выберите один из четырёх режимов. ' + \
                                     res['user_state_update']['last_response']['tts']
            res['response']['buttons'] = res['user_state_update']['last_response']['buttons']
            res['response']['card'] = res['user_state_update']['last_response']['card']
            return res
        return get_book_info(res, res['user_state_update']['books'], book_mode)


def return_question(res: dict, question_original: dict) -> dict:
    question = question_original.copy()
    question['card']['title'] = question['book']
    if not question['card']['image_id']:
        question['card']['image_id'] = choice(IMAGES_FOR_QUESTIONS)

    book = question['book']
    if 'цитата' in book.lower() or 'картинка' in book.lower():
        question['tts'] = book + ' sil <[250]> ' + question['tts']
    else:
        try:
            author = AUTHORS[' '.join(book.split()[:2])]
            question['tts'] = author + ' ' + ' '.join(book.split()[2:]) + ' sil <[250]> ' + question['tts']
        except Exception:
            question['tts'] = 'Итак, следующая книга: ' + book + ' sil <[250]> ' + question['tts']

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


def get_questions(res: dict) -> dict:
    questions_copy = questions.copy()
    if res['user_state_update']['station']:
        questions_copy = list(filter(lambda x: not x['station'], questions_copy))
    shuffle(questions_copy)
    res['user_state_update']['questions'] = questions_copy[:20]
    return res


def return_books(res: dict) -> dict:
    card = {
        "type": "ImageGallery",
        "items": []
    }
    text = f'Скажите название интересующей Вас книги или выберите одну из пяти предложенных: ' \
           f'{" sil <[250]> ".join(res["user_state_update"]["books"])}. Чтобы посмотреть другие книги, скажите ' \
           f'"Дальше". Если хотите, чтобы я повторил, скажите "Повтори". А для того чтобы чтобы' \
           f' выйти в главное меню, скажите "Меню".'
    buttons = [
        {
            "title": 'Дальше',
            "payload": {
                "title": 'дальше'
            },
            "hide": True
        }
    ]
    for i in range(5):
        try:
            book_name = res['user_state_update']['books'].pop(i)
        except IndexError:
            res = get_books(res)
            book_name = res['user_state_update']['books'].pop(i)
        book = {
            "image_id": books_descriptions[book_name]['image_id'],
            "title": books_descriptions[book_name]['title'],
            "button": books_descriptions[book_name]['button']
        }
        card['items'].append(book)
        buttons.append(
            {
                "title": book['title'],
                "payload": {
                    "title": book['title'].lower()
                },
                "hide": True
            }
        )
    res = save_response(
        res=res,
        text=text,
        tts=text,
        buttons=buttons + [
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
        card=card
    )
    return res


def get_books(res: dict) -> dict:
    shuffle(BOOKS)
    res['user_state_update']['books'] = BOOKS.copy()
    return res


def get_book_reference(res: dict, book: str) -> dict:
    res['user_state_update']['books'] = book
    card = {
        "type": "ImageGallery",
        "items": []
    }
    text = f'Вы выбрали произведение {book} Скажите, что хотите узнать о данном произведении. Я могу' \
           f' рассказать основную информацию о книге, о персонажах, интересные факты или полезные ссылки. Для ' \
           f'выбора произнесите название одного из режимов: "Основная информация", sil <[250]>  "Персонажи", ' \
           f'sil <[250]> "Факты" или sil <[150]> "Ссылки". Также Вы можете вернуться обратно на витрину ' \
           f'и выбрать другую книгу. Для этого скажите "К витрине". Если хотите, чтобы я повторил, скажите "Повтори".' \
           f' А для того чтобы выйти в главное меню, скажите "Меню".'
    buttons = [
        {
            "title": 'К витрине',
            "payload": {
                "title": 'к витрине'
            },
            "hide": True
        }
    ]
    for key in list(books_descriptions[book].keys())[3:]:
        if not books_descriptions[book][key]['image_id']:
            image_id = choice(IMAGES_FOR_QUESTIONS)
        else:
            image_id = books_descriptions[book][key]['image_id']
        item = {
            "image_id": image_id,
            "title": books_descriptions[book][key]['title'],
            "button": books_descriptions[book][key]['button']
        }
        card['items'].append(item)
        buttons.append(
            {
                "title": item['title'],
                "payload": {
                    "title": item['title'].lower()
                },
                "hide": True
            }
        )
    res = save_response(
        res=res,
        text=text,
        tts=text,
        buttons=buttons + [
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
        card=card
    )
    return res


def get_book_info(res: dict, book: str, mode: str) -> dict:
    buttons = [
        {
            "title": 'К витрине',
            "payload": {
                "title": 'к витрине'
            },
            "hide": True
        }
    ]
    for key in list(books_descriptions[book].keys())[3:]:
        if key != mode:
            buttons.append(
                {
                    "title": books_descriptions[book][key]['title'],
                    "payload": {
                        "title": books_descriptions[book][key]['title'].lower()
                    },
                    "hide": True
                }
            )
    res = save_response(
        res=res,
        text=books_descriptions[book][mode]['text'],
        tts=books_descriptions[book][mode]['tts'],
        buttons=buttons + [
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
        card=books_descriptions[book][mode]['card']
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
