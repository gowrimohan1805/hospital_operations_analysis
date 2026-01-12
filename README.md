# 🏥 Hospital Operations Analysis – Patient Flow Optimization

## Objective
Analyze hospital patient flow to identify operational bottlenecks,
optimize doctor allocation, and reduce patient waiting times using EDA.

## Project Structure
- `generate_data.py` – Synthetic hospital dataset generator
- `analyze_hospital_flow.py` – End-to-end EDA and visualization
- `hospital_operations_data.csv` – Simulated operations data
- `output/` – Generated charts and reports

## Key Insights
- Identified doctor wait time as primary bottleneck
- Department-level delays (ER, Cardiology)
- Time-of-day demand vs capacity mismatch
- Triage prioritization violations detected

## Tech Stack
- Python
- Pandas, NumPy
- Matplotlib, Seaborn

## How to Run
```bash
pip install pandas numpy matplotlib seaborn
python generate_data.py
python analyze_hospital_flow.py
