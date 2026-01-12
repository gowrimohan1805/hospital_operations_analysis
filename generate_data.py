import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_hospital_data(num_records=5000):
    np.random.seed(42)
    random.seed(42)

    # 1. Basic Dimensions
    patient_ids = [f'P{str(i).zfill(5)}' for i in range(1, num_records + 1)]
    departments = ['ER', 'OPD', 'Cardiology', 'Orthopedics', 'Neurology', 'Pediatrics']
    # Probabilities for departments (ER and OPD usually higher volume)
    dept_probs = [0.25, 0.35, 0.10, 0.10, 0.10, 0.10]
    
    triage_levels = ['Low', 'Medium', 'High', 'Critical']
    # Triage distribution depends on department, but simplified here
    triage_probs = [0.4, 0.3, 0.2, 0.1]
    
    visit_types = ['Emergency', 'Scheduled']
    outcomes = ['Discharged', 'Admitted', 'Referred']
    
    doctor_ids = [f'D{str(i).zfill(3)}' for i in range(1, 21)] # 20 Doctors

    # 2. Generate Base Data
    data = {
        'PatientID': patient_ids,
        'Department': np.random.choice(departments, num_records, p=dept_probs),
        'TriageLevel': np.random.choice(triage_levels, num_records, p=triage_probs),
        'VisitType': np.random.choice(visit_types, num_records, p=[0.4, 0.6]),
        'DoctorID': np.random.choice(doctor_ids, num_records),
        'Outcome': np.random.choice(outcomes, num_records, p=[0.7, 0.2, 0.1])
    }
    
    df = pd.DataFrame(data)

    # 3. Generate Timestamps
    # Start date for the data
    start_date = datetime(2025, 1, 1)
    
    # Generate arrival times over 30 days
    # Use exponential distribution for arrival gaps to simulate Poisson process, but uniform is easier for spread
    # Let's just pick random seconds added to start_date
    seconds_in_month = 30 * 24 * 60 * 60
    arrival_offsets = np.random.randint(0, seconds_in_month, num_records)
    arrival_times = [start_date + timedelta(seconds=int(x)) for x in arrival_offsets]
    arrival_times.sort() # Sort by arrival
    df['ArrivalTime'] = arrival_times

    # Function to generate durations based on logic
    def generate_flow(row):
        # Registration Wait
        # Critical/Emergency should be faster
        if row['TriageLevel'] == 'Critical' or row['Department'] == 'ER':
            reg_wait = np.random.exponential(scale=5) # 5 mins avg
        else:
            reg_wait = np.random.exponential(scale=20) # 20 mins avg
            # Add some outliers
            if random.random() < 0.05: reg_wait += 60 
            
        registration_time = row['ArrivalTime'] + timedelta(minutes=max(1, reg_wait))
        
        # Doctor Wait
        # Depends on doctor load mostly, but simplified simulation
        doc_wait = np.random.exponential(scale=30)
        # Critical patients jump queue
        if row['TriageLevel'] == 'Critical':
            doc_wait = np.random.exponential(scale=5)
            
        consult_start = registration_time + timedelta(minutes=max(1, doc_wait))
        
        # Consultation Duration
        consult_duration = np.random.normal(loc=15, scale=5) # 15 mins avg
        if row['Department'] in ['Cardiology', 'Neurology']:
            consult_duration += 10 # Specialists take longer
        if row['TriageLevel'] == 'Critical':
            consult_duration += 20 # Critical takes longer
            
        consult_end = consult_start + timedelta(minutes=max(2, consult_duration))
        
        return pd.Series([registration_time, consult_start, consult_end])

    print("Generating synthetic timestamps...")
    time_cols = df.apply(generate_flow, axis=1)
    time_cols.columns = ['RegistrationTime', 'ConsultationStartTime', 'ConsultationEndTime']
    
    df = pd.concat([df, time_cols], axis=1)
    
    # Randomly introduce some data quality issues (optional, per requirements)
    # Missing timestamps (simulating system error) - 1%
    mask = np.random.random(num_records) < 0.01
    df.loc[mask, 'RegistrationTime'] = pd.NaT
    
    # Save
    output_path = 'hospital_operations_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {num_records} records to {output_path}")
    
    # Validation Print
    print("\nSample Data:")
    print(df.head())
    print("\nData Types:")
    print(df.dtypes)

if __name__ == "__main__":
    generate_hospital_data()
