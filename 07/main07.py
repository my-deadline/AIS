from __future__ import print_function
import json
import random

import pymorphy2
import re

with open("coffee.txt", encoding='utf-8') as file:
    cups = [row.strip() for row in file]
with open("tree2.json", encoding='utf-8') as json_file:
    coffee_file = json.load(json_file)
morph = pymorphy2.MorphAnalyzer()
session = -1


def parser(s):
    phrase = re.sub(r'[^\w\s]', '', s.lower()).split()
    norm_phrase = list()
    for word in phrase:
        norm_phrase.append(morph.parse(word)[0].normal_form)
    return norm_phrase


def handle(phrase):
    global session
    if len(set(phrase) & {'привет', 'хай', 'халоу', 'приветствовать', 'здравствуй', 'здравствуйте'}) != 0:
        greed()
        return

    if len(set(phrase) & {'уметь', 'функция', 'предназначение'}) != 0:
        skills()
        return

    if len(set(phrase) & {'пока', 'стоп'}) != 0:
        print('Жаль, что ты уходишь, пока!')
        exit(0)

    if len(set(phrase) & {'аллергия', 'веган'}) != 0:
        print(
            'Я немного знаю об альтернативном молоке! Возможно тебе понравится кокосовое, банановое или овсяное молоко)')
        return

    if (len(set(phrase) & {'нравиться', 'любить', 'вкусный'}) != 0
            and len(set(phrase) & {'он', 'оно', 'кофе'}) != 0):
        print('Просто обожаю!')
        return

    if len(set(phrase) & {'топинг', 'добавить'}) != 0:
        print('Я всем советую пить кофе без топингов, чтобы лучше узнать вкус и аромат кофе')
        print('(Если это не раф конечно)')
        return

    if (len(set(phrase) & {'рассказать', 'думать', 'написать', 'показать', 'знаешь', 'выпить'}) != 0
            and len(set(phrase) & {'всё', 'все', 'весь', 'список'}) != 0):
        show_all()
        return



    for i in range(len(cups)):
        if str(parser(cups[i]))[1:-1] in str(phrase)[1:-1]:
            if 'рассказать' in phrase:
                print_info(i)
                return

            if ('хотеть' in phrase and len(set(phrase) & {'узнать', 'спросить', 'услышать', 'изучить', 'почитать',
                                                          'расспросить'}) != 0):
                print_info(i)
                return
            session = i
            check_params(phrase)


    if (len(set(phrase) & {'думать', 'считать'}) != 0
            and len(set(phrase) & {'ты'}) != 0):
        thoughts()
        return

    if 'какой' in phrase or 'выпить' in phrase or 'кофе' in phrase:
        if len(set(phrase) & {'любой', 'рандомный', 'неважно', 'какойнибудь', 'случайный', 'незнаю', 'помогать',
                              'помощь'}) != 0:
            get_random()

    else:
        print('Я почитаю об этом вечером, спроси еще что нибудь..')



def greed():
    print('Хай! Меня зовут Кофеловер!')


def skills():
    print('Я не очень разговорчивый еще и только учусь, могу помочь выбрать для тебя кофе, рассказать ')
    print('о кофе которых я знаю, подсказать по характеристикам, топингам, молоке..')



def thoughts():
    print('Интересный вопрос, но понимаешь... все относительно.. мне нужно время подумать.. ')


def show_all():
    print('Я недавно в этом деле и знаю только про..')
    for i in range(len(coffee_file)):
        print(str(i + 1) + '. ' + coffee_file[i]['name'])


def get_random():
    i = random.randint(0, 50)
    print('Мне кажется, тебе бы подошел..')
    print_info(i)


