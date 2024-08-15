"""
Concepts OOP Avancés : Héritage, Polymorphisme, Interfaces (ABCs)
"""

from abc import ABC, abstractmethod

# --- Héritage et Polymorphisme ---

class Animal(ABC):  # Animal devient une classe de base abstraite
    def __init__(self, nom):
        self.nom = nom

    @abstractmethod
    def crier(self):
        """Méthode abstraite que les sous-classes doivent implémenter."""
        pass

    def manger(self):
        print(f"{self.nom} mange.")

class Chien(Animal):
    def crier(self):
        return f"{self.nom} aboie : Ouaf ouaf !"

    def rapporter_balle(self):
        print(f"{self.nom} rapporte la balle.")

class Chat(Animal):
    def crier(self):
        return f"{self.nom} miaule : Miaou !"

    def chasser_souris(self):
        print(f"{self.nom} chasse une souris.")

# Démonstration du polymorphisme
animaux = [
    Chien("Médor"),
    Chat("Félix"),
    Chien("Rex")
]

print("\n--- Polymorphisme avec la méthode crier ---")
for animal in animaux:
    print(animal.crier()) # Appelle la méthode crier() spécifique à chaque type d'animal
    animal.manger()       # Appelle la méthode manger() de la classe de base Animal

# On peut vérifier le type et appeler des méthodes spécifiques si besoin
print("\n--- Actions spécifiques aux types ---")
for animal in animaux:
    if isinstance(animal, Chien):
        animal.rapporter_balle()
    elif isinstance(animal, Chat):
        animal.chasser_souris()

# Tentative d'instancier une classe abstraite (devrait échouer)
# try:
#     animal_abstrait = Animal("Fantome")
# except TypeError as e:
#     print(f"\nErreur attendue : {e}")

# --- Interfaces (Abstract Base Classes) ---

class Forme(ABC):
    @abstractmethod
    def aire(self):
        pass

    @abstractmethod
    def perimetre(self):
        pass

class Cercle(Forme):
    def __init__(self, rayon):
        self.rayon = rayon

    def aire(self):
        import math
        return math.pi * self.rayon ** 2

    def perimetre(self):
        import math
        return 2 * math.pi * self.rayon

class Rectangle(Forme):
    def __init__(self, longueur, largeur):
        self.longueur = longueur
        self.largeur = largeur

    def aire(self):
        return self.longueur * self.largeur

    def perimetre(self):
        return 2 * (self.longueur + self.largeur)

# Classe qui n'implémente pas toutes les méthodes abstraites (devrait échouer à l'instanciation)
# class TriangleIncomplet(Forme):
#     def __init__(self, base):
#         self.base = base
#     # La méthode perimetre() n'est pas implémentée
#     def aire(self):
#         return 0 # Placeholder

# try:
#     triangle_fail = TriangleIncomplet(5)
# except TypeError as e:
#     print(f"\nErreur attendue lors de l'instanciation de TriangleIncomplet : {e}")


formes = [
    Cercle(5),
    Rectangle(4, 6)
]

print("\n--- Polymorphisme avec les formes (via l'interface Forme) ---")
for forme_geom in formes:
    print(f"Type: {type(forme_geom).__name__}, Aire: {forme_geom.aire():.2f}, Perimetre: {forme_geom.perimetre():.2f}")

print("\nFin des exemples OOP avancés.") 