# Ganked from: https://github.com/shrddr/huffman_heap/blob/main/unpack.py

import io
import struct
from collections import Counter

from bitstring import BitArray


class Node:
    def __init__(self, char, freq, left=None, right=None) -> None:
        self.c = char
        self.f = freq
        self.left = left
        self.right = right

    def __lt__(self, other):  # noqa: ANN204
        return self.f < other.f

    def __le__(self, other):  # noqa: ANN204
        return self.f <= other.f

    def __repr__(self):  # noqa: ANN204
        return f'{self.c}:{self.f}'


class MinHeap:
    def __init__(self) -> None:
        self.arr = []

    def size(self):  # noqa: ANN201
        return len(self.arr)

    def push(self, obj):  # noqa: ANN201
        self.arr.append(obj)
        child_idx = self.size() - 1

        while True:
            parent_idx = (child_idx - 1) // 2
            if self.arr[parent_idx] <= self.arr[child_idx]:
                return

            self.arr[parent_idx], self.arr[child_idx] = self.arr[child_idx], self.arr[parent_idx]
            child_idx = parent_idx

            if child_idx <= 0:
                return

    def pop(self):  # noqa: ANN201
        obj = self.arr[0]

        last = self.arr.pop()
        if self.size() == 0:
            return obj
        self.arr[0] = last

        parent_idx = 0
        child_idx = 2 * parent_idx + 1
        while child_idx < self.size():
            if child_idx + 1 < self.size() and self.arr[child_idx + 1] < self.arr[child_idx]:
                child_idx += 1

            if self.arr[parent_idx] <= self.arr[child_idx]:
                return obj

            self.arr[parent_idx], self.arr[child_idx] = self.arr[child_idx], self.arr[parent_idx]

            parent_idx = child_idx
            child_idx = 2 * child_idx + 1

        return obj


def make_tree(freqs):  # noqa: ANN201
    h = MinHeap()
    for c, f in freqs.items():
        h.push(Node(c, f))

    while h.size() > 1:
        a = h.pop()
        b = h.pop()
        n = Node(a.c + b.c, a.f + b.f, a, b)
        h.push(n)

    return h.pop()


def decode(tree, freqs, packed, bits, verbose=False, check_stats=False):  # noqa: ANN201
    p = BitArray(bytes=packed)
    p = p[:bits]
    if verbose:
        print(p.bin)  # noqa: T201
    unpacked = ''
    pos = 0
    while pos < len(p):
        node = tree
        while True:
            if pos >= len(p):
                raise ValueError(f'invalid tree: out of message bounds, {unpacked=}')
            bit = p[pos]
            node = node.right if bit else node.left
            pos += 1
            if node is None:
                raise ValueError(f'invalid tree: dead end while walking, {unpacked=}')
            if node.left is None and node.right is None:
                break
        unpacked += node.c

    if check_stats:
        stats = Counter(unpacked)
        for c, f in freqs.items():
            if stats[c] != f:
                raise ValueError(f"incorrect '{c}' freq: header={f} processed={stats[c]}, {unpacked=}")

    return unpacked


def read(file, fmt):  # noqa: ANN201
    i = struct.calcsize(fmt)
    ret = struct.unpack(fmt, file.read(i))
    if type(ret) == tuple and len(ret) == 1:
        return ret[0]
    return ret


def get_freqs(file):  # noqa: ANN201
    file_len, always0, chars_count = read(file, 'III')
    freqs = {}
    for _i in range(chars_count):
        count = read(file, 'I')
        char = read(file, 'cxxx').decode('ascii')
        freqs[char] = count
    return freqs


def unpack_file(file):  # noqa: ANN201
    freqs = get_freqs(file)
    tree = make_tree(freqs)

    packed_bits, packed_bytes, unpacked_bytes = read(file, 'III')

    packed = file.read(packed_bytes)
    return decode(tree, freqs, packed, packed_bits)


def unpack(data):  # noqa: ANN201
    if type(data) == bytes:
        data = io.BytesIO(data)

    return unpack_file(data)
