"""
Design Pattern : Decorator (Décorateur)

Permet d'ajouter dynamiquement des fonctionnalités à un objet sans modifier sa structure.
"""

class Cafe:
    def cout(self):
        return 2
    def description(self):
        return "Café simple"

class DecorateurCafe:
    def __init__(self, cafe):
        self._cafe = cafe
    def cout(self):
        return self._cafe.cout()
    def description(self):
        return self._cafe.description()

class Lait(DecorateurCafe):
    def cout(self):
        return self._cafe.cout() + 0.5
    def description(self):
        return self._cafe.description() + ", lait"

class Chocolat(DecorateurCafe):
    def cout(self):
        return self._cafe.cout() + 0.7
    def description(self):
        return self._cafe.description() + ", chocolat"

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Decorator ---")
    boisson = Cafe()
    print(f"{boisson.description()} : {boisson.cout()}€")

    boisson = Lait(boisson)
    print(f"{boisson.description()} : {boisson.cout()}€")

    boisson = Chocolat(boisson)
    print(f"{boisson.description()} : {boisson.cout()}€") 