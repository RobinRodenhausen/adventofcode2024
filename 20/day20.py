import heapq


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


# N E S W
DIRECTIONS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


def dijkstra_with_cheats(map: list[list[bool]], start: tuple[int, int]) -> dict[tuple[int, int, int], int]:
    max_y, max_x = len(map), len(map[0])
    start_state: tuple[int, int, int] = (*start, 1)

    priority_queue: list[tuple[tuple[int, int, int], int]] = []
    heapq.heappush(priority_queue, (start_state, 0))
    visited: dict[tuple[int, int, int], int] = {start_state: 0}

    while priority_queue:
        (x, y, cheats), score = heapq.heappop(priority_queue)
        if visited.get((x, y, cheats), float("inf")) < score:
            continue

        for direction in DIRECTIONS:
            dx, dy = DIRECTIONS[direction]
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < max_x and 0 <= new_y < max_y:  # and grid[new_y][new_x]:
                if map[new_y][new_x]:
                    new_score = score + 1
                    new_cheats = cheats
                elif not map[new_y][new_x] and cheats > 0:
                    new_score = score + 1
                    new_cheats = cheats - 1
                else:
                    continue

                if new_score < visited.get((new_x, new_y, new_cheats), float("inf")):
                    visited[(new_x, new_y, new_cheats)] = new_score
                    heapq.heappush(priority_queue, ((new_x, new_y, new_cheats), new_score))

    return visited


def dijkstra(
    grid: list[list[bool]], start: tuple[int, int]
) -> tuple[dict[tuple[int, int], int], dict[tuple[int, int], tuple[int, int]]]:
    max_y, max_x = len(grid), len(grid[0])

    priority_queue: list[tuple[tuple[int, int], int]] = []
    heapq.heappush(priority_queue, (start, 0))
    cost: dict[tuple[int, int], int] = {start: 0}
    previous: dict[tuple[int, int], tuple[int, int]] = {start: (-1, -1)}

    while priority_queue:
        (x, y), score = heapq.heappop(priority_queue)

        for direction in DIRECTIONS:
            dx, dy = DIRECTIONS[direction]
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < max_x and 0 <= new_y < max_y and grid[new_y][new_x]:
                new_score = score + 1

                if (new_x, new_y) not in cost or new_score < cost.get((new_x, new_y), float("inf")):
                    cost[(new_x, new_y)] = new_score
                    heapq.heappush(priority_queue, ((new_x, new_y), new_score))
                    previous[(new_x, new_y)] = (x, y)

    return cost, previous


def day20():
    lines = read_lines("20/input_example")
    lines = read_lines("20/input")

    map: list[list[bool]] = []
    start: tuple[int, int] = (-1, -1)
    end: tuple[int, int] = (-1, -1)
    for y, line in enumerate(lines):
        map.append([])
        for x, c in enumerate(line):
            if c == "#":
                map[y].append(False)
                continue
            map[y].append(True)
            if c == "S":
                start = (x, y)
            if c == "E":
                end = (x, y)

    visited = dijkstra_with_cheats(map, start)

    fastest_no_cheat: int = visited.get((*end, 1), float("inf"))  # pyright: ignore
    fastest_cheat: int = visited.get((*end, 0), float("inf"))  # pyright: ignore
    print(f"Fastest without cheats: {fastest_no_cheat}")
    print(f"Fastest with cheats: {fastest_cheat}")

    cost, previous = dijkstra(map, start)

    print(f"Fastest without cheats: {cost[end]}")
    path: list[tuple[int, int]] = []
    while end != start:
        path.append(end)
        end = previous[end]
    path.append(start)

    total_1: int = 0
    total_2: int = 0

    for i in range(len(path)):
        for j in range(i + 102, len(path)):
            dist = abs(path[j][0] - path[i][0]) + abs(path[j][1] - path[i][1])
            if (j - i) - dist < 100:
                continue

            if dist == 2:
                total_1 += 1
            if dist <= 20:
                total_2 += 1

    print(f"Total 1: {total_1}")
    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day20()
