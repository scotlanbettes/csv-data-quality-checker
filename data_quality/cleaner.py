import pandas as pd


def trim_whitespace(df):
    """
    Remove leading and trailing whitespace from text values.

    The original dataframe is not modified.
    """
    cleaned_df = df.copy()

    text_columns = cleaned_df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned_df[column] = cleaned_df[column].apply(
            lambda value: (
                value.strip()
                if isinstance(value, str)
                else value
            )
        )

    return cleaned_df


def remove_duplicate_rows(df):
    """
    Remove fully duplicated rows.

    The returned dataframe has its index reset.
    """
    cleaned_df = (
        df.drop_duplicates()
        .reset_index(drop=True)
    )

    return cleaned_df


def standardize_empty_strings(df):
    """
    Convert empty or whitespace-only strings to pandas NA.

    This makes missing-value handling more consistent.
    """
    cleaned_df = df.copy()

    text_columns = cleaned_df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned_df[column] = cleaned_df[column].apply(
            lambda value: (
                pd.NA
                if isinstance(value, str)
                and value.strip() == ""
                else value
            )
        )

    return cleaned_df


def clean_dataframe(
    df,
    trim_spaces=True,
    remove_duplicates=True,
    normalize_empty_strings=True,
):
    """
    Run selected cleaning operations on a dataframe.
    """
    cleaned_df = df.copy()

    if trim_spaces:
        cleaned_df = trim_whitespace(cleaned_df)

    if normalize_empty_strings:
        cleaned_df = standardize_empty_strings(
            cleaned_df
        )

    if remove_duplicates:
        cleaned_df = remove_duplicate_rows(
            cleaned_df
        )

    return cleaned_df
