prix_ht = 100.0
taux_tva_decimal = 0.20  # 20% de TVA

if prix_ht < 0 or taux_tva_decimal < 0:
    print("Erreur: Le prix HT et le taux de TVA doivent être positifs.")
else:
    montant_tva = prix_ht * taux_tva_decimal
    prix_ttc = prix_ht + montant_tva

    # Affichage formaté
    print(f"Prix HT: {prix_ht:.2f}")
    print(f"Taux TVA: {taux_tva_decimal*100:.2f}%")
    print(f"Montant TVA: {montant_tva:.2f}")
    print(f"Prix TTC: {prix_ttc:.2f}")

# Test avec une valeur négative
# prix_ht_test = -50
# if prix_ht_test < 0 or taux_tva_decimal < 0:
#     print("Erreur test (prix négatif): Le prix HT et le taux de TVA doivent être positifs.") 