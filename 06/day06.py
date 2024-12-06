def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def turn_right(dx: int, dy: int) -> tuple[int, int]:
    if dx == -1:
        return (0, 1)
    if dx == 1:
        return (0, -1)
    if dy == 1:
        return (1, 0)
    if dy == -1:
        return (-1, 0)
    raise Exception("Invalid direction")


def move_to_obstruction(
    x: int,
    y: int,
    dx: int,
    dy: int,
    x_max: int,
    y_max: int,
    obstructions: list[tuple[int, int]],
    visited: set[tuple[int, int]],
    visited_direction: set[tuple[int, int, int, int]],
    potential_loop_obstruction: set[tuple[int, int]],
) -> tuple[tuple[int, int], bool]:
    while (x + dx, y + dy) not in obstructions:
        x += dx
        y += dy
        visited.add((x, y))
        visited_direction.add((x, y, dx, dy))
        if x <= 0 or x >= x_max - 1 or y <= 0 or y >= y_max - 1:
            return (x, y), False
        if (x, y) in visited and (x, y, *turn_right(dx, dy)) in visited_direction:
            potential_loop_obstruction.add((x + dx, y + dy))
    return (x, y), True


def day6():
    lines = read_lines("06/input_example")
    # lines = read_lines("06/input")

    # map: list[list[str]] = []
    start: tuple[int, int] = (0, 0)
    obstructions: list[tuple[int, int]] = []

    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == "#":
                obstructions.append((x, y))
            if char == "^":
                start = (x, y)

    direction: tuple[int, int] = (-1, 0)
    visited: set[tuple[int, int]] = set()
    visited.add(start)
    turn_points: list[tuple[int, int]] = []
    x_max = len(lines)
    y_max = len(lines[0])
    current = start
    has_next = True

    visited_direction: set[tuple[int, int, int, int]] = set()
    visited_direction.add((start[0], start[1], direction[0], direction[1]))
    potential_loop_obstruction: set[tuple[int, int]] = set()

    while has_next:
        current, has_next = move_to_obstruction(
            *current, *direction, x_max, y_max, obstructions, visited, visited_direction, potential_loop_obstruction
        )
        turn_points.append(current)
        direction = turn_right(*direction)

    print(f"Total 1: {len(visited)}")

    for x, y, dx, dy in visited_direction:
        if x + dx >= x_max or x + dx < 0 or y + dy >= y_max or y + dy < 0:
            continue
        tmp_visited_direction: set[tuple[int, int, int, int]] = set()
        tmp_turn_points: list[tuple[int, int, int, int]] = []
        tmp_obstructions = obstructions.copy()
        tmp_obstructions.append((x + dx, y + dy))
        direction = turn_right(dx, dy)
        current: tuple[int, int] = (x, y)
        tmp_turn_points.append((*current, dx, dy))
        has_next: bool = True
        while has_next:
            current, has_next = move_to_obstruction(
                *current, *direction, x_max, y_max, tmp_obstructions, set(), tmp_visited_direction, set()
            )

            if (*current, *direction) in tmp_turn_points and has_next:
                potential_loop_obstruction.add((x + dx, y + dy))
                break

            tmp_turn_points.append((*current, *direction))
            direction = turn_right(*direction)

    potential_loop_obstruction.discard(start)
    print(potential_loop_obstruction)
    print(f"Total 2: {len(potential_loop_obstruction)}")  # 1603 too high


if __name__ == "__main__":
    day6()
