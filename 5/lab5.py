import random
import string
import time

import matplotlib.pyplot as plt


def naive_search(text: str, pattern: str) -> list[int]:
    n = len(text)
    m = len(pattern)
    if m == 0:
        return list(range(n + 1))

    positions = []
    for i in range(n - m + 1):
        if text[i : i + m] == pattern:
            positions.append(i)
    return positions


def boyer_moore_search(text: str, pattern: str) -> list[int]:
    n = len(text)
    m = len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    bad_char = {}
    for i, ch in enumerate(pattern):
        bad_char[ch] = i

    positions = []
    i = 0
    while i <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1

        if j < 0:
            positions.append(i)
            if i + m < n:
                i += m - bad_char.get(text[i + m], -1)
            else:
                i += 1
        else:
            i += max(1, j - bad_char.get(text[i + j], -1))

    return positions


def rabin_karp_search(text: str, pattern: str) -> list[int]:
    n = len(text)
    m = len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    base = 256
    mod = 1_000_000_007

    pattern_hash = 0
    window_hash = 0
    high_base = pow(base, m - 1, mod)

    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod

    positions = []

    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            if text[i : i + m] == pattern:
                positions.append(i)

        if i < n - m:
            window_hash = (
                base * (window_hash - ord(text[i]) * high_base) + ord(text[i + m])
            ) % mod

    return positions


def build_lps(pattern: str) -> list[int]:
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text: str, pattern: str) -> list[int]:
    n = len(text)
    m = len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    lps = build_lps(pattern)
    positions = []

    i = 0
    j = 0

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                positions.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return positions


def generate_test_text(n: int, pattern: str, insertions: int = 8) -> str:
    alphabet = string.ascii_lowercase + " "
    chars = [random.choice(alphabet) for _ in range(n)]

    m = len(pattern)
    if m == 0 or n < m:
        return "".join(chars)

    max_insertions = min(insertions, n - m + 1)
    positions = sorted(random.sample(range(0, n - m + 1), max_insertions))
    for pos in positions:
        chars[pos : pos + m] = pattern

    return "".join(chars)


def average_time(search_fn, text: str, pattern: str, repeats: int = 3) -> float:
    total = 0.0
    for _ in range(repeats):
        start = time.perf_counter()
        search_fn(text, pattern)
        total += time.perf_counter() - start
    return total / repeats


def demo_small_example() -> None:
    text = "aaaaa"
    pattern = "aa"

    print("Пример: text='aaaaa', pattern='aa'")
    print("Наивный:", naive_search(text, pattern))
    print("Бойер-Мур:", boyer_moore_search(text, pattern))
    print("Рабин-Карп:", rabin_karp_search(text, pattern))
    print("КМП:", kmp_search(text, pattern))
    print()


def benchmark_algorithms() -> None:
    pattern = "algorithm"
    sizes = [2000, 4000, 8000, 16000, 32000]

    methods = [
        ("Наивный", naive_search),
        ("Бойер-Мур", boyer_moore_search),
        ("Рабин-Карп", rabin_karp_search),
        ("КМП", kmp_search),
    ]

    results = {name: [] for name, _ in methods}

    print("Сравнение времени (среднее за 3 запуска):")
    print("n | Наивный | Бойер-Мур | Рабин-Карп | КМП")

    for n in sizes:
        text = generate_test_text(n, pattern)
        baseline = naive_search(text, pattern)

        for name, fn in methods[1:]:
            if fn(text, pattern) != baseline:
                raise ValueError(f"Ошибка: {name} дал другой результат для n={n}")

        line_values = [str(n)]
        for name, fn in methods:
            avg = average_time(fn, text, pattern, repeats=3)
            results[name].append(avg)
            line_values.append(f"{avg:.6f}")

        print(" | ".join(line_values))

    plt.figure(figsize=(9, 5))
    for name, _ in methods:
        plt.plot(sizes, results[name], marker="o", label=name)

    plt.xlabel("Длина текста")
    plt.ylabel("Среднее время (с)")
    plt.title("Лаб. 5: сравнение алгоритмов поиска подстроки")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main() -> None:
    random.seed(42)
    print("Лабораторная работа 5")
    print("Алгоритмы работы со строками: поиск подстроки")
    print()

    demo_small_example()
    benchmark_algorithms()


if __name__ == "__main__":
    main()
