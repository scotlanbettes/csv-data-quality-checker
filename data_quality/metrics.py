import pandas as pd

from data_quality.validator import (
    check_duplicate_ids,
    check_empty_strings,
    check_whitespace_issues,
    check_inconsistent_data_types,
    check_outliers,
    check_inconsistent_capitalization,
)


# Weight assigned to each data-quality dimension.
# All weights add up to 1.0.
QUALITY_WEIGHTS = {
    "missing_values": 0.30,
    "duplicate_rows": 0.15,
    "duplicate_ids": 0.10,
    "empty_strings": 0.10,
    "whitespace_issues": 0.10,
    "inconsistent_data_types": 0.10,
    "outliers": 0.10,
    "inconsistent_capitalization": 0.05,
}


def _percentage(count, total):
    """Safely calculate a percentage."""
    if total == 0:
        return 0.0

    return round((count / total) * 100, 2)


def calculate_missing_percentage(df):
    """Calculate the percentage of missing cells."""
    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0.0

    missing_cells = int(df.isnull().sum().sum())

    return _percentage(missing_cells, total_cells)


def calculate_duplicate_percentage(df):
    """Calculate the percentage of duplicate rows."""
    total_rows = len(df)

    if total_rows == 0:
        return 0.0

    duplicate_rows = int(df.duplicated().sum())

    return _percentage(duplicate_rows, total_rows)


def calculate_duplicate_id_percentage(df, id_column="id"):
    """Calculate the percentage of duplicate IDs."""
    if id_column not in df.columns or len(df) == 0:
        return 0.0

    duplicate_ids = int(check_duplicate_ids(df, id_column))

    return _percentage(duplicate_ids, len(df))


def calculate_empty_string_percentage(df):
    """
    Calculate the percentage of actual blank or whitespace-only
    strings without counting missing values twice.
    """
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    if len(text_columns) == 0 or len(df) == 0:
        return 0.0

    total_text_cells = len(df) * len(text_columns)

    detected_empty = int(check_empty_strings(df).sum())

    missing_text_values = int(
        df[text_columns].isnull().sum().sum()
    )

    actual_empty_strings = max(
        detected_empty - missing_text_values,
        0
    )

    return _percentage(
        actual_empty_strings,
        total_text_cells
    )


def calculate_whitespace_percentage(df):
    """Calculate the percentage of text values with whitespace issues."""
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    if len(text_columns) == 0 or len(df) == 0:
        return 0.0

    total_text_cells = len(df) * len(text_columns)

    whitespace_count = int(
        check_whitespace_issues(df).sum()
    )

    return _percentage(
        whitespace_count,
        total_text_cells
    )


def calculate_inconsistent_type_percentage(df):
    """
    Calculate the percentage of columns containing
    more than one Python data type.
    """
    if len(df.columns) == 0:
        return 0.0

    type_results = check_inconsistent_data_types(df)

    inconsistent_columns = int(
        (type_results > 1).sum()
    )

    return _percentage(
        inconsistent_columns,
        len(df.columns)
    )


def calculate_outlier_percentage(df, id_column="id"):
    """Calculate the percentage of numeric values identified as outliers."""
    numeric_columns = list(
        df.select_dtypes(include="number").columns
    )

    numeric_columns = [
        column
        for column in numeric_columns
        if column != id_column
    ]

    if not numeric_columns:
        return 0.0

    total_numeric_values = int(
        df[numeric_columns]
        .notna()
        .sum()
        .sum()
    )

    if total_numeric_values == 0:
        return 0.0

    outlier_results = check_outliers(
        df,
        exclude_columns=[id_column]
    )

    outlier_count = int(outlier_results.sum())

    return _percentage(
        outlier_count,
        total_numeric_values
    )


def calculate_capitalization_percentage(df):
    """
    Calculate the percentage of text cells affected by
    inconsistent capitalization.
    """
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    if len(text_columns) == 0 or len(df) == 0:
        return 0.0

    total_text_cells = len(df) * len(text_columns)

    capitalization_results = (
        check_inconsistent_capitalization(df)
    )

    issue_count = int(
        capitalization_results.sum()
    )

    return _percentage(
        issue_count,
        total_text_cells
    )


def calculate_quality_breakdown(df, id_column="id"):
    """
    Return the percentage of issues detected for each
    quality dimension.
    """
    return {
        "missing_values":
            calculate_missing_percentage(df),

        "duplicate_rows":
            calculate_duplicate_percentage(df),

        "duplicate_ids":
            calculate_duplicate_id_percentage(
                df,
                id_column
            ),

        "empty_strings":
            calculate_empty_string_percentage(df),

        "whitespace_issues":
            calculate_whitespace_percentage(df),

        "inconsistent_data_types":
            calculate_inconsistent_type_percentage(df),

        "outliers":
            calculate_outlier_percentage(
                df,
                id_column
            ),

        "inconsistent_capitalization":
            calculate_capitalization_percentage(df),
    }


def calculate_quality_score(df, id_column="id"):
    """
    Calculate the Version 2 overall data-quality score.

    Each quality issue contributes a weighted penalty.
    The final score is always between 0 and 100.
    """
    breakdown = calculate_quality_breakdown(
        df,
        id_column
    )

    total_penalty = sum(
        breakdown[issue] * weight
        for issue, weight in QUALITY_WEIGHTS.items()
    )

    score = 100 - total_penalty

    return round(
        min(max(score, 0), 100),
        2
    )


def generate_quality_metrics(df, id_column="id"):
    """
    Generate the Version 2 data-quality summary.
    """
    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    duplicate_ids = int(
        check_duplicate_ids(df, id_column)
    )

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    detected_empty = int(
        check_empty_strings(df).sum()
    )

    missing_text_values = (
        int(df[text_columns].isnull().sum().sum())
        if len(text_columns) > 0
        else 0
    )

    empty_strings = max(
        detected_empty - missing_text_values,
        0
    )

    whitespace_issues = int(
        check_whitespace_issues(df).sum()
    )

    type_results = check_inconsistent_data_types(df)

    inconsistent_type_columns = int(
        (type_results > 1).sum()
    )

    outlier_results = check_outliers(
        df,
        exclude_columns=[id_column]
    )

    outliers = int(
        outlier_results.sum()
    )

    capitalization_results = (
        check_inconsistent_capitalization(df)
    )

    capitalization_issues = int(
        capitalization_results.sum()
    )

    breakdown = calculate_quality_breakdown(
        df,
        id_column
    )

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),

        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "duplicate_ids": duplicate_ids,
        "empty_strings": empty_strings,
        "whitespace_issues": whitespace_issues,
        "inconsistent_type_columns":
            inconsistent_type_columns,
        "outliers": outliers,
        "capitalization_issues":
            capitalization_issues,

        "missing_percentage":
            breakdown["missing_values"],

        "duplicate_percentage":
            breakdown["duplicate_rows"],

        "duplicate_id_percentage":
            breakdown["duplicate_ids"],

        "empty_string_percentage":
            breakdown["empty_strings"],

        "whitespace_percentage":
            breakdown["whitespace_issues"],

        "inconsistent_type_percentage":
            breakdown["inconsistent_data_types"],

        "outlier_percentage":
            breakdown["outliers"],

        "capitalization_percentage":
            breakdown["inconsistent_capitalization"],

        "quality_score":
            calculate_quality_score(
                df,
                id_column
        ),
    }
