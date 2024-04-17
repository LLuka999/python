n_str = "5" # Simule une saisie

try:
    n = int(n_str)
    if n < 0:
        print("Erreur: La factorielle n'est définie que pour les entiers positifs ou nuls.")
    elif n == 0:
        print("La factorielle de 0 est 1.")
    else:
        factorielle = 1
        for i in range(1, n + 1):
            factorielle *= i
        print(f"La factorielle de {n} est {factorielle}.")
except ValueError:
    print(f"Erreur: '{n_str}' n'est pas un nombre entier valide.")

# Tests:
# n_test_0 = 0 -> La factorielle de 0 est 1.
# n_test_1 = 1 -> La factorielle de 1 est 1.
# n_test_neg = -3 -> Erreur 