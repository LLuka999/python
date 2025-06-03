"""
Design Pattern : Facade (Façade)

Fournit une interface unifiée pour un ensemble d'interfaces dans un sous-système.
La façade définit une interface de haut niveau qui rend le sous-système plus facile à utiliser.
"""

class SystemeAudio:
    def allumer(self):
        print("Système audio allumé.")
    def regler_volume(self, niveau):
        print(f"Volume réglé à {niveau}.")

class SystemeLumiere:
    def allumer(self):
        print("Lumières allumées.")
    def tamiser(self):
        print("Lumières tamisées.")

class HomeCinemaFacade:
    def __init__(self):
        self.audio = SystemeAudio()
        self.lumiere = SystemeLumiere()
    def regarder_film(self):
        print("Préparation du home cinéma...")
        self.lumiere.allumer()
        self.lumiere.tamiser()
        self.audio.allumer()
        self.audio.regler_volume(20)
        print("Le film commence !")

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration de la Facade ---")
    home_cinema = HomeCinemaFacade()
    home_cinema.regarder_film() 