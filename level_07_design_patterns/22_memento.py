"""
Design Pattern : Memento (Mémento)

Permet de capturer et de restaurer l'état interne d'un objet sans violer l'encapsulation.
"""

class Memento:
    def __init__(self, etat):
        self._etat = etat
    def get_etat(self):
        return self._etat

class Origine:
    def __init__(self):
        self._etat = ""
    def set_etat(self, etat):
        self._etat = etat
    def get_etat(self):
        return self._etat
    def sauvegarder(self):
        return Memento(self._etat)
    def restaurer(self, memento):
        self._etat = memento.get_etat()

class Gardien:
    def __init__(self):
        self._mementos = []
    def ajouter(self, memento):
        self._mementos.append(memento)
    def get(self, index):
        return self._mementos[index]

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Memento ---")
    origine = Origine()
    gardien = Gardien()
    origine.set_etat("État #1")
    gardien.ajouter(origine.sauvegarder())
    origine.set_etat("État #2")
    gardien.ajouter(origine.sauvegarder())
    origine.set_etat("État #3")
    print(f"État courant : {origine.get_etat()}")
    origine.restaurer(gardien.get(0))
    print(f"État restauré : {origine.get_etat()}") 