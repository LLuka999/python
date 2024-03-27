compteur = 1

print("Début de la boucle while:")
while compteur <= 5:
    print(f"Compteur: {compteur}")
    compteur += 1  # Incrémentation du compteur

print("Fin de la boucle.")

# Exemple de boucle while avec condition de sortie anticipée (break)
print("\nAutre exemple de boucle while avec un break:")
compteur_break = 0
while True: # Boucle potentiellement infinie
    compteur_break +=1
    print(f"Compteur (break example): {compteur_break}")
    if compteur_break >= 3:
        print("Condition de sortie atteinte (break).")
        break
print("Sortie de la boucle à break.") 