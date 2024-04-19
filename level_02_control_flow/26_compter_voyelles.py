chaine_utilisateur = "Bonjour le Monde"
voyelles = "aeiouAEIOUàáâäéèêëíìîïóòôöúùûüÀÁÂÄÉÈÊËÍÌÎÏÓÒÔÖÚÙÛÜ"

compteur_voyelles = 0

print(f"Analyse de la chaîne: '{chaine_utilisateur}'")
for caractere in chaine_utilisateur:
    if caractere in voyelles:
        compteur_voyelles += 1

print(f"La chaîne '{chaine_utilisateur}' contient {compteur_voyelles} voyelles.")

# Variante: convertir la chaîne en minuscules d'abord
chaine_minuscules = chaine_utilisateur.lower()
voyelles_minuscules = "aeiouàáâäéèêëíìîïóòôöúùûü"
compteur_voyelles_variante = 0
for caractere in chaine_minuscules:
    if caractere in voyelles_minuscules:
        compteur_voyelles_variante +=1
print(f"(Variante avec conversion en minuscules: {compteur_voyelles_variante} voyelles)") 