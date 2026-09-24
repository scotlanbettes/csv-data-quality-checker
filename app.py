from pathlib import Path

import pandas as pd
import streamlit as st

from data_quality.cleaner import clean_dataframe
from data_quality.exporter import (
    dataframe_to_csv_bytes,
    quality_report_to_bytes,
)
from data_quality.metrics import (
    calculate_column_quality_scores,
    calculate_quality_breakdown,
    generate_quality_metrics,
)
from data_quality.reporting import (
    generate_quality_comparison,
)
from data_quality.validator import validate_dataframe


# =========================================================
# Page configuration
# =========================================================

st.set_page_config(
    page_title="CSV Data Quality Checker V2",
    page_icon="📊",
    layout="wide",
)


# =========================================================
# Header
# =========================================================

st.title("📊 CSV Data Quality Checker V2")

st.markdown(
    """
    Analyze CSV data, detect quality problems, clean common issues,
    compare before-and-after results, and download the improved dataset.
    """
)


# =========================================================
# Sidebar — Dataset selection
# =========================================================

st.sidebar.header("Dataset")

data_source = st.sidebar.radio(
    "Choose a data source",
    [
        "Upload CSV",
        "Sample dataset",
    ],
)

sample_path = (
    Path(__file__).parent
    / "sample_data"
    / "sample_dataset.csv"
)

uploaded_file = None

if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type=["csv"],
    )

    st.sidebar.caption(
        "Upload your own CSV file for analysis."
    )

else:
    st.sidebar.success(
        "The built-in sample dataset will be used."
    )


# =========================================================
# Load dataset
# =========================================================

df = None
dataset_source = None

if data_source == "Sample dataset":
    try:
        df = pd.read_csv(sample_path)
        dataset_source = "Built-in sample dataset"

    except Exception as error:
        st.error(
            f"Unable to load the sample dataset: {error}"
        )
        st.stop()

elif uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        dataset_source = (
            f"Uploaded file: {uploaded_file.name}"
        )

    except Exception as error:
        st.error(
            f"Unable to read the CSV file: {error}"
        )
        st.stop()


# =========================================================
# Welcome screen
# =========================================================

if df is None:
    st.info(
        "👈 Upload a CSV file from the sidebar, "
        "or select the sample dataset."
    )

    st.markdown(
        """
        ### Version 2 capabilities

        **Data-quality detection**
        - Missing values
        - Duplicate rows
        - Duplicate IDs
        - Empty strings
        - Leading/trailing whitespace
        - Inconsistent data types
        - Numeric outliers
        - Inconsistent capitalization

        **Data cleaning**
        - Trim whitespace
        - Standardize empty strings
        - Remove duplicate rows
        - Handle missing values
        - Standardize text capitalization

        **Analysis**
        - Overall quality score
        - Column-level quality scores
        - Before-and-after comparison
        - Downloadable cleaned CSV
        - Downloadable quality report
        """
    )

    st.stop()


if df.empty:
    st.warning(
        "The selected CSV file contains no rows."
    )
    st.stop()


st.caption(
    f"Dataset: **{dataset_source}**"
)


# =========================================================
# Primary / ID column selection
# =========================================================

st.sidebar.divider()

st.sidebar.header("Validation Settings")

id_options = ["None"] + list(df.columns)

default_id_index = (
    id_options.index("id")
    if "id" in df.columns
    else 0
)

selected_id = st.sidebar.selectbox(
    "ID / Primary key column",
    options=id_options,
    index=default_id_index,
    help=(
        "Select the column that should contain "
        "unique identifiers."
    ),
)

id_column = (
    None
    if selected_id == "None"
    else selected_id
)


# =========================================================
# Generate original quality results
# =========================================================

metrics = generate_quality_metrics(
    df,
    id_column=id_column,
)

validation_results = validate_dataframe(
    df,
    id_column=id_column,
)

quality_breakdown = calculate_quality_breakdown(
    df,
    id_column=id_column,
)

column_scores = calculate_column_quality_scores(
    df,
    id_column=id_column,
)


# =========================================================
# Dashboard tabs
# =========================================================

