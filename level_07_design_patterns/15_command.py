"""
Design Pattern : Command (Commande)

Permet d'encapsuler une requête comme un objet, séparant ainsi l'émetteur du récepteur.
"""

class Lumiere:
    def allumer(self):
        print("Lumière allumée.")
    def eteindre(self):
        print("Lumière éteinte.")

class Commande:
    def executer(self):
        pass

class AllumerLumiereCommande(Commande):
    def __init__(self, lumiere):
        self.lumiere = lumiere
    def executer(self):
        self.lumiere.allumer()

class EteindreLumiereCommande(Commande):
    def __init__(self, lumiere):
        self.lumiere = lumiere
    def executer(self):
        self.lumiere.eteindre()

class Telecommande:
    def soumettre(self, commande):
        commande.executer()

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Command ---")
    lumiere = Lumiere()
    allumer = AllumerLumiereCommande(lumiere)
    eteindre = EteindreLumiereCommande(lumiere)
    telecommande = Telecommande()
    telecommande.soumettre(allumer)
    telecommande.soumettre(eteindre) 