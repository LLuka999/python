personne = {'nom': 'Alice', 'age': 30, 'ville': 'Paris'}
print(f"Dictionnaire avant suppression : {personne}")
try:
    del personne['ville']
    print(f"Dictionnaire après suppression de 'ville' : {personne}")
except KeyError:
    print("La clé 'ville' n'existe pas dans le dictionnaire.") 