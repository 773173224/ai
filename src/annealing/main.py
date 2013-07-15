# -*- coding: utf8 -*-
#
# Алгоритм отжига
# Задача о расстановке ферзей
#
# Simulated Annealing Implementation for the n-Queens Problem
from copy import copy
from math import exp
import random

MAX_LENGTH = 20  # Размер поля

INITIAL_TEMPERATURE = 30.  # Начальная температура
FINAL_TEMPERATURE = 0.5  # Конечная температура
ALPHA = 0.99  # Коэфициент изменения температуры
STEPS_PER_CHANGE = 100  # Кол. интераций перед изменением температуры


class Board(list):
    """
    Класс поля
    """
    def __init__(self, solution=None):
        super(Board, self).__init__()

        for i in range(MAX_LENGTH):
            self.append([0] * MAX_LENGTH)

        if solution:
            self.apply(solution)

    def apply(self, solution):
        for x in range(MAX_LENGTH):
            y = solution[x]
            self[x][y] = 1

    def draw(self):
        for row in self:
            for i in row:
                if i:
                    print 'o',
                else:
                    print '.',
            print


class Solution(list):
    """
    Вариант решения. Список длинной MAX_LENGTH.
    Каждый элемент указывает строку размещения ферзя в i-й колонке.
    """
    dx = (-1, 1, -1, 1)
    dy = (-1, 1, 1, -1)

    def __init__(self):
        self.energy = 0
        super(Solution, self).__init__(range(MAX_LENGTH))
        random.shuffle(self)
        self.calculate_energy()

    def tweak(self):
        """
        Меняем местами две колонки для получения нового решения.
        """
        i1 = random.randint(0, MAX_LENGTH - 1)
        i2 = random.randint(0, MAX_LENGTH - 1)

        while i1 == i2:
            i2 = random.randint(0, MAX_LENGTH - 1)

        self[i1], self[i2] = self[i2], self[i1]
        self.calculate_energy()

    def calculate_energy(self):
        board = Board(self)
        conflicts = 0

        for x in range(MAX_LENGTH):
            y = self[x]

            # Проверяем диагонали
            for i in range(4):
                tx, ty, dx, dy = x, y, self.dx[i], self.dy[i]

                while True:
                    tx += dx
                    ty += dy

                    if tx < 0 or ty < 0 or tx >= MAX_LENGTH or ty >= MAX_LENGTH:
                        break

                    if board[tx][ty]:
                        conflicts += 1

        self.energy = conflicts

if __name__ == "__main__":
    print u'Пример решения задачи размешения ферзей на шаматном поле без конфликтов'
    print u'методом отжига'
    print
    print u'Размер поля:', MAX_LENGTH
    print u'Начальная температура:', INITIAL_TEMPERATURE
    print u'Конечная температура:', FINAL_TEMPERATURE
    print u'Коэфициент изменения температуры:', ALPHA
    print u'Кол. интераций перед изменением температуры:', STEPS_PER_CHANGE
    print
    print u'NOTE: При вычислении отображается текущая итерация, температура, '
    print u'энергия(кол. конфликтов) и кол. принятых худших решений'
    raw_input(u'<ENTER>')

    best = Solution()
    temperature = INITIAL_TEMPERATURE
    timer = 0

    while temperature > FINAL_TEMPERATURE:
        timer += 1
        accepted = 0  # Кол. принятых худших решений
        current = copy(best)
        working = copy(current)
        
        for i in xrange(STEPS_PER_CHANGE):
            use_new = False
            working.tweak()

            if working.energy <= current.energy:
                use_new = True
                if working.energy < best.energy:
                    best = copy(working)
            else:
                delta = working.energy - current.energy
                if random.random() < exp(-delta / temperature):
                    accepted += 1
                    use_new = True

            if use_new:
                current = copy(working)
            else:
                working = copy(current)

        print '%s: t: %.02f Энергия: %s Принято худших: %s' % (timer, temperature, best.energy, accepted)

        if best.energy == 0:
            break
        temperature *= ALPHA

    board = Board(best)
    board.draw()
    print 'Энергия(кол. конфликтов): %s' % best.energy
