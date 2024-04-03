mot = "Python"

print(f"Itération sur la chaîne '{mot}':")
for caractere in mot:
    print(f"Caractère: {caractere}")

print("\nItération avec index et caractère (enumerate):")
for index, caractere_enum in enumerate(mot):
    print(f"Index: {index}, Caractère: {caractere_enum}") 