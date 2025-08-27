string = "hello world"

print(string[-(len(string) - 1)])  # Output: "e"

# Un index negatif permet de compter à partir de la fin de la chaîne.
# Ici, -11 (-len) correspond au premier caractère de la chaîne.
# C'est aussi le cas pour les listes et autres séquences en Python.

print(string[3:-1]) # Output: "lo worl"

# ça permet de prendre une sous-chaîne en partant du 4ème caractère jusqu'à l'avant-dernier.
# C'est utile pour extraire des parties spécifiques d'une chaîne ou d'une liste.
# Il suffit de spécifier l'index de début et l'index de fin (exclusif) pour obtenir la sous-chaîne désirée.

print(string[3:]) # Output: "lo world"
# Ici, on commence à partir du 4ème caractère jusqu'à la fin de la chaîne.
# C'est pratique pour obtenir une partie de la chaîne sans avoir à connaître sa longueur exacte.

print(string[:5]) # Output: "hello"
# Ici, on prend les 5 premiers caractères de la chaîne.
# C'est utile pour obtenir un préfixe ou une partie initiale d'une chaîne.

x = [1, 2, 3, 4, 5]

# En faisant ceci, on crée une nouvelle référence à la même liste.
# Toute modification de y affectera x, car ils pointent vers le même objet en mémoire
y = x
y[1] = 10
print(y)
print(x)