import random
import time


def max_non_overlapping(intervals):
    intervals = sorted(intervals, key=lambda x: x[1])
    result = []
    last_end = float("-inf")
    for left, right in intervals:
        if left >= last_end:
            result.append((left, right))
            last_end = right
    return result


def max_requests(requests):
    requests = sorted(requests, key=lambda x: x[2])
    result = []
    last_end = float("-inf")
    for req_id, start, end in requests:
        if start >= last_end:
            result.append((req_id, start, end))
            last_end = end
    return result


def min_cover_segments(segments, left_border, right_border):
    segments = sorted(segments, key=lambda x: (x[0], x[1]))
    i = 0
    n = len(segments)
    current = left_border
    result = []

    while current < right_border:
        best_right = current
        best_segment = None
        while i < n and segments[i][0] <= current:
            if segments[i][1] > best_right:
                best_right = segments[i][1]
                best_segment = segments[i]
            i += 1
        if best_segment is None:
            return None
        result.append(best_segment)
        current = best_right

    return result


def random_intervals(n, max_coord=100000):
    intervals = []
    for _ in range(n):
        a = random.randint(0, max_coord - 1)
        b = random.randint(a + 1, max_coord)
        intervals.append((a, b))
    return intervals


def random_requests(n, max_time=50000):
    requests = []
    for i in range(1, n + 1):
        start = random.randint(0, max_time - 1)
        end = random.randint(start + 1, max_time)
        requests.append((i, start, end))
    return requests


def random_covering_segments(n, left_border, right_border):
    segments = []
    current = left_border
    step = max(1, (right_border - left_border) // max(2, n // 3))
    while current < right_border:
        nxt = min(right_border, current + random.randint(step, step * 2))
        start = max(left_border, current - random.randint(0, step))
        segments.append((start, nxt))
        current = nxt
    while len(segments) < n:
        a = random.randint(left_border, right_border - 1)
        b = random.randint(a + 1, right_border + step)
        segments.append((a, b))
    return segments


def benchmark_task1():
    print("\nОценка времени. Задача 1")
    print("n | время (с) | выбрано")
    for n in [1000, 2000, 4000, 8000]:
        intervals = random_intervals(n)
        t0 = time.perf_counter()
        ans = max_non_overlapping(intervals)
        t1 = time.perf_counter()
        print(f"{n} | {t1 - t0:.6f} | {len(ans)}")


def benchmark_task2():
    print("\nОценка времени. Задача 2")
    print("n | время (с) | принято заявок")
    for n in [1000, 2000, 4000, 8000]:
        requests = random_requests(n)
        t0 = time.perf_counter()
        ans = max_requests(requests)
        t1 = time.perf_counter()
        print(f"{n} | {t1 - t0:.6f} | {len(ans)}")


def benchmark_task3():
    print("\nОценка времени. Задача 3")
    print("n | время (с) | отрезков в покрытии")
    left_border = 0
    right_border = 10000
    for n in [1000, 2000, 4000, 8000]:
        segments = random_covering_segments(n, left_border, right_border)
        t0 = time.perf_counter()
        ans = min_cover_segments(segments, left_border, right_border)
        t1 = time.perf_counter()
        count = len(ans) if ans is not None else 0
        print(f"{n} | {t1 - t0:.6f} | {count}")


def demo_task1():
    print("Задача 1. Максимальное множество непересекающихся отрезков")
    intervals = [(1, 3), (2, 5), (4, 6), (6, 7), (5, 9), (8, 10)]
    ans = max_non_overlapping(intervals)
    print("Исходные отрезки:", intervals)
    print("Выбранные отрезки:", ans)
    print("Количество:", len(ans))


def demo_task2():
    print("\nЗадача 2. Максимальное количество заявок")
    requests = [
        (1, 9, 10),
        (2, 9, 12),
        (3, 10, 11),
        (4, 11, 13),
        (5, 13, 14),
        (6, 12, 15),
    ]
    ans = max_requests(requests)
    print("Заявки (id, start, end):", requests)
    print("Принятые заявки:", ans)
    print("Количество:", len(ans))


def demo_task3():
    print("\nЗадача 3. Минимальное покрытие интервала")
    left_border = 2
    right_border = 12
    segments = [(1, 4), (3, 6), (5, 8), (7, 11), (10, 13), (2, 5), (8, 12)]
    ans = min_cover_segments(segments, left_border, right_border)
    print("Границы:", (left_border, right_border))
    print("Отрезки:", segments)
    print("Покрытие:", ans)
    print("Количество:", len(ans) if ans else 0)


def main():
    random.seed(42)
    print("Лабораторная работа 6")
    print("Жадные алгоритмы")
    demo_task1()
    demo_task2()
    demo_task3()
    benchmark_task1()
    benchmark_task2()
    benchmark_task3()


if __name__ == "__main__":
    main()
