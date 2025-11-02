import math
s = int(input("Entrez le nombre de côtés: "))
n = int(input("Entrez la longueur d'un côté: "))

a = s/(2*math.tan(math.radians(180/n)))
p = n * s
print(f"{a * p * 0.5:.0f}")