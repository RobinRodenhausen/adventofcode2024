def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


DIRECTIONS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}


def move_box_1(x: int, y: int, dx: int, dy: int, warehouse: list[list[str]]) -> bool:
    bx, by = x + dx, y + dy
    # If box is at wall stay in place
    if warehouse[by][bx] == "#":
        return False
    # if box has empty space move
    if warehouse[by][bx] == ".":
        warehouse[y][x] = "."
        warehouse[by][bx] = "O"
        return True
    if warehouse[by][bx] == "O":
        if move_box_1(bx, by, dx, dy, warehouse):
            warehouse[y][x] = "."
            warehouse[by][bx] = "O"
            return True
    return False


def day15_1():
    lines = read_lines("15/input_example1")
    lines = read_lines("15/input_example2")
    lines = read_lines("15/input")

    warehouse_lines, instruction_lines = "\n".join(lines).split("\n\n")

    warehouse: list[list[str]] = []
    robot: tuple[int, int] = (-1, -1)
    for y, line in enumerate(warehouse_lines.split("\n")):
        warehouse.append([])
        for x, char in enumerate(line):
            if char == "@":
                robot = (x, y)
                warehouse[y].append(".")
                continue
            warehouse[y].append(char)

    instructions = instruction_lines.replace("\n", "")

    for char in instructions:
        dx, dy = DIRECTIONS[char]
        x, y = robot
        x += dx
        y += dy

        # If wall stay in place
        if warehouse[y][x] == "#":
            continue
        # If empty space move
        if warehouse[y][x] == ".":
            robot = (x, y)
            continue
        # If box
        if warehouse[y][x] == "O":
            if move_box_1(x, y, dx, dy, warehouse):
                robot = (x, y)

    total_1: int = 0

    for y, line in enumerate(warehouse):
        for x, char in enumerate(line):
            if char == "O":
                total_1 += 100 * y + x

    print(f"Total 1: {total_1}")


def can_move_box(x: int, y: int, dx: int, dy: int, warehouse: list[list[str]]) -> bool:
    if dy == 0:
        b2x, b2y = x + 2 * dx, y
        if warehouse[b2y][b2x] == "#":
            return False
        if warehouse[b2y][b2x] == ".":
            return True

        if warehouse[b2y][b2x] in ["[", "]"]:
            if can_move_box(b2x, b2y, dx, dy, warehouse):
                return True
    if dx == 0:
        x1, y1 = x, y
        if warehouse[y][x] == "[":
            x2 = x + 1
            y2 = y
        else:  # warehouse[y][x] == "]":
            x2 = x - 1
            y2 = y
        bx1, by1 = x1, y1 + dy
        bx2, by2 = x2, y2 + dy
        if warehouse[by1][bx1] == "#" or warehouse[by2][bx2] == "#":
            return False
        if warehouse[by1][bx1] == "." and warehouse[by2][bx2] == ".":
            return True
        # Boxes aligned
        if warehouse[y1][x1] == warehouse[by1][bx1]:
            if can_move_box(bx1, by1, dx, dy, warehouse):
                return True
        # Boxes unaligned
        else:
            # If both boxes have another box behind them
            if warehouse[by1][bx1] in ["[", "]"] and warehouse[by2][bx2] in ["[", "]"]:
                if can_move_box(bx1, by1, dx, dy, warehouse) and can_move_box(bx2, by2, dx, dy, warehouse):
                    return True
            # If only one box has another box behind it
            elif warehouse[by1][bx1] in ["[", "]"]:
                if can_move_box(bx1, by1, dx, dy, warehouse):
                    return True
            elif warehouse[by2][bx2] in ["[", "]"]:
                if can_move_box(bx2, by2, dx, dy, warehouse):
                    return True
    return False


