personne = {'nom': 'Alice', 'age': 30}
try:
    print(f"Nom : {personne['nom']}")
except KeyError:
    print("La clé 'nom' n'existe pas dans le dictionnaire.") 