import pandas as pd

from data_quality.cleaner import (
    trim_whitespace,
    remove_duplicate_rows,
    standardize_empty_strings,
    clean_dataframe,
)


def test_trim_whitespace():
    df = pd.DataFrame({
        "name": [
            " Alice ",
            "Bob ",
            " Charlie",
        ],
        "age": [20, 21, 22],
    })

    result = trim_whitespace(df)

    assert result["name"].tolist() == [
        "Alice",
        "Bob",
        "Charlie",
    ]


def test_remove_duplicate_rows():
    df = pd.DataFrame({
        "id": [1, 2, 2, 3],
        "name": [
            "Alice",
            "Bob",
            "Bob",
            "David",
        ],
    })

    result = remove_duplicate_rows(df)

    assert len(result) == 3
    assert result["id"].tolist() == [
        1,
        2,
        3,
    ]


def test_standardize_empty_strings():
    df = pd.DataFrame({
        "name": [
            "Alice",
            "",
            "   ",
            "David",
        ],
    })

    result = standardize_empty_strings(df)

    assert result["name"].isna().sum() == 2


def test_clean_dataframe():
    df = pd.DataFrame({
        "id": [1, 2, 2, 3],
        "name": [
            " Alice ",
            " Bob ",
            " Bob ",
            "   ",
        ],
    })

    result = clean_dataframe(df)

    assert len(result) == 3

    assert result["name"].iloc[0] == "Alice"
    assert result["name"].iloc[1] == "Bob"
    assert pd.isna(result["name"].iloc[2])
