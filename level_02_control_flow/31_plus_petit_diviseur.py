n_str = "91" # Simule une saisie

try:
    n = int(n_str)
    if n <= 1:
        print("Erreur: Veuillez entrer un entier strictement supérieur à 1.")
    else:
        for diviseur in range(2, n + 1):
            if n % diviseur == 0:
                if diviseur == n:
                    print(f"{n} est un nombre premier.")
                else:
                    print(f"Le plus petit diviseur de {n} autre que 1 est {diviseur}.")
                break
except ValueError:
    print(f"Erreur: '{n_str}' n'est pas un nombre entier valide.")

# Test avec un nombre premier
# n_test = 13 -> 13 est un nombre premier
# n_test = 15 -> Le plus petit diviseur de 15 autre que 1 est 3 