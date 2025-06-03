#!/usr/bin/env python3
"""
💰 Calculatrice Financière - Méthode Markova
============================================

Une calculatrice financière complète pour :
- Calculs d'intérêts composés
- Amortissement de prêts
- Planification d'épargne
- Comparaison d'investissements
- Calculs de rentabilité

Auteur: Méthode Markova
Niveau: 06 - Mini-projets concrets
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json


@dataclass
class LoanPayment:
    """Représente un paiement d'emprunt."""
    numero: int
    capital: float
    interet: float
    paiement_total: float
    solde_restant: float


@dataclass
class InvestmentResult:
    """Résultat d'un calcul d'investissement."""
    montant_initial: float
    montant_final: float
    gain_total: float
    rendement_pct: float
    duree_annees: float


class FinanceCalculator:
    """Calculatrice financière principale."""
    
    @staticmethod
    def interet_compose(capital: float, taux: float, duree: int, 
                       freq_capitalisation: int = 1, versements: float = 0) -> InvestmentResult:
        """
        Calcule les intérêts composés.
        
        Args:
            capital: Capital initial
            taux: Taux d'intérêt annuel (en %)
            duree: Durée en années
            freq_capitalisation: Fréquence de capitalisation par an
            versements: Versements réguliers annuels
            
        Returns:
            Résultat de l'investissement
        """
        taux_decimal = taux / 100
        
        if versements == 0:
            # Intérêts composés simples
            montant_final = capital * (1 + taux_decimal / freq_capitalisation) ** (freq_capitalisation * duree)
        else:
            # Avec versements réguliers (rente)
            if taux_decimal == 0:
                montant_final = capital + (versements * duree)
            else:
                # Formule de la valeur future d'une annuité
                facteur = (1 + taux_decimal / freq_capitalisation) ** (freq_capitalisation * duree)
                montant_final = capital * facteur
                
                # Ajout des versements avec intérêts
                taux_periode = taux_decimal / freq_capitalisation
                nb_versements = freq_capitalisation * duree
                versement_periode = versements / freq_capitalisation
                
                if taux_periode != 0:
                    valeur_versements = versement_periode * ((facteur - 1) / taux_periode)
                    montant_final += valeur_versements
                else:
                    montant_final += versements * duree
        
        gain_total = montant_final - capital - (versements * duree)
        rendement_pct = (gain_total / (capital + versements * duree)) * 100 if capital + versements * duree > 0 else 0
        
        return InvestmentResult(
            montant_initial=capital,
            montant_final=montant_final,
            gain_total=gain_total,
            rendement_pct=rendement_pct,
            duree_annees=duree
        )
    
    @staticmethod
    def calcul_pret(montant: float, taux: float, duree_mois: int) -> Tuple[float, List[LoanPayment]]:
        """
        Calcule l'amortissement d'un prêt.
        
        Args:
            montant: Montant du prêt
            taux: Taux d'intérêt annuel (en %)
            duree_mois: Durée en mois
            
        Returns:
            Tuple (mensualité, tableau d'amortissement)
        """
        taux_mensuel = (taux / 100) / 12
        
        if taux_mensuel == 0:
            mensualite = montant / duree_mois
        else:
            # Formule de calcul de mensualité
            mensualite = montant * (taux_mensuel * (1 + taux_mensuel) ** duree_mois) / \
                        ((1 + taux_mensuel) ** duree_mois - 1)
        
        # Tableau d'amortissement
        tableau = []
        solde = montant
        
        for mois in range(1, duree_mois + 1):
            interet_mois = solde * taux_mensuel
            capital_mois = mensualite - interet_mois
            solde -= capital_mois
            
            # Ajustement pour le dernier paiement
            if mois == duree_mois and solde != 0:
                capital_mois += solde
                mensualite = capital_mois + interet_mois
                solde = 0
            
            tableau.append(LoanPayment(
                numero=mois,
                capital=capital_mois,
                interet=interet_mois,
                paiement_total=mensualite,
                solde_restant=max(0, solde)
            ))
        
        return mensualite, tableau
    
    @staticmethod
    def objectif_epargne(objectif: float, duree_annees: int, taux: float = 0) -> Dict[str, float]:
        """
        Calcule l'épargne nécessaire pour atteindre un objectif.
        
        Args:
            objectif: Montant objectif
            duree_annees: Durée en années
            taux: Taux de rendement annuel (en %)
            
        Returns:
            Dictionnaire avec les résultats
        """
        taux_decimal = taux / 100
        
        if taux_decimal == 0:
            # Sans intérêts
            epargne_mensuelle = objectif / (duree_annees * 12)
            epargne_annuelle = objectif / duree_annees
        else:
            # Avec intérêts composés
            facteur = (1 + taux_decimal) ** duree_annees
            
            # Épargne en une fois (valeur actuelle)
            epargne_unique = objectif / facteur
            
            # Épargne mensuelle (rente)
            taux_mensuel = taux_decimal / 12
            nb_mois = duree_annees * 12
            facteur_mensuel = (1 + taux_mensuel) ** nb_mois
            epargne_mensuelle = objectif * taux_mensuel / (facteur_mensuel - 1)
            epargne_annuelle = epargne_mensuelle * 12
        
        return {
            "objectif": objectif,
            "duree_annees": duree_annees,
            "taux": taux,
            "epargne_mensuelle": epargne_mensuelle,
            "epargne_annuelle": epargne_annuelle,
            "epargne_unique": epargne_unique if taux_decimal > 0 else objectif,
            "total_verse": epargne_mensuelle * 12 * duree_annees,
            "interets_gagnes": objectif - (epargne_mensuelle * 12 * duree_annees)
        }
    
    @staticmethod
    def comparaison_investissements(scenarios: List[Dict]) -> List[Dict]:
        """
        Compare plusieurs scénarios d'investissement.
        
        Args:
            scenarios: Liste de scénarios avec capital, taux, durée
            
        Returns:
            Liste des résultats comparés
        """
        resultats = []
        
        for i, scenario in enumerate(scenarios):
            result = FinanceCalculator.interet_compose(
                scenario['capital'],
                scenario['taux'],
                scenario['duree'],
                scenario.get('freq_capitalisation', 1),
                scenario.get('versements', 0)
            )
            
            resultats.append({
                'scenario': f"Scénario {i+1}",
                'paramètres': scenario,
                'résultat': result,
                'roi_annuel': result.rendement_pct / result.duree_annees
            })
        
        # Tri par rendement décroissant
        resultats.sort(key=lambda x: x['résultat'].rendement_pct, reverse=True)
        
        return resultats
    
    @staticmethod
    def calcul_inflation(montant: float, taux_inflation: float, annees: int) -> Dict[str, float]:
        """
        Calcule l'impact de l'inflation.
        
        Args:
            montant: Montant actuel
            taux_inflation: Taux d'inflation annuel (en %)
            annees: Nombre d'années
            
        Returns:
            Impact de l'inflation
        """
        facteur_inflation = (1 + taux_inflation / 100) ** annees
        valeur_future_nominale = montant
        valeur_future_reelle = montant / facteur_inflation
        perte_pouvoir_achat = montant - valeur_future_reelle
        
        return {
            "montant_initial": montant,
            "taux_inflation": taux_inflation,
            "duree_annees": annees,
            "valeur_reelle_future": valeur_future_reelle,
            "perte_pouvoir_achat": perte_pouvoir_achat,
            "perte_pourcentage": (perte_pouvoir_achat / montant) * 100
        }


