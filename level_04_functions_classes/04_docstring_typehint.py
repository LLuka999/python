"""
Docstrings et annotations de type (type hints)
- Docstring : documentation intégrée
- Type hints : annotation des types d'arguments et de retour
"""

def multiplier(a: int, b: int) -> int:
    """
    Multiplie deux entiers et retourne le résultat.
    :param a: premier entier
    :param b: second entier
    :return: produit de a et b
    """
    return a * b


def dire_age(nom: str, age: int = 18) -> None:
    """
    Affiche l'âge d'une personne.
    :param nom: prénom de la personne
    :param age: âge (par défaut 18)
    """
    print(f"{nom} a {age} ans.")

# --- Exemples d'utilisation ---
print(multiplier(6, 7))
dire_age("Sophie", 25)
dire_age("Paul") 