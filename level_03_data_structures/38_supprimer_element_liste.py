ma_liste = [1, 2, 3, 4]
print(f"Liste avant suppression : {ma_liste}")
try:
    ma_liste.remove(3)
    print(f"Liste après suppression de 3 : {ma_liste}")
except ValueError:
    print("L'élément 3 n'est pas dans la liste.") 