chaine_originale = "Python"

# Méthode avec slicing (la plus pythonique)
chaine_inverse_slicing = chaine_originale[::-1]
print(f"Chaîne originale: '{chaine_originale}'")
print(f"Inverse (avec slicing): '{chaine_inverse_slicing}'")

# Méthode avec une boucle (plus explicite)
chaine_inverse_boucle = ""
for caractere in chaine_originale:
    chaine_inverse_boucle = caractere + chaine_inverse_boucle # Ajoute au début
print(f"Inverse (avec boucle): '{chaine_inverse_boucle}'")

# Test avec une chaîne vide ou un palindrome
# palindrome = "radar"
# print(f"\nTest avec '{palindrome}': '{palindrome[::-1]}'") # Devrait être 'radar'
# chaine_vide = ""
# print(f"Test avec chaîne vide: '{chaine_vide[::-1]}'") # Devrait être '' 