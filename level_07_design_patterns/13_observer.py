"""
Design Pattern : Observer (Observateur)

Permet de notifier automatiquement un groupe d'objets dépendants lorsqu'un objet change d'état.
"""

class Sujet:
    def __init__(self):
        self._observateurs = []
        self._etat = None
    def attacher(self, observateur):
        self._observateurs.append(observateur)
    def detacher(self, observateur):
        self._observateurs.remove(observateur)
    def notifier(self):
        for obs in self._observateurs:
            obs.actualiser(self)
    def changer_etat(self, nouvel_etat):
        self._etat = nouvel_etat
        self.notifier()
    @property
    def etat(self):
        return self._etat

class Observateur:
    def __init__(self, nom):
        self.nom = nom
    def actualiser(self, sujet):
        print(f"{self.nom} a été notifié. Nouvel état : {sujet.etat}")

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration de l'Observer ---")
    sujet = Sujet()
    obs1 = Observateur("Observateur 1")
    obs2 = Observateur("Observateur 2")
    sujet.attacher(obs1)
    sujet.attacher(obs2)
    sujet.changer_etat("État A")
    sujet.changer_etat("État B")
    sujet.detacher(obs1)
    sujet.changer_etat("État C") 