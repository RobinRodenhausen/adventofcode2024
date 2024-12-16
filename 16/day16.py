import heapq
from collections import deque


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


# N E S W
DIRECTIONS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


def dijkstra(maze: list[list[bool]], start: tuple[int, int]) -> dict[tuple[int, int, str], int]:
    rows, cols = len(maze), len(maze[0])
    start_state: tuple[int, int, str] = (*start, "E")

    priority_queue: list[tuple[tuple[int, int, str], int]] = []
    heapq.heappush(priority_queue, (start_state, 0))
    visited: dict[tuple[int, int, str], int] = {start_state: 0}

    while priority_queue:
        (x, y, direction), score = heapq.heappop(priority_queue)
        if visited.get((x, y, direction), float("inf")) < score:
            continue

        # Move straight
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_y][new_x]:
            new_score = score + 1
            if new_score < visited.get((new_x, new_y, direction), float("inf")):
                visited[(new_x, new_y, direction)] = new_score
                heapq.heappush(priority_queue, ((new_x, new_y, direction), new_score))

        turns = "WE" if direction in "NS" else "NS"

        # Turn
        for new_direction in turns:
            new_score = score + 1000
            if new_score < visited.get((x, y, new_direction), float("inf")):
                visited[(x, y, new_direction)] = new_score
                heapq.heappush(priority_queue, ((x, y, new_direction), new_score))
    return visited


def reverse(maze: list[list[bool]], visited: dict[tuple[int, int, str], int], end: tuple[int, int]) -> set[tuple[int, int]]:
    rows, cols = len(maze), len(maze[0])
    min_cost: int = min(
        visited.get((end[0], end[1], direction), float("inf")) for direction in DIRECTIONS.keys()
    )  # pyright: ignore[reportAssignmentType]

    path: set[tuple[int, int, str]] = set()
    q: deque[tuple[int, int, str]] = deque()

    for direction in DIRECTIONS.keys():
        state = (*end, direction)
        if state in visited and visited[state] == min_cost:
            path.add(state)
            q.append(state)

    while q:
        x, y, direction = q.popleft()
        score = visited[(x, y, direction)]

        dx, dy = DIRECTIONS[direction]
        new_x, new_y = x - dx, y - dy
        if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_y][new_x]:
            prev_score = score - 1
            prev_state = (new_x, new_y, direction)
            if prev_score >= 0 and prev_state in visited and visited[prev_state] == prev_score and prev_state not in path:
                path.add(prev_state)
                q.append(prev_state)

        turns = "WE" if direction in "NS" else "NS"

        prev_score = score - 1000
        if prev_score >= 0:
            for new_direction in turns:
                prev_state = (x, y, new_direction)
                if prev_state in visited and visited[prev_state] == prev_score and prev_state not in path:
                    path.add(prev_state)
                    q.append(prev_state)

    return {(x, y) for (x, y, _) in path}


def day16():
    lines = read_lines("16/input_example1")
    lines = read_lines("16/input_example2")
    lines = read_lines("16/input")

    maze: list[list[bool]] = []
    start: tuple[int, int] = (-1, -1)
    end: tuple[int, int] = (-1, -1)
    for y, line in enumerate(lines):
        maze.append([])
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
            if char == "E":
                end = (x, y)
            if char == "#":
                maze[y].append(False)
            else:
                maze[y].append(True)

    visited = dijkstra(maze, start)

    total_1: int = min(visited.get((*end, direction), float("inf")) for direction in DIRECTIONS.keys())  # pyright: ignore
    print(f"Total 1: {total_1}")

    path = reverse(maze, visited, end)
    print(f"Total 2: {len(path)}")


if __name__ == "__main__":
    day16()
