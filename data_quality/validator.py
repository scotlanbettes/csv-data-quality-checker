import pandas as pd


def check_missing_values(df):
    """Return the number of missing values in each column."""
    return df.isnull().sum()


def check_duplicate_rows(df):
    """Return the number of duplicate rows."""
    return df.duplicated().sum()


def check_duplicate_ids(df, id_column="id"):
    """Return the number of duplicate IDs."""
    if id_column not in df.columns:
        return 0

    return df[id_column].duplicated().sum()


def check_empty_strings(df):
    """
    Return the number of empty or whitespace-only strings
    in each text column.
    """
    results = {}

    for column in df.select_dtypes(include=["object", "string"]).columns:
        results[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

    return pd.Series(results, dtype="int64")


def check_whitespace_issues(df):
    """
    Return the number of values with leading or trailing
    whitespace in each text column.
    """
    results = {}

    for column in df.select_dtypes(include=["object", "string"]).columns:
        values = df[column].dropna().astype(str)

        results[column] = (
            values.ne(values.str.strip())
        ).sum()

    return pd.Series(results, dtype="int64")


def check_inconsistent_data_types(df):
    """
    Return the number of distinct Python data types
    found in each column.

    A value greater than 1 may indicate mixed or
    inconsistent data types.
    """
    results = {}

    for column in df.columns:
        non_null_values = df[column].dropna()

        if non_null_values.empty:
            results[column] = 0
            continue

        detected_types = non_null_values.map(type).nunique()
        results[column] = detected_types

    return pd.Series(results, dtype="int64")


def check_outliers(df, exclude_columns=None):
    """
    Detect outliers in numeric columns using the IQR method.

    Values below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR
    are counted as outliers.
    """
    results = {}
    exclude_columns = set(exclude_columns or [])

    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        if column in exclude_columns:
            continue

        values = df[column].dropna()

        if values.empty:
            results[column] = 0
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            results[column] = 0
            continue

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outliers = (
            (values < lower_bound) |
            (values > upper_bound)
        ).sum()

        results[column] = int(outliers)

    return pd.Series(results, dtype="int64")


def validate_dataframe(df, id_column="id"):
    """
    Run all available data-quality checks and return the results.
    """
    results = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": check_missing_values(df),
        "duplicate_rows": check_duplicate_rows(df),
        "duplicate_ids": check_duplicate_ids(df, id_column),
        "empty_strings": check_empty_strings(df),
        "whitespace_issues": check_whitespace_issues(df),
        "inconsistent_data_types": check_inconsistent_data_types(df),
        "outliers": check_outliers(
            df,
            exclude_columns=[id_column]
        ),
    }

    return results
