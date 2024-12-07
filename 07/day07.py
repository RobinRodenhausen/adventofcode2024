def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def calculate_all_combinations1(index: int, numbers: list[int], current_result: int, results: list[int]) -> None:
    if index == len(numbers):
        results.append(current_result)
        return
    calculate_all_combinations1(index + 1, numbers, current_result + numbers[index], results)
    calculate_all_combinations1(index + 1, numbers, current_result * numbers[index], results)


def calculate_all_combinations2(index: int, numbers: list[int], current_result: int, results: list[int]) -> None:
    if index == len(numbers):
        results.append(current_result)
        return
    calculate_all_combinations2(index + 1, numbers, current_result + numbers[index], results)
    calculate_all_combinations2(index + 1, numbers, current_result * numbers[index], results)
    calculate_all_combinations2(index + 1, numbers, int(str(current_result) + str(numbers[index])), results)


def day7():
    lines = read_lines("07/input_example")
    lines = read_lines("07/input")

    equations: dict[int, list[int]] = {}
    for line in lines:
        result, numbers = line.split(": ")
        equations[int(result)] = [int(n) for n in numbers.split(" ")]

    total_1: int = 0
    total_2: int = 0
    for result, numbers in equations.items():
        possible_results1: list[int] = []
        calculate_all_combinations1(1, numbers, numbers[0], possible_results1)

        if result in possible_results1:
            total_1 += result

        possible_results2: list[int] = []
        calculate_all_combinations2(1, numbers, numbers[0], possible_results2)

        if result in possible_results2:
            total_2 += result

    print(f"Total 1: {total_1}")
    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day7()
