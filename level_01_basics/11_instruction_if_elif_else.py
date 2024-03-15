note = 75  # Vous pouvez changer cette valeur pour tester

print(f"Pour une note de {note}:")

if note >= 90:
    mention = "Très Bien"
elif note >= 80:
    mention = "Bien"
elif note >= 70:
    mention = "Assez Bien"
elif note >= 60:
    mention = "Passable"
else:
    mention = "Échec"

print(f"Mention: {mention}")

# Test avec d'autres valeurs pour la couverture
# note = 95 # Devrait afficher Très Bien
# note = 82 # Devrait afficher Bien
# note = 65 # Devrait afficher Passable
# note = 40 # Devrait afficher Échec 