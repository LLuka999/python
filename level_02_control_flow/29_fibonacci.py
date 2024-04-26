n_str = "10" # Simule une saisie

try:
    n = int(n_str)
    if n <= 0:
        print("Erreur: Veuillez entrer un nombre de termes positif.")
    elif n == 1:
        print(f"Les {n} premiers nombres de Fibonacci sont: [0]")
    else:
        fib_sequence = [0, 1]
        # On a déjà 2 termes, donc on boucle n-2 fois
        for _ in range(2, n):
            prochain_nombre = fib_sequence[-1] + fib_sequence[-2]
            fib_sequence.append(prochain_nombre)
        print(f"Les {n} premiers nombres de Fibonacci sont: {fib_sequence}")

except ValueError:
    print(f"Erreur: '{n_str}' n'est pas un nombre entier valide.")

# Tests
# n_test_1 = 1 -> [0]
# n_test_2 = 2 -> [0, 1]
# n_test_0 = 0 -> Erreur
# n_test_neg = -5 -> Erreur 