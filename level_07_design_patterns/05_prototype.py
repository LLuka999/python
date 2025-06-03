"""
Design Pattern : Prototype

Permet de créer de nouveaux objets en copiant un prototype existant, au lieu d'instancier une nouvelle classe.
Utile pour éviter le coût de création d'un objet complexe.
"""
import copy

class Prototype:
    def clone(self):
        return copy.deepcopy(self)

class Robot(Prototype):
    def __init__(self, nom, puissance, outils=None):
        self.nom = nom
        self.puissance = puissance
        self.outils = outils or []
    def __str__(self):
        return f"Robot(nom={self.nom}, puissance={self.puissance}, outils={self.outils})"

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Prototype ---")
    robot_original = Robot("R2D2", 100, ["tournevis", "clé"])
    print(f"Original : {robot_original}")

    robot_clone = robot_original.clone()
    robot_clone.nom = "C3PO"
    robot_clone.outils.append("marteau")
    print(f"Clone modifié : {robot_clone}")
    print(f"Original après modification du clone : {robot_original}") 