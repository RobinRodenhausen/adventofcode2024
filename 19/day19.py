from collections import defaultdict


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def can_construct_1(towel_patterns: list[str], design: str, memo: dict[str, bool]) -> bool:
    if design in memo:
        return memo[design]
    if design == "":
        return True

    for pattern in towel_patterns:
        if design.startswith(pattern):
            if can_construct_1(towel_patterns, design[len(pattern) :], memo):
                memo[design] = True
                return True

    memo[design] = False
    return False


def can_construct_2(towel_patterns: list[str], design: str, memo: defaultdict[str, int]) -> int:
    if design in memo:
        return memo[design]
    if design == "":
        return 1

    for pattern in towel_patterns:
        pass
        if design.startswith(pattern):
            memo[design] += can_construct_2(towel_patterns, design[len(pattern) :], memo)

    return memo[design]


def day19():
    lines = read_lines("19/input_example")
    lines = read_lines("19/input")

    towel_patterns = lines[0].split(", ")
    designs = lines[2:]

    total_1: int = 0
    for design in designs:
        if can_construct_1(towel_patterns, design, {}):
            total_1 += 1

    print(f"Total 1: {total_1}")

    total_2: int = 0
    memo: defaultdict[str, int] = defaultdict(int)
    for design in designs:
        total_2 += can_construct_2(towel_patterns, design, memo)

    print(f"Total 2: {total_2}")

    # Alternative for part 1
    total_1_2: int = 0
    for design in designs:
        if memo[design] > 0:
            total_1_2 += 1

    print(f"Total 1_2: {total_1_2}")


if __name__ == "__main__":
    day19()
