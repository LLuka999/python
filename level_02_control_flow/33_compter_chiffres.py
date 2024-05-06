n_str = "123456" # Simule une saisie

try:
    n = int(n_str)
    n_abs_str = str(abs(n)) # On ignore le signe
    nb_chiffres = len(n_abs_str)
    print(f"Le nombre {n} contient {nb_chiffres} chiffres.")
except ValueError:
    print(f"Erreur: '{n_str}' n'est pas un nombre entier valide.")

# Test avec un nombre négatif
# n_test = -789 -> Le nombre -789 contient 3 chiffres. 