def afficher_interet_compose(result: InvestmentResult) -> None:
    """Affiche les résultats d'intérêts composés."""
    print(f"\n💰 RÉSULTATS INTÉRÊTS COMPOSÉS")
    print("=" * 50)
    print(f"💵 Capital initial      : {result.montant_initial:,.2f} €")
    print(f"💎 Montant final        : {result.montant_final:,.2f} €")
    print(f"📈 Gain total           : {result.gain_total:,.2f} €")
    print(f"📊 Rendement total      : {result.rendement_pct:.2f}%")
    print(f"📊 Rendement annuel moy.: {result.rendement_pct/result.duree_annees:.2f}%")
    print(f"⏱️  Durée               : {result.duree_annees:.1f} ans")


def afficher_tableau_amortissement(mensualite: float, tableau: List[LoanPayment], 
                                  resume_seulement: bool = True) -> None:
    """Affiche le tableau d'amortissement d'un prêt."""
    print(f"\n🏠 AMORTISSEMENT DE PRÊT")
    print("=" * 80)
    print(f"💳 Mensualité : {mensualite:.2f} €")
    
    total_capital = sum(p.capital for p in tableau)
    total_interets = sum(p.interet for p in tableau)
    total_paye = total_capital + total_interets
    
    print(f"💰 Total remboursé : {total_paye:,.2f} € (Capital: {total_capital:,.2f} € + Intérêts: {total_interets:,.2f} €)")
    
    if resume_seulement:
        print(f"\n📊 RÉSUMÉ PAR ANNÉE:")
        print(f"{'Année':<6} {'Capital':<12} {'Intérêts':<12} {'Total':<12} {'Solde':<12}")
        print("-" * 60)
        
        for annee in range(1, len(tableau) // 12 + 2):
            debut = (annee - 1) * 12
            fin = min(annee * 12, len(tableau))
            
            if debut >= len(tableau):
                break
            
            paiements_annee = tableau[debut:fin]
            capital_annee = sum(p.capital for p in paiements_annee)
            interets_annee = sum(p.interet for p in paiements_annee)
            total_annee = capital_annee + interets_annee
            solde_fin = paiements_annee[-1].solde_restant if paiements_annee else 0
            
            print(f"{annee:<6} {capital_annee:<12,.0f} {interets_annee:<12,.0f} {total_annee:<12,.0f} {solde_fin:<12,.0f}")
    else:
        print(f"\n📋 TABLEAU DÉTAILLÉ:")
        print(f"{'Mois':<4} {'Capital':<10} {'Intérêts':<10} {'Total':<10} {'Solde':<12}")
        print("-" * 50)
        
        for paiement in tableau[:min(12, len(tableau))]:  # Affiche seulement les 12 premiers mois
            print(f"{paiement.numero:<4} {paiement.capital:<10,.0f} {paiement.interet:<10,.0f} "
                  f"{paiement.paiement_total:<10,.0f} {paiement.solde_restant:<12,.0f}")
        
        if len(tableau) > 12:
            print("... (utilisez l'option détaillée pour voir tous les mois)")


def interface_interet_compose() -> None:
    """Interface pour le calcul d'intérêts composés."""
    try:
        print("\n💰 CALCUL D'INTÉRÊTS COMPOSÉS")
        print("-" * 40)
        
        capital = float(input("💵 Capital initial (€) : "))
        taux = float(input("📈 Taux d'intérêt annuel (%) : "))
        duree = int(input("⏱️  Durée (années) : "))
        
        print("\n🔄 Fréquence de capitalisation :")
        print("1. Annuelle (1 fois/an)")
        print("2. Semestrielle (2 fois/an)")
        print("3. Trimestrielle (4 fois/an)")
        print("4. Mensuelle (12 fois/an)")
        print("5. Quotidienne (365 fois/an)")
        
        freq_choice = input("👉 Votre choix [1] : ").strip() or "1"
        freq_map = {"1": 1, "2": 2, "3": 4, "4": 12, "5": 365}
        freq = freq_map.get(freq_choice, 1)
        
        versements_input = input("💰 Versements réguliers annuels (€) [0] : ").strip()
        versements = float(versements_input) if versements_input else 0
        
        result = FinanceCalculator.interet_compose(capital, taux, duree, freq, versements)
        afficher_interet_compose(result)
        
    except ValueError:
        print("❌ Erreur : Veuillez entrer des valeurs numériques valides")


def interface_pret() -> None:
    """Interface pour le calcul d'amortissement de prêt."""
    try:
        print("\n🏠 CALCUL D'AMORTISSEMENT DE PRÊT")
        print("-" * 40)
        
        montant = float(input("💰 Montant du prêt (€) : "))
        taux = float(input("📈 Taux d'intérêt annuel (%) : "))
        duree_annees = float(input("⏱️  Durée (années) : "))
        
        duree_mois = int(duree_annees * 12)
        mensualite, tableau = FinanceCalculator.calcul_pret(montant, taux, duree_mois)
        
        afficher_tableau_amortissement(mensualite, tableau, resume_seulement=True)
        
        detail = input("\n👀 Voir le tableau détaillé ? (o/N) : ").lower()
        if detail in ['o', 'oui', 'y', 'yes']:
            afficher_tableau_amortissement(mensualite, tableau, resume_seulement=False)
        
    except ValueError:
        print("❌ Erreur : Veuillez entrer des valeurs numériques valides")


def interface_objectif_epargne() -> None:
    """Interface pour le calcul d'objectif d'épargne."""
    try:
        print("\n🎯 PLANIFICATION D'ÉPARGNE")
        print("-" * 40)
        
        objectif = float(input("🎯 Objectif financier (€) : "))
        duree = int(input("⏱️  Durée pour atteindre l'objectif (années) : "))
        taux_input = input("📈 Taux de rendement annuel (%) [0] : ").strip()
        taux = float(taux_input) if taux_input else 0
        
        result = FinanceCalculator.objectif_epargne(objectif, duree, taux)
        
        print(f"\n🎯 PLANIFICATION POUR {objectif:,.0f} € EN {duree} ANS")
        print("=" * 60)
        print(f"💰 Épargne mensuelle requise : {result['epargne_mensuelle']:,.2f} €")
        print(f"💰 Épargne annuelle requise  : {result['epargne_annuelle']:,.2f} €")
        
        if taux > 0:
            print(f"💎 Ou versement unique maintenant : {result['epargne_unique']:,.2f} €")
            print(f"📊 Total versé (mensuel)     : {result['total_verse']:,.2f} €")
            print(f"📈 Intérêts gagnés           : {result['interets_gagnes']:,.2f} €")
        
    except ValueError:
        print("❌ Erreur : Veuillez entrer des valeurs numériques valides")


def interface_comparaison() -> None:
    """Interface pour comparer des investissements."""
    scenarios = []
    
    print("\n⚖️  COMPARAISON D'INVESTISSEMENTS")
    print("-" * 40)
    
    try:
        nb_scenarios = int(input("🔢 Nombre de scénarios à comparer [2] : ") or "2")
        nb_scenarios = min(max(nb_scenarios, 2), 5)  # Entre 2 et 5
        
        for i in range(nb_scenarios):
            print(f"\n📊 Scénario {i+1}:")
            capital = float(input(f"  💵 Capital initial (€) : "))
            taux = float(input(f"  📈 Taux annuel (%) : "))
            duree = int(input(f"  ⏱️  Durée (années) : "))
            
            scenarios.append({
                'capital': capital,
                'taux': taux,
                'duree': duree
            })
        
        resultats = FinanceCalculator.comparaison_investissements(scenarios)
        
        print(f"\n🏆 COMPARAISON DES SCÉNARIOS (triés par rendement)")
        print("=" * 80)
        
        for i, res in enumerate(resultats):
            print(f"\n🥇 {res['scenario']} (Rang {i+1})")
            print(f"   💵 Capital: {res['paramètres']['capital']:,.0f} € | "
                  f"📈 Taux: {res['paramètres']['taux']:.1f}% | "
                  f"⏱️  Durée: {res['paramètres']['duree']} ans")
            print(f"   💎 Résultat: {res['résultat'].montant_final:,.0f} € "
                  f"(+{res['résultat'].gain_total:,.0f} €)")
            print(f"   📊 Rendement: {res['résultat'].rendement_pct:.1f}% total "
                  f"({res['roi_annuel']:.1f}%/an)")
        
    except ValueError:
        print("❌ Erreur : Veuillez entrer des valeurs numériques valides")


def interface_inflation() -> None:
    """Interface pour calculer l'impact de l'inflation."""
    try:
        print("\n📉 IMPACT DE L'INFLATION")
        print("-" * 40)
        
        montant = float(input("💰 Montant actuel (€) : "))
        taux_inflation = float(input("📉 Taux d'inflation annuel (%) [2] : ") or "2")
        annees = int(input("⏱️  Nombre d'années [10] : ") or "10")
        
        result = FinanceCalculator.calcul_inflation(montant, taux_inflation, annees)
        
        print(f"\n📉 IMPACT DE L'INFLATION SUR {montant:,.0f} €")
        print("=" * 50)
        print(f"📅 Dans {annees} ans avec {taux_inflation}% d'inflation :")
        print(f"💸 Valeur réelle équivalente : {result['valeur_reelle_future']:,.2f} €")
        print(f"📉 Perte de pouvoir d'achat  : {result['perte_pouvoir_achat']:,.2f} €")
        print(f"📊 Perte en pourcentage      : {result['perte_pourcentage']:.1f}%")
        
        print(f"\n💡 Pour maintenir le même pouvoir d'achat, il faudrait : {montant * (1 + taux_inflation/100)**annees:,.2f} €")
        
    except ValueError:
        print("❌ Erreur : Veuillez entrer des valeurs numériques valides")


def main():
    """Fonction principale avec interface interactive."""
    print("💰 CALCULATRICE FINANCIÈRE - MÉTHODE MARKOVA")
    print("=" * 60)
    
    while True:
        print("\n🎯 MENU PRINCIPAL:")
        print("1. 💰 Intérêts composés")
        print("2. 🏠 Amortissement de prêt")
        print("3. 🎯 Objectif d'épargne")
        print("4. ⚖️  Comparaison d'investissements")
        print("5. 📉 Impact de l'inflation")
        print("0. 🚪 Quitter")
        print("-" * 50)
        
        choix = input("👉 Votre choix : ").strip()
        
        try:
            if choix == "0":
                print("👋 Bonne gestion financière !")
                break
            
            elif choix == "1":
                interface_interet_compose()
            
            elif choix == "2":
                interface_pret()
            
            elif choix == "3":
                interface_objectif_epargne()
            
            elif choix == "4":
                interface_comparaison()
            
            elif choix == "5":
                interface_inflation()
            
            else:
                print("❌ Choix invalide")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu !")
            break
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")


if __name__ == "__main__":
    main() 