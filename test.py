# import math
# s = int(input("Entrez le nombre de côtés: "))
# n = int(input("Entrez la longueur d'un côté: "))

# a = s/(2*math.tan(math.radians(180/n)))
# p = n * s
# print(f"{a * p * 0.5:.0f}")

n = 5
for i in range(n, -1, -1):
    for j in range(i + 1):
        print("*", end=" ")
    print()
for i in range(0, n+1):
    for j in range(i + 1):
        print("*", end=" ")
    print()