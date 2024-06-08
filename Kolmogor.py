import pandas as pd
import scipy.stats as st

def ks_test(real_data_file, generated_data_file):
    real_data = pd.read_csv(real_data_file, header=None).squeeze()
    generated_data = pd.read_csv(generated_data_file, header=None).squeeze()
    ks_stat, p_value = st.ks_2samp(real_data, generated_data)
    return ks_stat, p_value

datasets = {
    "Agario": {
        "real_packet_sizes": 'MjerenjaNET/Agario_length.csv',
        "generated_packet_sizes": 'FilteredData/Agario_packet_sizes.csv',
        "real_inter_arrival_times": 'MjerenjaNET/Agario_time.csv',
        "generated_inter_arrival_times": 'FilteredData/Agario_inter_arrival_times.csv'
    },
    "Radio": {
        "real_packet_sizes": 'MjerenjaNET/Radio_length.csv',
        "generated_packet_sizes": 'FilteredData/Radio_packet_sizes.csv',
        "real_inter_arrival_times": 'MjerenjaNET/Radio_time.csv',
        "generated_inter_arrival_times": 'FilteredData/Radio_inter_arrival_times.csv'
    },
    "Video": {
        "real_packet_sizes": 'MjerenjaNET/Video_length.csv',
        "generated_packet_sizes": 'FilteredData/Video_packet_sizes.csv',
        "real_inter_arrival_times": 'MjerenjaNET/Video_time.csv',
        "generated_inter_arrival_times": 'FilteredData/Video_inter_arrival_times.csv'
    }
}

for name, paths in datasets.items():
    print(f"\nK-S test results for {name} dataset:")
    
    ks_stat_packet_sizes, p_value_packet_sizes = ks_test(paths["real_packet_sizes"], paths["generated_packet_sizes"])
    print(f'Packet sizes: KS Statistic = {ks_stat_packet_sizes}, p-value = {p_value_packet_sizes}')
    
    ks_stat_inter_arrival_times, p_value_inter_arrival_times = ks_test(paths["real_inter_arrival_times"], paths["generated_inter_arrival_times"])
    print(f'Inter-arrival times: KS Statistic = {ks_stat_inter_arrival_times}, p-value = {p_value_inter_arrival_times}')
