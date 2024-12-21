import re
from itertools import permutations


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


# 789
# 456
# 123
# #0A
NUMERIC_KEYPAD: dict[str, tuple[int, int]] = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "N#": (0, 3),  # Do not move here
    "0": (1, 3),
    "A": (2, 3),
}

# #^A
# <v>
DIRECTIONAL_KEYPAD: dict[str, tuple[int, int]] = {
    "D#": (0, 0),  # Do not move here
    "^": (1, 0),
    "a": (2, 0),  # 'A' in directional keypad, to have a unique key
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

KEYPADS = NUMERIC_KEYPAD | DIRECTIONAL_KEYPAD

DIRECTIONS: dict[str, tuple[int, int]] = {
    "^": (0, -1),  # N
    ">": (1, 0),  # E
    "v": (0, 1),  # S
    "<": (-1, 0),  # W
}


def get_paths(start: tuple[int, int], end: tuple[int, int], avoid: str) -> list[str]:
    """Find the shortest path between two positions on a directional keypad"""
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    moves: list[str] = []

    if dx < 0:
        moves.extend(["<"] * abs(dx))
    else:
        moves.extend([">"] * dx)
    if dy < 0:
        moves.extend(["^"] * abs(dy))
    else:
        moves.extend(["v"] * dy)

    valid_moves: list[str] = []
    for permutation in set(permutations(moves)):
        current = start
        for move in permutation:
            new_x = current[0] + DIRECTIONS[move][0]
            new_y = current[1] + DIRECTIONS[move][1]
            if (new_x, new_y) == KEYPADS[avoid]:
                break
            current = (new_x, new_y)
        else:
            valid_moves.append("".join(permutation) + "a")

    # If there are no moves we press the same thing twice
    return valid_moves if valid_moves else ["a"]


cache: dict[tuple[str, int, int], int] = {}


def get_minimum_length(sequence: str, limit: int, depth: int) -> int:
    if (sequence, limit, depth) in cache:
        return cache[(sequence, limit, depth)]

    current = KEYPADS["A"] if depth == 0 else KEYPADS["a"]
    avoid = "N#" if depth == 0 else "D#"

    length: int = 0
    for char in sequence:
        next = KEYPADS[char]
        paths = get_paths(current, next, avoid)

        if depth >= limit:
            length += len(min(paths, key=len))
        else:
            min_moves = float("inf")
            for path in paths:
                try:
                    min_moves = min(min_moves, get_minimum_length(path, limit, depth + 1))
                except:
                    pass
            if min_moves == float("inf"):
                length += len(min(paths, key=len))
            else:
                length += int(min_moves)

        current = next

    cache[(sequence, limit, depth)] = length
    return length


def get_number_from_sequence(sequence: str) -> int:
    numbers = re.findall(r"\d+", sequence)
    return int("".join(numbers))


def day21():
    lines = read_lines("21/input_example")
    lines = read_lines("21/input")
    sequences: list[str] = [line for line in lines]

    total_1: int = 0
    total_2: int = 0
    for sequence in sequences:
        number = get_number_from_sequence(sequence)
        length = get_minimum_length(sequence, 2, 0)
        print(f"Sequence: {sequence}, Number: {number}, Length: {length}")
        total_1 += number * length

        length = get_minimum_length(sequence, 25, 0)
        print(f"Sequence: {sequence}, Number: {number}, Length: {length}")
        total_2 += number * length

    print(f"Total 1: {total_1}")
    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day21()
