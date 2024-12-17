import re


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_combo_operand(operand: int, register: list[int]) -> int:
    if 0 <= operand <= 3:
        return operand
    elif 4 <= operand <= 6:
        return register[operand - 4]
    else:
        # raise ValueError(f"Invalid operand: {operand}")
        return -1


def perform(cip: int, register: list[int], program: list[int], output: list[int]) -> int:
    opcode: int = program[cip]
    literal_operand: int = program[cip + 1]
    combo_operand: int = get_combo_operand(program[cip + 1], register)

    # adv
    if opcode == 0:
        register[0] = register[0] // 2**combo_operand
        cip += 2
    # bxl
    elif opcode == 1:
        register[1] = register[1] ^ literal_operand
        cip += 2
    # bst
    elif opcode == 2:
        register[1] = combo_operand % 8
        cip += 2
    # jnz
    elif opcode == 3:
        if register[0] != 0:
            cip = literal_operand
        else:
            cip += 2
    # bxc
    elif opcode == 4:
        register[1] = register[1] ^ register[2]
        cip += 2
    # out
    elif opcode == 5:
        output.append(combo_operand % 8)
        cip += 2
    # bdv
    elif opcode == 6:
        register[1] = register[0] // 2**combo_operand
        cip += 2
    # cdv
    elif opcode == 7:
        register[2] = register[0] // 2**combo_operand
        cip += 2

    return cip


def run(register: list[int], program: list[int]) -> list[int]:
    # current instruction pointer
    cip: int = 0
    output: list[int] = []

    while cip < len(program):
        cip = perform(cip, register, program, output)

    return output


# https://old.reddit.com/r/adventofcode/comments/1hg38ah/2024_day_17_solutions/m2gge90/
# ????????????????????????????
def get_best_quine_input(program: list[int], cursor: int, sofar: int) -> int:
    for candidate in range(8):
        if run([sofar * 8 + candidate, 0, 0], program) == program[cursor:]:
            if cursor == 0:
                return sofar * 8 + candidate
            ret = get_best_quine_input(program, cursor - 1, sofar * 8 + candidate)
            if ret >= 0:
                return ret
    return -1


def day17():
    lines = read_lines("17/input_example1")
    lines = read_lines("17/input_example2")
    lines = read_lines("17/input")

    register_lines, program_lines = "\n".join(lines).split("\n\n")

    # 0: A, 1: B, 2: C
    register: list[int] = list(map(int, re.findall(r"-?\d+", register_lines)))
    program: list[int] = list(map(int, re.findall(r"-?\d+", program_lines)))

    output = run(register, program)

    print(f"Result 1: {",".join(map(str, output))}")

    print(f"Result 2: {get_best_quine_input(program, len(program) - 1, 0)}")


# Brute Force does not work if the result is 190593310997519 .......
def day17_2():
    lines = read_lines("17/input_example2")
    # lines = read_lines("17/input")

    register_lines, program_lines = "\n".join(lines).split("\n\n")

    # 0: A, 1: B, 2: C
    register: list[int] = list(map(int, re.findall(r"-?\d+", register_lines)))
    program: list[int] = list(map(int, re.findall(r"-?\d+", program_lines)))

    total_2: int = -1
    for a in range(100000000):
        print(a)
        register[0] = a
        cip: int = 0
        output: list[int] = []
        while cip < len(program):
            opcode: int = program[cip]
            literal_operand: int = program[cip + 1]
            combo_operand: int = get_combo_operand(program[cip + 1], register)

            # adv
            if opcode == 0:
                register[0] = register[0] // 2**combo_operand
                cip += 2
            # bxl
            elif opcode == 1:
                register[1] = register[1] ^ literal_operand
                cip += 2
            # bst
            elif opcode == 2:
                register[1] = combo_operand % 8
                cip += 2
            # jnz
            elif opcode == 3:
                if register[0] != 0:
                    cip = literal_operand
                else:
                    cip += 2
            # bxc
            elif opcode == 4:
                register[1] = register[1] ^ register[2]
                cip += 2
            # out
            elif opcode == 5:
                output.append(combo_operand % 8)
                cip += 2
            # bdv
            elif opcode == 6:
                register[1] = register[0] // 2**combo_operand
                cip += 2
            # cdv
            elif opcode == 7:
                register[2] = register[0] // 2**combo_operand
                cip += 2

            for i, val in enumerate(output):
                if val != program[i]:
                    break
                if i == len(program) - 1:
                    total_2 = a
        if total_2 >= 0:
            break
    print(f"Result 2: {total_2}")


if __name__ == "__main__":
    day17()
    # day17_2()
