import pandas as pd

from data_quality.validator import (
    check_missing_values,
    check_duplicate_rows,
    check_duplicate_ids,
)


def test_missing_values():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", None, "Charlie"],
    })

    result = check_missing_values(df)

    assert result["name"] == 1


def test_duplicate_rows():
    df = pd.DataFrame({
        "id": [1, 2, 2],
        "name": ["Alice", "Bob", "Bob"],
    })

    result = check_duplicate_rows(df)

    assert result == 1


def test_duplicate_ids():
    df = pd.DataFrame({
        "id": [1, 2, 2, 3],
        "name": ["Alice", "Bob", "Bob", "David"],
    })

    result = check_duplicate_ids(df)

    assert result == 1
