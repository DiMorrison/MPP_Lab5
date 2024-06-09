import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib
import matplotlib.pyplot as plt
import csv

# wireshark filter: ((ip.src == 104.17.232.168) && (ip.dst == 192.168.1.10)) || ((ip.src == 192.168.1.10) && (ip.dst == 104.17.232.168))

#Učitavanje podataka iz datoteke
data_array=[]
time = []
length = []
with open('agario.csv') as csvDataFile:
	csvReader = csv.reader(csvDataFile, delimiter='\n')
	for row in csvReader:
		split_row = row[0].split(",")
		time.append(split_row[1].strip("\""))
		length.append(split_row[5].strip("\""))
		
# make time and length numpy arrays
time = np.array(time[1:])
length = np.array(length[1:])

time_ms = []
for t in time:
	t = float(t)
	t = t * 1000
	time_ms.append(t)
time_ms = np.array(time_ms)

time_ms1 = time_ms[:time_ms.size-1]
time_ms2 = time_ms[1:]
# deduct time_ms2 from time_ms1
time_ms_diff = time_ms2 - time_ms1

# Convert length array to numeric data type
length = length.astype(float)

print("Osnovne informacije o empirijskim podacima:")
# calculate mean, median, min, max for time_ms_diff and length
print('---------------------------------')
print('---------------------------------')
print('Veličina paketa:')
print('---------------------------------')
print('---------------------------------')
print('Minimum: ', np.min(length))
print('---------------------------------')
print('Maksimum: ', np.max(length))
print('---------------------------------')
print('Srednja vrijednost: ', np.mean(length))
print('---------------------------------')
print('Medijan: ', np.median(length))
print('---------------------------------')
print('---------------------------------')
print('Međudolazno vrijeme:')
print('---------------------------------')
print('---------------------------------')
print('Minimum: ', np.min(time_ms_diff))
print('---------------------------------')
print('Maksimum: ', np.max(time_ms_diff))
print('---------------------------------')
print('Srednja vrijednost: ', np.mean(time_ms_diff))
print('---------------------------------')
print('Medijan: ', np.median(time_ms_diff))
print('---------------------------------')


# make time and length dataframes
time_ms_diff_df = pd.DataFrame(time_ms_diff)
length_df = pd.DataFrame(length)

# turn time_ms_diff dataframe into csv file
time_ms_diff_df.to_csv('time_ms_diff.csv', index=False, header=False)
# turn length dataframe into csv file
length_df.to_csv('length.csv', index=False, header=False)


	