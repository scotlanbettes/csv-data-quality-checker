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
    }

    return results
