import random
from datetime import datetime, timedelta
import scipy.stats as stats

import numpy as np
import Generator

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
    return int(stats.expon.rvs(1 / lambda_value, size=1)[0])


def do_action_for_seconds(time: int, state):
    end_time = datetime.now() + timedelta(seconds=time)

    while True:
        if datetime.now() >= end_time:
            break
        Generator.generate_packet_with_distribution(state)


if __name__ == "__main__":
    print("Starting Markov Chain simulation")
    state = random.choice([0, 1, 2])
    duration = 0
    while True:
        print(f"Current state: {state}")
        if state == 0:
            duration = random_exponential(lambda1)
            print(f"Agario: {duration} seconds")
            do_action_for_seconds(duration, state)
            state = np.random.choice([1, 2], p=[P[0][1], P[0][2]])

        elif state == 1:
            duration = random_exponential(lambda2)
            print(f"Radio: {duration} seconds")
            do_action_for_seconds(duration, state)
            state = np.random.choice([0, 2], p=[P[1][0], P[1][2]])

        elif state == 2:
            duration = random_exponential(lambda3)
            print(f"Video: {duration} seconds")
            do_action_for_seconds(duration, state)
            state = np.random.choice([0, 1], p=[P[2][0], P[2][1]])

        else:
            print("Invalid state")
            break
