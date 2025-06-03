"""
Design Pattern : Chain of Responsibility (Chaîne de responsabilité)

Permet de passer une requête le long d'une chaîne de gestionnaires jusqu'à ce qu'un d'eux la traite.
"""

class Handler:
    def __init__(self, successeur=None):
        self.successeur = successeur
    def handle(self, request):
        if self.successeur:
            return self.successeur.handle(request)
        return None

class HandlerChiffre(Handler):
    def handle(self, request):
        if request.isdigit():
            print(f"HandlerChiffre traite la requête : {request}")
        else:
            super().handle(request)

class HandlerMajuscule(Handler):
    def handle(self, request):
        if request.isupper():
            print(f"HandlerMajuscule traite la requête : {request}")
        else:
            super().handle(request)

class HandlerDefault(Handler):
    def handle(self, request):
        print(f"Handler par défaut : rien à faire pour '{request}'")

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration de la Chain of Responsibility ---")
    chaine = HandlerChiffre(HandlerMajuscule(HandlerDefault()))
    tests = ["123", "ABC", "abc", "42"]
    for t in tests:
        chaine.handle(t) 