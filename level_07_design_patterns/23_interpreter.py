"""
Design Pattern : Interpreter (Interpréteur)

Permet de définir une grammaire pour un langage et d'interpréter des phrases de ce langage.
"""
from abc import ABC, abstractmethod

class Expression(ABC):
    @abstractmethod
    def interpreter(self, contexte):
        pass

class ExpressionNombre(Expression):
    def __init__(self, nombre):
        self.nombre = nombre
    def interpreter(self, contexte):
        return self.nombre

class ExpressionAddition(Expression):
    def __init__(self, gauche, droite):
        self.gauche = gauche
        self.droite = droite
    def interpreter(self, contexte):
        return self.gauche.interpreter(contexte) + self.droite.interpreter(contexte)

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration de l'Interpreter ---")
    # Interprète l'expression : (5 + 10) + 20
    expr = ExpressionAddition(ExpressionAddition(ExpressionNombre(5), ExpressionNombre(10)), ExpressionNombre(20))
    print(f"Résultat de l'expression : {expr.interpreter({})}") 