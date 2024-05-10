liste_nombres = [3, 7, 2, 9, 4]

if len(liste_nombres) == 0:
    print("Erreur: La liste est vide, impossible de trouver le maximum.")
else:
    maximum = liste_nombres[0]
    for nombre in liste_nombres[1:]:
        if nombre > maximum:
            maximum = nombre
    print(f"Le maximum de la liste {liste_nombres} est {maximum}.")

# Test avec une liste vide
# liste_vide = []
# if len(liste_vide) == 0:
#     print("Erreur: La liste est vide, impossible de trouver le maximum.") 