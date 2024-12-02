def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def is_report_safe(l: list[int]) -> bool:
    if (all(l[i] < l[i + 1] for i in range(len(l) - 1)) or all(l[i] > l[i + 1] for i in range(len(l) - 1))) and not any(
        abs(l[i] - l[i + 1]) > 3 for i in range(len(l) - 1)
    ):
        # print(f"Safe: {l}")
        return True
    else:
        return False


def day2():
    lines = read_lines("02/input_example")
    lines = read_lines("02/input")

    total_1: int = 0
    total_2: int = 0
    for line in lines:
        l: list[int] = [int(x) for x in line.split(" ")]
        # print(f"List: {l}")

        # Report is inherently safe
        if is_report_safe(l):
            total_1 += 1
            total_2 += 1
            continue

        for i in range(len(l)):
            if is_report_safe(l[:i] + l[i + 1 :]):
                # print(f"{l} is safe with damper")
                total_2 += 1
                break

    print(f"Total 1: {total_1}")
    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day2()
