#!/usr/bin/env python3
"""
🚀 Démonstration des Projets - Méthode Markova
==============================================

Script de démonstration pour tous les mini-projets du niveau 6.
Permet de tester rapidement chaque application avec des données d'exemple.

Auteur: Méthode Markova
Niveau: 06 - Mini-projets concrets
"""

import subprocess
import sys
import os
from pathlib import Path


def clear_screen():
    """Efface l'écran selon l'OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def afficher_header():
    """Affiche l'en-tête du programme de démonstration."""
    clear_screen()
    print("🚀 DÉMONSTRATION DES PROJETS - MÉTHODE MARKOVA")
    print("=" * 70)
    print("Niveau 06 - Mini-projets concrets")
    print("Testez tous les projets avec des exemples intégrés !")
    print()


def lancer_projet(script_name: str, description: str) -> None:
    """
    Lance un projet spécifique.
    
    Args:
        script_name: Nom du script Python
        description: Description du projet
    """
    print(f"\n🎯 Lancement de : {description}")
    print("-" * 50)
    
    if not Path(script_name).exists():
        print(f"❌ Erreur : Le fichier {script_name} n'existe pas")
        input("👉 Appuyez sur Entrée pour continuer...")
        return
    
    print(f"🚀 Démarrage de {script_name}...")
    print("💡 Tip: Utilisez Ctrl+C pour revenir au menu principal")
    print()
    
    try:
        # Lance le script dans le même processus Python
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
    except KeyboardInterrupt:
        print("\n🔄 Retour au menu principal...")
    
    input("\n👉 Appuyez sur Entrée pour continuer...")


def demo_rapide():
    """Affiche une démonstration rapide de chaque projet."""
    print("\n🎬 DÉMONSTRATION RAPIDE DES PROJETS")
    print("=" * 50)
    
    projets = [
        {
            "nom": "Gestionnaire de Tâches",
            "fichier": "01_task_manager.py",
            "description": "• Gestion complète de tâches avec priorités\n  • Sauvegarde automatique en JSON\n  • Statistiques d'avancement",
            "exemple": "Exemple : Ajouter 'Apprendre Python', marquer comme terminé"
        },
        {
            "nom": "Analyseur de Texte",
            "fichier": "02_text_analyzer.py", 
            "description": "• Statistiques complètes (mots, caractères, phrases)\n  • Analyse de fréquence et lisibilité\n  • Recherche de motifs regex",
            "exemple": "Exemple : Analyser un article, calculer sa complexité"
        },
        {
            "nom": "Générateur de Mots de Passe",
            "fichier": "03_password_generator.py",
            "description": "• Génération sécurisée avec critères personnalisables\n  • Évaluation de la force des mots de passe\n  • Conseils de sécurité intégrés",
            "exemple": "Exemple : Générer un mot de passe de 16 caractères"
        },
        {
            "nom": "Convertisseur d'Unités",
            "fichier": "04_unit_converter.py",
            "description": "• Conversion entre longueurs, poids, volumes, etc.\n  • Températures (Celsius, Fahrenheit, Kelvin)\n  • Interface intuitive par catégories",
            "exemple": "Exemple : Convertir 100 km/h en m/s"
        },
        {
            "nom": "Carnet d'Adresses",
            "fichier": "05_address_book.py",
            "description": "• Base de données SQLite intégrée\n  • Recherche et filtrage avancés\n  • Export en JSON/CSV",
            "exemple": "Exemple : Ajouter un contact, rechercher par entreprise"
        },
        {
            "nom": "Calculatrice Financière",
            "fichier": "06_finance_calculator.py",
            "description": "• Intérêts composés et amortissement de prêts\n  • Planification d'épargne et d'objectifs\n  • Comparaison d'investissements",
            "exemple": "Exemple : Calculer un prêt de 200 000€ sur 20 ans"
        },
        {
            "nom": "Framework ETL",
            "fichier": "07_etl_framework.py",
            "description": "• Connecteurs pour SGBD, Parquet, NoSQL\n  • Pipelines de transformation configurable\n  • Monitoring et métriques intégrés",
            "exemple": "Exemple : Extraire depuis SQLite, transformer et charger en Parquet"
        }
    ]
    
    for i, projet in enumerate(projets, 1):
        print(f"\n{i}. 📁 {projet['nom']}")
        print(f"   📄 Fichier : {projet['fichier']}")
        print(f"   ✨ Fonctionnalités :")
        print(f"   {projet['description']}")
        print(f"   💡 {projet['exemple']}")
        print()
    
    print("🎯 Chaque projet est entièrement fonctionnel et documenté !")
    print("🔧 Code source disponible avec commentaires détaillés")
    print("📚 Utilise les concepts des niveaux 1-5 (variables, boucles, fonctions, etc.)")
    
    input("\n👉 Appuyez sur Entrée pour continuer...")


