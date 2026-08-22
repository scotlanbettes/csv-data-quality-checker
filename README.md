📊 CSV Data Quality Checker

An interactive Streamlit application for assessing the quality of CSV datasets.

The application identifies common data-quality issues such as missing values, duplicate rows, and duplicate IDs, then calculates an overall data-quality score and presents the results through an interactive dashboard.

🚀 Live Demo: https://csv-data-quality-checker-zbqqjhzwciuvngr2gjerh3.streamlit.app/

👉 Open the CSV Data Quality Checker: https://csv-data-quality-checker-zbqqjhzwciuvngr2gjerh3.streamlit.app/

No installation is required.

You can click "Try sample dataset" to explore the dashboard immediately, or upload your own CSV file.

✨ Features
📁 Upload CSV datasets
▶️ Try the included sample dataset
🔎 Preview uploaded datasets
📊 Display dataset overview
⚠️ Detect missing values
🔁 Detect duplicate rows
🆔 Detect duplicate IDs
📈 Calculate missing-value percentage
📈 Calculate duplicate-row percentage
⭐ Calculate an overall data-quality score
📊 Visualize quality metrics
✅ Display validation results
📖 Explain the quality-score methodology
🧪 Quick Demo

A sample dataset is included in:

sample_data/sample_dataset.csv

The sample dataset intentionally contains data-quality issues so users can immediately see the application in action.

Example result:

Rows: 6
Columns: 5
Total Cells: 30
Quality Score: 86.67 / 100
Assessment: Good

To try the application:

Open the Live Demo.
Click "Try sample dataset".
Explore the quality results.
Optionally upload your own CSV file.
🛠️ Technology Stack
Python
Pandas
Streamlit
Pytest
Git & GitHub
Streamlit Community Cloud
📂 Project Structure
csv-data-quality-checker/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data_quality/
│ ├── metrics.py
│ └── validator.py
│
├── tests/
│ └── test_validator.py
│
├── sample_data/
│ └── sample_dataset.csv
│
└── docs/
└── quality_score.md
📐 Quality Score

The application calculates an overall quality score starting from 100.

The current formula is:

Quality Score =
100 - Missing Percentage - Duplicate Row Percentage

The final score cannot fall below 0.

Example

If a dataset has:

Missing Percentage: 6.67%
Duplicate Row Percentage: 6.66%

Then:

100 - 6.67 - 6.66 = 86.67

Therefore:

Quality Score: 86.67 / 100
Assessment: Good
Score Interpretation
Score Assessment
90–100 Excellent
75–89.99 Good
50–74.99 Needs Attention
0–49.99 Poor

For the complete methodology, see docs/quality_score.md.

🔍 Data Quality Checks
Missing Values

The application identifies empty or null cells and calculates the percentage of missing cells in the dataset.

Duplicate Rows

The application identifies rows that appear more than once and calculates the percentage of duplicate rows.

Duplicate IDs

If the dataset contains an id column, the application checks for duplicate ID values.

If an id column is not present, duplicate-ID validation is skipped.

Validation Results

The dashboard displays:

Total rows checked
Duplicate rows
Duplicate IDs
Missing values by column
💻 Run Locally

1. Clone the repository
   git clone https://github.com/scotlanbettes/csv-data-quality-checker.git
   cd csv-data-quality-checker
2. Create a virtual environment

Windows PowerShell:

python -m venv .venv

Activate it:

.venv\Scripts\Activate.ps1 3. Install dependencies
pip install -r requirements.txt 4. Run the application
streamlit run app.py

The application will open in your browser.

🧪 Testing

The project includes automated tests for the data-validation functionality.

Run:

python -m pytest

Current test status:

7 passed
🎯 Project Purpose

Data quality is an important part of data analysis, data engineering, and business operations.

This project demonstrates how a reusable Python data-quality engine can be combined with an interactive dashboard to help users:

Upload a dataset
Identify common data-quality issues
Quantify those issues
Calculate an overall quality score
Investigate missing and duplicate data
Understand the quality of their dataset

The project also demonstrates practical experience with Python development, data processing, data validation, automated testing, Streamlit application development, Git/GitHub collaboration, pull requests, and cloud deployment.

👥 Contributors
Scotlan Bettes

Contributions:

Designed the data-quality checking workflow
Developed data validation functionality
Implemented missing-value detection
Implemented duplicate-row detection
Implemented duplicate-ID validation
Developed quality metrics
Implemented the overall quality-score calculation
Developed automated tests
Created the sample dataset
Contributed to project documentation
Managed Git/GitHub repository workflow
Integrated project contributions
Prepared the project for deployment

GitHub:
https://github.com/scotlanbettes

Job Munyoki

Contributions:

Developed the Streamlit dashboard
Implemented CSV upload functionality
Built the dataset overview interface
Integrated data-quality metrics into the dashboard
Implemented quality-score presentation
Added validation-result displays
Added missing-values-by-column visualization
Implemented quality-breakdown visualization
Improved the interactive user experience
Contributed through Git branches and pull requests
Tested the dashboard and CSV workflow

GitHub:
https://github.com/JobMunyoki

🤝 Collaboration Workflow

The project was developed collaboratively using Git and GitHub.

Create Feature Branch
↓
Develop Feature
↓
Test Locally
↓
Commit Changes
↓
Push Feature Branch
↓
Create Pull Request
↓
Review / Integration
↓
Merge into Main
↓
Deploy Application

This project demonstrates practical collaborative software-development practices using Git, GitHub, feature branches, and pull requests.

🔗 Project Links

Live Application:

https://csv-data-quality-checker-zbqqjhzwciuvngr2gjerh3.streamlit.app/

GitHub Repository:

https://github.com/scotlanbettes/csv-data-quality-checker

📄 License

This project is intended for demonstration purposes.
