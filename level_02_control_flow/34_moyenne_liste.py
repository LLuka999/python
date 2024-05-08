liste_nombres = [10, 20, 30, 40, 50]

if len(liste_nombres) == 0:
    print("Erreur: La liste est vide, impossible de calculer la moyenne.")
else:
    moyenne = sum(liste_nombres) / len(liste_nombres)
    print(f"La moyenne des valeurs {liste_nombres} est {moyenne:.1f}.")

# Test avec une liste vide
# liste_vide = []
# if len(liste_vide) == 0:
#     print("Erreur: La liste est vide, impossible de calculer la moyenne.") 