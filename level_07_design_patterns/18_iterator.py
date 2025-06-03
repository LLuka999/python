"""
Design Pattern : Iterator (Itérateur)

Permet de parcourir les éléments d'une collection sans exposer sa représentation sous-jacente.
"""

class Collection:
    def __init__(self):
        self._items = []
    def ajouter(self, item):
        self._items.append(item)
    def __iter__(self):
        return Iterateur(self)

class Iterateur:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0
    def __next__(self):
        if self._index < len(self._collection._items):
            item = self._collection._items[self._index]
            self._index += 1
            return item
        raise StopIteration
    def __iter__(self):
        return self

# --- Utilisation ---
if __name__ == "__main__":
    print("--- Démonstration de l'Iterator ---")
    collection = Collection()
    collection.ajouter("A")
    collection.ajouter("B")
    collection.ajouter("C")
    for item in collection:
        print(f"Élément : {item}") 