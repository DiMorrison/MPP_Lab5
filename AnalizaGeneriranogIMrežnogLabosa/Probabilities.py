import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the simulation data
generated_data = pd.read_csv('StateDurationsGenerated.csv')
net_data = pd.read_csv('StateDurationsNET.csv')

# Calculate empirical probabilities
total_time_generated = generated_data['Trajanje_u_min'].sum()
total_time_net = net_data['Trajanje_u_min'].sum()

empirical_probabilities_generated = generated_data.groupby('Stanje')['Trajanje_u_min'].sum() / total_time_generated
empirical_probabilities_net = net_data.groupby('Stanje')['Trajanje_u_min'].sum() / total_time_net

print("Empirical Probabilities (Generated):")
print(empirical_probabilities_generated)
print("\nEmpirical Probabilities (NET):")
print(empirical_probabilities_net)

# Define the transition intensity matrix Q
lambda1 = 1 / 27
lambda2 = 1 / 20
lambda3 = 1 / 13

Q = np.array([
    [-lambda1, 0.25 * lambda1, 0.75 * lambda1],
    [lambda2 * 0.12, -lambda2, 0.88 * lambda2],
    [lambda3 * 0.37, lambda3 * 0.63, -lambda3]
])

# Calculate theoretical stationary probabilities
def calculate_stationary_distribution(Q):
    num_states = Q.shape[0]
    A = np.copy(Q.T)
    A[-1, :] = 1
    b = np.zeros(num_states)
    b[-1] = 1
    stationary_probs = np.linalg.solve(A, b)
    return stationary_probs

theoretical_probabilities = calculate_stationary_distribution(Q)

print("\nTheoretical Stationary Probabilities:")
print(theoretical_probabilities)

# Compare empirical and theoretical probabilities
comparison_generated = pd.DataFrame({
    'Empirical': empirical_probabilities_generated,
    'Theoretical': theoretical_probabilities
})

comparison_net = pd.DataFrame({
    'Empirical': empirical_probabilities_net,
    'Theoretical': theoretical_probabilities
})

print("\nComparison of Empirical and Theoretical Probabilities (Generated):")
print(comparison_generated)

print("\nComparison of Empirical and Theoretical Probabilities (NET):")
print(comparison_net)

# Visualization
plt.figure(figsize=(12, 6))
plt.bar(comparison_generated.index - 0.2, comparison_generated['Empirical'], width=0.4, label='Empirical (Generated)', align='center')
plt.bar(comparison_generated.index + 0.2, comparison_generated['Theoretical'], width=0.4, label='Theoretical', align='center')
plt.xlabel('States')
plt.ylabel('Probabilities')
plt.title('Comparison of Empirical and Theoretical Probabilities (Generated)')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.bar(comparison_net.index - 0.2, comparison_net['Empirical'], width=0.4, label='Empirical (NET)', align='center')
plt.bar(comparison_net.index + 0.2, comparison_net['Theoretical'], width=0.4, label='Theoretical', align='center')
plt.xlabel('States')
plt.ylabel('Probabilities')
plt.title('Comparison of Empirical and Theoretical Probabilities (NET)')
plt.legend()
plt.show()
