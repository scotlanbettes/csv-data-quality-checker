import pandas as pd


def calculate_missing_percentage(df):
    """Calculate the percentage of missing cells in the dataframe."""
    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0.0

    missing_cells = df.isnull().sum().sum()

    return round((missing_cells / total_cells) * 100, 2)


def calculate_duplicate_percentage(df):
    """Calculate the percentage of duplicate rows."""
    total_rows = len(df)

    if total_rows == 0:
        return 0.0

    duplicate_rows = df.duplicated().sum()

    return round((duplicate_rows / total_rows) * 100, 2)


def calculate_quality_score(df):
    """
    Calculate an overall data-quality score.

    The score starts at 100 and is reduced based on
    missing and duplicate data.
    """
    missing_percentage = calculate_missing_percentage(df)
    duplicate_percentage = calculate_duplicate_percentage(df)

    score = 100 - missing_percentage - duplicate_percentage

    return round(max(score, 0), 2)


def generate_quality_metrics(df):
    """Generate a summary of important data-quality metrics."""
    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "missing_percentage": calculate_missing_percentage(df),
        "duplicate_percentage": calculate_duplicate_percentage(df),
        "quality_score": calculate_quality_score(df),
    }
