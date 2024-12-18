import heapq


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


DIRECTIONS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


def dijkstra(grid: list[list[bool]], start: tuple[int, int]) -> dict[tuple[int, int], int]:
    rows, cols = len(grid), len(grid[0])

    priority_queue: list[tuple[tuple[int, int], int]] = []
    heapq.heappush(priority_queue, (start, 0))
    visited: dict[tuple[int, int], int] = {start: 0}

    while priority_queue:
        (x, y), score = heapq.heappop(priority_queue)
        if visited.get((x, y), float("inf")) < score:
            continue

        # Move straight
        for direction in DIRECTIONS:
            dx, dy = DIRECTIONS[direction]
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < cols and 0 <= new_y < rows and grid[new_y][new_x]:
                new_score = score + 1
                if new_score < visited.get((new_x, new_y), float("inf")):
                    visited[(new_x, new_y)] = new_score
                    heapq.heappush(priority_queue, ((new_x, new_y), new_score))

    return visited


def debug_grid(grid: list[list[bool]]):
    for line in grid:
        print("".join("." if cell else "#" for cell in line))


def day18():
    lines = read_lines("18/input_example")
    size: int = 7

    lines = read_lines("18/input")
    size: int = 71

    grid: list[list[bool]] = []

    for y in range(size):
        grid.append([True] * size)

    for i, line in enumerate(lines):
        x, y = line.split(",")
        grid[int(y)][int(x)] = False

        if i >= 1023 or i >= 11 and size == 7:  # pyright: ignore[reportUnnecessaryComparison]
            break

    visited = dijkstra(grid, (0, 0))

    total_1: int = visited.get((size - 1, size - 1), -1)
    print(f"Total 1: {total_1}")

    for i, line in enumerate(lines):
        # Skip the first 1024 lines since they are already processed
        if i <= 1023 and size == 71 or i <= 11 and size == 7:  # pyright: ignore[reportUnnecessaryComparison]
            continue
        x, y = line.split(",")
        grid[int(y)][int(x)] = False

        visited = dijkstra(grid, (0, 0))

        end = visited.get((size - 1, size - 1), -1)
        if end == -1:
            total_2: str = f"{x},{y}"
            print(f"Total 2: {total_2}")
            break


if __name__ == "__main__":
    day18()
