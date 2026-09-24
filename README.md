# 📊 CSV Data Quality Checker

A Python and Streamlit application for analyzing, validating, cleaning, and improving the quality of CSV datasets.

CSV Data Quality Checker identifies common data-quality problems, calculates dataset and column-level quality scores, provides interactive cleaning tools, compares data before and after cleaning, and allows users to download cleaned datasets and quality reports.

![Python Tests](https://github.com/scotlanbettes/csv-data-quality-checker/actions/workflows/tests.yml/badge.svg)

---

## 🚀 Version 2

Version 2 significantly expands the original CSV Data Quality Checker from a basic validation dashboard into a more complete data-quality analysis and cleaning application.

### Version 2 Developer

**Job Munyoki**

Version 2 was independently developed by Job Munyoki, building on the original Version 1 collaborative project.

The V2 work includes:

- Advanced data-quality validation
- Weighted quality scoring
- Column-level quality scores
- Numeric outlier detection
- Empty-string detection
- Whitespace detection
- Inconsistent data-type detection
- Inconsistent capitalization detection
- Interactive data-cleaning tools
- Missing-value handling strategies
- Text capitalization standardization
- Before-and-after quality comparison
- Cleaned CSV export
- Data-quality report export
- Redesigned five-tab Streamlit dashboard
- Expanded automated test suite
- GitHub Actions continuous integration

---

## 🌐 Live Application

Version 2 is deployed on Streamlit Community Cloud:

https://csv-data-quality-checker-v2.streamlit.app/

No installation is required.

You can:

- Select the built-in sample dataset
- Upload your own CSV file
- Analyze data-quality issues
- Clean detected problems
- Compare before-and-after quality scores
- Download the cleaned CSV
- Download a data-quality report

---

# ✨ Version 2 Features

## 🔍 Advanced Data Quality Validation

The application can detect:

- Missing values
- Duplicate rows
- Duplicate IDs
- Empty strings
- Whitespace-only values
- Leading and trailing whitespace
- Inconsistent Python data types
- Numeric outliers
- Inconsistent capitalization

---

## ⭐ Weighted Data Quality Score

Version 2 uses a weighted scoring model instead of the original Version 1 formula.

The overall score starts at **100** and applies weighted penalties based on detected quality problems.

| Quality Dimension           | Weight |
| --------------------------- | -----: |
| Missing Values              |    30% |
| Duplicate Rows              |    15% |
| Duplicate IDs               |    10% |
| Empty Strings               |    10% |
| Whitespace Issues           |    10% |
| Inconsistent Data Types     |    10% |
| Numeric Outliers            |    10% |
| Inconsistent Capitalization |     5% |

The final score is restricted to:

```text
0 ≤ Quality Score ≤ 100
```

This gives a more complete assessment than only considering missing values and duplicate rows.

---

## 🔎 Column-Level Quality Scores

Version 2 also calculates quality scores for individual columns.

Each column can be evaluated for relevant issues such as:

- Missing values
- Empty strings
- Whitespace
- Mixed data types
- Outliers
- Capitalization inconsistencies
- Duplicate IDs for the selected identifier column

This helps users identify exactly which columns require attention.

---

# 🧹 Data Cleaning

Version 2 can actively clean datasets rather than only identifying problems.

Available cleaning operations include:

### Whitespace Cleaning

- Remove leading whitespace
- Remove trailing whitespace

### Empty Value Standardization

Whitespace-only or blank strings can be converted into standardized missing values.

### Duplicate Removal

Fully duplicated rows can be automatically removed.

### Missing-Value Handling

Available strategies include:

- Drop rows containing missing values
- Fill numeric values using the mean
- Fill numeric values using the median
- Fill text values using the mode
- Fill values using a custom replacement

### Text Standardization

Selected text columns can be converted to:

- Title Case
- lowercase
- UPPERCASE

Cleaning is performed on a copy of the uploaded dataset so the original data remains unchanged.

---

# 📊 Version 2 Dashboard

The Streamlit interface is organized into five main tabs.

## 📊 Overview

Displays:

- Dataset row count
- Column count
- Total cells
- Overall quality score
- Missing values
- Duplicate rows
- Duplicate IDs
- Outliers
- Empty strings
- Whitespace issues
- Type inconsistencies
- Capitalization issues
- Dataset preview
- Quality breakdown visualization

## ⚠️ Issues

Provides detailed information about detected problems, including:

- Missing values by column
- Empty strings
- Whitespace problems
- Mixed data types
- Numeric outliers
- Capitalization inconsistencies
- Duplicate rows
- Duplicate IDs

## 🔎 Column Analysis

Displays:

- Column name
- Data type
- Missing percentage
- Empty-string percentage
- Whitespace percentage
- Inconsistent-type percentage
- Outlier percentage
- Capitalization percentage
- Duplicate-ID percentage
- Column quality score

Users can also inspect individual columns.

## 🧹 Data Cleaning

Provides interactive controls for:

- Trimming whitespace
- Standardizing empty strings
- Removing duplicate rows
- Handling missing values
- Selecting columns to clean
- Standardizing capitalization
- Previewing cleaned data
- Comparing before/after scores
- Downloading the cleaned CSV

## 📄 Report

Provides a before-and-after quality comparison showing how cleaning affected the dataset.

Users can also download a text-based data-quality report.

---

# 📈 Before-and-After Comparison

Version 2 tracks the impact of cleaning operations.

Example:

```text
Before Cleaning
Quality Score: 78.40

After Cleaning
Quality Score: 94.70

Quality Score Change: +16.30
```

The reporting engine also tracks changes such as:

- Rows removed
- Missing values resolved
- Duplicate rows removed
- Duplicate IDs resolved
- Empty strings resolved
- Whitespace issues resolved
- Outliers resolved
- Capitalization issues resolved

---

# ⬇️ Export Features

Version 2 supports downloadable outputs.

## Cleaned CSV

Users can download the cleaned dataset as:

```text
cleaned_dataset.csv
```

## Quality Report

Users can also download:

```text
data_quality_report.txt
```

The report includes:

- Original quality metrics
- Cleaned quality metrics
- Quality score comparison
- Cleaning summary
- Issues resolved

---

# 🆔 Configurable Identifier Column

Version 1 automatically looked for a column named:

```text
id
```

Version 2 allows users to choose the column that represents the dataset's identifier or primary key.

If no identifier column is required, duplicate-ID checking can be disabled.

---

# 🧪 Automated Testing

The project contains automated tests for validation, metrics, cleaning, reporting, and export functionality.

Run the test suite using:

```bash
python -m pytest
```

Current Version 2 test status:

```text
34 passed
```

Test files include:

```text
tests/
├── test_validator.py
├── test_cleaner.py
├── test_reporting.py
└── test_exporter.py
```

---

# ⚙️ Continuous Integration

Version 2 uses **GitHub Actions** for automated testing.

The workflow runs whenever code is pushed or a pull request is opened against:

```text
main
version-2
```

Workflow file:

```text
.github/workflows/tests.yml
```

The CI pipeline:

```text
Checkout Repository
        ↓
Set Up Python
        ↓
Install Dependencies
        ↓
Install Pytest
        ↓
Run Automated Tests
        ↓
Pass / Fail
```

This helps ensure that new changes do not break existing functionality.

---

# 🛠️ Technology Stack

- Python
- Pandas
- Streamlit
- Pytest
- Git
- GitHub
- GitHub Actions
- Streamlit Community Cloud

---

# 📂 Project Structure

```text
csv-data-quality-checker/
│
├── app.py
├── README.md
├── requirements.txt
├── V2_PLAN.md
│
├── data_quality/
│   ├── __init__.py
│   ├── validator.py
│   ├── metrics.py
│   ├── cleaner.py
│   ├── reporting.py
│   └── exporter.py
│
├── tests/
│   ├── test_validator.py
│   ├── test_cleaner.py
│   ├── test_reporting.py
│   └── test_exporter.py
│
├── sample_data/
│   └── sample_dataset.csv
│
├── docs/
│   └── quality_score.md
│
└── .github/
    └── workflows/
        └── tests.yml
```

---

# 💻 Run Locally

## 1. Clone the repository

```bash
git clone https://github.com/scotlanbettes/csv-data-quality-checker.git
cd csv-data-quality-checker
```

To work specifically with Version 2:

```bash
git checkout version-2
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install application dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For development and testing:

```bash
pip install pytest
```

---

## 4. Run the application

```bash
streamlit run app.py
```

If the Streamlit launcher is unavailable, use:

```bash
python -m streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

## 5. Run automated tests

```bash
python -m pytest
```

---

# 📁 Sample Dataset

A demonstration dataset is included at:

```text
sample_data/sample_dataset.csv
```

The Version 2 sample dataset intentionally contains several data-quality issues so users can immediately explore the application's detection and cleaning features.

The sample includes examples of:

- Missing values
- Duplicate rows
- Duplicate IDs
- Whitespace issues
- Empty strings
- Inconsistent capitalization
- Numeric outliers

---

# 🎯 Project Purpose

Data quality is important in data analysis, data engineering, machine learning, reporting, and business operations.

Poor-quality datasets can contain:

- Missing information
- Duplicate records
- Invalid identifiers
- Inconsistent formatting
- Mixed data types
- Unexpected numerical values
- Formatting inconsistencies

CSV Data Quality Checker demonstrates how a reusable Python data-quality engine can be combined with an interactive Streamlit interface to help users:

1. Upload data
2. Detect quality problems
3. Quantify those problems
4. Identify problematic columns
5. Clean common issues
6. Compare data before and after cleaning
7. Export improved datasets
8. Generate quality reports

The project also demonstrates practical experience with:

- Python software development
- Pandas data processing
- Data validation
- Data cleaning
- Statistical outlier detection
- Application architecture
- Automated testing
- Continuous integration
- Streamlit development
- Git and GitHub
- Branch-based development
- Cloud deployment

---

# 📜 Project History

## Version 1 — Collaborative Development

The original version of CSV Data Quality Checker was developed collaboratively by:

- **Scotlan Bettes**
- **Job Munyoki**

Version 1 focused on:

- CSV upload
- Missing-value detection
- Duplicate-row detection
- Duplicate-ID validation
- Basic quality metrics
- Overall quality score
- Streamlit dashboard
- Dataset visualization
- Automated tests
- Git/GitHub collaboration

### Scotlan Bettes — Version 1 Contributions

- Designed the original data-quality workflow
- Developed validation functionality
- Implemented missing-value detection
- Implemented duplicate-row detection
- Implemented duplicate-ID validation
- Developed quality metrics
- Implemented the original quality-score calculation
- Developed automated tests
- Created sample data
- Contributed documentation
- Managed repository integration
- Supported deployment preparation

GitHub:

https://github.com/scotlanbettes

### Job Munyoki — Version 1 Contributions

- Developed the Streamlit dashboard
- Implemented CSV upload functionality
- Built the dataset-overview interface
- Integrated quality metrics into the dashboard
- Implemented quality-score presentation
- Added validation-result displays
- Added missing-value visualizations
- Implemented quality-breakdown visualization
- Improved application UX
- Tested the dashboard and CSV workflow
- Contributed through feature branches and pull requests

GitHub:

https://github.com/JobMunyoki

---

# 🚀 Version 2 — Independent Upgrade

**Developer: Job Munyoki**

Version 2 builds on the original collaborative project and was independently designed and implemented as a major upgrade by Job Munyoki.

Version 2 development includes:

- Expanded validation engine
- Empty-string detection
- Whitespace detection
- Mixed data-type detection
- IQR-based numeric outlier detection
- Capitalization inconsistency detection
- Configurable identifier column
- Weighted dataset-quality scoring
- Column-level quality scoring
- Data-cleaning engine
- Missing-value strategies
- Text standardization
- Before-and-after reporting
- CSV export
- Quality-report export
- Redesigned Streamlit dashboard
- Expanded automated test suite
- GitHub Actions CI
- Streamlit Community Cloud deployment
- Version 2 documentation

GitHub:

https://github.com/JobMunyoki

---

# 🌿 Development Workflow

Version 2 is developed on a dedicated branch:

```text
version-2
```

Typical workflow:

```text
Plan Feature
    ↓
Implement Feature
    ↓
Write / Update Tests
    ↓
Run Tests Locally
    ↓
Commit Changes
    ↓
Push to version-2
    ↓
GitHub Actions Runs Tests
    ↓
Review Results
    ↓
Deploy / Continue Development
```

The Version 2 branch is maintained separately from the original Version 1 code while the upgrade is finalized and prepared for integration.

---

# 🔗 Project Links

## Version 2 Live Application

https://csv-data-quality-checker-v2.streamlit.app/

## GitHub Repository

https://github.com/scotlanbettes/csv-data-quality-checker

## Version 2 Branch

https://github.com/scotlanbettes/csv-data-quality-checker/tree/version-2

## Version 2 Pull Request

https://github.com/scotlanbettes/csv-data-quality-checker/pull/4

## Job Munyoki GitHub

https://github.com/JobMunyoki

## Scotlan Bettes GitHub

https://github.com/scotlanbettes

---

# 📄 License / Usage

This project is currently maintained as a portfolio, demonstration, and educational software project.
