"""
Introduction aux fonctions en Python
- Définition
- Appel
- Paramètres
- Valeur de retour
- Docstring
"""

def dire_bonjour(nom):
    """Affiche un message de salutation personnalisé."""
    print(f"Bonjour, {nom} !")


def addition(a, b):
    """Retourne la somme de deux nombres."""
    return a + b


def afficher_menu():
    """Affiche un menu simple à l'écran."""
    print("1. Dire bonjour")
    print("2. Additionner deux nombres")
    print("3. Quitter")


# --- Exemples d'utilisation ---
dire_bonjour("Alice")
resultat = addition(3, 5)
print(f"3 + 5 = {resultat}")
afficher_menu()

# --- Paramètres par défaut ---
def saluer(nom, message="Bonjour"):
    print(f"{message}, {nom} !")

saluer("Bob")  # Utilise le message par défaut
saluer("Bob", message="Salut")  # Message personnalisé

# --- Arguments nommés ---
def infos_personne(nom, age, ville):
    print(f"Nom : {nom}, Âge : {age}, Ville : {ville}")

infos_personne(age=30, ville="Paris", nom="Claire")

# --- Nombre variable d'arguments ---
def additionner(*nombres):
    total = 0
    for n in nombres:
        total += n
    return total

print(f"Somme de 1, 2, 3 : {additionner(1, 2, 3)}")
print(f"Somme de 5, 10 : {additionner(5, 10)}")

# --- Portée des variables ---
def fonction_locale():
    x = 10  # Variable locale
    print(f"x dans la fonction : {x}")

x = 5  # Variable globale
fonction_locale()
print(f"x dans le programme principal : {x}")

# --- Fonctions comme objets ---
def crier(message):
    print(message.upper())

def executer_fonction(f, texte):
    f(texte)

executer_fonction(crier, "bonjour tout le monde") 