annee_str = "2024" # Simule une saisie, peut être remplacé par input()

try:
    annee = int(annee_str)
    if annee <= 0:
        print("Erreur: Veuillez entrer une année positive.")
    else:
        est_bissextile = False
        if (annee % 4 == 0 and annee % 100 != 0) or (annee % 400 == 0):
            est_bissextile = True

        if est_bissextile:
            print(f"{annee} est une année bissextile.")
        else:
            print(f"{annee} n'est pas une année bissextile.")

except ValueError:
    print(f"Erreur: '{annee_str}' n'est pas une année valide.")

# Exemples de test:
# annee_test_1 = 2000 # Bissextile
# annee_test_2 = 1900 # Non bissextile
# annee_test_3 = 2023 # Non bissextile
# annee_test_4 = 0 # Erreur 