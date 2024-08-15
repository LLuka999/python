"""
Introduction aux classes en Python
- Définition d'une classe
- Constructeur (__init__)
- Attributs d'instance
- Méthodes
- Instanciation et utilisation d'objets
- Méthode spéciale __str__
"""

# Définition d'une classe simple
class Personne:
    def __init__(self, nom, age):
        self.nom = nom  # Attribut d'instance
        self.age = age
    
    def se_presenter(self):
        print(f"Bonjour, je m'appelle {self.nom} et j'ai {self.age} ans.")
    
    def anniversaire(self):
        self.age += 1
        print(f"Joyeux anniversaire {self.nom} ! Tu as maintenant {self.age} ans.")
    
    def __str__(self):
        return f"Personne(nom={self.nom}, age={self.age})"

# Instanciation et utilisation d'objets
alice = Personne("Alice", 28)
bob = Personne("Bob", 35)

alice.se_presenter()
bob.se_presenter()

alice.anniversaire()
print(alice)

# --- Héritage ---
class Employe(Personne):
    def __init__(self, nom, age, poste):
        super().__init__(nom, age)  # Appel au constructeur de la classe parente
        self.poste = poste
    
    # Surcharge de méthode
    def se_presenter(self):
        print(f"Bonjour, je m'appelle {self.nom}, j'ai {self.age} ans et je suis {self.poste}.")

# Instanciation d'une classe dérivée
carole = Employe("Carole", 40, "ingénieure")
carole.se_presenter()

# --- Attribut de classe ---
class Compteur:
    nombre_instances = 0  # Attribut de classe
    def __init__(self):
        Compteur.nombre_instances += 1

# Création de plusieurs instances
c1 = Compteur()
c2 = Compteur()
print(f"Nombre d'instances de Compteur : {Compteur.nombre_instances}")

# --- Méthode de classe et méthode statique ---
class Utilitaires:
    @classmethod
    def afficher_info_classe(cls):
        print(f"Ceci est la classe {cls.__name__}")
    
    @staticmethod
    def addition(a, b):
        return a + b

Utilitaires.afficher_info_classe()
print(f"Addition statique : {Utilitaires.addition(10, 5)}")

# --- Encapsulation et Propriétés ---
class CompteBancaire:
    def __init__(self, titulaire, solde_initial):
        self.titulaire = titulaire
        self.__solde = solde_initial  # Attribut "privé" par convention (name mangling)

    @property
    def solde(self):
        """Getter pour le solde."""
        return self.__solde

    @solde.setter
    def solde(self, nouveau_solde):
        """Setter pour le solde, avec validation."""
        if nouveau_solde < 0:
            print("Erreur : Le solde ne peut pas être négatif.")
        else:
            self.__solde = nouveau_solde

    @solde.deleter
    def solde(self):
        """Deleter pour le solde (exemple)."""
        print("Le solde a été supprimé (exemple de deleter).")
        del self.__solde

    def depot(self, montant):
        if montant > 0:
            self.__solde += montant
            print(f"Dépôt de {montant} effectué. Nouveau solde : {self.__solde}")
        else:
            print("Le montant du dépôt doit être positif.")

    def retrait(self, montant):
        if 0 < montant <= self.__solde:
            self.__solde -= montant
            print(f"Retrait de {montant} effectué. Nouveau solde : {self.__solde}")
        else:
            print("Montant de retrait invalide ou solde insuffisant.")

# Utilisation de la classe CompteBancaire
compte_jean = CompteBancaire("Jean Dupont", 1000)

print(f"Titulaire : {compte_jean.titulaire}")
print(f"Solde initial : {compte_jean.solde}")  # Accès via le getter

compte_jean.solde = 1200  # Modification via le setter
print(f"Nouveau solde après dépôt (via setter) : {compte_jean.solde}")

compte_jean.solde = -50 # Tentative de solde négatif (setter)

compte_jean.depot(500)
compte_jean.retrait(200)
compte_jean.retrait(2000) # Tentative de retrait excessif

# Démonstration du deleter (optionnel)
# del compte_jean.solde
# try:
#     print(compte_jean.solde)
# except AttributeError as e:
#     print(e) 