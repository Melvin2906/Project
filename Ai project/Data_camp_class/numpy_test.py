import numpy as np
from numpy import array

height = [1.75, 1.80, 1.65, 1.90, 1.55]
nb_height = array(height)

weight = [70, 80, 60, 90, 50]
nb_weight = array(weight)

bmi = nb_weight / (nb_height ** 2)
print(bmi)
print(f"Cet array est de type {type(bmi)} et a pour taille {bmi.shape}")

# Tous les éléments d'un array de np sont forcément du même type
# Pour faire un 2d array il faut faire un array de listes
array_2d = array([[1, 2, 3], [4, 5, 6]])
print(array_2d)
print(f"Cet array est de type {type(array_2d)} et a pour taille {array_2d.shape}")

print("'array_2d[row, column]' et 'array_2d[row][column]' sont deux expressions équivalentes")

# Select the entire second column of np_baseball: np_weight_lb
np_weight_lb = array_2d[:, 1]

np_baseball = [[1.75, 1.80, 65], [1.70, 1.20, 65], [1.90, 1.55, 45]]
avg = np.mean(np_baseball[:,0])
print("Average: " + str(avg))

# Print median height
med = np.median(np_baseball[:, 0])
print("Median: " + str(med))

# Print out the standard deviation on height
stddev = np.std(np_baseball[:, 0])
print("Standard Deviation: " + str(stddev))

# Print out correlation between first and second column
corr = np.corrcoef(np_baseball[:, 0], np_baseball[:, 1])
print("Correlation: " + str(corr))