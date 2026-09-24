from data_quality.reporting import generate_cleaning_report


def dataframe_to_csv_bytes(df):
    """
    Convert a dataframe to downloadable CSV bytes.
    """
    csv_data = df.to_csv(
        index=False
    )

    return csv_data.encode("utf-8")


def generate_text_quality_report(
    before_df,
    after_df,
    id_column="id",
):
    """
    Generate a readable text data-quality report.
    """
    report = generate_cleaning_report(
        before_df,
        after_df,
        id_column=id_column,
    )

    before = report["before"]
    after = report["after"]
    changes = report["changes"]

    lines = [
        "CSV DATA QUALITY CHECKER - VERSION 2",
        "=" * 40,
        "",
        "BEFORE CLEANING",
        "-" * 20,
        f"Rows: {before['total_rows']}",
        f"Columns: {before['total_columns']}",
        f"Missing Values: {before['missing_values']}",
        f"Duplicate Rows: {before['duplicate_rows']}",
        f"Duplicate IDs: {before['duplicate_ids']}",
        f"Empty Strings: {before['empty_strings']}",
        f"Whitespace Issues: {before['whitespace_issues']}",
        f"Outliers: {before['outliers']}",
        (
            "Capitalization Issues: "
            f"{before['capitalization_issues']}"
        ),
        f"Quality Score: {before['quality_score']}%",
        "",
        "AFTER CLEANING",
        "-" * 20,
        f"Rows: {after['total_rows']}",
        f"Columns: {after['total_columns']}",
        f"Missing Values: {after['missing_values']}",
        f"Duplicate Rows: {after['duplicate_rows']}",
        f"Duplicate IDs: {after['duplicate_ids']}",
        f"Empty Strings: {after['empty_strings']}",
        f"Whitespace Issues: {after['whitespace_issues']}",
        f"Outliers: {after['outliers']}",
        (
            "Capitalization Issues: "
            f"{after['capitalization_issues']}"
        ),
        f"Quality Score: {after['quality_score']}%",
        "",
        "CLEANING SUMMARY",
        "-" * 20,
        f"Rows Removed: {changes['rows_removed']}",
        (
            "Missing Values Resolved: "
            f"{changes['missing_values_resolved']}"
        ),
        (
            "Duplicate Rows Removed: "
            f"{changes['duplicate_rows_removed']}"
        ),
        (
            "Duplicate IDs Resolved: "
            f"{changes['duplicate_ids_resolved']}"
        ),
        (
            "Empty Strings Resolved: "
            f"{changes['empty_strings_resolved']}"
        ),
        (
            "Whitespace Issues Resolved: "
            f"{changes['whitespace_issues_resolved']}"
        ),
        (
            "Capitalization Issues Resolved: "
            f"{changes['capitalization_issues_resolved']}"
        ),
        (
            "Quality Score Change: "
            f"{changes['quality_score_change']:+.2f}"
        ),
    ]

    return "\n".join(lines)


def quality_report_to_bytes(
    before_df,
    after_df,
    id_column="id",
):
    """
    Convert the quality report to downloadable bytes.
    """
    report = generate_text_quality_report(
        before_df,
        after_df,
        id_column=id_column,
    )

    return report.encode("utf-8")
