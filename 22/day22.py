from collections import defaultdict


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def seq1(number: int) -> int:
    return ((number * 64) ^ number) % 16777216


def seq2(number: int) -> int:
    return ((number // 32) ^ number) % 16777216


def seq3(number: int) -> int:
    return ((number * 2048) ^ number) % 16777216


def day22():
    lines = read_lines("22/input_example1")
    lines = read_lines("22/input_example2")
    lines = read_lines("22/input")

    total_1: int = 0
    buyer_prices: list[list[int]] = []
    for i, line in enumerate(lines):
        number = int(line)
        buyer_prices.append([])
        buyer_prices[i].append(int(str(number)[-1]))

        for _ in range(2000):
            number = seq3(seq2(seq1(number)))
            buyer_prices[i].append(number % 10)

        total_1 += number

    print(f"Total 1: {total_1}")

    sequence_prices: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
    for buyer in buyer_prices:
        buyer_dict: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
        for i, price in enumerate(buyer):
            if i < 4:
                continue
            s1 = buyer[i - 3] - buyer[i - 4]
            s2 = buyer[i - 2] - buyer[i - 3]
            s3 = buyer[i - 1] - buyer[i - 2]
            s4 = buyer[i] - buyer[i - 1]

            sequence = (s1, s2, s3, s4)

            # Monkey is stupid. It sells at the first occurrence of a sequence not at the best price for that sequence.
            # if buyer_dict[sequence] < price:
            if sequence not in buyer_dict:
                buyer_dict[sequence] = price

        for key, value in buyer_dict.items():
            sequence_prices[key] += value

    # 2450 too high
    # 2423
    print(f"Total 2: {max(sequence_prices.values())}")


if __name__ == "__main__":
    day22()
