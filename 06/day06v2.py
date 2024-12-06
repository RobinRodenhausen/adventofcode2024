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
) -> tuple[tuple[int, int], bool]:
    while (x + dx, y + dy) not in obstructions:
        x += dx
        y += dy
        visited.add((x, y))
        visited_direction.add((x, y, dx, dy))
        if x <= 0 or x >= x_max - 1 or y <= 0 or y >= y_max - 1:
            return (x, y), False
    return (x, y), True


def day6():
    lines = read_lines("06/input_example")
    lines = read_lines("06/input")

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
    x_max = len(lines)
    y_max = len(lines[0])
    current = start
    has_next = True

    potential_loop_obstruction: set[tuple[int, int]] = set()

    while has_next:
        current, has_next = move_to_obstruction(*current, *direction, x_max, y_max, obstructions, visited, set())
        direction = turn_right(*direction)

    print(f"Total 1: {len(visited)}")

    for i, (x, y) in enumerate(visited):
        # It is so slow...
        print(f"{i} - {x}, {y}")
        # Keep track of visited directions to find loop
        tmp_visited_direction: set[tuple[int, int, int, int]] = set()
        # Add obstruction in front of current position
        tmp_obstructions = obstructions.copy()
        tmp_obstructions.append((x, y))
        # Turn because of new obstruction
        direction: tuple[int, int] = (-1, 0)
        current: tuple[int, int] = start
        has_next: bool = True

        while has_next:
            if (*current, *direction) in tmp_visited_direction:
                potential_loop_obstruction.add((x, y))
                break

            tmp_visited_direction.add((*current, *direction))  # pyright: ignore[reportArgumentType]

            current, has_next = move_to_obstruction(
                *current, *direction, x_max, y_max, tmp_obstructions, set(), tmp_visited_direction
            )

            direction = turn_right(*direction)

    potential_loop_obstruction.discard(start)
    print(potential_loop_obstruction)
    print(f"Total 2: {len(potential_loop_obstruction)}")  # 1603 too high


if __name__ == "__main__":
    day6()
