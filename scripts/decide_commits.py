import os
import random
from datetime import datetime, timezone

SKIP_WEIGHT = 0.20
ONE_WEIGHT = 0.60
TWO_WEIGHT = 0.20

LAST_UPDATE = os.path.join("data", "last_update.txt")
MAX_GAP_DAYS = 3


def days_since_last_commit():
    try:
        with open(LAST_UPDATE, "r", encoding="utf-8") as f:
            last = datetime.fromisoformat(f.read().strip()).date()
    except (OSError, ValueError):
        return MAX_GAP_DAYS + 1
    today = datetime.now(timezone.utc).date()
    return (today - last).days


def roll():
    r = random.random()
    if r < SKIP_WEIGHT:
        return 0
    if r < SKIP_WEIGHT + ONE_WEIGHT:
        return 1
    return 2


def decide_commits():
    commits = roll()
    if days_since_last_commit() >= MAX_GAP_DAYS:
        return max(1, commits)
    return commits


if __name__ == "__main__":
    print(f"commits={decide_commits()}")