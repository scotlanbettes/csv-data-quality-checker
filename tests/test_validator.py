import pandas as pd
from data_quality.metrics import (
    calculate_missing_percentage,
    calculate_duplicate_percentage,
    calculate_quality_score,
    generate_quality_metrics,
)

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


def test_missing_percentage():
    df = pd.DataFrame({
        "id": [1, 2],
        "name": ["Alice", None],
    })

    result = calculate_missing_percentage(df)

    assert result == 25.0


def test_duplicate_percentage():
    df = pd.DataFrame({
        "id": [1, 2, 2, 3],
        "name": ["Alice", "Bob", "Bob", "David"],
    })

    result = calculate_duplicate_percentage(df)

    assert result == 25.0


def test_quality_score():
    df = pd.DataFrame({
        "id": [1, 2, 2, 3],
        "name": ["Alice", "Bob", "Bob", None],
    })

    result = calculate_quality_score(df)

    assert result == 62.5


def test_generate_quality_metrics():
    df = pd.DataFrame({
        "id": [1, 2, 2, 3],
        "name": ["Alice", "Bob", "Bob", None],
    })

    result = generate_quality_metrics(df)

    assert result["total_rows"] == 4
    assert result["total_columns"] == 2
    assert result["missing_values"] == 1
    assert result["duplicate_rows"] == 1
    assert result["missing_percentage"] == 12.5
    assert result["duplicate_percentage"] == 25.0
    assert result["quality_score"] == 62.5
