chaine_test = "radar" # Exemple de palindrome
chaine_test_non_palindrome = "Python"

def est_palindrome(s):
    # Optionnel: prétraitement pour ignorer la casse et les espaces
    # s_preparee = "".join(s.lower().split()) 
    # return s_preparee == s_preparee[::-1]
    return s == s[::-1] # Version simple

print(f"Analyse de '{chaine_test}':")
if est_palindrome(chaine_test):
    print(f"'{chaine_test}' est un palindrome.")
else:
    print(f"'{chaine_test}' n'est pas un palindrome.")

print(f"\nAnalyse de '{chaine_test_non_palindrome}':")
if est_palindrome(chaine_test_non_palindrome):
    print(f"'{chaine_test_non_palindrome}' est un palindrome.")
else:
    print(f"'{chaine_test_non_palindrome}' n'est pas un palindrome.")

# Test avec casse et espaces (nécessiterait le prétraitement commenté)
# chaine_complexe = "Engage le jeu que je le gagne"
# print(f"\nAnalyse de '{chaine_complexe}' (avec prétraitement idéal):")
# if est_palindrome(chaine_complexe): # Ne fonctionnera qu'avec le prétraitement actif
#     print(f"'{chaine_complexe}' est un palindrome.")
# else:
#     print(f"'{chaine_complexe}' n'est pas un palindrome.") 