"""
Fonctions lambda en Python
- Définition
- Utilisation avec map, filter, sorted
"""

# Fonction lambda simple
carre = lambda x: x ** 2
print(carre(5))

# Utilisation avec map
nombres = [1, 2, 3, 4]
carres = list(map(lambda x: x ** 2, nombres))
print(carres)

# Utilisation avec filter
pairs = list(filter(lambda x: x % 2 == 0, nombres))
print(pairs)

# Utilisation avec sorted
prenoms = ["Alice", "bob", "Charlie", "david"]
prenoms_tries = sorted(prenoms, key=lambda s: s.lower())
print(prenoms_tries) 