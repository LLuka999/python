#!/usr/bin/env python3
"""
🔐 Générateur de Mots de Passe - Méthode Markova
=================================================

Un générateur de mots de passe sécurisé qui propose :
- Génération avec critères personnalisables
- Évaluation de la force du mot de passe
- Plusieurs méthodes de génération
- Conseils de sécurité
- Export sécurisé

Auteur: Méthode Markova
Niveau: 06 - Mini-projets concrets
"""

import random
import string
import secrets
import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PasswordCriteria:
    """Critères pour la génération de mots de passe."""
    length: int = 12
    use_uppercase: bool = True
    use_lowercase: bool = True
    use_digits: bool = True
    use_symbols: bool = True
    exclude_ambiguous: bool = True
    exclude_chars: str = ""
    must_include: str = ""


class PasswordGenerator:
    """Générateur de mots de passe sécurisé."""
    
    def __init__(self):
        """Initialise le générateur."""
        # Caractères ambigus à éviter par défaut
        self.ambiguous_chars = "0O1lI|`"
        
        # Jeux de caractères
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def _get_character_pool(self, criteria: PasswordCriteria) -> str:
        """
        Construit le pool de caractères selon les critères.
        
        Args:
            criteria: Critères de génération
            
        Returns:
            String contenant tous les caractères utilisables
        """
        pool = ""
        
        if criteria.use_uppercase:
            pool += self.uppercase
        if criteria.use_lowercase:
            pool += self.lowercase
        if criteria.use_digits:
            pool += self.digits
        if criteria.use_symbols:
            pool += self.symbols
        
        # Supprime les caractères ambigus si demandé
        if criteria.exclude_ambiguous:
            pool = ''.join(c for c in pool if c not in self.ambiguous_chars)
        
        # Supprime les caractères exclus personnalisés
        if criteria.exclude_chars:
            pool = ''.join(c for c in pool if c not in criteria.exclude_chars)
        
        return pool
    
    def generate_random(self, criteria: PasswordCriteria) -> str:
        """
        Génère un mot de passe aléatoire.
        
        Args:
            criteria: Critères de génération
            
        Returns:
            Mot de passe généré
        """
        pool = self._get_character_pool(criteria)
        
        if not pool:
            raise ValueError("Aucun caractère disponible avec ces critères")
        
        # Génération sécurisée avec secrets
        password = ''.join(secrets.choice(pool) for _ in range(criteria.length))
        
        # S'assure que le mot de passe respecte les exigences minimales
        password = self._ensure_criteria_met(password, criteria)
        
        # Ajoute les caractères obligatoires si spécifiés
        if criteria.must_include:
            password = self._include_required_chars(password, criteria)
        
        return password
    
    def generate_pronounceable(self, length: int = 12) -> str:
        """
        Génère un mot de passe prononçable (alternance voyelles/consonnes).
        
        Args:
            length: Longueur du mot de passe
            
        Returns:
            Mot de passe prononçable
        """
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        
        password = ""
        for i in range(length):
            if i % 2 == 0:  # Position paire = consonne
                password += secrets.choice(consonants)
            else:  # Position impaire = voyelle
                password += secrets.choice(vowels)
        
        # Ajoute quelques chiffres et majuscules pour la sécurité
        if length > 6:
            # Remplace quelques caractères par des majuscules
            password = self._add_random_case(password)
            # Ajoute quelques chiffres
            password = self._add_random_digits(password, min(2, length // 4))
        
        return password
    
    def generate_passphrase(self, word_count: int = 4, separator: str = "-") -> str:
        """
        Génère une phrase de passe avec des mots aléatoires.
        
        Args:
            word_count: Nombre de mots
            separator: Séparateur entre les mots
            
        Returns:
            Phrase de passe
        """
        # Liste de mots courants mais non triviaux
        words = [
            "horizon", "cascade", "thunder", "whisper", "crystal", "phoenix", "glacier",
            "bambou", "tornade", "mystere", "lumiere", "aventure", "courage", "silence",
            "orange", "violet", "bronze", "argent", "rubine", "saphir", "emeraude",
            "montagne", "riviere", "foret", "desert", "ocean", "planete", "etoile",
            "papillon", "libellule", "colibri", "elephant", "panthere", "dolphin",
            "keyboard", "melody", "rhythm", "harmony", "symphony", "poetry", "canvas"
        ]
        
        selected_words = [secrets.choice(words) for _ in range(word_count)]
        
        # Ajoute un nombre aléatoire pour plus de sécurité
        selected_words.append(str(secrets.randbelow(9999)))
        
        return separator.join(selected_words)
    
    def _ensure_criteria_met(self, password: str, criteria: PasswordCriteria) -> str:
        """
        S'assure que le mot de passe respecte tous les critères.
        
        Args:
            password: Mot de passe à vérifier
            criteria: Critères requis
            
        Returns:
            Mot de passe modifié si nécessaire
        """
        pool = self._get_character_pool(criteria)
        password_list = list(password)
        
        # Vérifie et corrige chaque critère
        if criteria.use_uppercase and not any(c in self.uppercase for c in password):
            pos = secrets.randbelow(len(password_list))
            password_list[pos] = secrets.choice(self.uppercase)
        
        if criteria.use_lowercase and not any(c in self.lowercase for c in password):
            pos = secrets.randbelow(len(password_list))
            password_list[pos] = secrets.choice(self.lowercase)
        
        if criteria.use_digits and not any(c in self.digits for c in password):
            pos = secrets.randbelow(len(password_list))
            password_list[pos] = secrets.choice(self.digits)
        
        if criteria.use_symbols and not any(c in self.symbols for c in password):
            pos = secrets.randbelow(len(password_list))
            password_list[pos] = secrets.choice(self.symbols)
        
        return ''.join(password_list)
    
    def _include_required_chars(self, password: str, criteria: PasswordCriteria) -> str:
        """
        Inclut les caractères obligatoires dans le mot de passe.
        
        Args:
            password: Mot de passe de base
            criteria: Critères avec caractères requis
            
        Returns:
            Mot de passe avec caractères requis
        """
        password_list = list(password)
        
        for char in criteria.must_include:
            if char not in password_list:
                # Remplace un caractère aléatoire
                pos = secrets.randbelow(len(password_list))
                password_list[pos] = char
        
        return ''.join(password_list)
    
    def _add_random_case(self, password: str) -> str:
        """Ajoute des majuscules aléatoires."""
        password_list = list(password.lower())
        for _ in range(len(password_list) // 3):
            pos = secrets.randbelow(len(password_list))
            if password_list[pos].isalpha():
                password_list[pos] = password_list[pos].upper()
        return ''.join(password_list)
    
    def _add_random_digits(self, password: str, count: int) -> str:
        """Ajoute des chiffres aléatoires."""
        password_list = list(password)
        for _ in range(count):
            pos = secrets.randbelow(len(password_list))
            password_list[pos] = secrets.choice(self.digits)
        return ''.join(password_list)


class PasswordStrengthAnalyzer:
    """Analyseur de force des mots de passe."""
    
    def analyze(self, password: str) -> Dict[str, any]:
        """
        Analyse la force d'un mot de passe.
        
        Args:
            password: Mot de passe à analyser
            
        Returns:
            Dictionnaire avec l'analyse détaillée
        """
        if not password:
            return {"score": 0, "level": "Invalide", "feedback": ["Mot de passe vide"]}
        
        score = 0
        feedback = []
        
        # Critères d'évaluation
        length = len(password)
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        # Calcul du score
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        
        if has_lower:
            score += 1
        if has_upper:
            score += 1
        if has_digit:
            score += 1
        if has_symbol:
            score += 1
        
        # Vérifications supplémentaires
        unique_chars = len(set(password))
        if unique_chars >= length * 0.7:  # 70% de caractères uniques
            score += 1
        
        # Pénalités
        if re.search(r'(.)\1{2,}', password):  # Répétitions
            score -= 1
            feedback.append("Évitez les répétitions de caractères")
        
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):  # Séquences
            score -= 1
            feedback.append("Évitez les séquences numériques")
        
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            score -= 1
            feedback.append("Évitez les séquences alphabétiques")
        
        # Mots de passe courants
        common_passwords = ['password', 'motdepasse', '12345678', 'qwerty', 'azerty']
        if password.lower() in common_passwords:
            score = 0
            feedback.append("Mot de passe trop courant")
        
        # Recommandations
        if not has_lower:
            feedback.append("Ajoutez des lettres minuscules")
        if not has_upper:
            feedback.append("Ajoutez des lettres majuscules")
        if not has_digit:
            feedback.append("Ajoutez des chiffres")
        if not has_symbol:
            feedback.append("Ajoutez des symboles (!@#$%...)")
        if length < 12:
            feedback.append("Utilisez au moins 12 caractères")
        
        # Détermination du niveau
        if score <= 2:
            level = "Très faible"
            color = "🔴"
        elif score <= 4:
            level = "Faible"
            color = "🟠"
        elif score <= 6:
            level = "Moyen"
            color = "🟡"
        elif score <= 8:
            level = "Fort"
            color = "🟢"
        else:
            level = "Très fort"
            color = "💚"
        
        return {
            "score": score,
            "max_score": 9,
            "level": level,
            "color": color,
            "feedback": feedback,
            "details": {
                "length": length,
                "has_lowercase": has_lower,
                "has_uppercase": has_upper,
                "has_digits": has_digit,
                "has_symbols": has_symbol,
                "unique_chars": unique_chars
            }
        }


def show_password_tips() -> None:
    """Affiche des conseils de sécurité."""
    print("\n🛡️  CONSEILS DE SÉCURITÉ:")
    print("=" * 50)
    print("✅ Utilisez un mot de passe unique pour chaque compte")
    print("✅ Minimum 12 caractères (16+ recommandé)")
    print("✅ Mélangez majuscules, minuscules, chiffres et symboles")
    print("✅ Évitez les informations personnelles")
    print("✅ Utilisez un gestionnaire de mots de passe")
    print("✅ Activez l'authentification à deux facteurs")
    print("❌ N'utilisez jamais le même mot de passe partout")
    print("❌ Évitez les mots du dictionnaire")
    print("❌ Ne partagez jamais vos mots de passe")


def interactive_criteria_setup() -> PasswordCriteria:
    """Configuration interactive des critères."""
    print("\n⚙️  CONFIGURATION DU MOT DE PASSE:")
    print("-" * 40)
    
    try:
        length = int(input("🔢 Longueur [12] : ") or "12")
        length = max(4, min(128, length))  # Limite entre 4 et 128
        
        use_upper = input("🔤 Majuscules ? [O/n] : ").lower() not in ['n', 'non', 'no']
        use_lower = input("🔤 Minuscules ? [O/n] : ").lower() not in ['n', 'non', 'no']
        use_digits = input("🔢 Chiffres ? [O/n] : ").lower() not in ['n', 'non', 'no']
        use_symbols = input("🔣 Symboles ? [O/n] : ").lower() not in ['n', 'non', 'no']
        
        exclude_ambiguous = input("🚫 Exclure caractères ambigus (0O1lI|) ? [O/n] : ").lower() not in ['n', 'non', 'no']
        
        exclude_chars = input("🚫 Caractères à exclure (optionnel) : ").strip()
        must_include = input("✅ Caractères à inclure (optionnel) : ").strip()
        
        return PasswordCriteria(
            length=length,
            use_uppercase=use_upper,
            use_lowercase=use_lower,
            use_digits=use_digits,
            use_symbols=use_symbols,
            exclude_ambiguous=exclude_ambiguous,
            exclude_chars=exclude_chars,
            must_include=must_include
        )
    
    except ValueError:
        print("❌ Valeur invalide, utilisation des paramètres par défaut")
        return PasswordCriteria()


def main():
    """Fonction principale avec interface interactive."""
    generator = PasswordGenerator()
    analyzer = PasswordStrengthAnalyzer()
    
    print("🔐 GÉNÉRATEUR DE MOTS DE PASSE - MÉTHODE MARKOVA")
    print("=" * 60)
    
    while True:
        print("\n🎯 OPTIONS:")
        print("1. 🔀 Générer mot de passe aléatoire")
        print("2. 🗣️  Générer mot de passe prononçable")
        print("3. 📝 Générer phrase de passe")
        print("4. ⚙️  Configuration personnalisée")
        print("5. 🔍 Analyser un mot de passe")
        print("6. 🛡️  Conseils de sécurité")
        print("0. 🚪 Quitter")
        print("-" * 50)
        
        choice = input("👉 Votre choix : ").strip()
        
        try:
            if choice == "0":
                print("👋 Restez en sécurité !")
                break
            
            elif choice == "1":
                criteria = PasswordCriteria()  # Critères par défaut
                password = generator.generate_random(criteria)
                analysis = analyzer.analyze(password)
                
                print(f"\n🔐 Mot de passe généré :")
                print(f"📋 {password}")
                print(f"\n🎯 Force : {analysis['color']} {analysis['level']} ({analysis['score']}/{analysis['max_score']})")
                
                if analysis['feedback']:
                    print("💡 Suggestions :")
                    for tip in analysis['feedback'][:3]:
                        print(f"   • {tip}")
            
            elif choice == "2":
                try:
                    length = int(input("🔢 Longueur [12] : ") or "12")
                    length = max(6, min(32, length))
                except ValueError:
                    length = 12
                
                password = generator.generate_pronounceable(length)
                analysis = analyzer.analyze(password)
                
                print(f"\n🗣️  Mot de passe prononçable :")
                print(f"📋 {password}")
                print(f"\n🎯 Force : {analysis['color']} {analysis['level']} ({analysis['score']}/{analysis['max_score']})")
            
            elif choice == "3":
                try:
                    word_count = int(input("🔢 Nombre de mots [4] : ") or "4")
                    word_count = max(2, min(8, word_count))
                except ValueError:
                    word_count = 4
                
                separator = input("🔗 Séparateur [-] : ") or "-"
                
                passphrase = generator.generate_passphrase(word_count, separator)
                analysis = analyzer.analyze(passphrase)
                
                print(f"\n📝 Phrase de passe :")
                print(f"📋 {passphrase}")
                print(f"\n🎯 Force : {analysis['color']} {analysis['level']} ({analysis['score']}/{analysis['max_score']})")
            
            elif choice == "4":
                criteria = interactive_criteria_setup()
                password = generator.generate_random(criteria)
                analysis = analyzer.analyze(password)
                
                print(f"\n🔐 Mot de passe personnalisé :")
                print(f"📋 {password}")
                print(f"\n🎯 Force : {analysis['color']} {analysis['level']} ({analysis['score']}/{analysis['max_score']})")
                
                if analysis['feedback']:
                    print("💡 Suggestions :")
                    for tip in analysis['feedback']:
                        print(f"   • {tip}")
            
            elif choice == "5":
                password = input("🔍 Entrez le mot de passe à analyser : ").strip()
                if password:
                    analysis = analyzer.analyze(password)
                    
                    print(f"\n📊 ANALYSE DÉTAILLÉE:")
                    print("-" * 30)
                    print(f"🎯 Force : {analysis['color']} {analysis['level']}")
                    print(f"📊 Score : {analysis['score']}/{analysis['max_score']}")
                    print(f"📏 Longueur : {analysis['details']['length']} caractères")
                    print(f"🔤 Minuscules : {'✅' if analysis['details']['has_lowercase'] else '❌'}")
                    print(f"🔤 Majuscules : {'✅' if analysis['details']['has_uppercase'] else '❌'}")
                    print(f"🔢 Chiffres : {'✅' if analysis['details']['has_digits'] else '❌'}")
                    print(f"🔣 Symboles : {'✅' if analysis['details']['has_symbols'] else '❌'}")
                    print(f"🎨 Caractères uniques : {analysis['details']['unique_chars']}")
                    
                    if analysis['feedback']:
                        print("\n💡 Recommandations :")
                        for tip in analysis['feedback']:
                            print(f"   • {tip}")
                else:
                    print("❌ Aucun mot de passe saisi")
            
            elif choice == "6":
                show_password_tips()
            
            else:
                print("❌ Choix invalide")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu !")
            break
        except Exception as e:
            print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    main() 