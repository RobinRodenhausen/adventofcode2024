from collections import defaultdict


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def day8():
    lines = read_lines("08/input_example2")
    lines = read_lines("08/input_example")
    lines = read_lines("08/input")

    y_max: int = len(lines)
    x_max: int = len(lines[0])

    antennas: dict[str, list[tuple[int, int]]] = defaultdict(list)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                continue
            antennas[char].append((x, y))

    antinodes_1: set[tuple[int, int]] = set()
    antinodes_2: set[tuple[int, int]] = set()
    for _, positions in antennas.items():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                dx = x1 - x2
                dy = y1 - y2

                # Part 1
                x1d = x1 + dx
                y1d = y1 + dy
                if x1d < 0 or x1d >= x_max or y1d < 0 or y1d >= y_max:
                    pass
                else:
                    antinodes_1.add((x1d, y1d))

                x2d = x2 - dx
                y2d = y2 - dy
                if x2d < 0 or x2d >= x_max or y2d < 0 or y2d >= y_max:
                    pass
                else:
                    antinodes_1.add((x2 - dx, y2 - dy))

                # Part 2
                break_d1 = False
                break_d2 = False
                multi_d1 = 0
                multi_d2 = 0

                while not break_d1:
                    x1d = x1 + multi_d1 * dx
                    y1d = y1 + multi_d1 * dy
                    if x1d < 0 or x1d >= x_max or y1d < 0 or y1d >= y_max:
                        break_d1 = True
                    else:
                        multi_d1 += 1
                        antinodes_2.add((x1d, y1d))

                while not break_d2:
                    x2d = x2 - multi_d2 * dx
                    y2d = y2 - multi_d2 * dy
                    if x2d < 0 or x2d >= x_max or y2d < 0 or y2d >= y_max:
                        break_d2 = True
                    else:
                        multi_d2 += 1
                        antinodes_2.add((x2d, y2d))

    print(f"Total 1: {len(antinodes_1)}")
    print(f"Total 2: {len(antinodes_2)}")


if __name__ == "__main__":
    day8()
