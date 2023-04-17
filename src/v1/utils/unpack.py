import io
import struct
from collections import Counter
from typing import Optional

from bitstring import BitArray


class Node:
    def __init__(self, char: str, freq: int, left: Optional["Node"] = None, right: Optional["Node"] = None) -> None:
        self.c: str = char
        self.f: int = freq
        self.left: Optional["Node"] = left
        self.right: Optional["Node"] = right

    def __lt__(self, other: "Node") -> bool:
        return self.f < other.f

    def __le__(self, other: "Node") -> bool:
        return self.f <= other.f

    def __repr__(self) -> str:
        return f"{self.c}:{self.f}"


class MinHeap:
    def __init__(self) -> None:
        self.arr: list[Node] = []

    def size(self) -> int:
        return len(self.arr)

    def push(self, obj: Node) -> None:
        self.arr.append(obj)
        child_idx: int = self.size() - 1

        while True:
            parent_idx: int = (child_idx - 1) // 2
            if self.arr[parent_idx] <= self.arr[child_idx]:
                return

            self.arr[parent_idx], self.arr[child_idx] = self.arr[child_idx], self.arr[parent_idx]
            child_idx = parent_idx

            if child_idx <= 0:
                return

    def pop(self) -> Node:
        obj: Node = self.arr[0]

        last = self.arr.pop()
        if self.size() == 0:
            return obj
        self.arr[0] = last

        parent_idx: int = 0
        child_idx: int = 2 * parent_idx + 1
        while child_idx < self.size():
            if child_idx + 1 < self.size() and self.arr[child_idx + 1] < self.arr[child_idx]:
                child_idx += 1

            if self.arr[parent_idx] <= self.arr[child_idx]:
                return obj

            self.arr[parent_idx], self.arr[child_idx] = self.arr[child_idx], self.arr[parent_idx]

            parent_idx = child_idx
            child_idx = 2 * child_idx + 1

        return obj


def make_tree(freqs: dict[str, int]) -> Node:
    h = MinHeap()
    for c, f in freqs.items():
        h.push(Node(c, f))

    while h.size() > 1:
        a = h.pop()
        b = h.pop()
        n = Node(a.c + b.c, a.f + b.f, a, b)
        h.push(n)

    return h.pop()


def decode(
    tree: Node, freqs: dict[str, int], packed: bytes, bits: int, verbose: bool = False, check_stats: bool = False
) -> str:
    p = BitArray(bytes=packed)
    p = p[:bits]
    if verbose:
        print(p.bin)  # noqa: T201
    unpacked: str = ""
    pos: int = 0
    while pos < len(p):
        node: Node = tree
        while True:
            if pos >= len(p):
                raise ValueError(f"invalid tree: out of message bounds, {unpacked=}")
            bit: bool = p[pos]
            node = node.right if bit else node.left
            pos += 1
            if node is None:
                raise ValueError(f"invalid tree: dead end while walking, {unpacked=}")
            if node.left is None and node.right is None:
                break
        unpacked += node.c

    if check_stats:
        stats: Counter = Counter(unpacked)
        for c, f in freqs.items():
            if stats[c] != f:
                raise ValueError(f"incorrect '{c}' freq: header={f} processed={stats[c]}, {unpacked=}")

    return unpacked


def read(file: io.BytesIO, fmt: str) -> tuple:
    i: int = struct.calcsize(fmt)
    ret: tuple = struct.unpack(fmt, file.read(i))
    if type(ret) == tuple and len(ret) == 1:
        return ret[0]
    return ret


def get_freqs(file: io.BytesIO) -> dict[str, int]:
    file_len: int
    always0: int
    chars_count: int
    file_len, always0, chars_count = read(file, "III")
    freqs: dict[str, int] = {}
    for _i in range(chars_count):
        count: int = read(file, "I")
        char: str = read(file, "cxxx").decode("ascii")
        freqs[char] = count
    return freqs


def unpack_file(file: io.BytesIO) -> str:
    freqs: dict[str, int] = get_freqs(file)
    tree: Node = make_tree(freqs)

    packed_bits: int
    packed_bytes: int
    unpacked_bytes: int
    packed_bits, packed_bytes, unpacked_bytes = read(file, "III")

    packed: bytes = file.read(packed_bytes)
    return decode(tree, freqs, packed, packed_bits)


def unpack(data: bytes) -> str:
    if type(data) == bytes:
        data = io.BytesIO(data)

    return unpack_file(data)
