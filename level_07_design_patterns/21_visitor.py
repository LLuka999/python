"""
Design Pattern : Visitor (Visiteur)

Permet de séparer un algorithme de la structure de l'objet sur lequel il opère.
"""
from abc import ABC, abstractmethod

class Element(ABC):
    @abstractmethod
    def accepter(self, visiteur):
        pass

class ElementA(Element):
    def accepter(self, visiteur):
        visiteur.visiter_element_a(self)
    def operation_a(self):
        return "Opération spécifique à ElementA"

class ElementB(Element):
    def accepter(self, visiteur):
        visiteur.visiter_element_b(self)
    def operation_b(self):
        return "Opération spécifique à ElementB"

class Visiteur(ABC):
    @abstractmethod
    def visiter_element_a(self, element):
        pass
    @abstractmethod
    def visiter_element_b(self, element):
        pass

class VisiteurConcret(Visiteur):
    def visiter_element_a(self, element):
        print(f"Visiteur : {element.operation_a()}")
    def visiter_element_b(self, element):
        print(f"Visiteur : {element.operation_b()}")

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Visitor ---")
    elements = [ElementA(), ElementB()]
    visiteur = VisiteurConcret()
    for elem in elements:
        elem.accepter(visiteur) 