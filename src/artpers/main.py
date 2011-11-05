# -*- coding: utf8 -*-
# Application of ART (Adaptive Resonance Theory) to personalization.
#
# Кластеризация данных о покупателях и выдача рекомендаций
import random

MAX_ITEMS = 15
MAX_CUSTOMERS = 20
TOTAL_PROTOTYPE_VECTORS = 5

BETA = 1.0  # Бета-параметр. Разме кластера
VIGILANCE = 0.9  # 0 <= VIGILANCE < 1. Параметр внимательности

DATABASE = []
PROTOTYPES = []

VERBOSITY = False


def bit_wise_and(v1, v2):
    return Vector([item[0] & item[1] for item in zip(v1, v2)])


class Vector(list):

    def __init__(self, init=None, rand=False):
        if not init:
            if rand:
                init = [random.randint(0, 1) for _ in range(MAX_ITEMS)]
            else:
                init = [0] * MAX_ITEMS

        super(Vector, self).__init__(init)

    def __eq__(self, other):
        return self.id == other.id

    @property
    def magn(self):
        """
        magnitude
        """
        for i in self:
            assert i <= 1

        return float(sum(self))


class Prototype(Vector):
    _id = 0

    def __init__(self, customer):
        Prototype._id += 1
        self.id = self._id
        super(Prototype, self).__init__(list(customer))
        self.customers = []
        self.changed = False
        self.add_customer(customer)

    def __repr__(self):
        l = super(Prototype, self).__repr__()
        return 'p#%2i %s' % (self.id, l)

    def add_customer(self, customer):
        if customer.cluster and customer.cluster == self:
            return

        if customer.cluster:
            customer.cluster.remove_customer(customer)

        self.customers.append(customer)
        customer.cluster = self
        self.update()

    def remove_customer(self, customer):
        self.customers.remove(customer)
        customer.cluster = None

        if not self.customers:
            PROTOTYPES.remove(self)
        else:
            self.update()

    def update(self):
        v = zip(*self.customers)

        for i, row in enumerate(v):
            self[i] = reduce(lambda a, b: a & b, row)

    @property
    def sum_vector(self):
        v = zip(*self.customers)
        return [sum(item) for item in v]


class Customer(Vector):
    _id = 0

    def __init__(self, *args, **kwargs):
        Customer._id += 1
        self.id = self._id
        super(Customer, self).__init__(*args, **kwargs)
        self.cluster = None

    def __repr__(self):
        l = super(Customer, self).__repr__()
        return 'c#%2i %s' % (self.id, l)

    def recomedation(self):
        if not self.cluster:
            return None

        max_val = -1
        recomedation = []

        for i, item in enumerate(self.cluster.sum_vector):
            if not self[i]:
                if item > max_val:
                    max_val = item
                    recomedation = [i]
                elif item == max_val:
                    recomedation.append(i)

        return recomedation


def init():
    for i in range(MAX_CUSTOMERS):
        DATABASE.append(Customer(rand=True))


def performART1():
    done = False
    count = 50

    while not done:
        done = True

        for customer in DATABASE:
            # Пытаемся найти подходящий кластер
            for prototype in PROTOTYPES:
                if customer.cluster and customer.cluster == prototype:
                    continue

                and_result = bit_wise_and(customer, prototype)
                result = and_result.magn / (BETA + prototype.magn)
                test = customer.magn / (BETA + MAX_ITEMS)

                # Проверка на схожесть
                if result > test:
                    # Тест на внимательность
                    if and_result.magn / customer.magn < VIGILANCE:
                        if customer.cluster and VERBOSITY:
                            print u'Customer #%s moved from cluster #%s to #%s' % \
                                (customer.id, customer.cluster.id, prototype.id)
                        elif VERBOSITY:
                            print u'Customer #%s appended to cluster #%s' % \
                                (customer.id, prototype.id)

                        done = False
                        prototype.add_customer(customer)

            # Создаем новый кластер для неопределенного вектора
            if not customer.cluster:
                done = False
                if len(PROTOTYPES) < TOTAL_PROTOTYPE_VECTORS:
                    if VERBOSITY:
                        print u'Created new cluster for customer #%s' % customer.id
                    new_prototype = Prototype(customer)
                    PROTOTYPES.append(new_prototype)

        count -= 1
        if count <= 0:
            break


if __name__ == "__main__":
    init()
    performART1()

    for prototype in PROTOTYPES:
        print prototype
        print '-------------------------------'
        for c in prototype.customers:
            print c, c.recomedation()
        print
