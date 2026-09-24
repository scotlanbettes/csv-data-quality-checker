import pandas as pd

from data_quality.metrics import generate_quality_metrics


def generate_cleaning_report(
    before_df,
    after_df,
    id_column="id",
):
    """
    Compare a dataframe before and after cleaning.

    Returns:
    - metrics before cleaning
    - metrics after cleaning
    - summary of changes
    """
    before_metrics = generate_quality_metrics(
        before_df,
        id_column=id_column,
    )

    after_metrics = generate_quality_metrics(
        after_df,
        id_column=id_column,
    )

    changes = {
        "rows_removed":
            len(before_df) - len(after_df),

        "missing_values_resolved":
            before_metrics["missing_values"]
            - after_metrics["missing_values"],

        "duplicate_rows_removed":
            before_metrics["duplicate_rows"]
            - after_metrics["duplicate_rows"],

        "duplicate_ids_resolved":
            before_metrics["duplicate_ids"]
            - after_metrics["duplicate_ids"],

        "empty_strings_resolved":
            before_metrics["empty_strings"]
            - after_metrics["empty_strings"],

        "whitespace_issues_resolved":
            before_metrics["whitespace_issues"]
            - after_metrics["whitespace_issues"],

        "outliers_resolved":
            before_metrics["outliers"]
            - after_metrics["outliers"],

        "capitalization_issues_resolved":
            before_metrics["capitalization_issues"]
            - after_metrics["capitalization_issues"],

        "quality_score_change": round(
            after_metrics["quality_score"]
            - before_metrics["quality_score"],
            2,
                ),
    }

    return {
        "before": before_metrics,
        "after": after_metrics,
        "changes": changes,
    }


def generate_quality_comparison(
    before_df,
    after_df,
    id_column="id",
):
    """
    Create a dataframe showing before-and-after
    data-quality metrics.
    """
    report = generate_cleaning_report(
        before_df,
        after_df,
        id_column=id_column,
    )

    before = report["before"]
    after = report["after"]

    comparison = pd.DataFrame({
        "metric": [
            "Rows",
            "Missing Values",
            "Duplicate Rows",
            "Duplicate IDs",
            "Empty Strings",
            "Whitespace Issues",
            "Inconsistent Type Columns",
            "Outliers",
            "Capitalization Issues",
            "Quality Score",
        ],
        "before": [
            before["total_rows"],
            before["missing_values"],
            before["duplicate_rows"],
            before["duplicate_ids"],
            before["empty_strings"],
            before["whitespace_issues"],
            before["inconsistent_type_columns"],
            before["outliers"],
            before["capitalization_issues"],
            before["quality_score"],
        ],
        "after": [
            after["total_rows"],
            after["missing_values"],
            after["duplicate_rows"],
            after["duplicate_ids"],
            after["empty_strings"],
            after["whitespace_issues"],
            after["inconsistent_type_columns"],
            after["outliers"],
            after["capitalization_issues"],
            after["quality_score"],
        ],
    })

    comparison["change"] = (
        comparison["after"]
        - comparison["before"]
    )

    return comparison
