from collections import defaultdict


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def custom_sort(x: int, rules: defaultdict[int, list[int]], current_update: list[int]):
    return sum(1 for rule in rules[x] if rule in current_update)


def day5():
    lines = read_lines("05/input_example")
    lines = read_lines("05/input")

    rules: defaultdict[int, list[int]] = defaultdict(list)
    updates: list[list[int]] = []

    for line in lines:
        if "|" in line:
            b, a = line.split("|")
            rules[int(a)].append(int(b))
        elif line:
            updates.append([int(x) for x in line.split(",")])

    total_1: int = 0
    broken_updates: list[list[int]] = []
    for update in updates:
        for index, page in enumerate(update):
            break_update = False
            for rule in rules[page]:
                if rule in update[index + 1 :]:
                    break_update = True
                    break
            if break_update:
                broken_updates.append(update)
                break
        else:
            total_1 += update[int((len(update) - 1) / 2)]

    print(f"Total 1: {total_1}")

    total_2: int = 0
    for broken_update in broken_updates:
        fixed_update = sorted(broken_update, key=lambda x: custom_sort(x, rules, broken_update))
        total_2 += fixed_update[int((len(fixed_update) - 1) / 2)]

    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day5()
