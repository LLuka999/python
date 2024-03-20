nombre_str = "7" # Simule une saisie utilisateur, peut être remplacé par input()

try:
    nombre = int(nombre_str)
    if nombre % 2 == 0:
        print(f"{nombre} est pair.")
    else:
        print(f"{nombre} est impair.")
except ValueError:
    print(f"Erreur: \"{nombre_str}\" n'est pas un nombre entier valide.")

# Test avec un nombre pair
# nombre_test_pair = 4
# if nombre_test_pair % 2 == 0:
#     print(f"{nombre_test_pair} est pair (test).") 
# else:
#     print(f"{nombre_test_pair} est impair (test).")

# Test avec une entrée invalide
# try:
#     int("abc")
# except ValueError:
#     print("Erreur: Saisie invalide (test).") 