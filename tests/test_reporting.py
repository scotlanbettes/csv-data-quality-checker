import pandas as pd

from data_quality.cleaner import clean_dataframe

from data_quality.reporting import (
    generate_cleaning_report,
    generate_quality_comparison,
)


def test_generate_cleaning_report():
    before_df = pd.DataFrame({
        "id": [1, 2, 2, 3],
        "name": [
            " Alice ",
            "Bob",
            "Bob",
            "",
        ],
    })

    after_df = clean_dataframe(
        before_df,
        missing_strategy="mode",
    )

    report = generate_cleaning_report(
        before_df,
        after_df,
    )

    assert report["before"]["total_rows"] == 4
    assert report["after"]["total_rows"] == 3

    assert report["changes"]["rows_removed"] == 1

    assert (
        report["changes"]["duplicate_rows_removed"]
        == 1
    )

    assert (
        report["changes"]["empty_strings_resolved"]
        == 1
    )

    assert (
        report["changes"]["whitespace_issues_resolved"]
        == 1
    )

    assert report["changes"]["quality_score_change"] > 0


def test_generate_quality_comparison():
    before_df = pd.DataFrame({
        "id": [1, 2, 2],
        "name": [
            "Alice",
            "Bob",
            "Bob",
        ],
    })

    after_df = before_df.drop_duplicates().reset_index(
        drop=True
    )

    result = generate_quality_comparison(
        before_df,
        after_df,
    )

    assert "metric" in result.columns
    assert "before" in result.columns
    assert "after" in result.columns
    assert "change" in result.columns

    duplicate_row = result[
        result["metric"] == "Duplicate Rows"
    ].iloc[0]

    assert duplicate_row["before"] == 1
    assert duplicate_row["after"] == 0
    assert duplicate_row["change"] == -1


def test_cleaning_report_with_no_changes():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": [
            "Alice",
            "Bob",
            "Charlie",
        ],
    })

    report = generate_cleaning_report(
        df,
        df.copy(),
    )

    assert report["changes"]["rows_removed"] == 0

    assert (
        report["changes"]["duplicate_rows_removed"]
        == 0
    )

    assert (
        report["changes"]["whitespace_issues_resolved"]
        == 0
    )

    assert report["changes"]["quality_score_change"] == 0
