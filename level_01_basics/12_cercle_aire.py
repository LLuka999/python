import math

rayon = 5.0  # Valeur d'exemple, peut être remplacée par input()

if rayon <= 0:
    print("Erreur: Le rayon doit être un nombre positif.")
else:
    aire = math.pi * (rayon ** 2)
    aire_arrondie = round(aire, 2)
    print(f"Le rayon du cercle est: {rayon}")
    print(f"L'aire du cercle est: {aire_arrondie}")

# Test avec une valeur invalide
# rayon_test_negatif = -2
# if rayon_test_negatif <= 0:
#     print("Erreur test (négatif): Le rayon doit être un nombre positif.")

# Test avec rayon = 0
# rayon_test_zero = 0
# if rayon_test_zero <= 0:
#     print("Erreur test (zéro): Le rayon doit être un nombre positif.") 