"""
Design Pattern : Flyweight (Poids-mouche)

Permet de partager le plus possible des données entre plusieurs objets pour limiter la consommation de mémoire.
"""

class Flyweight:
    def __init__(self, couleur):
        self.couleur = couleur
    def operation(self, forme):
        print(f"Forme '{forme}' de couleur partagée '{self.couleur}'")

class FlyweightFactory:
    def __init__(self):
        self._flyweights = {}
    def get_flyweight(self, couleur):
        if couleur not in self._flyweights:
            self._flyweights[couleur] = Flyweight(couleur)
        return self._flyweights[couleur]
    def count(self):
        return len(self._flyweights)

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Flyweight ---")
    factory = FlyweightFactory()
    couleurs = ["rouge", "bleu", "rouge", "vert", "bleu"]
    formes = ["cercle", "carré", "triangle", "cercle", "carré"]
    for couleur, forme in zip(couleurs, formes):
        flyweight = factory.get_flyweight(couleur)
        flyweight.operation(forme)
    print(f"Nombre d'objets Flyweight créés : {factory.count()}") 