def check_params(phrase):
    a = ''
    b = ''
    d = 0
    if len(set(phrase) & {'кислый', 'кислинка', 'кислотность'}) != 0:
        # a = morph.parse('кислый')[0]
        a = ' кислотность '
        b = ' кислый'
        d = float(coffee_file[session]['sourness']) * 10
        # print(d)

    if len(set(phrase) & {'ароматный', 'аромат', 'пахнуть', 'запах'}) != 0:
        # a = morph.parse('ароматный')[0]
        a = ' аромат '
        b = ' ароматный'
        d = int(coffee_file[session]['flavor']) // 10
        # print(d)

    if len(set(phrase) & {'мягкий', 'нежный', 'легкий', 'лаять'}) != 0:
        # a = morph.parse('мягкий')[0]
        b = ' мягкий '
        d = int(coffee_file[session]['sweetness']) // 10

    if len(set(phrase) & {'насыщенный', 'горький', 'крепкий', 'яркий'}) != 0:
        a = ' насыщенность '
        b = ' насыщенный'
        d = int(coffee_file[session]['mouthfeel']) // 10

    if d == 1 or d == 2 or d == 3:
        print('По моему мнению, этот кофе совсем не ' + b)
        return
    elif d == 4 or d == 5 or d == 6:
        print('Я думаю, что' + a + 'у этого кофе на среднем уровне')
        return
    elif d == 7 or d == 8 or d == 9:
        print('Да, пожалуй, кофе, которым ты интересуешься' + b)
        return

    if len(set(phrase) & {'степень', 'обжарка'}) != 0:
        d = coffee_file[session]["roast"]

    if d == 1:
        print('Этот кофе светлой обжарки')
        return
    elif d == 2:
        print('Этот кофе средней обжарки')
        return
    elif d == 3:
        print('Этот кофе сильной обжарки')
        return

    if (len(set(phrase) & {'молоко', 'сливки'}) != 0
            and len(set(phrase) & {'содержит', 'содержать', 'есть'}) != 0):
        if coffee_file[session]["milk"]:
            print('Да, в нем есть молоко')
        else:
            print('Нет, этот кофе без молока')


def print_info(i):
    global session
    session = i
    country = coffee_file[i]["country"]

    print(coffee_file[i]['name'] + ' произведен в ' + morph.parse(country)[0].inflect({'gent'}).word.title())


    print('Могу сказать что этот кофе..')
    if coffee_file[session]["milk"]:
        print('..с добавлением молока (ты всегда можешь использовать альтернативное)', end="")
    else:
        print('без молока, ', end="")
    roast = coffee_file[session]["roast"]
    if roast == 1:
        print(' обычно светлой обжарки,'),
    elif roast == 2:
        print(' обычно средней обжарки,'),
    elif roast == 3:
        print(' обычно сильной обжарки,'),

    sweetness = coffee_file[session]['sweetness'] // 10

    if sweetness == 1 or sweetness == 2 or sweetness == 3:
        print('не самый мягкий, но ', end=""),
    elif sweetness == 4 or sweetness == 5 or sweetness == 6:
        print('достаточно мягкий, но ', end=""),
    elif sweetness == 7 or sweetness == 8 or sweetness == 9:
        print('мягкий, даже нежный, но ', end=""),

    mouthfeel = coffee_file[session]['mouthfeel'] // 10
    if mouthfeel == 1 or mouthfeel == 2 or mouthfeel == 3:
        print('и не такой насыщенный. При этом,', end=""),
    elif mouthfeel == 4 or mouthfeel == 5 or mouthfeel == 6:
        print('и достаточно насыщенный. При этом,', end="")
    elif mouthfeel == 7 or mouthfeel == 8 or mouthfeel == 9:
        print(' очень насыщенный. При этом', end="")

    sourness = coffee_file[session]['sourness'] * 10
    if sourness == 1 or sourness == 2 or sourness == 3:
        print(' в нем почти нет кислинки.'),
    elif sourness == 4 or sourness == 5 or sourness == 6:
        print(' в нем есть сбалансированная кислинка.')
    elif sourness == 7 or sourness == 8 or sourness == 9:
        print(' кислинка в нем достаточно сильно выделяется.')
    print('Я считаю, это хорошие показатели, рекомендую попробовать)')


def main():
    p = True
    while p:
        string = input()
        norm_phrase = parser(string)
        handle(norm_phrase)


if __name__ == "__main__":
    main()