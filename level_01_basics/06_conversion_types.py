nombre_str = "123"
print(f"Chaîne originale: {nombre_str}, Type: {type(nombre_str)}")

nombre_int = int(nombre_str)
print(f"Convertie en entier: {nombre_int}, Type: {type(nombre_int)}")

flottant_val = 45.67
print(f"Flottant original: {flottant_val}, Type: {type(flottant_val)}")

flottant_en_int = int(flottant_val)
print(f"Converti en entier: {flottant_en_int}, Type: {type(flottant_en_int)}")

int_en_chaine = str(flottant_en_int)
print(f"Entier converti en chaîne: {int_en_chaine}, Type: {type(int_en_chaine)}") 