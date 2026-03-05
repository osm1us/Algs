import random
import time

import matplotlib.pyplot as plt


def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def gnome_sort(arr):
    i = 0
    n = len(arr)
    while i < n:
        if i == 0 or arr[i - 1] <= arr[i]:
            i += 1
        else:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            i -= 1
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def time_one(sort_fn, data):
    arr = data[:]
    start = time.perf_counter()
    sort_fn(arr)
    return time.perf_counter() - start


def test_size_growth():
    random.seed(42)
    sizes = [100, 200, 300, 400, 500]
    bubble_times = []
    gnome_times = []
    insertion_times = []

    for n in sizes:
        data = [random.randint(0, 1000) for _ in range(n)]
        bubble_times.append(time_one(bubble_sort, data))
        gnome_times.append(time_one(gnome_sort, data))
        insertion_times.append(time_one(insertion_sort, data))

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bubble_times, label="пузырек")
    plt.plot(sizes, gnome_times, label="гномья")
    plt.plot(sizes, insertion_times, label="вставками")
    plt.xlabel("n")
    plt.ylabel("время (с)")
    plt.title("Время сортировки от размера массива")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("Тест по размеру:")
    for n, bt, gt, it in zip(sizes, bubble_times, gnome_times, insertion_times):
        print(f"n={n:3d} пузырек={bt:.6f}c гномья={gt:.6f}c вставками={it:.6f}c")


def make_nearly_sorted(n, swaps=5):
    arr = list(range(n))
    for _ in range(swaps):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def test_ordered_vs_bad():
    random.seed(7)
    n = 200
    nearly = make_nearly_sorted(n, swaps=8)
    bad = list(range(n, 0, -1))

    nearly_bubble = time_one(bubble_sort, nearly)
    nearly_gnome = time_one(gnome_sort, nearly)
    nearly_insertion = time_one(insertion_sort, nearly)

    bad_bubble = time_one(bubble_sort, bad)
    bad_gnome = time_one(gnome_sort, bad)
    bad_insertion = time_one(insertion_sort, bad)

    print("\nТест порядка (почти отсортирован):")
    print(f"пузырек={nearly_bubble:.6f}c")
    print(f"гномья={nearly_gnome:.6f}c")
    print(f"вставками={nearly_insertion:.6f}c")

    print("\nТест порядка (обратно отсортирован):")
    print(f"пузырек={bad_bubble:.6f}c")
    print(f"гномья={bad_gnome:.6f}c")
    print(f"вставками={bad_insertion:.6f}c")

    labels = ["пузырек", "гномья", "вставками"]
    nearly_times = [nearly_bubble, nearly_gnome, nearly_insertion]
    bad_times = [bad_bubble, bad_gnome, bad_insertion]

    x = list(range(len(labels)))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar([i - width / 2 for i in x], nearly_times, width, label="почти отсортирован")
    plt.bar([i + width / 2 for i in x], bad_times, width, label="обратно отсортирован")
    plt.xticks(x, labels)
    plt.ylabel("время (с)")
    plt.title("Сравнение по порядку данных")
    plt.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    test_size_growth()
    test_ordered_vs_bad()


if __name__ == "__main__":
    main()
