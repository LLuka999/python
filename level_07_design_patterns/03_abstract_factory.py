"""
Design Pattern : Abstract Factory (Fabrique Abstraite)

Fournit une interface pour créer des familles d'objets liés ou dépendants sans spécifier leurs classes concrètes.
"""

from abc import ABC, abstractmethod

# --- Interfaces des produits ---
class Chaise(ABC):
    @abstractmethod
    def s_asseoir(self) -> str:
        pass

class Canape(ABC):
    @abstractmethod
    def s_allonger(self) -> str:
        pass

# --- Produits Concrets ---
class ChaiseModerne(Chaise):
    def s_asseoir(self) -> str:
        return "On s'assoit sur une chaise moderne."

class ChaiseVictorien(Chaise):
    def s_asseoir(self) -> str:
        return "On s'assoit sur une chaise de style victorien."

class CanapeModerne(Canape):
    def s_allonger(self) -> str:
        return "On s'allonge sur un canapé moderne."

class CanapeVictorien(Canape):
    def s_allonger(self) -> str:
        return "On s'allonge sur un canapé de style victorien."

# --- Fabrique Abstraite ---
class FabriqueMeubles(ABC):
    @abstractmethod
    def creer_chaise(self) -> Chaise:
        pass

    @abstractmethod
    def creer_canape(self) -> Canape:
        pass

# --- Fabriques Concrètes ---
class FabriqueModerne(FabriqueMeubles):
    def creer_chaise(self) -> Chaise:
        return ChaiseModerne()
    def creer_canape(self) -> Canape:
        return CanapeModerne()

class FabriqueVictorienne(FabriqueMeubles):
    def creer_chaise(self) -> Chaise:
        return ChaiseVictorien()
    def creer_canape(self) -> Canape:
        return CanapeVictorien()

# --- Utilisation ---
def client_code(fabrique: FabriqueMeubles):
    chaise = fabrique.creer_chaise()
    canape = fabrique.creer_canape()
    print(chaise.s_asseoir())
    print(canape.s_allonger())

if __name__ == "__main__":
    print("--- Démonstration de l'Abstract Factory ---")
    print("Meubles modernes :")
    client_code(FabriqueModerne())
    print("\nMeubles victoriens :")
    client_code(FabriqueVictorienne()) 