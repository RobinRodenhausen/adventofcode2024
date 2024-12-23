import functools
from collections import defaultdict

connections: defaultdict[str, set[str]] = defaultdict(set)


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


@functools.cache
def is_clique(st: frozenset[str], node: str) -> frozenset[str]:
    largest = st
    opts = connections[node]
    if st.issubset(opts):
        st |= frozenset([node])
        largest = st
        for opt in opts:
            if opt in st:
                continue
            candidate = is_clique(st, opt)
            if len(candidate) > len(largest):
                largest = candidate
    return largest


def find_largest_clique(nodes: set[str]) -> frozenset[str]:
    largest: frozenset[str] = frozenset()
    for node in nodes:
        tmp: frozenset[str] = frozenset()
        candidate = is_clique(tmp, node)
        if len(candidate) > len(largest):
            largest = candidate
    return largest


def day23():
    lines = read_lines("23/input_example")
    lines = read_lines("23/input")

    nodes: set[str] = set()

    for line in lines:
        c1, c2 = line.split("-")
        connections[c1].add(c2)
        connections[c2].add(c1)
        nodes.add(c1)
        nodes.add(c2)

    triangles: set[tuple[str, str, str]] = set()

    for c1 in connections:
        for c2 in connections[c1]:
            for c3 in connections[c1]:
                if c2 != c3 and c3 in connections[c2]:
                    triangle = tuple(sorted([c1, c2, c3]))
                    triangles.add(triangle)  # pyright: ignore[reportArgumentType]

    total_1: int = 0
    for t in triangles:
        if any(c.startswith("t") for c in t):
            total_1 += 1

    print(f"Total 1: {total_1}")

    largest_clique = find_largest_clique(nodes)
    print(f"Total 2: {','.join(sorted(largest_clique))}")


if __name__ == "__main__":
    day23()
