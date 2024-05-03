n_str = "36" # Simule une saisie

try:
    n = int(n_str)
    if n <= 0:
        print("Erreur: Veuillez entrer un entier strictement positif.")
    else:
        diviseurs = []
        for i in range(1, n + 1):
            if n % i == 0:
                diviseurs.append(i)
        diviseurs_str = ", ".join(str(d) for d in diviseurs)
        print(f"Les diviseurs de {n} sont: {diviseurs_str}")
except ValueError:
    print(f"Erreur: '{n_str}' n'est pas un nombre entier valide.")

# Test avec n=1 -> Les diviseurs de 1 sont: 1
# Test avec n=13 -> Les diviseurs de 13 sont: 1, 13 