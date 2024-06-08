import csv
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import expon
import statsmodels.api as sm

# average trajanje sesije 1. izvor =  27 s

# average trajanje sesije  2. izvor = 20 s

# average trajanje sesije  3. izvor =  13 s

# definiraj eksponencijalnu razdiobu trajanja za svaku uslugu
# lambda = 1/prosjek

# 1. izvor
lambda1 = 1 / 27
# 2. izvor
lambda2 = 1 / 20
# 3. izvor
lambda3 = 1 / 13

# Generiranje uzoraka iz eksponencijalne distribucije za svaku uslugu
uzroci1 = expon.rvs(scale=1 / lambda1, size=1000)
uzroci2 = expon.rvs(scale=1 / lambda2, size=1000)
uzroci3 = expon.rvs(scale=1 / lambda3, size=1000)

# Plotiranje histograma
plt.hist(uzroci1, bins=30, alpha=0.5, label='izvor 1', color='red')
plt.hist(uzroci2, bins=30, alpha=0.5, label='izvor 2', color="yellow")
plt.hist(uzroci3, bins=30, alpha=0.5, label='izvor 3', color='blue')

plt.xlabel('Trajanje usluge (sekunde)')
plt.ylabel('Broj uzoraka')
plt.title('Eksponencijalna distribucija trajanja usluga')
plt.legend()
plt.grid(True)
plt.show()

# 3 su stanja, 1. su društvene mreže, 2. je muzika, 3. je TV/Video
# dakle matrice su 3x3

# P je matrica vjerojatnosti prijelaza
P = np.array([[0.0, 0.25, 0.75],
              [0.12, 0.0, 0.88],
              [0.37, 0.63, 0.0]])

# Q je matrica intenziteta prijelaza
Q = np.array([[-lambda1, 0.25 * lambda1, 0.75 * lambda1],
              [lambda2 * 0.12, -lambda2, 0.88 * lambda2],
              [lambda3 * 0.37, lambda3 * 0.63, -lambda3]])

Trajanje1 = np.random.exponential(scale=1 / lambda1)
Trajanje2 = np.random.exponential(scale=1 / lambda2)
Trajanje3 = np.random.exponential(scale=1 / lambda3)

# Prikaz rezultata
print("Trajanje stanja 1 (): {0}sekundi i lambda je: {1}".format(round(Trajanje1, 2), round(lambda1, 3)))
print("Trajanje stanja 2 (): {0}sekundi i lambda je: {1}".format(round(Trajanje2, 2), round(lambda2, 3)))
print("Trajanje stanja 3 (): {0}sekundi i lambda je: {1}".format(round(Trajanje3, 2), round(lambda3, 3)))
print()
print("Vjerojatnosti prijelaza između stanja (matrica P):")
print(P)
print()
print("Matrica intenziteta prijelaza (matrica Q):")
print(Q)
print()


# simulacija ponašanja 1 korisnika koristeći markoveljev lanac i razdiobe trajanja sjednica

# Funkcija za generiranje trajanja sjednice za pojedinu kategoriju aplikacije
def GenerirajTrajanjeSjednice(category_lambda):
    return round(np.random.exponential(scale=1 / category_lambda), 4)

trenutnoStanje = np.random.choice([0, 1, 2])
brojKoraka = 200
stanja = [trenutnoStanje]
trajanjeSjednica = []
trajanjePojedineSjednice = [0, 0, 0]
vjerojatnostPrijelaza = [0, 0, 0]
odabirStanja = [lambda1, lambda2, lambda3]
odabirMogucnosti = [0, 1, 2]


# Simulacija ponašanja korisnika
with open('StanjaVremena.csv', 'w', newline='') as pisac:
    writer = csv.writer(pisac)
    writer.writerow(['Stanje', 'Trajanje_u_min'])
    for _ in range(brojKoraka):
        # Generiraj trajanje sjednice za trenutno stanje
        trajanjeSjednice = GenerirajTrajanjeSjednice(odabirStanja[trenutnoStanje])
        trajanjePojedineSjednice[trenutnoStanje] += trajanjeSjednice
        trajanjeSjednica.append(trajanjeSjednice)
        writer.writerow([trenutnoStanje, trajanjeSjednice])

        # Izračunaj vjerojatnosti prijelaza u sljedeće stanje
        # vjerojatnost prijelaza = -qij/qii za i!=j
        for i in range(3):
            if i == trenutnoStanje:
                vjerojatnostPrijelaza[i] = 0
            else:
                vjerojatnostPrijelaza[i] = Q[trenutnoStanje, i] / -Q[trenutnoStanje, trenutnoStanje]

        # Odaberi sljedeće stanje temeljem vjerojatnosti prijelaza
        sljedeceStanje = np.random.choice(odabirMogucnosti, p=vjerojatnostPrijelaza)
        trenutnoStanje = sljedeceStanje
        stanja.append(trenutnoStanje)


# Izračun ECDF za svaku kategoriju
ecdf1 = sm.distributions.ECDF(uzroci1)
ecdf2 = sm.distributions.ECDF(uzroci2)
ecdf3 = sm.distributions.ECDF(uzroci3)

# Vizualizacija rezultata
plt.figure(figsize=(10, 6))

plt.plot(ecdf1.x, ecdf1.y, label='Izvor 1', linestyle='-', marker='o')
plt.plot(ecdf2.x, ecdf2.y, label='Izvor 2', linestyle='--', marker='s')
plt.plot(ecdf3.x, ecdf3.y, label='Izvor 3', linestyle='-.', marker='d')

plt.xlabel('Trajanje (sekunde)')
plt.ylabel('ECDF')
plt.title('Empirijska funkcija razdiobe trajanja aplikacija')
plt.legend()
plt.grid(True)
plt.show()

# Računanje vremena provedenog u svakom stanju

print("Trajanje sjednica po kategorijama:")
print("Izvor 1: {0}sekundi".format(round(trajanjePojedineSjednice[0], 2)))
print("Izvor 2: {0}sekundi".format(round(trajanjePojedineSjednice[1], 2)))
print("Izvor 3: {0}sekundi".format(round(trajanjePojedineSjednice[2], 2)))
print("Ukupno trajanje sjednica: {0}sekundi\n".format(round(sum(trajanjePojedineSjednice), 2)))

print("Vjerojatnost izvora 1: {0}".format(round(trajanjePojedineSjednice[0] / sum(trajanjePojedineSjednice), 6)))
print("Vjerojatnost izvora 2: {0}".format(round(trajanjePojedineSjednice[1] / sum(trajanjePojedineSjednice), 6)))
print("Vjerojatnost izvora 3: {0}".format(round(trajanjePojedineSjednice[2] / sum(trajanjePojedineSjednice), 6)))
print("Ukupna vjerojatnost trajanja sjednica: {0}".format(round(sum(trajanjePojedineSjednice) / sum(trajanjePojedineSjednice), 6)))
