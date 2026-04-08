import random
import time


def schedule_orders(orders, days):
    orders = sorted(orders, key=lambda x: x[1], reverse=True)
    slots = [None] * (days + 1)
    total_profit = 0

    for order_id, price, deadline in orders:
        d = min(deadline, days)
        while d >= 1:
            if slots[d] is None:
                slots[d] = (order_id, price, deadline)
                total_profit += price
                break
            d -= 1

    selected = [slots[d] for d in range(1, days + 1) if slots[d] is not None]
    return selected, total_profit


def min_children_groups(children):
    children = sorted(children, key=lambda x: x[1])
    groups = []
    i = 0
    n = len(children)

    while i < n:
        start_age = children[i][1]
        group = [children[i]]
        i += 1
        while i < n and children[i][1] - start_age <= 2:
            group.append(children[i])
            i += 1
        groups.append(group)

    return groups


def random_orders(n, days):
    orders = []
    for i in range(1, n + 1):
        price = random.randint(10, 2000)
        deadline = random.randint(1, days)
        orders.append((i, price, deadline))
    return orders


def random_children(n):
    children = []
    for i in range(1, n + 1):
        age = random.randint(5, 15)
        children.append((i, age))
    return children


def demo_task1():
    print("Задача 1. Заказы с дедлайнами")
    days = 5
    orders = [
        (1, 100, 2),
        (2, 19, 1),
        (3, 27, 2),
        (4, 25, 1),
        (5, 15, 3),
        (6, 90, 4),
    ]
    selected, total = schedule_orders(orders, days)
    print("Дней:", days)
    print("Заказы (id, стоимость, дедлайн):", orders)
    print("Выбранные заказы:", selected)
    print("Суммарная стоимость:", total)


def demo_task2():
    print("\nЗадача 2. Минимум групп по возрасту")
    children = [(1, 6), (2, 7), (3, 9), (4, 10), (5, 12), (6, 12), (7, 13)]
    groups = min_children_groups(children)
    print("Дети (id, возраст):", children)
    print("Количество групп:", len(groups))
    for i, group in enumerate(groups, 1):
        print(f"Группа {i}: {group}")


def benchmark_task1():
    print("\nОценка времени. Задача 1")
    print("n | дни | время (с) | выбрано")
    for n in [1000, 2000, 4000, 8000]:
        days = max(10, n // 5)
        orders = random_orders(n, days)
        t0 = time.perf_counter()
        selected, _ = schedule_orders(orders, days)
        t1 = time.perf_counter()
        print(f"{n} | {days} | {t1 - t0:.6f} | {len(selected)}")


def benchmark_task2():
    print("\nОценка времени. Задача 2")
    print("n | время (с) | групп")
    for n in [1000, 2000, 4000, 8000, 16000]:
        children = random_children(n)
        t0 = time.perf_counter()
        groups = min_children_groups(children)
        t1 = time.perf_counter()
        print(f"{n} | {t1 - t0:.6f} | {len(groups)}")


def main():
    random.seed(42)
    print("Лабораторная работа 7")
    print("Жадные алгоритмы")
    demo_task1()
    demo_task2()
    benchmark_task1()
    benchmark_task2()


if __name__ == "__main__":
    main()
