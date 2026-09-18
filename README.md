# DataOps-Troubleshooting-Scenarios

## 🚀 Overview
A modular portfolio repository designed to showcase real-world solutions for operational data challenges, pipeline bottlenecks, data integrity anomalies, and stakeholder requirements in high-volume environments (WFM & Operations).

---

## 🛠️ Case 3: Extreme Manual Data Sanitization (Python & Polars)

### 📌 Problem
In high-volume operational environments (like WFM and CRM systems), raw data exports from legacy databases frequently arrive with severe integrity issues:
- Mixed string formats and trailing/leading white spaces.
- Hidden null values in critical keys (`transaction_id`, `agent_name`).
- Corrupted status codes and negative metric values (e.g., negative handle times).
- Traditional iterative approaches (like standard Pandas loops) cause severe performance bottlenecks on large datasets.

### 💡 Solution
Built a high-performance, multithreaded data sanitization pipeline leveraging **Polars** (built on Rust) and vectorized regular expressions (`Regex`). The pipeline automatically cleans strings, standardizes states, corrects anomalies, and filters out corrupted rows in seconds.

### ⚙️ Tech Stack
- **Language:** Python 3.11+
- **Library:** Polars (High-performance dataframe library)
- **Utilities:** Regular Expressions (Regex), OS module
- **Version Control:** Git & GitHub

### 📂 Project Structure
```text
DataOps-Troubleshooting-Scenarios/
├── data/
│   ├── raw_operations.csv      # Unstructured raw data with injected anomalies
│   └── clean_operations.csv    # Processed and standardized output data
├── src/
│   └── sanitizer.py            # Main Polars sanitization script
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation

🏃‍♂️ How to Run Locally

    Clone the repository:
    Bash

    git clone [https://github.com/YOUR_USERNAME/DataOps-Troubleshooting-Scenarios.git](https://github.com/YOUR_USERNAME/DataOps-Troubleshooting-Scenarios.git)
    cd DataOps-Troubleshooting-Scenarios

    Install dependencies:
    Bash

    pip install -r requirements.txt

    Run the sanitization script:
    Bash

    python src/sanitizer.py

Developed by Jhonnier Zambrano – Data Operations & WFM Analyst.