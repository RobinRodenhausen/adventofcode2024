def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def day25():
    lines = read_lines("25/input_example")
    lines = read_lines("25/input")

    key_lock_lines = "\n".join(lines).split("\n\n")
    keys: list[tuple[int, int, int, int, int]] = []
    locks: list[tuple[int, int, int, int, int]] = []

    for key_lock_line in key_lock_lines:
        # t: list[int, int, int, int, int] = [0, 0, 0, 0, 0]
        t: list[int] = [-1, -1, -1, -1, -1]
        for _, line in enumerate(key_lock_line.split("\n")):
            for x, char in enumerate(line):
                if char == "#":
                    t[x] += 1

        if all(x == "#" for x in key_lock_line[0]):
            keys.append(tuple(t))
        elif all(x == "#" for x in key_lock_line[-1]):
            locks.append(tuple(t))
        else:
            raise ValueError("Invalid key/lock")

    total_1: int = 0
    for key in keys:
        for lock in locks:
            if all(key[i] + lock[i] < 6 for i in range(len(key))):
                total_1 += 1
                # print(f"Key: {key}, Lock: {lock}")
            else:
                # print(f"Key: {key}, Lock: {lock} - Not valid")
                pass

    print(f"Total 1: {total_1}")


if __name__ == "__main__":
    day25()
