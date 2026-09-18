import random

SKIP_WEIGHT = 0.20
ONE_WEIGHT = 0.60
TWO_WEIGHT = 0.20


def decide_commits():
    roll = random.random()
    if roll < SKIP_WEIGHT:
        return 0
    if roll < SKIP_WEIGHT + ONE_WEIGHT:
        return 1
    return 2


if __name__ == "__main__":
    print(f"commits={decide_commits()}")