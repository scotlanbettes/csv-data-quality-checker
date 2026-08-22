from pathlib import Path

import pandas as pd
import streamlit as st

from data_quality.metrics import generate_quality_metrics
from data_quality.validator import validate_dataframe


st.set_page_config(
    page_title="CSV Data Quality Checker",
    page_icon="📊",
    layout="wide",
)


st.title("📊 CSV Data Quality Checker")

st.markdown(
    """
    Upload a CSV file to assess its data quality, identify potential
    issues, and review an overall quality score.
    """
)


# ---------------------------------------------------------
# Sidebar — Dataset selection
# ---------------------------------------------------------

st.sidebar.header("Dataset")

sample_path = Path(__file__).parent / "sample_data" / "sample_dataset.csv"

st.sidebar.markdown("### Try the demo")

use_sample = st.sidebar.button(
    "▶ Try sample dataset",
    use_container_width=True,
)

st.sidebar.caption(
    "A sample CSV is included with this project so you can "
    "explore the dashboard without preparing a file."
)

st.sidebar.divider()

st.sidebar.markdown("### Upload your own CSV")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=["csv"],
)


# ---------------------------------------------------------
# Load selected dataset
# ---------------------------------------------------------

df = None
dataset_source = None

if use_sample:
    try:
        df = pd.read_csv(sample_path)
        dataset_source = "Built-in sample dataset"
    except Exception as error:
        st.error(f"Unable to load the sample dataset: {error}")
        st.stop()

elif uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        dataset_source = f"Uploaded file: {uploaded_file.name}"
    except Exception as error:
        st.error(f"Unable to read the CSV file: {error}")
        st.stop()


# ---------------------------------------------------------
# Welcome screen
# ---------------------------------------------------------

if df is None:
    st.info(
        "👈 Click **Try sample dataset** in the sidebar, "
        "or upload your own CSV file."
    )

    st.markdown(
        """
        ### What this application checks

        - Missing values
        - Duplicate rows
        - Duplicate IDs
        - Missing-value percentage
        - Duplicate-row percentage
        - Overall data-quality score

        ### Quick start

        **Recruiter/demo:** Click **Try sample dataset**.

        **Your own data:** Upload any CSV file using the uploader.
        """
    )

    st.stop()


if df.empty:
    st.warning("The selected CSV file contains no rows.")
    st.stop()


# ---------------------------------------------------------
# Dataset source
# ---------------------------------------------------------

st.caption(f"Dataset: **{dataset_source}**")


# ---------------------------------------------------------
# Dataset overview
# ---------------------------------------------------------

st.header("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rows", len(df))

with col2:
    st.metric("Columns", len(df.columns))

with col3:
    st.metric("Total Cells", df.shape[0] * df.shape[1])


with st.expander("Preview dataset", expanded=True):
    st.dataframe(df, use_container_width=True)


# ---------------------------------------------------------
# Generate quality metrics
# ---------------------------------------------------------

metrics = generate_quality_metrics(df)


# ---------------------------------------------------------
# Data Quality Score
# ---------------------------------------------------------

st.header("Data Quality Score")

score = metrics["quality_score"]

if score >= 90:
    score_status = "Excellent"
elif score >= 75:
    score_status = "Good"
elif score >= 50:
    score_status = "Needs Attention"
else:
    score_status = "Poor"


score_col1, score_col2 = st.columns(2)

with score_col1:
    st.metric(
        "Overall Quality Score",
        f"{score:.2f}/100",
    )

with score_col2:
    st.metric(
        "Assessment",
        score_status,
    )


# ---------------------------------------------------------
# Quality Metrics
# ---------------------------------------------------------

st.header("Quality Metrics")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

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
        "Missing %",
        f'{metrics["missing_percentage"]:.2f}%',
    )

with metric_col4:
    st.metric(
        "Duplicate %",
        f'{metrics["duplicate_percentage"]:.2f}%',
    )


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

st.header("Validation Results")

id_column = None

if "id" in df.columns:
    id_column = "id"
else:
    st.info(
        "No 'id' column was detected. "
        "Duplicate-ID validation will be skipped."
    )


validation_results = validate_dataframe(
    df,
    id_column=id_column or "id",
)


validation_col1, validation_col2, validation_col3 = st.columns(3)

with validation_col1:
    st.metric(
        "Rows Checked",
        validation_results["total_rows"],
    )

with validation_col2:
    st.metric(
        "Duplicate Rows",
        int(validation_results["duplicate_rows"]),
    )

with validation_col3:
    st.metric(
        "Duplicate IDs",
        int(validation_results["duplicate_ids"]),
    )


# ---------------------------------------------------------
# Missing values by column
# ---------------------------------------------------------

st.header("Missing Values by Column")

missing_values = validation_results["missing_values"]

missing_table = (
    missing_values[missing_values > 0]
    .sort_values(ascending=False)
    .rename("Missing Values")
    .to_frame()
)

if missing_table.empty:
    st.success("No missing values were detected.")
else:
    st.dataframe(
        missing_table,
        use_container_width=True,
    )


# ---------------------------------------------------------
# Quality visualization
# ---------------------------------------------------------

st.header("Quality Breakdown")

chart_data = pd.DataFrame(
    {
        "Metric": [
            "Missing Data %",
            "Duplicate Rows %",
        ],
        "Percentage": [
            metrics["missing_percentage"],
            metrics["duplicate_percentage"],
        ],
    }
)

st.bar_chart(
    chart_data,
    x="Metric",
    y="Percentage",
)


# ---------------------------------------------------------
# Methodology
# ---------------------------------------------------------

with st.expander("How is the quality score calculated?"):
    st.markdown(
        """
        The quality score starts at **100**.

        The score is reduced according to:

        - Missing-cell percentage
        - Duplicate-row percentage

        The formula is:

        **Quality Score = 100 − Missing Percentage − Duplicate Percentage**

        The final score cannot fall below 0.
        """
    )


st.caption(
    "CSV Data Quality Checker — Streamlit dashboard"
)
