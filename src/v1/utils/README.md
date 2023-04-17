# Utils

## Unpack module

### `class PriorityQueue`

A priority queue implementation using the heapq module.

- Methods:
  - `push(obj: Node) -> None`: Push a Node object onto the priority queue.
  - `pop() -> Node`: Pop and return the Node object with the lowest frequency from the priority queue.
  - `size() -> int`: Return the number of elements in the priority queue.

### `make_tree(freqs: dict[str, int]) -> Node`

Create a Huffman tree based on the given character frequencies.

- `freqs`: A dictionary containing character frequencies.
- Returns: The root node of the created Huffman tree.

### `decode(tree: Node, freqs: dict[str, int], packed: bytes, bits: int, verbose=False, check_stats=False) -> str`

Decodes a Huffman-encoded message using the given tree and frequency dictionary.

- `tree`: The root node of the Huffman tree.
- `freqs`: A dictionary containing character frequencies.
- `packed`: The packed message to decode.
- `bits`: The number of bits in the packed message.
- `verbose`: Whether to print debug information.
- `check_stats`: Whether to check the decoded message against the expected frequency statistics.
- Returns: The decoded message as a string.

### `get_freqs(file) -> dict[str, int]`

Reads the frequency dictionary from a Huffman-encoded file.

- `file`: A file-like object to read from.
- Returns: A dictionary mapping characters to frequencies.

### `unpack_file(file) -> str`

Decodes a Huffman-encoded file.

- `file`: A file-like object containing the Huffman-encoded data.
- Returns: The decoded message as a string.

### `unpack(data) -> str`

Decodes a Huffman-encoded message or file.

- `data`: A bytes-like object containing the Huffman-encoded data, or a file-like object.
- Returns: The decoded message as a string.
