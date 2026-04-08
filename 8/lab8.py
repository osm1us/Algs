import random
import time
import matplotlib.pyplot as plt


def brute_force_knapsack(items, capacity):
    n = len(items)
    best_value = 0
    best_weight = 0
    best_set = []

    for mask in range(1 << n):
        total_weight = 0
        total_value = 0
        chosen = []
        for i in range(n):
            if (mask >> i) & 1:
                name, weight, value = items[i]
                total_weight += weight
                total_value += value
                chosen.append(items[i])
        if total_weight <= capacity and total_value > best_value:
            best_value = total_value
            best_weight = total_weight
            best_set = chosen

    return best_set, best_weight, best_value


def greedy_knapsack(items, capacity):
    items_sorted = sorted(items, key=lambda x: x[2] / x[1], reverse=True)
    total_weight = 0
    total_value = 0
    chosen = []

    for item in items_sorted:
        name, weight, value = item
        if total_weight + weight <= capacity:
            chosen.append(item)
            total_weight += weight
            total_value += value

    return chosen, total_weight, total_value


def random_items(n):
    items = []
    for i in range(1, n + 1):
        weight = random.randint(1, 25)
        value = random.randint(10, 200)
        items.append((f"предмет_{i}", weight, value))
    return items


def demo():
    print("Задача 1. Рюкзак: полный перебор и жадный алгоритм")
    items = [
        ("A", 3, 25),
        ("B", 2, 20),
        ("C", 1, 15),
        ("D", 4, 40),
        ("E", 5, 50),
    ]
    capacity = 7

    brute_set, brute_w, brute_v = brute_force_knapsack(items, capacity)
    greedy_set, greedy_w, greedy_v = greedy_knapsack(items, capacity)

    print("Вместимость рюкзака:", capacity)
    print("Предметы (имя, вес, стоимость):", items)
    print("\nПолный перебор:")
    print("Выбрано:", brute_set)
    print("Вес:", brute_w, "Стоимость:", brute_v)
    print("\nЖадный:")
    print("Выбрано:", greedy_set)
    print("Вес:", greedy_w, "Стоимость:", greedy_v)


def benchmark():
    print("\nОценка времени")
    print("n | время полный перебор (с) | время жадный (с)")
    sizes = [8, 10, 12, 14, 16]
    brute_times = []
    greedy_times = []
    for n in sizes:
        items = random_items(n)
        capacity = max(10, int(sum(x[1] for x in items) * 0.4))

        t0 = time.perf_counter()
        brute_force_knapsack(items, capacity)
        t1 = time.perf_counter()

        t2 = time.perf_counter()
        greedy_knapsack(items, capacity)
        t3 = time.perf_counter()

        brute_elapsed = t1 - t0
        greedy_elapsed = t3 - t2
        brute_times.append(brute_elapsed)
        greedy_times.append(greedy_elapsed)
        print(f"{n} | {brute_elapsed:.6f} | {greedy_elapsed:.6f}")
    return sizes, brute_times, greedy_times


def main():
    random.seed(42)
    print("Лабораторная работа 8")
    print("Жадные алгоритмы")
    demo()
    sizes, brute_times, greedy_times = benchmark()
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, brute_times, marker="o", label="полный перебор")
    plt.plot(sizes, greedy_times, marker="o", label="жадный")
    plt.xlabel("n")
    plt.ylabel("время (с)")
    plt.title("Сравнение времени для задачи о рюкзаке")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