(
    overview_tab,
    issues_tab,
    columns_tab,
    cleaning_tab,
    report_tab,
) = st.tabs(
    [
        "📊 Overview",
        "⚠️ Issues",
        "🔎 Column Analysis",
        "🧹 Data Cleaning",
        "📄 Report",
    ]
)


# =========================================================
# TAB 1 — OVERVIEW
# =========================================================

with overview_tab:

    st.subheader("Dataset Overview")

    overview_col1, overview_col2, overview_col3, overview_col4 = (
        st.columns(4)
    )

    with overview_col1:
        st.metric(
            "Rows",
            metrics["total_rows"],
        )

    with overview_col2:
        st.metric(
            "Columns",
            metrics["total_columns"],
        )

    with overview_col3:
        st.metric(
            "Total Cells",
            df.shape[0] * df.shape[1],
        )

    with overview_col4:
        st.metric(
            "Quality Score",
            f'{metrics["quality_score"]:.2f}/100',
        )

    # -----------------------------------------------------
    # Score assessment
    # -----------------------------------------------------

    score = metrics["quality_score"]

    if score >= 90:
        score_status = "Excellent"

    elif score >= 75:
        score_status = "Good"

    elif score >= 50:
        score_status = "Needs Attention"

    else:
        score_status = "Poor"

    st.info(
        f"Overall assessment: **{score_status}**"
    )

    # -----------------------------------------------------
    # Main issue metrics
    # -----------------------------------------------------

    st.subheader("Key Quality Metrics")

    metric_col1, metric_col2, metric_col3, metric_col4 = (
        st.columns(4)
    )

    with metric_col1:
        st.metric(
            "Missing Values",
            metrics["missing_values"],
            f'{metrics["missing_percentage"]:.2f}%',
        )

    with metric_col2:
        st.metric(
            "Duplicate Rows",
            metrics["duplicate_rows"],
            f'{metrics["duplicate_percentage"]:.2f}%',
        )

    with metric_col3:
        st.metric(
            "Duplicate IDs",
            metrics["duplicate_ids"],
            f'{metrics["duplicate_id_percentage"]:.2f}%',
        )

    with metric_col4:
        st.metric(
            "Outliers",
            metrics["outliers"],
            f'{metrics["outlier_percentage"]:.2f}%',
        )

    # -----------------------------------------------------
    # Additional issue metrics
    # -----------------------------------------------------

    metric_col5, metric_col6, metric_col7, metric_col8 = (
        st.columns(4)
    )

    with metric_col5:
        st.metric(
            "Empty Strings",
            metrics["empty_strings"],
        )

    with metric_col6:
        st.metric(
            "Whitespace Issues",
            metrics["whitespace_issues"],
        )

    with metric_col7:
        st.metric(
            "Type Issues",
            metrics["inconsistent_type_columns"],
        )

    with metric_col8:
        st.metric(
            "Capitalization Issues",
            metrics["capitalization_issues"],
        )

    # -----------------------------------------------------
    # Dataset preview
    # -----------------------------------------------------

    st.subheader("Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True,
    )

    # -----------------------------------------------------
    # Quality breakdown
    # -----------------------------------------------------

    st.subheader("Quality Breakdown")

    breakdown_chart = pd.DataFrame(
        {
            "Issue": [
                "Missing Values",
                "Duplicate Rows",
                "Duplicate IDs",
                "Empty Strings",
                "Whitespace",
                "Data Types",
                "Outliers",
                "Capitalization",
            ],
            "Percentage": [
                quality_breakdown[
                    "missing_values"
                ],
                quality_breakdown[
                    "duplicate_rows"
                ],
                quality_breakdown[
                    "duplicate_ids"
                ],
                quality_breakdown[
                    "empty_strings"
                ],
                quality_breakdown[
                    "whitespace_issues"
                ],
                quality_breakdown[
                    "inconsistent_data_types"
                ],
                quality_breakdown[
                    "outliers"
                ],
                quality_breakdown[
                    "inconsistent_capitalization"
                ],
            ],
        }
    )

    st.bar_chart(
        breakdown_chart,
        x="Issue",
        y="Percentage",
    )


