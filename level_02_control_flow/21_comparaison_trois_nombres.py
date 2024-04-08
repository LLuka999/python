num1 = 10
num2 = 25
num3 = 15

print(f"Nombres donnés: {num1}, {num2}, {num3}")

if (num1 >= num2) and (num1 >= num3):
    plus_grand = num1
elif (num2 >= num1) and (num2 >= num3):
    plus_grand = num2
else:
    plus_grand = num3

print(f"Le plus grand nombre est {plus_grand}.")

# Test avec d'autres combinaisons
# num1, num2, num3 = 30, 10, 20  # Devrait afficher 30
# num1, num2, num3 = 5, 5, 2    # Devrait afficher 5 