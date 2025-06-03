"""
Design Pattern : Mediator (Médiateur)

Permet de réduire les dépendances entre les objets en les faisant communiquer via un objet médiateur.
"""

class Mediator:
    def __init__(self):
        self.utilisateurs = []
    def enregistrer(self, utilisateur):
        self.utilisateurs.append(utilisateur)
        utilisateur.mediator = self
    def envoyer(self, message, expediteur):
        for utilisateur in self.utilisateurs:
            if utilisateur != expediteur:
                utilisateur.recevoir(message)

class Utilisateur:
    def __init__(self, nom):
        self.nom = nom
        self.mediator = None
    def envoyer(self, message):
        print(f"{self.nom} envoie : {message}")
        self.mediator.envoyer(message, self)
    def recevoir(self, message):
        print(f"{self.nom} reçoit : {message}")

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Mediator ---")
    mediator = Mediator()
    alice = Utilisateur("Alice")
    bob = Utilisateur("Bob")
    charlie = Utilisateur("Charlie")
    mediator.enregistrer(alice)
    mediator.enregistrer(bob)
    mediator.enregistrer(charlie)
    alice.envoyer("Bonjour à tous !")
    bob.envoyer("Salut Alice !") 