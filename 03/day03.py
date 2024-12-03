import re


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def day3():
    lines = read_lines("03/input_example1")
    lines = read_lines("03/input_example2")
    lines = read_lines("03/input")

    input = "".join(lines)

    matches = re.findall(r"(mul\(\d{1,3},\d{1,3}\))|(don\'t\(\))|(do\(\))", input)

    print(matches)

    total_1: int = 0
    total_2: int = 0
    skip = False
    for match in matches:
        if match[0]:
            mul1, mul2 = re.findall(r"\d{1,3}", match[0])
            total_1 += int(mul1) * int(mul2)
            if not skip:
                total_2 += int(mul1) * int(mul2)
        if match[1]:
            skip = True
            continue
        if match[2]:
            skip = False
            continue

    print(f"Total 1: {total_1}")
    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day3()
