"""
Manipulation de fichiers texte en Python
- Écriture
- Lecture
- Ajout
- Lecture ligne à ligne
"""

# Écriture dans un fichier
with open("exemple.txt", "w", encoding="utf-8") as f:
    f.write("Bonjour\n")
    f.write("Ceci est un fichier texte.\n")

# Lecture du fichier
with open("exemple.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
    print("Contenu du fichier :")
    print(contenu)

# Ajout dans le fichier
with open("exemple.txt", "a", encoding="utf-8") as f:
    f.write("Ligne ajoutée.\n")

# Lecture ligne à ligne
with open("exemple.txt", "r", encoding="utf-8") as f:
    print("Lecture ligne à ligne :")
    for ligne in f:
        print(ligne.strip()) 