print("Début de la boucle avec possibilité de break:")
for i in range(10):
    print(f"Itération: {i}")
    if i == 3:
        print(f"Condition de break atteinte à l'itération {i}.")
        break  # Sortie de la boucle

print("Boucle terminée après break.")

# Autre exemple avec une boucle while
print("\nAutre exemple avec while et break:")
compteur = 0
while compteur < 100: # Potentiellement beaucoup d'itérations
    print(f"Compteur actuel: {compteur}")
    if compteur >= 2:
        print("Le compteur a atteint 2 ou plus, on sort.")
        break
    compteur += 1
print("Fin de la boucle while après break.") 