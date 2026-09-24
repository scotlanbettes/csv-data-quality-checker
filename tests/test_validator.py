import pandas as pd

from data_quality.metrics import (
    calculate_missing_percentage,
    calculate_duplicate_percentage,
    calculate_quality_score,
    calculate_quality_breakdown,
    calculate_column_quality_scores,
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

    # V2 weighted scoring:
    # Missing values: 12.5% * 0.30 = 3.75
    # Duplicate rows: 25% * 0.15 = 3.75
    # Duplicate IDs: 25% * 0.10 = 2.50
    # Total penalty = 10
    assert result == 90.0


def test_quality_breakdown():
    df = pd.DataFrame({
        "id": [1, 2, 2, 3],
        "name": ["Alice", "Bob", "Bob", None],
    })

    result = calculate_quality_breakdown(df)

    assert result["missing_values"] == 12.5
    assert result["duplicate_rows"] == 25.0
    assert result["duplicate_ids"] == 25.0
    assert result["empty_strings"] == 0.0
    assert result["whitespace_issues"] == 0.0
    assert result["inconsistent_data_types"] == 0.0
    assert result["outliers"] == 0.0
    assert result["inconsistent_capitalization"] == 0.0


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
    assert result["duplicate_ids"] == 1

    assert result["empty_strings"] == 0
    assert result["whitespace_issues"] == 0
    assert result["inconsistent_type_columns"] == 0
    assert result["outliers"] == 0
    assert result["capitalization_issues"] == 0

    assert result["missing_percentage"] == 12.5
    assert result["duplicate_percentage"] == 25.0
    assert result["duplicate_id_percentage"] == 25.0

    assert result["empty_string_percentage"] == 0.0
    assert result["whitespace_percentage"] == 0.0
    assert result["inconsistent_type_percentage"] == 0.0
    assert result["outlier_percentage"] == 0.0
    assert result["capitalization_percentage"] == 0.0

    assert result["quality_score"] == 90.0


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


def test_column_quality_scores():
    df = pd.DataFrame({
        "id": [1, 2, 2, 3, 4, 5],
        "city": [
            "Nairobi",
            "nairobi",
            "NAIROBI",
            "Mombasa",
            "",
            None,
        ],
        "age": [20, 21, 22, 23, 24, 100],
    })

    result = calculate_column_quality_scores(df)

    assert len(result) == 3

    assert set(result["column"]) == {
        "id",
        "city",
        "age",
    }

    id_score = result.loc[
        result["column"] == "id",
        "quality_score"
    ].iloc[0]

    city_score = result.loc[
        result["column"] == "city",
        "quality_score"
    ].iloc[0]

    age_score = result.loc[
        result["column"] == "age",
        "quality_score"
    ].iloc[0]

    assert id_score == 99.17
    assert city_score == 87.5
    assert age_score == 97.5
