def compute_sum_of_hashes(line: str) -> int:
    return sum(map(get_hash, line.split(',')))


def get_hash(step: str) -> int:
    value: int = 0
    for character in step:
        value += ord(character)
        value *= 17
        value = value % 256
    return value
