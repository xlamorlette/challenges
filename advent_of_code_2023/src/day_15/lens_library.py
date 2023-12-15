import functools


def compute_sum_of_hashes(line: str) -> int:
    return sum(map(get_hash, line.split(',')))


def get_hash(step: str) -> int:
    return functools.reduce(lambda value, character: ((value + ord(character)) * 17) % 256, step, 0)