def move_box_2(x: int, y: int, dx: int, dy: int, warehouse: list[list[str]]) -> bool:
    if dy == 0:
        b1x, b1y = x + dx, y
        b2x, b2y = x + 2 * dx, y
        if warehouse[b2y][b2x] == "#":
            return False
        if warehouse[b2y][b2x] == ".":
            warehouse[b2y][b2x] = warehouse[b1y][b1x]
            warehouse[b1y][b1x] = warehouse[y][x]
            warehouse[y][x] = "."
            return True

        if warehouse[b2y][b2x] in ["[", "]"]:
            if move_box_2(b2x, b2y, dx, dy, warehouse):
                warehouse[b2y][b2x] = warehouse[b1y][b1x]
                warehouse[b1y][b1x] = warehouse[y][x]
                warehouse[y][x] = "."
                return True
    if dx == 0:
        x1, y1 = x, y
        if warehouse[y][x] == "[":
            x2 = x + 1
            y2 = y
        else:  # warehouse[y][x] == "]":
            x2 = x - 1
            y2 = y
        bx1, by1 = x1, y1 + dy
        bx2, by2 = x2, y2 + dy
        if warehouse[by1][bx1] == "#" or warehouse[by2][bx2] == "#":
            return False
        if warehouse[by1][bx1] == "." and warehouse[by2][bx2] == ".":
            warehouse[by1][bx1] = warehouse[y1][x1]
            warehouse[by2][bx2] = warehouse[y2][x2]
            warehouse[y1][x1] = "."
            warehouse[y2][x2] = "."
            return True
        # Boxes aligned
        if warehouse[y1][x1] == warehouse[by1][bx1]:
            if move_box_2(bx1, by1, dx, dy, warehouse):
                warehouse[by1][bx1] = warehouse[y1][x1]
                warehouse[by2][bx2] = warehouse[y2][x2]
                warehouse[y1][x1] = "."
                warehouse[y2][x2] = "."
                return True
        # Boxes unaligned
        else:
            # CHECK IF WHOLE STACK CAN EVEN MOVE
            # Otherwise it will move part of the boxes even though it shouldn't be possible. Occurs first in instruction 638...
            if not can_move_box(x, y, dx, dy, warehouse):
                return False
            # If both boxes have another box behind them
            if warehouse[by1][bx1] in ["[", "]"] and warehouse[by2][bx2] in ["[", "]"]:
                if move_box_2(bx1, by1, dx, dy, warehouse) and move_box_2(bx2, by2, dx, dy, warehouse):
                    warehouse[by1][bx1] = warehouse[y1][x1]
                    warehouse[by2][bx2] = warehouse[y2][x2]
                    warehouse[y1][x1] = "."
                    warehouse[y2][x2] = "."
                    return True
            # If only one box has another box behind it
            elif warehouse[by1][bx1] in ["[", "]"]:
                if move_box_2(bx1, by1, dx, dy, warehouse):
                    warehouse[by1][bx1] = warehouse[y1][x1]
                    warehouse[by2][bx2] = warehouse[y2][x2]
                    warehouse[y1][x1] = "."
                    warehouse[y2][x2] = "."
                    return True
            elif warehouse[by2][bx2] in ["[", "]"]:
                if move_box_2(bx2, by2, dx, dy, warehouse):
                    warehouse[by1][bx1] = warehouse[y1][x1]
                    warehouse[by2][bx2] = warehouse[y2][x2]
                    warehouse[y1][x1] = "."
                    warehouse[y2][x2] = "."
                    return True
    return False


def debug_warehouse(warehouse: list[list[str]], robot: tuple[int, int]):
    for y, line in enumerate(warehouse):
        for x, char in enumerate(line):
            if (x, y) == robot:
                print("@", end="")
            else:
                print(char, end="")
        print()
    print()


def day15_2():
    lines = read_lines("15/input_example1")
    lines = read_lines("15/input_example2")
    # lines = read_lines("15/input_example3")
    lines = read_lines("15/input")

    warehouse_lines, instruction_lines = "\n".join(lines).split("\n\n")

    warehouse: list[list[str]] = []
    robot: tuple[int, int] = (-1, -1)
    for y, line in enumerate(warehouse_lines.split("\n")):
        warehouse.append([])
        for x, char in enumerate(line):
            if char == "@":
                robot = (-1, y)
                warehouse[y].append("@")
                warehouse[y].append(".")
                continue
            if char == "O":
                warehouse[y].append("[")
                warehouse[y].append("]")
                continue
            warehouse[y].append(char)
            warehouse[y].append(char)

    robot_x = warehouse[robot[1]].index("@")
    robot = (robot_x, robot[1])
    warehouse[robot[1]][robot[0]] = "."

    instructions = instruction_lines.replace("\n", "")

    for i, char in enumerate(instructions):

        # if i >= 638:
        #     debug_warehouse(warehouse, robot)
        #     print(i, char)
        dx, dy = DIRECTIONS[char]
        x, y = robot
        x += dx
        y += dy

        # If wall stay in place
        if warehouse[y][x] == "#":
            continue
        # If empty space move
        if warehouse[y][x] == ".":
            robot = (x, y)
            continue
        # If box
        if warehouse[y][x] in ["[", "]"]:
            if move_box_2(x, y, dx, dy, warehouse):
                robot = (x, y)

    total_2: int = 0
    for y, line in enumerate(warehouse):
        for x, char in enumerate(line):
            if char == "[":
                total_2 += 100 * y + x

    print(f"Total 2: {total_2}")
    # 1350905 too high without prior can_move_box check


if __name__ == "__main__":
    day15_1()
    day15_2()