# =========================================================
# TAB 2 — ISSUES
# =========================================================

with issues_tab:

    st.subheader("Detected Data Quality Issues")

    # -----------------------------------------------------
    # Missing values
    # -----------------------------------------------------

    st.markdown("### Missing Values")

    missing_values = (
        validation_results["missing_values"]
    )

    missing_table = (
        missing_values[
            missing_values > 0
        ]
        .sort_values(
            ascending=False
        )
        .rename(
            "Missing Values"
        )
        .to_frame()
    )

    if missing_table.empty:
        st.success(
            "No missing values detected."
        )

    else:
        st.dataframe(
            missing_table,
            use_container_width=True,
        )

    # -----------------------------------------------------
    # Empty strings
    # -----------------------------------------------------

    st.markdown("### Empty Strings")

    empty_strings = (
        validation_results["empty_strings"]
    )

    empty_table = (
        empty_strings[
            empty_strings > 0
        ]
        .sort_values(
            ascending=False
        )
        .rename(
            "Empty Strings"
        )
        .to_frame()
    )

    if empty_table.empty:
        st.success(
            "No empty strings detected."
        )

    else:
        st.dataframe(
            empty_table,
            use_container_width=True,
        )

    # -----------------------------------------------------
    # Whitespace issues
    # -----------------------------------------------------

    st.markdown(
        "### Leading / Trailing Whitespace"
    )

    whitespace = (
        validation_results["whitespace_issues"]
    )

    whitespace_table = (
        whitespace[
            whitespace > 0
        ]
        .sort_values(
            ascending=False
        )
        .rename(
            "Whitespace Issues"
        )
        .to_frame()
    )

    if whitespace_table.empty:
        st.success(
            "No whitespace issues detected."
        )

    else:
        st.dataframe(
            whitespace_table,
            use_container_width=True,
        )

    # -----------------------------------------------------
    # Inconsistent data types
    # -----------------------------------------------------

    st.markdown(
        "### Inconsistent Data Types"
    )

    type_results = validation_results[
        "inconsistent_data_types"
    ]

    type_table = (
        type_results[
            type_results > 1
        ]
        .sort_values(
            ascending=False
        )
        .rename(
            "Distinct Python Types"
        )
        .to_frame()
    )

    if type_table.empty:
        st.success(
            "No inconsistent data types detected."
        )

    else:
        st.dataframe(
            type_table,
            use_container_width=True,
        )

    # -----------------------------------------------------
    # Outliers
    # -----------------------------------------------------

    st.markdown("### Numeric Outliers")

    outlier_results = (
        validation_results["outliers"]
    )

    outlier_table = (
        outlier_results[
            outlier_results > 0
        ]
        .sort_values(
            ascending=False
        )
        .rename(
            "Outliers"
        )
        .to_frame()
    )

    if outlier_table.empty:
        st.success(
            "No numeric outliers detected."
        )

    else:
        st.dataframe(
            outlier_table,
            use_container_width=True,
        )

    # -----------------------------------------------------
    # Capitalization
    # -----------------------------------------------------

    st.markdown(
        "### Inconsistent Capitalization"
    )

    capitalization = validation_results[
        "inconsistent_capitalization"
    ]

    capitalization_table = (
        capitalization[
            capitalization > 0
        ]
        .sort_values(
            ascending=False
        )
        .rename(
            "Affected Values"
        )
        .to_frame()
    )

    if capitalization_table.empty:
        st.success(
            "No capitalization inconsistencies detected."
        )

    else:
        st.dataframe(
            capitalization_table,
            use_container_width=True,
        )

    # -----------------------------------------------------
    # Duplicate summary
    # -----------------------------------------------------

    st.markdown("### Duplicate Data")

    duplicate_col1, duplicate_col2 = (
        st.columns(2)
    )

    with duplicate_col1:
        st.metric(
            "Duplicate Rows",
            metrics["duplicate_rows"],
        )

    with duplicate_col2:
        st.metric(
            "Duplicate IDs",
            metrics["duplicate_ids"],
        )


