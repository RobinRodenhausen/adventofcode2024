def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def climb_slope(current: tuple[int, int], map: list[list[int]], goals: set[tuple[int, int]]) -> int:
    x, y = current
    if map[y][x] == 9:
        goals.add((x, y))

    for dx, dy in DIRECTIONS:
        new_x = x + dx
        new_y = y + dy
        if new_x < 0 or new_y < 0 or new_x >= len(map[0]) or new_y >= len(map):
            continue
        if map[new_y][new_x] - map[y][x] != 1:
            continue
        climb_slope((new_x, new_y), map, goals)
    return len(goals)


def climb_slope_2(current: tuple[int, int], map: list[list[int]], total: int = 0) -> int:
    x, y = current
    if map[y][x] == 9:
        return 1

    for dx, dy in DIRECTIONS:
        new_x = x + dx
        new_y = y + dy
        if new_x < 0 or new_y < 0 or new_x >= len(map[0]) or new_y >= len(map):
            continue
        if map[new_y][new_x] - map[y][x] != 1:
            continue
        total += climb_slope_2((new_x, new_y), map)
    return total


def day10():
    lines = read_lines("10/input_example")
    lines = read_lines("10/input")

    starts: list[tuple[int, int]] = []
    map: list[list[int]] = []

    for y, line in enumerate(lines):
        map.append([])
        for x, char in enumerate(line):
            if char == ".":
                map[y].append(-1)
                continue
            if char == "0":
                starts.append((x, y))
            map[y].append(int(char))

    total_1: int = 0
    for start in starts:
        total_1 += climb_slope(start, map, set())

    print(f"Total 1: {total_1}")

    total_2: int = 0
    for start in starts:
        total_2 += climb_slope_2(start, map)

    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day10()
