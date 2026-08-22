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


# Sidebar
st.sidebar.header("Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"],
)

if uploaded_file is None:
    st.info("👈 Upload a CSV file from the sidebar to begin.")
    st.markdown(
        """
        ### What this application checks

        - Missing values
        - Duplicate rows
        - Duplicate IDs
        - Missing-value percentage
        - Duplicate-row percentage
        - Overall data-quality score
        """
    )
    st.stop()


# Load CSV
try:
    df = pd.read_csv(uploaded_file)
except Exception as error:
    st.error(f"Unable to read the CSV file: {error}")
    st.stop()


if df.empty:
    st.warning("The uploaded CSV file contains no rows.")
    st.stop()


# Dataset overview
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


# Generate quality metrics using the existing data-quality engine
metrics = generate_quality_metrics(df)


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
    st.metric("Overall Quality Score", f"{score:.2f}/100")

with score_col2:
    st.metric("Assessment", score_status)


# Quality metrics
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


# Validation
st.header("Validation Results")

id_column = None

if "id" in df.columns:
    id_column = "id"
else:
    st.info(
        "No 'id' column was detected. Duplicate-ID validation will be skipped."
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


# Missing values by column
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


# Quality visualization
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


# Methodology
with st.expander("How is the quality score calculated?"):
    st.markdown(
        """
        The quality score starts at **100**.

        The score is reduced according to the percentage of:

        - Missing cells
        - Duplicate rows

        The formula is:

        **Quality Score = 100 − Missing Percentage − Duplicate Percentage**

        The final score cannot fall below 0.
        """
    )


st.caption(
    "CSV Data Quality Checker — Streamlit dashboard"
)
