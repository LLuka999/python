import random

nombre_secret = random.randint(1, 100)
tentatives = 0

print("Jeu: Devinez le nombre !")
print("Je pense à un nombre entre 1 et 100.")

while True:
    proposition_str = input("Votre proposition: ")
    tentatives += 1

    try:
        proposition = int(proposition_str)
        if proposition < 1 or proposition > 100:
            print("Veuillez entrer un nombre entre 1 et 100.")
            continue

        if proposition < nombre_secret:
            print("Trop petit !")
        elif proposition > nombre_secret:
            print("Trop grand !")
        else:
            print(f"Bravo ! Vous avez trouvé le nombre {nombre_secret} en {tentatives} tentatives.")
            break
    except ValueError:
        print(f"'{proposition_str}' n'est pas un nombre valide. Essayez encore.")

print("Fin du jeu.") 