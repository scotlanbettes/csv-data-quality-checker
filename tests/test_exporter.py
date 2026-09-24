import pandas as pd

from data_quality.cleaner import clean_dataframe

from data_quality.exporter import (
    dataframe_to_csv_bytes,
    generate_text_quality_report,
    quality_report_to_bytes,
)


def test_dataframe_to_csv_bytes():
    df = pd.DataFrame({
        "id": [1, 2],
        "name": [
            "Alice",
            "Bob",
        ],
    })

    result = dataframe_to_csv_bytes(df)

    assert isinstance(result, bytes)

    decoded = result.decode("utf-8")

    assert "id,name" in decoded
    assert "Alice" in decoded
    assert "Bob" in decoded


def test_generate_text_quality_report():
    before_df = pd.DataFrame({
        "id": [1, 2, 2],
        "name": [
            " Alice ",
            "Bob",
            "Bob",
        ],
    })

    after_df = clean_dataframe(
        before_df
    )

    report = generate_text_quality_report(
        before_df,
        after_df,
    )

    assert (
        "CSV DATA QUALITY CHECKER - VERSION 2"
        in report
    )

    assert "BEFORE CLEANING" in report
    assert "AFTER CLEANING" in report
    assert "CLEANING SUMMARY" in report
    assert "Quality Score" in report


def test_quality_report_to_bytes():
    before_df = pd.DataFrame({
        "id": [1, 2, 2],
        "name": [
            "Alice",
            "Bob",
            "Bob",
        ],
    })

    after_df = clean_dataframe(
        before_df
    )

    result = quality_report_to_bytes(
        before_df,
        after_df,
    )

    assert isinstance(result, bytes)

    decoded = result.decode("utf-8")

    assert "CLEANING SUMMARY" in decoded
