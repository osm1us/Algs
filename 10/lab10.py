import heapq
import random
import time
from collections import Counter


class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right


def build_huffman_tree(text):
    freq = Counter(text)
    heap = []
    uid = 0
    for ch, count in freq.items():
        heapq.heappush(heap, (count, uid, Node(count, char=ch)))
        uid += 1

    if len(heap) == 1:
        count, node_id, node = heapq.heappop(heap)
        root = Node(count, left=node)
        return root

    while len(heap) > 1:
        f1, id1, n1 = heapq.heappop(heap)
        f2, id2, n2 = heapq.heappop(heap)
        parent = Node(f1 + f2, left=n1, right=n2)
        heapq.heappush(heap, (parent.freq, uid, parent))
        uid += 1

    return heap[0][2]


def build_codes(root):
    codes = {}

    def walk(node, prefix):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = prefix if prefix else "0"
            return
        walk(node.left, prefix + "0")
        walk(node.right, prefix + "1")

    walk(root, "")
    return codes


def encode_text(text, codes):
    return "".join(codes[ch] for ch in text)


def decode_text(encoded, root):
    result = []
    node = root
    for bit in encoded:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node.char is not None:
            result.append(node.char)
            node = root
    return "".join(result)


def demo():
    text = "алгоритмы и анализ сложности"
    root = build_huffman_tree(text)
    codes = build_codes(root)
    encoded = encode_text(text, codes)
    decoded = decode_text(encoded, root)

    print("Лабораторная работа 10")
    print("Код Хаффмана")
    print("Исходный текст:", text)
    print("\nСловарь кодов:")
    for ch in sorted(codes.keys()):
        print(f"'{ch}': {codes[ch]}")
    print("\nДлина исходного в битах (8 бит на символ):", len(text) * 8)
    print("Длина после кодирования:", len(encoded))
    print("Закодированный текст:", encoded)
    print("Восстановленный текст:", decoded)
    print("Совпадение:", decoded == text)


def random_text(n):
    alphabet = "оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъ "
    return "".join(random.choice(alphabet) for _ in range(n))


def benchmark():
    print("\nОценка времени")
    print("n | построение+коды (с) | кодирование (с) | декодирование (с)")
    for n in [1000, 5000, 10000, 20000, 50000]:
        text = random_text(n)

        t0 = time.perf_counter()
        root = build_huffman_tree(text)
        codes = build_codes(root)
        t1 = time.perf_counter()

        t2 = time.perf_counter()
        encoded = encode_text(text, codes)
        t3 = time.perf_counter()

        t4 = time.perf_counter()
        decoded = decode_text(encoded, root)
        t5 = time.perf_counter()

        ok = decoded == text
        print(f"{n} | {t1 - t0:.6f} | {t3 - t2:.6f} | {t5 - t4:.6f} | совпало={ok}")


def main():
    random.seed(42)
    demo()
    benchmark()


if __name__ == "__main__":
    main()
