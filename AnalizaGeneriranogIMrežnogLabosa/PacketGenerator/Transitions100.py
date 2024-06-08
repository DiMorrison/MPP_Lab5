import random
from datetime import datetime, timedelta
import scipy.stats as stats
import numpy as np
import csv

# Agario
lambda1 = 1 / 27
# Radio
lambda2 = 1 / 20
# Video
lambda3 = 1 / 13

P = np.array([[0.0, 0.25, 0.75],
              [0.12, 0.0, 0.88],
              [0.37, 0.63, 0.0]])

def random_exponential(lambda_value):
    return int(stats.expon.rvs(scale=1 / lambda_value, size=1)[0])

if __name__ == "__main__":
    print("Starting Markov Chain simulation")
    state = random.choice([0, 1, 2])
    ind = 0

    with open('StateDurations.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['State', 'Duration'])

        while ind < 200:
            ind += 1
            print(f"Current state: {state}")

            if state == 0:
                duration = random_exponential(lambda1)
                print(f"Agario: {duration} seconds")
                next_state = np.random.choice([1, 2], p=[P[0][1], P[0][2]])

            elif state == 1:
                duration = random_exponential(lambda2)
                print(f"Radio: {duration} seconds")
                next_state = np.random.choice([0, 2], p=[P[1][0], P[1][2]])

            elif state == 2:
                duration = random_exponential(lambda3)
                print(f"Video: {duration} seconds")
                next_state = np.random.choice([0, 1], p=[P[2][0], P[2][1]])

            else:
                print("Invalid state")
                break

            # Write the current state and duration to the CSV file
            writer.writerow([state, duration])

            state = next_state

    print("Simulation completed and data recorded in 'StateDurations.csv'")
