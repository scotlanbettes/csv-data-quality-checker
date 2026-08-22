# CSV Data Quality Checker

A Python application for validating CSV datasets and measuring overall data quality.

The project identifies common data-quality issues such as missing values, duplicate records, and duplicate IDs, then calculates an overall quality score and presents results through an interactive Streamlit dashboard.

---

## Features

- CSV file validation
- Missing-value detection
- Duplicate-row detection
- Duplicate-ID detection
- Data-quality metrics
- Overall quality score calculation
- Interactive Streamlit dashboard
- Automated tests with Pytest

---

## Technology Stack

- Python
- Pandas
- Streamlit
- Pytest
- Git & GitHub

---

## Installation

Clone the repository:

```bash
git clone https://github.com/scotlanbettes/csv-data-quality-checker.git
cd csv-data-quality-checker
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run Tests

```bash
python -m pytest
```

---

## Launch Dashboard

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Data Quality Metrics

The application measures:

### Missing Values

Percentage of empty cells in the dataset.

### Duplicate Rows

Percentage of duplicated records.

### Duplicate IDs

Duplicate values within the ID column.

### Quality Score

The quality score starts at:

```text
100
```

and is reduced by:

```text
Missing Percentage
+
Duplicate Percentage
```

Formula:

```text
Quality Score =
100 - Missing Percentage - Duplicate Percentage
```

Minimum score:

```text
0
```

Maximum score:

```text
100
```

---

## Example

Dataset:

| Rows | Missing % | Duplicate % |
| ---- | --------- | ----------- |
| 100  | 10        | 5           |

Quality Score:

```text
100 - 10 - 5 = 85
```

---

## Project Structure

```text
csv-data-quality-checker/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data_quality/
│   ├── validator.py
│   └── metrics.py
│
├── tests/
│   └── test_validator.py
│
└── sample_data/
    └── sample_dataset.csv
```

---

## Author Contributions

### Scotlan Bettes

- Data validation engine
- Quality metrics implementation
- Quality score calculation
- Automated testing
- Documentation

### Job Munyoki

- Streamlit dashboard development
- Dashboard visualizations
- User interface implementation
- CSV upload workflow

---
