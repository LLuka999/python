"""
Design Pattern : Proxy

Fournit un substitut ou un représentant d'un autre objet pour contrôler l'accès à cet objet.
"""

class Image:
    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier
        self.charger_image()
    def charger_image(self):
        print(f"Chargement de l'image {self.nom_fichier}...")
    def afficher(self):
        print(f"Affichage de l'image {self.nom_fichier}.")

class ProxyImage:
    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier
        self._image = None
    def afficher(self):
        if self._image is None:
            self._image = Image(self.nom_fichier)
        self._image.afficher()

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Proxy ---")
    image = ProxyImage("photo.png")
    print("Première demande d'affichage :")
    image.afficher()
    print("\nSeconde demande d'affichage :")
    image.afficher() 