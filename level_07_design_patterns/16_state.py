"""
Design Pattern : State (État)

Permet à un objet de changer de comportement lorsque son état interne change.
"""
from abc import ABC, abstractmethod

class Etat(ABC):
    @abstractmethod
    def action(self, contexte):
        pass

class EtatRepos(Etat):
    def action(self, contexte):
        print("Le robot est au repos.")
        contexte.etat = EtatTravail()

class EtatTravail(Etat):
    def action(self, contexte):
        print("Le robot travaille.")
        contexte.etat = EtatRepos()

class Robot:
    def __init__(self):
        self.etat = EtatRepos()
    def faire_action(self):
        self.etat.action(self)

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du State ---")
    robot = Robot()
    for _ in range(4):
        robot.faire_action() 