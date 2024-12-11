from collections import defaultdict


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def day11_1():
    line = read_lines("11/input_example")[0]
    line = read_lines("11/input")[0]

    stones: list[str] = line.split(" ")

    for _ in range(25):
        tmp: list[str] = []
        for stone in stones:
            if stone == "0":
                tmp.append("1")
            elif len(stone) % 2 == 0:
                tmp.append(str(int(stone[: len(stone) // 2])))
                tmp.append(str(int(stone[len(stone) // 2 :])))
            else:
                tmp.append(str(int(stone) * 2024))
        stones = tmp

    print(f"Total 1: {len(stones)}")


def day11_2():
    line = read_lines("11/input_example")[0]
    line = read_lines("11/input")[0]

    stones: defaultdict[str, int] = defaultdict(int)
    for stone in line.split(" "):
        stones[stone] += 1

    for i in range(75):
        tmp: defaultdict[str, int] = defaultdict(int)
        for stone, amount in stones.items():
            if stone == "0":
                tmp["1"] += amount
            elif len(stone) % 2 == 0:

                tmp[str(int(stone[: len(stone) // 2]))] += amount
                tmp[str(int(stone[len(stone) // 2 :]))] += amount
            else:
                tmp[str(int(stone) * 2024)] += amount
        stones = tmp
        # Alternative for 1
        if i == 24:
            print(f"Total 1: {sum(stones.values())}")
    print(f"Total 2: {sum(stones.values())}")


if __name__ == "__main__":
    day11_1()
    day11_2()
