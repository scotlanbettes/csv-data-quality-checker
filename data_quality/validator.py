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

    for column in df.select_dtypes(include="object").columns:
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

    for column in df.select_dtypes(include="object").columns:
        values = df[column].dropna().astype(str)

        results[column] = (
            values.ne(values.str.strip())
        ).sum()

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
    }

    return results
