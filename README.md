# Hospital Operations Analysis 🏥

A data-driven analysis of hospital patient flow, doctor allocation, and system bottlenecks. This project uses synthetic data to simulate 5,000 patient visits and identifies key efficiency improvements.

## 📊 Live Report
**[View the Interactive Report](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/)**

## 📂 Project Structure

*   `index.html`: The static web report (Landing Page).
*   `analyze_hospital_flow.py`: Main Python script for EDA and visualization.
*   `generate_data.py`: Script to generate the synthetic dataset.
*   `assets/`: Contains generated charts and images.
*   `hospital_operations_data.csv`: The generated synthetic dataset.

## 🚀 How to Run

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/hospital-analysis.git
    cd hospital-analysis
    ```

2.  **Install Dependencies**:
    ```bash
    pip install pandas numpy matplotlib seaborn
    ```

3.  **Generate Data** (Optional, csv is included):
    ```bash
    python generate_data.py
    ```

4.  **Run Analysis**:
    ```bash
    python analyze_hospital_flow.py
    ```
    This will regenerate the charts in the `output/` directory (you may need to copy them to `assets/` to update the website).

## 📈 Key Findings
*   **Critical Care**: Highly efficient with <5 min wait times.
*   **Bottleneck**: Doctor consultation wait times average 28.5 mins for non-critical cases.
*   **Recommendation**: Implement a "Fast Track" lane for Low-acuity patients.

---
*Created with Python, Pandas, and Seaborn.*
