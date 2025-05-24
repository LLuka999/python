def est_annee_bissextile(annee):
    """
    Vérifie si une année est bissextile.
    Une année est bissextile si elle est divisible par 4,
    sauf si elle est divisible par 100 mais pas par 400.
    """
    if not isinstance(annee, int) or annee <= 0:
        return "Veuillez entrer un entier positif pour l'année."
    
    if (annee % 4 == 0 and annee % 100 != 0) or (annee % 400 == 0):
        return f"{annee} est une année bissextile."
    else:
        return f"{annee} n'est pas une année bissextile."

if __name__ == "__main__":
    # Cas de test tiré du fichier YAML
    annee_test = 2024
    print(est_annee_bissextile(annee_test))

    # Autres cas de test
    print(est_annee_bissextile(2000))  # Bissextile
    print(est_annee_bissextile(1900))  # Non bissextile
    print(est_annee_bissextile(2023))  # Non bissextile
    print(est_annee_bissextile(0))      # Entrée invalide
    print(est_annee_bissextile(-5))     # Entrée invalide
    print(est_annee_bissextile("abc"))  # Entrée invalide
    
    # Demander à l'utilisateur de saisir une année
    # try:
    #     annee_utilisateur = int(input("Veuillez entrer une année : "))
    #     print(est_annee_bissextile(annee_utilisateur))
    # except ValueError:
    #     print("Entrée invalide. Veuillez entrer un nombre entier.") 