import math
import re


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def move_robot(robot: tuple[int, int, int, int], seconds: int, x_max: int, y_max: int) -> tuple[int, int]:
    x, y, vx, vy = robot
    return (x + vx * seconds) % x_max, (y + vy * seconds) % y_max


def day14():
    lines = read_lines("14/input_example")
    lines = read_lines("14/input")

    x_max: int = 11
    y_max: int = 7
    x_max: int = 101
    y_max: int = 103

    robots: list[tuple[int, int, int, int]] = []
    for line in lines:
        x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
        robots.append((x, y, vx, vy))

    moved_robots: list[tuple[int, int]] = [move_robot(robot, 100, x_max, y_max) for robot in robots]

    x_middle: int = x_max // 2
    y_middle: int = y_max // 2
    quadrants: dict[str, int] = {"NW": 0, "NE": 0, "SE": 0, "SW": 0}

    for robot in moved_robots:
        x, y = robot
        if x < x_middle and y < y_middle:
            quadrants["NW"] += 1
        elif x > x_middle and y < y_middle:
            quadrants["NE"] += 1
        elif x > x_middle and y > y_middle:
            quadrants["SE"] += 1
        elif x < x_middle and y > y_middle:
            quadrants["SW"] += 1

    print(f"Total 1: {math.prod(quadrants.values())}")

    for i in range(100000):
        moved_robots_unique: set[tuple[int, int]] = set([move_robot(robot, i, x_max, y_max) for robot in robots])
        if len(moved_robots_unique) == len(robots):
            print(f"Total 2: {i}")
            break


if __name__ == "__main__":
    day14()
