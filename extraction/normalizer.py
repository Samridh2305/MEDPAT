from rapidfuzz import process
import re
from common.lab_test import LAB_TESTS

def normalize_test_name(
    raw_name: str,
) -> tuple[str | None, float]:

    best = process.extractOne(
        raw_name,
        LAB_TESTS,
    )

    if not best:
        return None, 0.0

    matched_name, score, _ = best

    if score < 85:
        return None, score / 100

    return matched_name, score / 100

def parse_reference_range(
    reference_range: str | None,
) -> tuple[float | None, float | None]:

    if not reference_range:
        return None, None

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)",
        reference_range,
    )

    if not match:
        return None, None

    return (
        float(match.group(1)),
        float(match.group(2)),
    )