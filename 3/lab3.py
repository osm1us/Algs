#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math

def next_perm_narayana(a):
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i < 0:
        return False
    j = n - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    a[i + 1 :] = reversed(a[i + 1 :])
    return True

def gen_narayana(n):
    a = list(range(1, n + 1))
    yield a[:]
    while next_perm_narayana(a):
        yield a[:]

def gen_johnson_trotter(n):
    perm = list(range(1, n + 1))
    direction = [-1] * n
    yield perm[:]

    def mobile_index():
        idx = -1
        for i in range(n):
            v = perm[i]
            d = direction[v - 1]
            ni = i + d
            if 0 <= ni < n and perm[ni] < v:
                if idx < 0 or perm[i] > perm[idx]:
                    idx = i
        return idx

    while True:
        mi = mobile_index()
        if mi < 0:
            break
        v = perm[mi]
        d = direction[v - 1]
        ni = mi + d
        perm[mi], perm[ni] = perm[ni], perm[mi]
        for x in range(v + 1, n + 1):
            direction[x - 1] *= -1
        yield perm[:]

def gen_inversion_vectors(n):
    if n == 0:
        yield []
        return
    code = [0] * n
    max_val = list(range(n, 0, -1))

    while True:
        elems = list(range(1, n + 1))
        perm = [elems.pop(c) for c in code]
        yield perm
        i = n - 1
        while i >= 0 and code[i] == max_val[i] - 1:
            code[i] = 0
            i -= 1
        if i < 0:
            break
        code[i] += 1

def demo_task1():
    print("Задача 1. Перестановки 1..n")

    n = 4
    print(f"n = {n}. Перестановки (Нарайана):")
    perms = list(gen_narayana(n))
    for i, p in enumerate(perms, 1):
        print(i, p)
    print("Всего:", len(perms))

    print("\nОценка времени для n = 8 (пример):")
    for name, gen in [
        ("Нарайана", gen_narayana),
        ("Джонсон-Троттер", gen_johnson_trotter),
        ("Инверсии", gen_inversion_vectors),
    ]:
        t0 = time.perf_counter()
        count = sum(1 for _ in gen(8))
        t1 = time.perf_counter()
        print(f"{name}: {count} перестановок, {t1 - t0:.4f} c")
    print()

def unique_permutations(seq):
    a = sorted(seq)
    yield a[:]
    while True:
        if not next_perm_narayana(a):
            break
        yield a[:]

def demo_task2():
    print("Задача 2. Уникальные перестановки мультимножества")

    for seq, label in [([1, 2, 1], "121"), ([1, 2, 3], "123")]:
        print(f"\nПоследовательность: {label}")
        perms = list(unique_permutations(seq))
        for p in perms:
            print("".join(map(str, p)))
        print("Всего уникальных:", len(perms))
    print()

def all_subsets(elements):
    n = len(elements)
    for mask in range(1, 1 << n):
        yield [elements[i] for i in range(n) if (mask >> i) & 1]

def demo_task3():
    print("Задача 3. Все варианты выборки")

    elements = ["стол", "стул", "шкаф"]
    print("Элементы:", elements)
    print("Подмножества по размеру:")
    for size in range(1, len(elements) + 1):
        subs = [s for s in all_subsets(elements) if len(s) == size]
        print("по", size, ":", subs)
    print()

def buy_max_items(budget, wishlist, prices):
    items = []
    for name, qty in wishlist:
        if name in prices and qty > 0 and prices[name] > 0:
            items.append((name, prices[name], qty))
    items.sort(key=lambda x: x[1])

    bought = {}
    rem = budget

    for name, price, max_qty in items:
        if price <= rem and name not in bought:
            bought[name] = [1, price]
            rem -= price

    for name, price, max_qty in items:
        if name not in bought:
            continue
        qty, cost = bought[name]
        add = min(max_qty - qty, int(rem / price))
        if add > 0:
            bought[name][0] += add
            bought[name][1] += add * price
            rem -= add * price

    result = [(name, data[0], data[1]) for name, data in bought.items()]
    return result, rem

def demo_task4():
    print("Задача 4. Покупка канцелярии")

    wishlist = [
        ("Ручка", 3),
        ("Блокнот", 2),
        ("Маркер", 5),
        ("Линейка", 1),
    ]
    prices = {
        "Ручка": 2.5,
        "Блокнот": 5.0,
        "Маркер": 1.2,
        "Линейка": 0.9,
    }
    budget = 15.0

    print("Бюджет:", budget, "руб.")
    print("Список:")
    for name, qty in wishlist:
        print(f"{name}: {qty} шт. по {prices[name]} руб.")

    chosen, remainder = buy_max_items(budget, wishlist, prices)

    print("\nРезультат:")
    print("Наименований куплено:", len(chosen))
    for name, qty, cost in chosen:
        print(f"{name}: {qty} шт., всего {cost:.2f} руб.")
    print("Остаток:", f"{remainder:.2f}", "руб.")
    print()

def main():
    import sys
    print("Лабораторная 3. Генерация перестановок")

    task = 0
    if len(sys.argv) > 1:
        try:
            task = int(sys.argv[1])
        except ValueError:
            task = 0

    if task == 0:
        demo_task1()
        demo_task2()
        demo_task3()
        demo_task4()
    elif task == 1:
        demo_task1()
    elif task == 2:
        demo_task2()
    elif task == 3:
        demo_task3()
    elif task == 4:
        demo_task4()
    else:
        print("Неизвестный пункт. Использование: python lab3.py [0|1|2|3|4]")


if __name__ == "__main__":
    main()
