def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def debug(file_system: list[int]):
    for i in file_system:
        if i == -1:
            print(".", end="")
        else:
            print(i, end="")
    print()


def get_filesystem() -> list[int]:
    line = read_lines("09/input_example")[0]
    line = read_lines("09/input")[0]

    file_system: list[int] = []
    file_id: int = 0
    for str_index, char in enumerate(line):
        # print(f"index: {str_index}, number: {char}, file_id: {file_id}")
        i_char = int(char)
        if str_index % 2 == 0:
            for _ in range(i_char):
                file_system.append(file_id)
            file_id += 1
        else:
            for _ in range(i_char):
                file_system.append(-1)
    return file_system


def calc_checksum(file_system: list[int]) -> int:
    total: int = 0
    for i, file_id in enumerate(file_system):
        if file_id == -1:
            continue
        total += i * file_id
    return total


def day9_1():
    file_system = get_filesystem()
    free_space = file_system.count(-1)

    for i, file_id in enumerate(file_system[::-1]):
        if file_id == -1:
            continue
        # Check if there is still free space to swap
        if i == free_space:
            break
        # Swap
        file_system[file_system.index(-1)] = file_id
        file_system[-i - 1] = -1

    total_1 = calc_checksum(file_system)
    print(f"Total 1: {total_1}")


def find_free_space(file_system: list[int], size: int) -> int:
    for i, char in enumerate(file_system):
        if char != -1:
            continue
        if i + size >= len(file_system):
            return -1
        if all(file_system[i + j] == -1 for j in range(size)):
            return i
    return -1


def get_file_size(file_system: list[int], file_id: int) -> int:
    size = 1
    index = file_system.index(file_id)
    while index + size < len(file_system) and file_system[index + size] == file_id:
        size += 1

    return size


def day9_2():
    file_system = get_filesystem()

    largest_file_id: int = file_system[-1] + 1
    reversed_file_system = file_system[::-1]
    for i, file_id in enumerate(reversed_file_system):
        # Skip empty spaces
        if file_id == -1:
            continue
        # Skip if already looked at file
        if file_id >= largest_file_id:
            continue
        else:
            largest_file_id = file_id

        # Get size of file
        file_size = get_file_size(file_system, file_id)
        # Check if there is free space for it
        free_index = find_free_space(file_system[: len(file_system) - i], file_size)

        # Continue if there is no free space
        if free_index == -1:
            continue

        # Swap
        for j in range(file_size):
            file_system[file_system.index(file_id)] = -1
        for j in range(file_size):
            file_system[free_index + j] = file_id

    total_2 = calc_checksum(file_system)
    print(f"Total 2: {total_2}")


if __name__ == "__main__":
    day9_1()
    day9_2()
