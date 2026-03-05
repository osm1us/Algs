import random
import time

import matplotlib.pyplot as plt


def gray_code_permutations(n):
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


def demo_task1():
    print("Задача 1. Перестановки 1..n (код Грэя)")

    n_demo = 4
    print(f"Пример для n={n_demo}:")
    for i, p in enumerate(gray_code_permutations(n_demo), 1):
        print(i, p)
    print()

    max_n = 9
    ns = list(range(1, max_n + 1))
    times = []

    print("Оценка времени:")
    for n in ns:
        t0 = time.perf_counter()
        count = 0
        for _ in gray_code_permutations(n):
            count += 1
        t1 = time.perf_counter()
        elapsed = t1 - t0
        times.append(elapsed)
        print(f"n={n:2d} перестановок={count:7d} время={elapsed:.6f} c")

    plt.figure(figsize=(8, 5))
    plt.plot(ns, times, marker="o", label="время")
    plt.xlabel("n")
    plt.ylabel("время (с)")
    plt.title("Время генерации перестановок (код Грэя)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


def random_perm_fisher_yates(n):
    arr = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def random_perm_sample(n):
    return random.sample(range(1, n + 1), n)


def random_perm_swaps(n):
    arr = list(range(1, n + 1))
    swaps = n * 3
    for _ in range(swaps):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def time_method(method, n, repeats):
    t0 = time.perf_counter()
    for _ in range(repeats):
        method(n)
    t1 = time.perf_counter()
    return t1 - t0


def demo_task2():
    print("Задача 2. Сравнение случайных перестановок")

    random.seed(42)
    sizes = [100, 200, 400, 800, 1200]
    methods = [
        ("Фишер-Йетс", random_perm_fisher_yates),
        ("random.sample", random_perm_sample),
        ("случайные обмены", random_perm_swaps),
    ]

    results = {name: [] for name, _ in methods}

    for n in sizes:
        repeats = max(5, 2000 // n)
        print(f"\nРазмер n={n}, повторов={repeats}")
        for name, method in methods:
            total = time_method(method, n, repeats)
            avg = total / repeats
            results[name].append(avg)
            print(f"{name}: среднее время {avg:.6f} c")

    plt.figure(figsize=(9, 5))
    for name, _ in methods:
        plt.plot(sizes, results[name], marker="o", label=name)
    plt.xlabel("n")
    plt.ylabel("среднее время (с)")
    plt.title("Сравнение генерации случайных перестановок")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    import sys

    print("Лабораторная 4. Генерация перестановок")

    task = 0
    if len(sys.argv) > 1:
        try:
            task = int(sys.argv[1])
        except ValueError:
            task = 0

    if task == 0:
        demo_task1()
        demo_task2()
    elif task == 1:
        demo_task1()
    elif task == 2:
        demo_task2()
    else:
        print("Неизвестный пункт. Использование: python lab4.py [0|1|2]")


if __name__ == "__main__":
    main()
