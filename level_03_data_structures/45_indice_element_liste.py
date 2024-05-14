fruits = ['pomme', 'banane', 'cerise']
element = 'banane'
print(f"Liste : {fruits}")
try:
    indice = fruits.index(element)
    print(f"L'indice de '{element}' est {indice}.")
except ValueError:
    print(f"L'élément '{element}' n'est pas dans la liste.") 