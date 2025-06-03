"""
Design Pattern : Factory Method (Méthode de Fabrique)

Définit une interface pour créer un objet, mais laisse les sous-classes décider quelle classe instancier.
Le Factory Method permet à une classe de déléguer l'instanciation à des sous-classes.
"""

from abc import ABC, abstractmethod

# --- Produit (Interface et Implémentations Concrètes) ---

class Produit(ABC):
    """Interface pour les produits que la méthode de fabrique va créer."""
    @abstractmethod
    def operation(self) -> str:
        pass

class ProduitConcretA(Produit):
    """Implémentation concrète d'un produit."""
    def operation(self) -> str:
        return "{Résultat du ProduitConcretA}"

class ProduitConcretB(Produit):
    """Autre implémentation concrète d'un produit."""
    def operation(self) -> str:
        return "{Résultat du ProduitConcretB}"

# --- Créateur (Interface et Implémentations Concrètes) ---

class Createur(ABC):
    """
    Déclare la méthode de fabrique, qui retourne un objet de type Produit.
    Peut également définir une implémentation par défaut de la méthode de fabrique.
    Contient généralement du code métier qui s'appuie sur le produit.
    """

    @abstractmethod
    def factory_method(self) -> Produit:
        """La méthode de fabrique que les sous-classes doivent implémenter."""
        pass

    def une_operation(self) -> str:
        """
        Code métier qui utilise le produit créé par la méthode de fabrique.
        Le Créateur ne connaît pas le type concret du produit qu'il utilise.
        """
        produit = self.factory_method()
        resultat = f"Createur: Le même code créateur a fonctionné avec {produit.operation()}"
        return resultat

class CreateurConcretA(Createur):
    """Sous-classe qui implémente la méthode de fabrique pour créer un ProduitConcretA."""
    def factory_method(self) -> Produit:
        return ProduitConcretA()

class CreateurConcretB(Createur):
    """Sous-classe qui implémente la méthode de fabrique pour créer un ProduitConcretB."""
    def factory_method(self) -> Produit:
        return ProduitConcretB()

# --- Utilisation ---

def client_code(createur: Createur):
    """
    Le code client travaille avec une instance d'un créateur concret,
    bien qu'à travers son interface de base (Createur).
    Tant que le client continue de travailler avec le créateur via l'interface de base,
    vous pouvez lui passer n'importe quelle sous-classe de créateur.
    """
    print(f"Client: Je ne connais pas la classe du créateur, mais cela fonctionne toujours.\n"
          f"{createur.une_operation()}", end="")

if __name__ == "__main__":
    print("--- Démonstration du Factory Method ---")

    print("App lancement avec CreateurConcretA.")
    client_code(CreateurConcretA())
    print("\n")

    print("App lancement avec CreateurConcretB.")
    client_code(CreateurConcretB())
    print("\n") 