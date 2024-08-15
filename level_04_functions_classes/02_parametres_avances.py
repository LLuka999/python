"""
Paramètres avancés dans les fonctions Python
- Paramètres avec valeur par défaut
- *args (arguments positionnels multiples)
- **kwargs (arguments nommés multiples)
"""

def saluer(nom, message="Bonjour"):
    print(f"{message}, {nom} !")


def additionner(*nombres):
    """Additionne un nombre variable d'arguments."""
    return sum(nombres)


def afficher_infos(**infos):
    """Affiche des informations passées sous forme de mots-clés."""
    for cle, valeur in infos.items():
        print(f"{cle} : {valeur}")

# --- Exemples d'utilisation ---
saluer("Bob")
saluer("Bob", "Salut")
print(additionner(1, 2, 3, 4))
afficher_infos(prenom="Alice", age=30, pays="France") 