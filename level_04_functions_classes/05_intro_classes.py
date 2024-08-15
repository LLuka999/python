"""
Introduction à la programmation orientée objet (POO)
- Définition d'une classe
- Constructeur (__init__)
- Attributs d'instance
- Méthode d'instance
"""

class Chien:
    def __init__(self, nom, age):
        self.nom = nom
        self.age = age

    def aboyer(self):
        print(f"{self.nom} aboie : Wouf !")

# --- Exemples d'utilisation ---
medor = Chien("Médor", 4)
print(f"Nom : {medor.nom}, Âge : {medor.age} ans")
medor.aboyer() 