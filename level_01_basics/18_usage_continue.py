print("Début de la boucle avec possibilité de continue:")
for i in range(5):
    if i % 2 == 0:
        print(f"Itération: {i} (pair, on saute l'affichage spécifique avec continue)")
        continue  # Passe à l'itération suivante
    print(f"Itération: {i} (impair, affichage normal)")

print("Boucle terminée.")

# Autre exemple avec une boucle while
print("\nAutre exemple avec while et continue:")
compteur = 0
while compteur < 5:
    compteur += 1
    if compteur == 3:
        print(f"Compteur est {compteur}, on saute cette itération avec continue.")
        continue
    print(f"Compteur (continue example): {compteur}")
print("Fin de la boucle while (continue example).") 