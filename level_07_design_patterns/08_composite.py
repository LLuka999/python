"""
Design Pattern : Composite

Permet de composer des objets en structures arborescentes pour représenter des hiérarchies partie-tout.
Le Composite permet aux clients de traiter de manière uniforme les objets individuels et les compositions d'objets.
"""

from abc import ABC, abstractmethod

class Composant(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass

class Feuille(Composant):
    def __init__(self, nom):
        self.nom = nom
    def operation(self) -> str:
        return self.nom

class Composite(Composant):
    def __init__(self, nom):
        self.nom = nom
        self._enfants = []
    def ajouter(self, composant: Composant):
        self._enfants.append(composant)
    def operation(self) -> str:
        resultats = [enfant.operation() for enfant in self._enfants]
        return f"{self.nom}({', '.join(resultats)})"

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Composite ---")
    feuille1 = Feuille("Feuille A")
    feuille2 = Feuille("Feuille B")
    composite1 = Composite("Noeud 1")
    composite1.ajouter(feuille1)
    composite1.ajouter(feuille2)

    feuille3 = Feuille("Feuille C")
    composite2 = Composite("Noeud 2")
    composite2.ajouter(feuille3)
    composite2.ajouter(composite1)

    print(composite2.operation()) 