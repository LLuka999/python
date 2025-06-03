"""
Design Pattern : Bridge (Pont)

Sépare l'abstraction de son implémentation afin qu'elles puissent évoluer indépendamment.
"""
from abc import ABC, abstractmethod

# --- Implémentation ---
class Couleur(ABC):
    @abstractmethod
    def appliquer_couleur(self) -> str:
        pass

class Rouge(Couleur):
    def appliquer_couleur(self) -> str:
        return "rouge"

class Bleu(Couleur):
    def appliquer_couleur(self) -> str:
        return "bleu"

# --- Abstraction ---
class Forme(ABC):
    def __init__(self, couleur: Couleur):
        self.couleur = couleur
    @abstractmethod
    def dessiner(self) -> str:
        pass

class Cercle(Forme):
    def dessiner(self) -> str:
        return f"Cercle de couleur {self.couleur.appliquer_couleur()}"

class Carre(Forme):
    def dessiner(self) -> str:
        return f"Carré de couleur {self.couleur.appliquer_couleur()}"

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Bridge ---")
    rouge = Rouge()
    bleu = Bleu()
    cercle_rouge = Cercle(rouge)
    carre_bleu = Carre(bleu)
    print(cercle_rouge.dessiner())
    print(carre_bleu.dessiner()) 