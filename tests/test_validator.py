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
    check_empty_strings,
    check_whitespace_issues,
    check_inconsistent_data_types,
    check_outliers,
    check_inconsistent_capitalization,
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


def test_empty_strings():
    df = pd.DataFrame({
        "name": ["Alice", "", "   ", None, "David"],
        "city": ["Nairobi", "Mombasa", "", "Kisumu", "Eldoret"],
    })

    result = check_empty_strings(df)

    assert result["name"] == 3
    assert result["city"] == 1


def test_whitespace_issues():
    df = pd.DataFrame({
        "name": ["Alice", " Bob", "Charlie ", " David "],
        "city": ["Nairobi", "Mombasa", "Kisumu", "Eldoret"],
    })

    result = check_whitespace_issues(df)

    assert result["name"] == 3
    assert result["city"] == 0


def test_inconsistent_data_types():
    df = pd.DataFrame({
        "mixed": [1, "2", 3.5, None],
        "normal": ["Alice", "Bob", "Charlie", "David"],
    })

    result = check_inconsistent_data_types(df)

    assert result["mixed"] == 3
    assert result["normal"] == 1


def test_outliers():
    df = pd.DataFrame({
        "age": [20, 21, 22, 23, 24, 100],
        "score": [70, 72, 74, 76, 78, 80],
        "name": ["A", "B", "C", "D", "E", "F"],
    })

    result = check_outliers(df)

    assert result["age"] == 1
    assert result["score"] == 0


def test_inconsistent_capitalization():
    df = pd.DataFrame({
        "city": [
            "Nairobi",
            "nairobi",
            "NAIROBI",
            "Mombasa",
            "Kisumu",
        ],
        "status": [
            "Active",
            "Inactive",
            "Pending",
            "Closed",
            "Open",
        ],
    })

    result = check_inconsistent_capitalization(df)

    assert result["city"] == 3
    assert result["status"] == 0