# =========================================================
# TAB 3 — COLUMN ANALYSIS
# =========================================================

with columns_tab:

    st.subheader(
        "Column-Level Quality Analysis"
    )

    st.markdown(
        """
        Each column receives its own quality score based
        on problems relevant to that column.
        """
    )

    st.dataframe(
        column_scores,
        use_container_width=True,
        hide_index=True,
    )

    # -----------------------------------------------------
    # Column quality chart
    # -----------------------------------------------------

    if not column_scores.empty:

        st.subheader(
            "Column Quality Scores"
        )

        chart_columns = column_scores[
            [
                "column",
                "quality_score",
            ]
        ]

        st.bar_chart(
            chart_columns,
            x="column",
            y="quality_score",
        )

        # -------------------------------------------------
        # Individual column
        # -------------------------------------------------

        selected_column = st.selectbox(
            "Inspect a column",
            df.columns,
        )

        selected_analysis = column_scores[
            column_scores["column"]
            == selected_column
        ]

        if not selected_analysis.empty:

            row = selected_analysis.iloc[0]

            analysis_col1, analysis_col2, analysis_col3 = (
                st.columns(3)
            )

            with analysis_col1:
                st.metric(
                    "Quality Score",
                    f'{row["quality_score"]:.2f}/100',
                )

            with analysis_col2:
                st.metric(
                    "Missing %",
                    f'{row["missing_percentage"]:.2f}%',
                )

            with analysis_col3:
                st.metric(
                    "Data Type",
                    row["data_type"],
                )

            st.dataframe(
                selected_analysis,
                use_container_width=True,
                hide_index=True,
            )


# =========================================================
# TAB 4 — DATA CLEANING
# =========================================================

with cleaning_tab:

    st.subheader(
        "Interactive Data Cleaning"
    )

    st.markdown(
        """
        Select the cleaning operations you want to apply.
        The original uploaded dataset is never modified.
        """
    )

    # -----------------------------------------------------
    # Basic cleaning
    # -----------------------------------------------------

    st.markdown("### Basic Cleaning")

    clean_col1, clean_col2, clean_col3 = (
        st.columns(3)
    )

    with clean_col1:
        trim_spaces = st.checkbox(
            "Trim whitespace",
            value=True,
        )

    with clean_col2:
        normalize_empty = st.checkbox(
            "Standardize empty strings",
            value=True,
        )

    with clean_col3:
        remove_duplicates = st.checkbox(
            "Remove duplicate rows",
            value=True,
        )

    # -----------------------------------------------------
    # Missing values
    # -----------------------------------------------------

    st.markdown("### Missing Values")

    missing_option = st.selectbox(
        "Missing-value strategy",
        [
            "Do not handle",
            "Drop rows",
            "Mean",
            "Median",
            "Mode",
            "Custom value",
        ],
    )

    missing_columns = st.multiselect(
        "Columns for missing-value handling",
        options=list(df.columns),
        default=list(df.columns),
    )

    custom_missing_value = None

    if missing_option == "Custom value":
        custom_missing_value = st.text_input(
            "Custom replacement value",
            value="Unknown",
        )

    missing_strategy_map = {
        "Do not handle": None,
        "Drop rows": "drop",
        "Mean": "mean",
        "Median": "median",
        "Mode": "mode",
        "Custom value": "custom",
    }

    missing_strategy = (
        missing_strategy_map[
            missing_option
        ]
    )

    # -----------------------------------------------------
    # Text capitalization
    # -----------------------------------------------------

    st.markdown(
        "### Text Standardization"
    )

    text_case_option = st.selectbox(
        "Capitalization strategy",
        [
            "Do not change",
            "Title Case",
            "lowercase",
            "UPPERCASE",
        ],
    )

    text_columns = list(
        df.select_dtypes(
            include=[
                "object",
                "string",
            ]
        ).columns
    )

    text_case_columns = st.multiselect(
        "Text columns to standardize",
        options=text_columns,
        default=text_columns,
    )

    text_case_map = {
        "Do not change": None,
        "Title Case": "title",
        "lowercase": "lower",
        "UPPERCASE": "upper",
    }

    text_case_strategy = (
        text_case_map[
            text_case_option
        ]
    )

    # -----------------------------------------------------
    # Generate cleaned dataframe
    # -----------------------------------------------------

    try:
        cleaned_df = clean_dataframe(
            df,
            trim_spaces=trim_spaces,
            remove_duplicates=remove_duplicates,
            normalize_empty_strings=normalize_empty,
            missing_strategy=missing_strategy,
            custom_missing_value=custom_missing_value,
            missing_columns=missing_columns,
            text_case_strategy=text_case_strategy,
            text_case_columns=text_case_columns,
        )

    except Exception as error:
        st.error(
            f"Unable to clean the dataset: {error}"
        )

        cleaned_df = df.copy()

    # -----------------------------------------------------
    # Before / after scores
    # -----------------------------------------------------

    cleaned_metrics = generate_quality_metrics(
        cleaned_df,
        id_column=id_column,
    )

    before_col, after_col = st.columns(2)

    with before_col:
        st.metric(
            "Before Cleaning",
            f'{metrics["quality_score"]:.2f}/100',
        )

    with after_col:
        score_change = round(
            cleaned_metrics["quality_score"]
            - metrics["quality_score"],
            2,
        )

        st.metric(
            "After Cleaning",
            f'{cleaned_metrics["quality_score"]:.2f}/100',
            f"{score_change:+.2f}",
        )

    # -----------------------------------------------------
    # Preview
    # -----------------------------------------------------

    st.subheader(
        "Cleaned Dataset Preview"
    )

    st.dataframe(
        cleaned_df,
        use_container_width=True,
    )

    # -----------------------------------------------------
    # Download CSV
    # -----------------------------------------------------

    cleaned_csv = dataframe_to_csv_bytes(
        cleaned_df
    )

    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=cleaned_csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
        use_container_width=True,
    )


