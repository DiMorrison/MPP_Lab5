import pandas as pd
import sys
import os

def process_traffic_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Ensure the Time column is sorted
    df = df.sort_values(by='Time')
    
    # Calculate inter-arrival times
    df['Inter-arrival Time'] = df['Time'].diff().fillna(0)
    
    # Extract relevant columns
    inter_arrival_times = df[['Inter-arrival Time']]
    packet_sizes = df[['Length']]
    
    # Extract the base name of the file (without directory and extension)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Save to CSV files without headers
    inter_arrival_times.to_csv(f'./FilteredData/{base_name}_inter_arrival_times.csv', index=False, header=False)
    packet_sizes.to_csv(f'./FilteredData/{base_name}_packet_sizes.csv', index=False, header=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python filter.py <path_to_csv_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    process_traffic_data(file_path)
