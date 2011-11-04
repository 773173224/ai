# -*- coding: utf8 -*-
#
# Пример использования нейронной сети для распознавания цифр
# В test.py более интересный пример работы

from network import NeuralNetwork

LEARNING_RATE = 0.1
MOMENTUM_RATE = 0.8

data = [
    {
        'output': [1, 0, 0],
        'input': (
            1,1,1,1,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,1,1,1,1
        )
    },
    {
        'output': [0, 1, 0],
        'input': (
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1
        )
    },
    {
        'output': [0, 0, 1],
        'input': (
            0,1,1,1,1,
            0,0,0,0,1,
            0,0,0,1,0,
            0,0,1,0,0,
            0,1,0,0,0,
            1,0,0,0,0,
            1,1,1,1,1
        )
    },
]


def format(l):
    return ['%.2f' % i for i in l]

if __name__ == "__main__":
    FIRST_LAYER = 5 * 7
    SECOND_LAYER = 14
    OUTPUT_LAYER = 3
    print u'LEARNING_RATE', LEARNING_RATE
    print u'MOMENTUM_RATE', MOMENTUM_RATE
    print u'При вычислении отображается текущая среднеквадратичная ошибка'
    raw_input(u'<ENTER>')
    network = NeuralNetwork((FIRST_LAYER, SECOND_LAYER, OUTPUT_LAYER), learning_rate=LEARNING_RATE, momentum=MOMENTUM_RATE)
    network.teach(data, 10000)

    print u'Проверка обучения'
    for item in data:
        print format(network.calculate(item['input'])), format(item['output'])
