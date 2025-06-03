"""
Design Pattern : Adapter (Adaptateur)

Permet à des interfaces incompatibles de travailler ensemble.
"""

class PriseFrancaise:
    def brancher(self):
        return "Appareil branché sur une prise française."

class PriseAnglaise:
    def plug_in(self):
        return "Device plugged into a UK socket."

# Adaptateur
class AdaptateurPriseUKtoFR:
    def __init__(self, prise_uk):
        self.prise_uk = prise_uk
    def brancher(self):
        return self.prise_uk.plug_in()

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration de l'Adapter ---")
    prise_fr = PriseFrancaise()
    print(prise_fr.brancher())

    prise_uk = PriseAnglaise()
    adaptateur = AdaptateurPriseUKtoFR(prise_uk)
    print(adaptateur.brancher()) 