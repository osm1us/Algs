import random
import time


def build_conflict_graph_from_jobs(job_requirements):
    jobs = list(job_requirements.keys())
    graph = {job: set() for job in jobs}
    for i in range(len(jobs)):
        for j in range(i + 1, len(jobs)):
            a = jobs[i]
            b = jobs[j]
            if job_requirements[a] & job_requirements[b]:
                graph[a].add(b)
                graph[b].add(a)
    return graph


def build_graph_from_pairs(vertices, bad_pairs):
    graph = {v: set() for v in vertices}
    for a, b in bad_pairs:
        graph[a].add(b)
        graph[b].add(a)
    return graph


def greedy_coloring(graph):
    order = sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)
    color = {}
    for v in order:
        used = {color[u] for u in graph[v] if u in color}
        c = 1
        while c in used:
            c += 1
        color[v] = c
    return color


def color_groups(coloring):
    groups = {}
    for v, c in coloring.items():
        groups.setdefault(c, []).append(v)
    return [groups[k] for k in sorted(groups.keys())]


def demo_task1():
    print("Задача 1. Распределение работ между механизмами")
    job_requirements = {
        "A": {"M1", "M2"},
        "B": {"M2"},
        "C": {"M3"},
        "D": {"M1"},
        "E": {"M3", "M4"},
        "F": {"M4"},
    }
    graph = build_conflict_graph_from_jobs(job_requirements)
    coloring = greedy_coloring(graph)
    groups = color_groups(coloring)

    print("Работы и механизмы:", job_requirements)
    print("Шаги выполнения (параллельные работы в одном шаге):")
    for i, group in enumerate(groups, 1):
        print(f"Шаг {i}: {group}")
    print("Всего шагов:", len(groups))


def demo_task2():
    print("\nЗадача 2. Размещение грузов по контейнерам")
    cargos = ["G1", "G2", "G3", "G4", "G5", "G6", "G7"]
    bad_pairs = [("G1", "G2"), ("G1", "G3"), ("G2", "G4"), ("G3", "G4"), ("G5", "G6")]
    graph = build_graph_from_pairs(cargos, bad_pairs)
    coloring = greedy_coloring(graph)
    groups = color_groups(coloring)

    print("Грузы:", cargos)
    print("Нельзя вместе:", bad_pairs)
    for i, group in enumerate(groups, 1):
        print(f"Контейнер {i}: {group}")
    print("Минимум контейнеров (жадная оценка):", len(groups))


def random_jobs(n_jobs, n_mechanisms):
    mechanisms = [f"M{i}" for i in range(1, n_mechanisms + 1)]
    req = {}
    for i in range(1, n_jobs + 1):
        k = random.randint(1, min(4, n_mechanisms))
        req[f"J{i}"] = set(random.sample(mechanisms, k))
    return req


def random_incompatibilities(n_vertices, p):
    vertices = [f"X{i}" for i in range(1, n_vertices + 1)]
    pairs = []
    for i in range(n_vertices):
        for j in range(i + 1, n_vertices):
            if random.random() < p:
                pairs.append((vertices[i], vertices[j]))
    return vertices, pairs


def benchmark_task1():
    print("\nОценка времени. Задача 1")
    print("n работ | время (с) | шагов")
    for n in [100, 200, 300, 400]:
        req = random_jobs(n, 30)
        t0 = time.perf_counter()
        graph = build_conflict_graph_from_jobs(req)
        coloring = greedy_coloring(graph)
        groups = color_groups(coloring)
        t1 = time.perf_counter()
        print(f"{n} | {t1 - t0:.6f} | {len(groups)}")


def benchmark_task2():
    print("\nОценка времени. Задача 2")
    print("n грузов | время (с) | контейнеров")
    for n in [100, 200, 300, 400]:
        vertices, pairs = random_incompatibilities(n, 0.05)
        t0 = time.perf_counter()
        graph = build_graph_from_pairs(vertices, pairs)
        coloring = greedy_coloring(graph)
        groups = color_groups(coloring)
        t1 = time.perf_counter()
        print(f"{n} | {t1 - t0:.6f} | {len(groups)}")


def main():
    random.seed(42)
    print("Лабораторная работа 9")
    print("Жадные алгоритмы (раскраска графа)")
    demo_task1()
    demo_task2()
    benchmark_task1()
    benchmark_task2()


if __name__ == "__main__":
    main()
