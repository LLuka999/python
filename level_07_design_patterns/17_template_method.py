"""
Design Pattern : Template Method (Méthode Modèle)

Définit le squelette d'un algorithme dans une méthode, en laissant certaines étapes aux sous-classes.
"""
from abc import ABC, abstractmethod

class Recette(ABC):
    def preparer(self):
        self.etape1()
        self.etape2()
        self.etape3()
    @abstractmethod
    def etape1(self):
        pass
    @abstractmethod
    def etape2(self):
        pass
    def etape3(self):
        print("Étape finale commune : servir.")

class RecettePates(Recette):
    def etape1(self):
        print("Faire bouillir l'eau.")
    def etape2(self):
        print("Cuire les pâtes.")

class RecetteRiz(Recette):
    def etape1(self):
        print("Rincer le riz.")
    def etape2(self):
        print("Cuire le riz.")

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Template Method ---")
    print("Recette pâtes :")
    RecettePates().preparer()
    print("\nRecette riz :")
    RecetteRiz().preparer() 