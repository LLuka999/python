"""
Design Pattern : Singleton

Permet de s'assurer qu'une classe n'a qu'une seule instance et fournit un point d'accès global à cette instance.
"""

class Singleton:
    __instance = None

    @staticmethod
    def get_instance():
        """Méthode statique pour accéder à l'instance unique."""
        if Singleton.__instance is None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        """Constructeur privé pour empêcher l'instanciation directe."""
        if Singleton.__instance is not None:
            raise Exception("Cette classe est un Singleton ! Utilisez get_instance() pour obtenir l'objet.")
        else:
            Singleton.__instance = self
            self.data = "Donnée initiale du Singleton"

    def __str__(self):
        return f"Objet Singleton avec data: '{self.data}' (id: {id(self)})"

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration du Singleton ---")

    s1 = Singleton.get_instance()
    print(f"s1 : {s1}")

    s2 = Singleton.get_instance()
    print(f"s2 : {s2}")

    print(f"s1 et s2 sont la même instance : {s1 is s2}")

    s1.data = "Donnée modifiée par s1"
    print(f"s1 après modification : {s1}")
    print(f"s2 après modification de s1.data : {s2}") # s2 voit aussi la modification

    # Tentative d'instanciation directe (devrait lever une exception)
    try:
        print("\nTentative d'instanciation directe...")
        s3 = Singleton()
        print(s3)
    except Exception as e:
        print(f"Erreur : {e}")

    print("\nAutre façon de vérifier l'unicité :")
    s3 = Singleton.get_instance()
    s3.valeur_partagee = 100

    s4 = Singleton.get_instance()
    if hasattr(s4, 'valeur_partagee'):
        print(f"s4 a accès à valeur_partagee ({s4.valeur_partagee}) définie via s3, car c'est la même instance.")
    else:
        print("s4 n'a pas accès à valeur_partagee. Le Singleton ne fonctionne pas comme prévu.") 