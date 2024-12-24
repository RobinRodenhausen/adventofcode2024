from collections import Counter, defaultdict


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def debug(gates: dict[str, bool | None], gate_prefix: str) -> tuple[str, int]:
    binary: str = ""
    for g, v in sorted(gates.items())[::-1]:
        if g.startswith(gate_prefix):
            binary += "1" if v else "0"
    return binary, int(binary, 2)


def debug2(gates: list[str], parents: defaultdict[str, set[str]]) -> list[str]:
    broken_gates: list[str] = []
    for gate in gates:
        print(f"{gate}: {sorted(parents[gate])}")
        for g in parents[gate]:
            if g.startswith("x") or g.startswith("y"):
                continue
            broken_gates.append(g)

    print(sorted(broken_gates))
    print(Counter(broken_gates))
    print(len(broken_gates))
    print(len(set(broken_gates)))

    return broken_gates


def day24():
    lines = read_lines("24/input_example1")
    lines = read_lines("24/input_example2")
    lines = read_lines("24/input_example3")
    lines = read_lines("24/input")

    gate_lines, logic_lines = "\n".join(lines).split("\n\n")

    gates: dict[str, bool | None] = {}
    parents: defaultdict[str, set[str]] = defaultdict(set)
    children: defaultdict[str, set[str]] = defaultdict(set)
    potentially_broken_gates: set[str] = set()

    for gate_line in gate_lines.split("\n"):
        gate, value = gate_line.split(": ")
        gates[gate] = True if value == "1" else False

    operations: dict[str, tuple[str, str, str]] = {}
    for logic_line in logic_lines.split("\n"):
        g1, op, g2, _, g3 = logic_line.split(" ")

        parents[g3].add(g1)
        parents[g3].add(g2)
        children[g1].add(g3)
        children[g2].add(g3)

        potentially_broken_gates.add(g1)
        potentially_broken_gates.add(g2)
        potentially_broken_gates.add(g3)

        for g in [g1, g2, g3]:
            if g not in gates:
                gates[g] = None

        operations[g3] = (g1, g2, op)

    while any(g is None for g in gates.values()):
        for g3, (g1, g2, op) in operations.items():
            if gates[g3] is not None:
                continue

            if op == "AND":
                if gates[g1] is not None and gates[g2] is not None:
                    gates[g3] = gates[g1] and gates[g2]
            elif op == "OR":
                if gates[g1] is not None and gates[g2] is not None:
                    gates[g3] = gates[g1] or gates[g2]
            elif op == "XOR":
                if gates[g1] is not None and gates[g2] is not None:
                    gates[g3] = gates[g1] != gates[g2]

    binary: str = ""
    for g, v in sorted(gates.items())[::-1]:
        if g.startswith("z"):
            binary += "1" if v else "0"
    print(f"Total 1: {int(binary, 2)}")

    # Part 2
    xb, xi = debug(gates, "x")
    yb, yi = debug(gates, "y")
    zb, zi = debug(gates, "z")

    correct_int = xi + yi
    correct_bin = f"{correct_int:b}"
    print(correct_bin)
    print(zb)

    correct_gates: set[str] = set()

    # If I want to add two numbers, I know the correct value of the x and y gates
    for gate in potentially_broken_gates:
        if gate.startswith("x") or gate.startswith("y"):
            correct_gates.add(gate)

    for gate in correct_gates:
        potentially_broken_gates.discard(gate)

    rev_correct_bin = correct_bin[::-1]
    rev_zb = zb[::-1]

    broken_end_gates: list[str] = []

    # Check if bits on the z gates are correct
    for i in range(len(rev_correct_bin)):
        if rev_zb[i] != rev_correct_bin[i]:
            print(f"Error at z{i:02} - {rev_correct_bin[i]} != {rev_zb[i]}")
            broken_end_gates.append(f"z{i:02}")
        else:
            correct_gates.add(f"z{i:02}")

    print(f"Bits wrong: {len(broken_end_gates)}")
    # If the z bit is correct, it should be the correct output
    for gate in correct_gates:
        potentially_broken_gates.discard(gate)

    # If the child is correct, the parent should be correct
    # At this point only x,y,z gates are confirmed to be correct
    for gate in potentially_broken_gates:
        if gate.startswith("z"):
            continue
        for child in children[gate]:
            if child in correct_gates:
                correct_gates.add(gate)

    for gate in correct_gates:
        potentially_broken_gates.discard(gate)

    print(f"Potentially broken gates: {sorted(potentially_broken_gates)}")

    sorted_children = dict(sorted(children.items()))

    for k, v in sorted_children.items():
        if k.startswith("x") or k.startswith("y"):
            continue
        print(f"Parent {k}: {v}")

    broken_gates_tmp: list[str] = broken_end_gates
    for i in range(20):
        print(f"Loop {i}")
        broken_gates_tmp = debug2(broken_gates_tmp.copy(), parents)
        print(potentially_broken_gates)
        print(len(potentially_broken_gates))
        pass


if __name__ == "__main__":
    day24()
