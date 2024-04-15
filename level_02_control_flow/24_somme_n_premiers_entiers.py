n_str = "10" # Simule une saisie

try:
    n = int(n_str)
    if n < 0:
        print("Erreur: Veuillez entrer un entier positif ou nul.")
    elif n == 0:
        print("La somme des 0 premiers entiers est 0.")
    else:
        somme = 0
        for i in range(1, n + 1):
            somme += i
        print(f"La somme des {n} premiers entiers est {somme}.")

        # Alternative avec la formule mathématique
        somme_formule = n * (n + 1) // 2
        print(f"(Vérification par formule: {somme_formule})")

except ValueError:
    print(f"Erreur: '{n_str}' n'est pas un nombre entier valide.")

# Test avec n=0 et n négatif
# n_test_zero = 0 -> La somme des 0 premiers entiers est 0.
# n_test_neg = -5 -> Erreur: Veuillez entrer un entier positif ou nul. 