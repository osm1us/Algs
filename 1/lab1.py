import time

import matplotlib.pyplot as plt


def fib_rec(n, counter=None):
    if counter is not None:
        counter[0] += 1
    if n <= 1:
        return n
    return fib_rec(n - 1, counter) + fib_rec(n - 2, counter)


def fib_iter(n):
    if n <= 1:
        return n, 0
    a = 0
    b = 1
    iterations = 0
    for _ in range(2, n + 1):
        iterations += 1
        a, b = b, a + b
    return b, iterations


def measure_times(max_n):
    ns = list(range(max_n + 1))
    rec_times = []
    iter_times = []
    rec_calls = []
    iter_steps = []

    for n in ns:
        rec_counter = [0]
        start = time.perf_counter()
        fib_rec(n, rec_counter)
        rec_times.append(time.perf_counter() - start)
        rec_calls.append(rec_counter[0])

        start = time.perf_counter()
        _, steps = fib_iter(n)
        iter_times.append(time.perf_counter() - start)
        iter_steps.append(steps)

    return ns, rec_times, iter_times, rec_calls, iter_steps


def main():
    max_n = 40
    example_n = 10
    rec_counter = [0]
    rec_value = fib_rec(example_n, rec_counter)
    iter_value, iter_steps = fib_iter(example_n)

    print(f"рекурсивный алгоритм {rec_value}")
    print(f"итерационный алгоритм ({iter_value}, {iter_steps})")

    ns, rec_times, iter_times, rec_calls, iter_steps = measure_times(max_n)

    print("n | t_рек | t_ит | вызовы_рек | итерации")
    for n, rt, it, rc, ii in zip(ns, rec_times, iter_times, rec_calls, iter_steps):
        print(f"{n:2d} | {rt:.6f} | {it:.6f} | {rc:10d} | {ii:10d}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(ns, rec_times, label="рекурсивный")
    axes[0].plot(ns, iter_times, label="итерационный")
    axes[0].set_xlabel("n")
    axes[0].set_ylabel("время (с)")
    axes[0].set_title("Зависимость времени от n")
    axes[0].grid(True, linestyle="--", alpha=0.4)
    axes[0].legend()

    axes[1].plot(ns, rec_calls, label="вызовы рекурсии")
    axes[1].plot(ns, iter_steps, label="итерации")
    axes[1].set_xlabel("n")
    axes[1].set_ylabel("количество")
    axes[1].set_title("Вызовы/итерации от n")
    axes[1].grid(True, linestyle="--", alpha=0.4)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
