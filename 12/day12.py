from collections import defaultdict


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


# N E S W
DIRECTIONS_1: list[tuple[int, int]] = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def check_region_1(
    x: int, y: int, char: str, lines: list[str], checked: set[tuple[int, int]], area: int = 1, perimeter: int = 0
) -> tuple[int, int]:
    for dx, dy in DIRECTIONS_1:
        new_x = x + dx
        new_y = y + dy
        if new_x < 0 or new_y < 0 or new_x >= len(lines[0]) or new_y >= len(lines):
            perimeter += 1
        elif lines[new_y][new_x] != char:
            perimeter += 1
        elif (new_x, new_y) in checked:
            continue
        else:
            checked.add((new_x, new_y))
            tmp_area, tmp_perimeter = check_region_1(new_x, new_y, char, lines, checked, 1, 0)
            area += tmp_area
            perimeter += tmp_perimeter

    return area, perimeter


def day11_1():
    lines = read_lines("12/input_example")
    lines = read_lines("12/input")

    checked: set[tuple[int, int]] = set()
    fences: dict[str, list[tuple[int, int]]] = defaultdict(list)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if (x, y) in checked:
                continue
            checked.add((x, y))

            fences[char].append(check_region_1(x, y, char, lines, checked))

    total_1: int = 0
    for _, regions in fences.items():
        for region in regions:
            area, perimeter = region
            total_1 += area * perimeter

    print(f"Total 1: {total_1}")


DIRECTIONS_2: dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "NE": (1, -1),
    "E": (1, 0),
    "SE": (1, 1),
    "S": (0, 1),
    "SW": (-1, 1),
    "W": (-1, 0),
    "NW": (-1, -1),
}


def get_neighbor(x: int, y: int, direction: str, lines: list[str]) -> str:
    dx, dy = DIRECTIONS_2[direction]
    new_x = x + dx
    new_y = y + dy
    if new_x < 0 or new_y < 0 or new_x >= len(lines[0]) or new_y >= len(lines):
        return ""
    return lines[new_y][new_x]


def check_region_2(
    x: int, y: int, char: str, lines: list[str], checked: set[tuple[int, int]], area: int = 1, corners: int = 0
) -> tuple[int, int]:
    north = get_neighbor(x, y, "N", lines)
    east = get_neighbor(x, y, "E", lines)
    south = get_neighbor(x, y, "S", lines)
    west = get_neighbor(x, y, "W", lines)

    north_east = get_neighbor(x, y, "NE", lines)
    south_east = get_neighbor(x, y, "SE", lines)
    south_west = get_neighbor(x, y, "SW", lines)
    north_west = get_neighbor(x, y, "NW", lines)

    if north != char and east != char:
        corners += 1
    if east != char and south != char:
        corners += 1
    if south != char and west != char:
        corners += 1
    if west != char and north != char:
        corners += 1

    if north_east != char and north == char and east == char:
        corners += 1
    if south_east != char and east == char and south == char:
        corners += 1
    if south_west != char and south == char and west == char:
        corners += 1
    if north_west != char and west == char and north == char:
        corners += 1

    for dx, dy in DIRECTIONS_1:
        new_x = x + dx
        new_y = y + dy
        if new_x < 0 or new_y < 0 or new_x >= len(lines[0]) or new_y >= len(lines):
            continue
        elif lines[new_y][new_x] != char:
            continue
        elif (new_x, new_y) in checked:
            continue
        else:
            checked.add((new_x, new_y))
            tmp_area, tmp_corners = check_region_2(new_x, new_y, char, lines, checked, 1, 0)
            area += tmp_area
            corners += tmp_corners

    return area, corners


def day11_2():
    lines = read_lines("12/input_example")
    lines = read_lines("12/input")

    checked: set[tuple[int, int]] = set()
    fences: dict[str, list[tuple[int, int]]] = defaultdict(list)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if (x, y) in checked:
                continue
            checked.add((x, y))

            fences[char].append(check_region_2(x, y, char, lines, checked))

    total_2: int = 0
    for _, regions in fences.items():
        for region in regions:
            area, sides = region
            total_2 += area * sides

    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day11_1()
    day11_2()
