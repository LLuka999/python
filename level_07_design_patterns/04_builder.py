"""
Design Pattern : Builder (Constructeur)

Sépare la construction d'un objet complexe de sa représentation, de sorte que le même processus de construction puisse créer différentes représentations.
"""

from abc import ABC, abstractmethod

# --- Produit complexe ---
class Maison:
    def __init__(self):
        self.murs = None
        self.toit = None
        self.portes = None
        self.fenetres = None
        self.piscine = None

    def __str__(self):
        return (f"Maison avec : murs={self.murs}, toit={self.toit}, portes={self.portes}, "
                f"fenêtres={self.fenetres}, piscine={self.piscine}")

# --- Builder Abstrait ---
class MaisonBuilder(ABC):
    def __init__(self):
        self.maison = Maison()

    @abstractmethod
    def construire_murs(self):
        pass

    @abstractmethod
    def construire_toit(self):
        pass

    @abstractmethod
    def construire_portes(self):
        pass

    @abstractmethod
    def construire_fenetres(self):
        pass

    def get_maison(self):
        return self.maison

# --- Builders Concrets ---
class MaisonBoisBuilder(MaisonBuilder):
    def construire_murs(self):
        self.maison.murs = "murs en bois"
    def construire_toit(self):
        self.maison.toit = "toit en tuiles"
    def construire_portes(self):
        self.maison.portes = 2
    def construire_fenetres(self):
        self.maison.fenetres = 4

class MaisonLuxeBuilder(MaisonBuilder):
    def construire_murs(self):
        self.maison.murs = "murs en marbre"
    def construire_toit(self):
        self.maison.toit = "toit en ardoise"
    def construire_portes(self):
        self.maison.portes = 4
    def construire_fenetres(self):
        self.maison.fenetres = 10
    def construire_piscine(self):
        self.maison.piscine = True

# --- Directeur ---
class Directeur:
    def __init__(self, builder: MaisonBuilder):
        self._builder = builder

    def construire_maison(self):
        self._builder.construire_murs()
        self._builder.construire_toit()
        self._builder.construire_portes()
        self._builder.construire_fenetres()
        # Optionnel : piscine si le builder le propose
        if hasattr(self._builder, 'construire_piscine'):
            self._builder.construire_piscine()
        return self._builder.get_maison()

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Builder ---")
    builder_bois = MaisonBoisBuilder()
    directeur = Directeur(builder_bois)
    maison_bois = directeur.construire_maison()
    print(maison_bois)

    builder_luxe = MaisonLuxeBuilder()
    directeur = Directeur(builder_luxe)
    maison_luxe = directeur.construire_maison()
    print(maison_luxe) 