def afficher_conseils():
    """Affiche des conseils pour utiliser les projets."""
    print("\n💡 CONSEILS D'UTILISATION")
    print("=" * 40)
    print("🎯 Comment profiter au maximum des projets :")
    print()
    print("1. 📖 LIRE LE CODE")
    print("   • Chaque projet est bien commenté")
    print("   • Étudiez les classes et fonctions")
    print("   • Comprenez l'architecture utilisée")
    print()
    print("2. 🧪 EXPÉRIMENTER")
    print("   • Testez toutes les fonctionnalités")
    print("   • Essayez des cas limites")
    print("   • Modifiez les paramètres")
    print()
    print("3. 🔧 PERSONNALISER")
    print("   • Ajoutez vos propres fonctionnalités")
    print("   • Modifiez l'interface utilisateur")
    print("   • Intégrez plusieurs projets ensemble")
    print()
    print("4. 📝 APPRENDRE")
    print("   • Chaque projet illustre des concepts clés")
    print("   • Observez la gestion d'erreurs")
    print("   • Étudiez la validation des données")
    print()
    print("🎓 CONCEPTS CLÉS ILLUSTRÉS :")
    print("• Classes et programmation orientée objet")
    print("• Gestion de fichiers et bases de données")
    print("• Interfaces utilisateur en ligne de commande")
    print("• Validation et gestion d'erreurs")
    print("• Documentation et bonnes pratiques")
    print("• Ingénierie de données et pipelines ETL")
    
    input("\n👉 Appuyez sur Entrée pour continuer...")


def verifier_projets():
    """Vérifie que tous les fichiers de projets existent."""
    projets = [
        "01_task_manager.py",
        "02_text_analyzer.py", 
        "03_password_generator.py",
        "04_unit_converter.py",
        "05_address_book.py",
        "06_finance_calculator.py",
        "07_etl_framework.py"
    ]
    
    print("\n🔍 VÉRIFICATION DES PROJETS")
    print("=" * 40)
    
    tous_presents = True
    for projet in projets:
        if Path(projet).exists():
            taille = Path(projet).stat().st_size
            print(f"✅ {projet:<25} ({taille:,} octets)")
        else:
            print(f"❌ {projet:<25} (manquant)")
            tous_presents = False
    
    print()
    if tous_presents:
        print("🎉 Tous les projets sont présents et prêts à utiliser !")
    else:
        print("⚠️  Certains projets sont manquants. Vérifiez les fichiers.")
    
    input("\n👉 Appuyez sur Entrée pour continuer...")


def main():
    """Fonction principale avec menu interactif."""
    while True:
        afficher_header()
        
        print("🎯 MENU PRINCIPAL :")
        print("1. 📝 Gestionnaire de Tâches")
        print("2. 📊 Analyseur de Texte") 
        print("3. 🔐 Générateur de Mots de Passe")
        print("4. 📏 Convertisseur d'Unités")
        print("5. 👥 Carnet d'Adresses")
        print("6. 💰 Calculatrice Financière")
        print("7. 🚀 Framework ETL")
        print()
        print("🎬 D. Démonstration rapide")
        print("💡 C. Conseils d'utilisation")
        print("🔍 V. Vérifier les projets")
        print("0. 🚪 Quitter")
        print("-" * 70)
        
        choix = input("👉 Votre choix : ").strip().lower()
        
        try:
            if choix == "0":
                clear_screen()
                print("👋 Merci d'avoir testé les projets Méthode Markova !")
                print("🚀 Continuez à coder et à apprendre !")
                break
            
            elif choix == "1":
                lancer_projet("01_task_manager.py", "Gestionnaire de Tâches")
            
            elif choix == "2":
                lancer_projet("02_text_analyzer.py", "Analyseur de Texte")
            
            elif choix == "3":
                lancer_projet("03_password_generator.py", "Générateur de Mots de Passe")
            
            elif choix == "4":
                lancer_projet("04_unit_converter.py", "Convertisseur d'Unités")
            
            elif choix == "5":
                lancer_projet("05_address_book.py", "Carnet d'Adresses")
            
            elif choix == "6":
                lancer_projet("06_finance_calculator.py", "Calculatrice Financière")
            
            elif choix == "7":
                lancer_projet("07_etl_framework.py", "Framework ETL")
            
            elif choix in ["d", "demo"]:
                demo_rapide()
            
            elif choix in ["c", "conseils"]:
                afficher_conseils()
            
            elif choix in ["v", "verifier"]:
                verifier_projets()
            
            else:
                print("❌ Choix invalide")
                input("👉 Appuyez sur Entrée pour continuer...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu !")
            break
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")
            input("👉 Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main() 