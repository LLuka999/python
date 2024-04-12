nombre_str = "5" # Simule une saisie

try:
    nombre = int(nombre_str)
    print(f"Table de multiplication pour {nombre}:")
    for i in range(1, 11): # De 1 à 10 inclus
        resultat = nombre * i
        print(f"{nombre} x {i} = {resultat}")
except ValueError:
    print(f"Erreur: '{nombre_str}' n'est pas un nombre entier valide.")

# Test avec une autre valeur
# nombre_test = 7
# print(f"\nTable de multiplication pour {nombre_test} (test):")
# for i in range(1, 11):
#     print(f"{nombre_test} x {i} = {nombre_test * i}") 