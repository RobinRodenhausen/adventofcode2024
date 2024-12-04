def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def check_xmas_direction(x: int, y: int, direction: tuple[int, int], next: str, input: list[list[str]]) -> bool:
    xd, yd = direction
    if input[y + yd][x + xd] == next:
        if next == "S":
            return True
        else:
            if next == "M":
                n = "A"
            elif next == "A":
                n = "S"
            return check_xmas_direction(x + xd, y + yd, direction, n, input)  # pyright: ignore[reportPossiblyUnboundVariable]
    return False


def check_xmas_start(x: int, y: int, input: list[list[str]]) -> int:
    counter = 0

    directions = set([(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)])
    if x < 3:
        [directions.discard(t) for t in [(-1, 0), (-1, 1), (-1, -1)]]
    elif x < 2:
        [directions.discard(t) for t in [(-1, 0)]]

    if y < 3:
        [directions.discard(t) for t in [(0, -1), (1, -1), (-1, -1)]]
    elif y < 2:
        [directions.discard(t) for t in [(0, -1)]]

    if x >= len(input[0]) - 3:
        [directions.discard(t) for t in [(1, 0), (1, 1), (1, -1)]]
    elif x >= len(input[0]) - 2:
        [directions.discard(t) for t in [(1, 0)]]

    if y >= len(input) - 3:
        [directions.discard(t) for t in [(0, 1), (-1, 1), (1, 1)]]
    elif y >= len(input) - 2:
        [directions.discard(t) for t in [(0, 1)]]

    for direction in directions:
        if check_xmas_direction(x, y, direction, "M", input):
            counter += 1

    return counter


def check_x_mas_start(x: int, y: int, input: list[list[str]]) -> int:
    if x < 1 or x >= len(input[0]) - 1 or y < 1 or y >= len(input) - 1:
        return 0

    v1 = [input[y + 1][x + 1], input[y - 1][x - 1]]
    v2 = [input[y + 1][x - 1], input[y - 1][x + 1]]

    if "M" in v1 and "S" in v1 and "M" in v2 and "S" in v2:
        return 1

    return 0


def day4():
    lines = read_lines("04/input_example")
    lines = read_lines("04/input")

    input: list[list[str]] = []
    xmas_starts: list[tuple[int, int]] = []
    x_mas_starts: list[tuple[int, int]] = []

    for y, line in enumerate(lines):
        input.append([])
        for x, char in enumerate(line):
            input[y].append(char)
            if char == "X":
                xmas_starts.append((x, y))
            if char == "A":
                x_mas_starts.append((x, y))

    total_1 = 0
    for start in xmas_starts:
        total_1 += check_xmas_start(*start, input)

    print(f"Total 1: {total_1}")

    total_2 = 0

    for start in x_mas_starts:
        total_2 += check_x_mas_start(*start, input)

    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    # print([ord(x) for x in "XMAS"])
    day4()
