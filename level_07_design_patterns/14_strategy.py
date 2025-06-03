"""
Design Pattern : Strategy (Stratégie)

Permet de définir une famille d'algorithmes, de les encapsuler et de les rendre interchangeables dynamiquement.
"""
from abc import ABC, abstractmethod

class Strategie(ABC):
    @abstractmethod
    def executer(self, a, b):
        pass

class Addition(Strategie):
    def executer(self, a, b):
        return a + b

class Soustraction(Strategie):
    def executer(self, a, b):
        return a - b

class Contexte:
    def __init__(self, strategie: Strategie):
        self.strategie = strategie
    def calculer(self, a, b):
        return self.strategie.executer(a, b)

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration de la Strategy ---")
    contexte = Contexte(Addition())
    print(f"Addition : 5 + 3 = {contexte.calculer(5, 3)}")
    contexte.strategie = Soustraction()
    print(f"Soustraction : 5 - 3 = {contexte.calculer(5, 3)}") 