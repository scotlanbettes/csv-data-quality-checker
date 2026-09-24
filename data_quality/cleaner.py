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


def drop_missing_rows(df, subset=None):
    """
    Remove rows containing missing values.

    If subset is provided, only those columns are checked.
    """
    cleaned_df = (
        df.dropna(subset=subset)
        .reset_index(drop=True)
    )

    return cleaned_df


def fill_numeric_missing(df, strategy="mean", columns=None):
    """
    Fill missing values in numeric columns using
    either the mean or median.

    Supported strategies:
    - mean
    - median
    """
    cleaned_df = df.copy()

    if strategy not in {"mean", "median"}:
        raise ValueError(
            "Numeric strategy must be 'mean' or 'median'."
        )

    numeric_columns = list(
        cleaned_df.select_dtypes(
            include="number"
        ).columns
    )

    if columns is not None:
        numeric_columns = [
            column
            for column in numeric_columns
            if column in columns
        ]

    for column in numeric_columns:
        if strategy == "mean":
            fill_value = cleaned_df[column].mean()
        else:
            fill_value = cleaned_df[column].median()

        if pd.notna(fill_value):
            cleaned_df[column] = (
                cleaned_df[column]
                .fillna(fill_value)
            )

    return cleaned_df


def fill_text_missing_with_mode(df, columns=None):
    """
    Fill missing values in text columns using
    the most frequently occurring value.
    """
    cleaned_df = df.copy()

    text_columns = list(
        cleaned_df.select_dtypes(
            include=["object", "string"]
        ).columns
    )

    if columns is not None:
        text_columns = [
            column
            for column in text_columns
            if column in columns
        ]

    for column in text_columns:
        mode_values = (
            cleaned_df[column]
            .dropna()
            .mode()
        )

        if not mode_values.empty:
            cleaned_df[column] = (
                cleaned_df[column]
                .fillna(mode_values.iloc[0])
            )

    return cleaned_df


def fill_missing_with_custom_value(
    df,
    value,
    columns=None,
):
    """
    Fill missing values with a user-defined value.

    If columns is not provided, all columns are processed.
    """
    cleaned_df = df.copy()

    target_columns = (
        list(cleaned_df.columns)
        if columns is None
        else [
            column
            for column in columns
            if column in cleaned_df.columns
        ]
    )

    for column in target_columns:
        cleaned_df[column] = (
            cleaned_df[column]
            .fillna(value)
        )

    return cleaned_df


def handle_missing_values(
    df,
    strategy,
    custom_value=None,
    columns=None,
):
    """
    Apply a selected missing-value strategy.

    Supported strategies:
    - drop
    - mean
    - median
    - mode
    - custom
    """
    if strategy == "drop":
        return drop_missing_rows(
            df,
            subset=columns
        )

    if strategy in {"mean", "median"}:
        return fill_numeric_missing(
            df,
            strategy=strategy,
            columns=columns,
        )

    if strategy == "mode":
        return fill_text_missing_with_mode(
            df,
            columns=columns,
        )

    if strategy == "custom":
        if custom_value is None:
            raise ValueError(
                "A custom value must be provided "
                "when using the custom strategy."
            )

        return fill_missing_with_custom_value(
            df,
            value=custom_value,
            columns=columns,
        )

    raise ValueError(
        "Unsupported missing-value strategy."
    )


def clean_dataframe(
    df,
    trim_spaces=True,
    remove_duplicates=True,
    normalize_empty_strings=True,
    missing_strategy=None,
    custom_missing_value=None,
    missing_columns=None,
):
    """
    Run selected cleaning operations on a dataframe.

    Missing-value handling is optional.
    """
    cleaned_df = df.copy()

    if trim_spaces:
        cleaned_df = trim_whitespace(cleaned_df)

    if normalize_empty_strings:
        cleaned_df = standardize_empty_strings(
            cleaned_df
        )

    if missing_strategy is not None:
        cleaned_df = handle_missing_values(
            cleaned_df,
            strategy=missing_strategy,
            custom_value=custom_missing_value,
            columns=missing_columns,
        )

    if remove_duplicates:
        cleaned_df = remove_duplicate_rows(
            cleaned_df
        )

    return cleaned_df