# =========================================================
# TAB 5 — REPORT
# =========================================================

with report_tab:

    st.subheader(
        "Before vs After Quality Report"
    )

    comparison = generate_quality_comparison(
        df,
        cleaned_df,
        id_column=id_column,
    )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True,
    )

    # -----------------------------------------------------
    # Score comparison
    # -----------------------------------------------------

    report_col1, report_col2, report_col3 = (
        st.columns(3)
    )

    with report_col1:
        st.metric(
            "Original Score",
            f'{metrics["quality_score"]:.2f}/100',
        )

    with report_col2:
        st.metric(
            "Cleaned Score",
            f'{cleaned_metrics["quality_score"]:.2f}/100',
        )

    with report_col3:
        improvement = round(
            cleaned_metrics["quality_score"]
            - metrics["quality_score"],
            2,
        )

        st.metric(
            "Score Change",
            f"{improvement:+.2f}",
        )

    # -----------------------------------------------------
    # Download quality report
    # -----------------------------------------------------

    report_bytes = quality_report_to_bytes(
        df,
        cleaned_df,
        id_column=id_column,
    )

    st.download_button(
        label="⬇️ Download Quality Report",
        data=report_bytes,
        file_name="data_quality_report.txt",
        mime="text/plain",
        use_container_width=True,
    )


# =========================================================
# Methodology
# =========================================================

st.divider()

with st.expander(
    "How is the Version 2 quality score calculated?"
):
    st.markdown(
        """
        Version 2 uses a **weighted data-quality scoring model**.

        The score starts at **100** and applies weighted
        penalties for:

        - Missing values — **30%**
        - Duplicate rows — **15%**
        - Duplicate IDs — **10%**
        - Empty strings — **10%**
        - Whitespace issues — **10%**
        - Inconsistent data types — **10%**
        - Numeric outliers — **10%**
        - Inconsistent capitalization — **5%**

        The final score is restricted to the range
        **0–100**.

        Column-level scores use checks that are relevant
        to each individual column.
        """
    )


st.caption(
    "CSV Data Quality Checker V2 — Developed by Job Munyoki"
)
