import re


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


# MAGIC?!?!?!?!?!?!?!?!
# https://the-algorithms.com/algorithm/cramers-rule-2x-2?lang=python
def cramers_rule(ax: int, ay: int, bx: int, by: int, px: int, py: int):
    determinant = ax * by - ay * bx

    x = (px * by - py * bx) / determinant
    y = (py * ax - px * ay) / determinant

    return x, y


def day13():
    lines = read_lines("13/input_example")
    lines = read_lines("13/input")

    total_1: int = 0
    total_2: int = 0
    for line in "\n".join(lines).split("\n\n"):
        ax, ay, bx, by, px, py = map(int, re.findall(r"\d+", line))

        a, b = cramers_rule(ax, ay, bx, by, px, py)

        if a.is_integer() and b.is_integer() and 0 <= a < 100 and 0 <= b < 100:
            total_1 += 3 * int(a) + int(b)

        a, b = cramers_rule(ax, ay, bx, by, px + 10000000000000, py + 10000000000000)
        if a.is_integer() and b.is_integer() and 0 <= a and 0 <= b:
            total_2 += 3 * int(a) + int(b)

    print(f"Total 1: {total_1}")
    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day13()
