"""
Classes avancées en Python
- Méthode spéciale __str__
- Méthode de classe
- Méthode statique
- Héritage simple
"""

class Animal:
    def __init__(self, nom):
        self.nom = nom

    def parler(self):
        print(f"{self.nom} fait un bruit.")

    def __str__(self):
        return f"Animal : {self.nom}"

    @classmethod
    def espece(cls):
        return cls.__name__

    @staticmethod
    def infos_generales():
        print("Les animaux sont des êtres vivants.")

class Chat(Animal):
    def parler(self):
        print(f"{self.nom} miaule.")

# --- Exemples d'utilisation ---
tigre = Chat("Tigrou")
tigre.parler()
print(tigre)
print(Chat.espece())
Animal.infos_generales() 