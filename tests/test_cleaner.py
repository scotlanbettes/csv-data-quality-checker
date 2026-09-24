import pandas as pd

from data_quality.cleaner import (
    trim_whitespace,
    remove_duplicate_rows,
    standardize_empty_strings,
    drop_missing_rows,
    fill_numeric_missing,
    fill_text_missing_with_mode,
    fill_missing_with_custom_value,
    handle_missing_values,
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


def test_drop_missing_rows():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": [
            "Alice",
            None,
            "Charlie",
        ],
    })

    result = drop_missing_rows(df)

    assert len(result) == 2
    assert result["id"].tolist() == [1, 3]


def test_fill_numeric_missing_mean():
    df = pd.DataFrame({
        "age": [
            20.0,
            None,
            40.0,
        ],
    })

    result = fill_numeric_missing(
        df,
        strategy="mean",
    )

    assert result["age"].iloc[1] == 30.0
    assert result["age"].isna().sum() == 0


def test_fill_numeric_missing_median():
    df = pd.DataFrame({
        "score": [
            10.0,
            20.0,
            None,
            100.0,
        ],
    })

    result = fill_numeric_missing(
        df,
        strategy="median",
    )

    assert result["score"].iloc[2] == 20.0
    assert result["score"].isna().sum() == 0


def test_fill_text_missing_with_mode():
    df = pd.DataFrame({
        "city": [
            "Nairobi",
            None,
            "Nairobi",
            "Mombasa",
        ],
    })

    result = fill_text_missing_with_mode(df)

    assert result["city"].iloc[1] == "Nairobi"
    assert result["city"].isna().sum() == 0


def test_fill_missing_with_custom_value():
    df = pd.DataFrame({
        "status": [
            "Active",
            None,
            "Pending",
        ],
    })

    result = fill_missing_with_custom_value(
        df,
        value="Unknown",
    )

    assert result["status"].iloc[1] == "Unknown"
    assert result["status"].isna().sum() == 0


def test_clean_dataframe_with_missing_strategy():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": [
            " Alice ",
            None,
            " Charlie ",
        ],
        "age": [
            20.0,
            None,
            40.0,
        ],
    })

    result = clean_dataframe(
        df,
        missing_strategy="mean",
    )

    assert result["name"].iloc[0] == "Alice"
    assert result["name"].iloc[2] == "Charlie"
    assert result["age"].iloc[1] == 30.0
