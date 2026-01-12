import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for professional tables/plots
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")

OUTPUT_DIR = 'output'
DATA_FILE = 'hospital_operations_data.csv'

def load_and_preprocess():
    print("--- 1. Data Loading & Structure ---")
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found. Please run generate_data.py first.")
        return None

    df = pd.read_csv(DATA_FILE)
    
    # Convert timestamps
    time_cols = ['ArrivalTime', 'RegistrationTime', 'ConsultationStartTime', 'ConsultationEndTime']
    for col in time_cols:
        df[col] = pd.to_datetime(df[col])
        
    print(f"Dataset Shape: {df.shape}")
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    return df

def feature_engineering(df):
    print("\n--- 2. Feature Engineering ---")
    # Calculate durations in minutes
    df['RegistrationWait'] = (df['RegistrationTime'] - df['ArrivalTime']).dt.total_seconds() / 60
    df['DoctorWait'] = (df['ConsultationStartTime'] - df['RegistrationTime']).dt.total_seconds() / 60
    df['ConsultationDuration'] = (df['ConsultationEndTime'] - df['ConsultationStartTime']).dt.total_seconds() / 60
    df['TotalHospitalTime'] = (df['ConsultationEndTime'] - df['ArrivalTime']).dt.total_seconds() / 60
    
    # Validate logic (e.g. negative durations)
    neg_mask = (df['RegistrationWait'] < 0) | (df['DoctorWait'] < 0) | (df['ConsultationDuration'] < 0)
    if neg_mask.sum() > 0:
        print(f"WARNING: Found {neg_mask.sum()} records with negative durations. Marking as NaN.")
        df.loc[neg_mask, ['RegistrationWait', 'DoctorWait', 'ConsultationDuration']] = np.nan
        
    print("Metrics created: RegistrationWait, DoctorWait, ConsultationDuration, TotalHospitalTime")
    return df

def univariate_analysis(df):
    print("\n--- 4. Univariate Analysis ---")
    metrics = ['RegistrationWait', 'DoctorWait', 'ConsultationDuration', 'TotalHospitalTime']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, metric in enumerate(metrics):
        sns.histplot(data=df, x=metric, kde=True, ax=axes[i], color='skyblue')
        axes[i].set_title(f'Distribution of {metric} (min)')
        axes[i].set_xlabel('Minutes')
        
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/univariate_distributions.png')
    print(f"Saved distribution plots to {OUTPUT_DIR}/univariate_distributions.png")
    
    # Text summary
    print(df[metrics].describe().T[['mean', '50%', 'max', 'std']])

def department_analysis(df):
    print("\n--- 5. Department Analysis ---")
    agg_cols = {'RegistrationWait': 'mean', 'DoctorWait': 'mean', 'PatientID': 'count'}
    dept_stats = df.groupby('Department').agg(agg_cols).rename(columns={'PatientID': 'PatientCount'})
    
    print(dept_stats)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=dept_stats.index, y='DoctorWait', data=dept_stats, palette='viridis')
    plt.title('Average Doctor Wait Time by Department')
    plt.ylabel('Minutes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/department_wait_times.png')

def doctor_load_analysis(df):
    print("\n--- 6. Doctor Load Analysis ---")
    doc_stats = df.groupby('DoctorID').agg({
        'PatientID': 'count',
        'ConsultationDuration': 'mean',
        'DoctorWait': 'mean'
    }).sort_values('PatientID', ascending=False)
    
    print("Top 5 Busiest Doctors:")
    print(doc_stats.head())
    
    plt.figure(figsize=(14, 6))
    sns.scatterplot(data=doc_stats, x='PatientID', y='ConsultationDuration', size='DoctorWait', sizes=(20, 200))
    plt.title('Doctor Load: Patient Volume vs Avg Duration (Size = Avg Patient Wait)')
    plt.xlabel('Patients Processed')
    plt.ylabel('Avg Consultation Duration (min)')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/doctor_load_analysis.png')

def time_flow_analysis(df):
    print("\n--- 7. Time-Based Flow Analysis ---")
    df['Hour'] = df['ArrivalTime'].dt.hour
    df['DayOfWeek'] = df['ArrivalTime'].dt.day_name()
    
    # Hourly Arrival Pattern
    hourly_vol = df.groupby('Hour')['PatientID'].count()
    
    plt.figure(figsize=(12, 5))
    sns.lineplot(x=hourly_vol.index, y=hourly_vol.values, marker='o', linewidth=2)
    plt.title('Patient Arrival Pattern by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Patients')
    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.savefig(f'{OUTPUT_DIR}/hourly_arrival_pattern.png')

    # Heatmap of Wait Times: Day vs Hour
    pivot = df.pivot_table(index='DayOfWeek', columns='Hour', values='RegistrationWait', aggfunc='mean')
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = pivot.reindex(days_order)
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap='coolwarm', annot=False)
    plt.title('Heatmap: Avg Registration Wait by Day & Hour')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/wait_time_heatmap.png')

def triage_analysis(df):
    print("\n--- 8. Triage Effectiveness ---")
    triage_order = ['Critical', 'High', 'Medium', 'Low']
    
    print(df.groupby('TriageLevel')[['RegistrationWait', 'DoctorWait']].mean().reindex(triage_order))
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='TriageLevel', y='DoctorWait', order=triage_order, palette='Reds_r')
    plt.title('Doctor Wait Time Distribution by Triage Level')
    plt.ylim(0, 100) # Zoom in to see effectiveness
    plt.savefig(f'{OUTPUT_DIR}/triage_effectiveness.png')

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    df = load_and_preprocess()
    if df is None: return
    
    df = feature_engineering(df)
    
    univariate_analysis(df)
    department_analysis(df)
    doctor_load_analysis(df)
    time_flow_analysis(df)
    triage_analysis(df)
    
    print("\n--- Analysis Complete ---")
    print(f"All plots saved to ./{OUTPUT_DIR}")

if __name__ == "__main__":
    main()
