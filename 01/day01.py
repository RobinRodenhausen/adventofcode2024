def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def day1():
    # lines = read_lines("01/input_example")
    lines = read_lines("01/input")

    l1: list[int] = []
    l2: list[int] = []
    for line in lines:
        s = line.split("   ")
        l1.append(int(s[0]))
        l2.append(int(s[1]))

    l1 = sorted(l1)
    l2 = sorted(l2)

    total_1 = 0
    for i in range(len(l1)):
        total_1 += abs(l1[i] - l2[i])
    print(f"Total 1: {total_1}")

    total_2 = 0
    for i in l1:
        total_2 += i * l2.count(i)

    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day1()
