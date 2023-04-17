# Ganked and updated from: https://github.com/shrddr/huffman_heap/blob/main/unpack.py

import heapq
import io
import struct
from collections import Counter

from bitstring import BitArray


class Node:
    def __init__(self, char: str, freq: int, left: "Node" = None, right: "Node" = None) -> None:
        self.c = char
        self.f = freq
        self.left = left
        self.right = right

    def __lt__(self, other: "Node") -> bool:
        return self.f < other.f

    def __le__(self, other: "Node") -> bool:
        return self.f <= other.f

    def __repr__(self) -> str:
        return f"{self.c}:{self.f}"


class PriorityQueue:
    """
    A priority queue implementation using the heapq module.

    Methods
    -------
    push(obj: Node) -> None
        Push a Node object onto the priority queue.
    pop() -> Node
        Pop and return the Node object with the lowest frequency from the priority queue.
    size() -> int
        Return the number of elements in the priority queue.
    """

    def __init__(self) -> None:
        self.heap = []

    def push(self, obj: Node) -> None:
        """
        Push a Node object onto the priority queue.

        Parameters
        ----------
        obj : Node
            The Node object to push onto the priority queue.
        """
        heapq.heappush(self.heap, obj)

    def pop(self) -> Node:
        """
        Pop and return the Node object with the lowest frequency from the priority queue.

        Returns
        -------
        Node
            The Node object with the lowest frequency.
        """
        return heapq.heappop(self.heap)

    def size(self) -> int:
        """
        Return the number of elements in the priority queue.

        Returns
        -------
        int
            The number of elements in the priority queue.
        """
        return len(self.heap)


def make_tree(freqs: dict[str, int]) -> Node:
    pq = PriorityQueue()
    for c, f in freqs.items():
        pq.push(Node(c, f))

    while pq.size() > 1:
        a = pq.pop()
        b = pq.pop()
        n = Node(a.c + b.c, a.f + b.f, a, b)
        pq.push(n)

    return pq.pop()


def decode(
    tree: Node,
    freqs: dict[str, int],
    packed: bytes,
    bits: int,
    verbose: bool = False,
    check_stats: bool = False,
) -> str:
    """
    Decode the packed data using the given Huffman tree and character frequencies.

    Parameters
    ----------
    tree : Node
        The root node of the Huffman tree.
    freqs : dict[str, int]
        A dictionary containing character frequencies.
    packed : bytes
        The packed data to decode.
    bits : int
        The number of bits in the packed data.
    verbose : bool, optional, default: False
        If True, print the binary representation of the packed data.
    check_stats : bool, optional, default: False
        If True, verify that the decoded data matches the input character frequencies.

    Returns
    -------
    str
        The decoded data as a string.
    """
    p = BitArray(bytes=packed)
    p = p[:bits]
    if verbose:
        print(p.bin)  # noqa: T201
    unpacked = ""
    pos = 0
    while pos < len(p):
        node = tree
        while True:
            if pos >= len(p):
                raise ValueError(f"invalid tree: out of message bounds, {unpacked=}")
            bit = p[pos]
            node = node.right if bit else node.left
            pos += 1
            if node is None:
                raise ValueError(f"invalid tree: dead end while walking, {unpacked=}")
            if node.left is None and node.right is None:
                break
        unpacked += node.c

    if check_stats:
        stats = Counter(unpacked)
    for c, f in freqs.items():
        if stats[c] != f:
            raise ValueError(f"incorrect '{c}' freq: header={f} processed={stats[c]}, {unpacked=}")

    return unpacked


def read(file: io.BufferedReader, fmt: str) -> int | bytes:
    """
    Read and unpack data from a file according to the specified format.

    Parameters
    ----------
    file : io.BufferedReader
        The input file to read from.
    fmt : str
        The format string to use when unpacking data.

    Returns
    -------
    int | bytes
        The unpacked data, either as an integer or bytes.
    """
    i = struct.calcsize(fmt)
    ret = struct.unpack(fmt, file.read(i))
    if isinstance(ret, tuple) and len(ret) == 1:
        return ret[0]
    return ret


def get_freqs(file: io.BufferedReader) -> dict[str, int]:
    """
    Extract character frequencies from a file.

    Parameters
    ----------
    file : io.BufferedReader
        The input file containing the character frequencies.

    Returns
    -------
    dict[str, int]
        A dictionary containing character frequencies.
    """
    file_len, always0, chars_count = read(file, "III")
    freqs = {}
    for _i in range(chars_count):
        count = read(file, "I")
        char = read(file, "cxxx").decode("ascii")
        freqs[char] = count
    return freqs


def unpack_file(file: io.BufferedReader) -> str:
    """
    Unpack and decode data from a file.

    Parameters
    ----------
    file : io.BufferedReader
        The input file containing the packed data and character frequencies.

    Returns
    -------
    str
        The unpacked and decoded data as a string.
    """
    freqs = get_freqs(file)
    tree = make_tree(freqs)

    packed_bits, packed_bytes, unpacked_bytes = read(file, "III")

    packed = file.read(packed_bytes)
    return decode(tree, freqs, packed, packed_bits)


def unpack(data: bytes | io.BytesIO) -> str:
    """
    Unpack and decode data from a bytes object or a BytesIO object.

    Parameters
    ----------
    data : bytes | io.BytesIO
        The input data containing the packed data and character frequencies, either as bytes or a BytesIO object.

    Returns
    -------
    str
        The unpacked and decoded data as a string.
    """
    if isinstance(data, bytes):
        data = io.BytesIO(data)

    return unpack_file(data)
