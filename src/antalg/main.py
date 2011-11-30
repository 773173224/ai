# -*- coding: utf8 -*-
#
# Ant Algorithm Demonstration
#
# Задача коммивожера
# Алгоритм муравья

from math import sqrt
from random import randint, random
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import numpy as np

MAX_CITIES = 15
MAX_DISTANCE = 100
MAX_TOUR = MAX_CITIES * MAX_DISTANCE
MAX_TOURS = 500
MAX_TIME = MAX_TOURS * MAX_CITIES
INIT_PHEROMONE = 1.0 / MAX_CITIES

MAX_ANTS = 20
ALPHA = 1.  # вес фермента
BETA = 5.  # коэффициент эвристики, влияние априорных знаний(1/d, где d - растояние)
RHO = 0.5  # Интенсивность. Коф. испарение равен 1 - RHO. По результатам тестов лучше использовать >= 0.5
QVAL = 100  # Кол. феромонов на один проход


class City(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ant(object):

    def __init__(self, start_city):
        self.cur_city = start_city
        self.path = [start_city]
        self.tour_length = 0.

    def move_to_city(self, city):
        global DISTANCE, MAX_CITIES
        self.path.append(city)
        self.tour_length += DISTANCE[self.cur_city][city]
        if len(self.path) == MAX_CITIES:
            self.tour_length += DISTANCE[self.path[-1]][self.path[0]]
        self.cur_city = city

    def can_move(self):
        global MAX_CITIES
        return len(self.path) < MAX_CITIES

    def reset(self, city):
        self.cur_city = city
        self.path = [city]
        self.tour_length = 0.


ANTS = []  # [MAX_ANTS]
CITIES = []  # [MAX_CITIES]
DISTANCE = []  # [MAX_CITIES][MAX_CITIES]
PHEROMONE = []  # [MAX_CITIES][MAX_CITIES]
BEST = MAX_TOUR
BEST_ANT = None


def init():
    global DISTANCE, PHEROMONE, CITIES, ANTS
    DISTANCE = [[0.] * MAX_CITIES] * MAX_CITIES
    PHEROMONE = [[INIT_PHEROMONE] * MAX_CITIES] * MAX_CITIES

    for i in range(MAX_CITIES):
        CITIES.append(City(randint(0, MAX_DISTANCE), randint(0, MAX_DISTANCE)))

    # calculate distance
    for i in range(MAX_CITIES):
        for j in range(MAX_CITIES):
            if i != j and DISTANCE[i][j] == 0.:
                xd = CITIES[i].x - CITIES[j].x
                yd = CITIES[i].y - CITIES[j].y
                distance = sqrt(xd * xd + yd * yd)
                DISTANCE[i][j], DISTANCE[j][i] = distance, distance

    # create ants
    to = 0
    for i in range(MAX_ANTS):
        ANTS.append(Ant(to))
        to += 1
        to = to % MAX_CITIES


def ant_product(from_city, to_city):
    global DISTANCE, PHEROMONE, ALPHA, BETA

    return (PHEROMONE[from_city][to_city] ** ALPHA) * \
         ((1. / DISTANCE[from_city][to_city]) ** BETA)


def select_next_city(ant):
    global MAX_CITIES
    denom = 0.
    not_visited = []

    for to in range(MAX_CITIES):
        if to not in ant.path:
            not_visited.append(to)
            denom += ant_product(ant.cur_city, to)

    assert not_visited

    i = 0
    while True:
        p = ant_product(ant.cur_city, not_visited[i]) / denom
        if random() < p:
            return not_visited[i]
        i += 1
        i = i % len(not_visited)


def simulate_ants():
    global ANTS, MAX_CITIES
    moving = 0

    for ant in ANTS:
        if ant.can_move():
            ant.move_to_city(select_next_city(ant))
            moving += 1

    return moving


def update_trails():
    global MAX_CITIES, PHEROMONE, RHO, INIT_PHEROMONE, ANTS

    # pheromone evaporation
    for i in range(MAX_CITIES):
        for j in range(MAX_CITIES):
            if i != j:
                PHEROMONE[i][j] *= (1. - RHO)
                if PHEROMONE[i][j] < 0:
                    PHEROMONE[i][j] = INIT_PHEROMONE

    # add new pheromone
    for ant in ANTS:
        for i in range(MAX_CITIES):
            if i == MAX_CITIES - 1:
                from_city = ant.path[i]
                to_city = ant.path[0]
            else:
                from_city = ant.path[i]
                to_city = ant.path[i + 1]

            PHEROMONE[from_city][to_city] += QVAL / ant.tour_length
            PHEROMONE[to_city][from_city] = PHEROMONE[from_city][to_city]

    for i in range(MAX_CITIES):
        for j in range(MAX_CITIES):
            PHEROMONE[i][j] *= RHO


def restart_ants():
    global ANTS, BEST, BEST_ANT, MAX_CITIES
    to = 0

    for ant in ANTS:
        if ant.tour_length < BEST:
            BEST = ant.tour_length
            BEST_ANT = ant

        ant.reset(to)
        to += 1
        to = to % MAX_CITIES

if __name__ == '__main__':
    init()
    cur_time = 0
    while cur_time < MAX_TIME:
        cur_time += 1
        if cur_time % 1000 == 0:
            print 'time:', cur_time

        if simulate_ants() == 0:
            update_trails()
            cur_time != MAX_TIME and restart_ants()

    x, y = [], []
    for i in BEST_ANT.path:
        city = CITIES[i]
        x.append(city.x / float(MAX_DISTANCE))
        y.append(city.y / float(MAX_DISTANCE))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x = np.array(x)
    y = np.array(y)
    line = lines.Line2D(x, y, mfc='red', ms=12, marker='o')
    ax.add_line(line)
    plt.show()
