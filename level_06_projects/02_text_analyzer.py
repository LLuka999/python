#!/usr/bin/env python3
"""
📝 Analyseur de Texte - Méthode Markova
=======================================

Un analyseur de texte complet qui fournit :
- Statistiques de base (mots, caractères, phrases)
- Analyse de fréquence des mots
- Recherche de motifs et mots-clés
- Lisibilité et complexité
- Export des résultats

Auteur: Méthode Markova
Niveau: 06 - Mini-projets concrets
"""

import re
import json
from collections import Counter
from typing import Dict, List, Tuple, Set
import string


class TextAnalyzer:
    """Analyseur de texte avec diverses métriques."""
    
    def __init__(self, text: str = ""):
        """
        Initialise l'analyseur avec un texte.
        
        Args:
            text: Texte à analyser
        """
        self.original_text = text
        self.cleaned_text = self._clean_text(text)
        self.words = self._extract_words()
        self.sentences = self._extract_sentences()
    
    def _clean_text(self, text: str) -> str:
        """
        Nettoie le texte pour l'analyse.
        
        Args:
            text: Texte brut
            
        Returns:
            Texte nettoyé
        """
        # Supprime les caractères de contrôle et normalise les espaces
        cleaned = re.sub(r'\s+', ' ', text.strip())
        return cleaned
    
    def _extract_words(self) -> List[str]:
        """
        Extrait les mots du texte.
        
        Returns:
            Liste des mots en minuscules
        """
        # Utilise regex pour extraire les mots (lettres et apostrophes)
        words = re.findall(r"\b[a-zA-ZÀ-ÿ']+\b", self.cleaned_text.lower())
        return words
    
    def _extract_sentences(self) -> List[str]:
        """
        Extrait les phrases du texte.
        
        Returns:
            Liste des phrases
        """
        # Divise sur les points, exclamations, interrogations
        sentences = re.split(r'[.!?]+', self.cleaned_text)
        # Supprime les phrases vides et nettoie
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def basic_stats(self) -> Dict[str, int]:
        """
        Calcule les statistiques de base.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        return {
            "characters_total": len(self.original_text),
            "characters_no_spaces": len(self.original_text.replace(" ", "")),
            "words": len(self.words),
            "unique_words": len(set(self.words)),
            "sentences": len(self.sentences),
            "paragraphs": len([p for p in self.original_text.split('\n\n') if p.strip()])
        }
    
    def word_frequency(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Analyse la fréquence des mots.
        
        Args:
            top_n: Nombre de mots les plus fréquents à retourner
            
        Returns:
            Liste de tuples (mot, fréquence)
        """
        # Exclut les mots vides courants
        stop_words = {
            'le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir', 'que', 'pour',
            'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'pas', 'tout', 'plus',
            'par', 'grand', 'en', 'une', 'autre', 'dont', 'lui', 'très', 'sa', 'me', 'jour',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their'
        }
        
        # Filtre les mots vides et trop courts
        meaningful_words = [
            word for word in self.words 
            if word not in stop_words and len(word) > 2
        ]
        
        word_counts = Counter(meaningful_words)
        return word_counts.most_common(top_n)
    
    def readability_score(self) -> Dict[str, float]:
        """
        Calcule des métriques de lisibilité.
        
        Returns:
            Dictionnaire avec les scores
        """
        stats = self.basic_stats()
        
        if stats["sentences"] == 0 or stats["words"] == 0:
            return {"avg_words_per_sentence": 0, "avg_chars_per_word": 0, "complexity": "N/A"}
        
        avg_words_per_sentence = stats["words"] / stats["sentences"]
        avg_chars_per_word = stats["characters_no_spaces"] / stats["words"]
        
        # Score de complexité simple basé sur la longueur moyenne
        if avg_words_per_sentence < 15 and avg_chars_per_word < 5:
            complexity = "Facile"
        elif avg_words_per_sentence < 20 and avg_chars_per_word < 6:
            complexity = "Moyen"
        else:
            complexity = "Difficile"
        
        return {
            "avg_words_per_sentence": round(avg_words_per_sentence, 2),
            "avg_chars_per_word": round(avg_chars_per_word, 2),
            "complexity": complexity
        }
    
    def find_patterns(self, pattern: str, case_sensitive: bool = False) -> List[Dict[str, any]]:
        """
        Recherche des motifs dans le texte.
        
        Args:
            pattern: Motif à rechercher (regex supporté)
            case_sensitive: Recherche sensible à la casse
            
        Returns:
            Liste des correspondances avec positions
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        matches = []
        
        try:
            for match in re.finditer(pattern, self.original_text, flags):
                matches.append({
                    "text": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "line": self.original_text[:match.start()].count('\n') + 1
                })
        except re.error as e:
            return [{"error": f"Erreur dans le motif : {e}"}]
        
        return matches
    
    def keyword_density(self, keywords: List[str]) -> Dict[str, Dict[str, any]]:
        """
        Calcule la densité des mots-clés.
        
        Args:
            keywords: Liste des mots-clés à analyser
            
        Returns:
            Dictionnaire avec statistiques par mot-clé
        """
        results = {}
        total_words = len(self.words)
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = self.words.count(keyword_lower)
            density = (count / total_words * 100) if total_words > 0 else 0
            
            results[keyword] = {
                "count": count,
                "density": round(density, 2),
                "positions": [i for i, word in enumerate(self.words) if word == keyword_lower]
            }
        
        return results
    
    def export_analysis(self, filename: str = "text_analysis.json") -> None:
        """
        Exporte l'analyse complète en JSON.
        
        Args:
            filename: Nom du fichier d'export
        """
        analysis = {
            "text_preview": self.original_text[:100] + "..." if len(self.original_text) > 100 else self.original_text,
            "basic_stats": self.basic_stats(),
            "readability": self.readability_score(),
            "top_words": self.word_frequency(15),
            "analysis_timestamp": str(__import__('datetime').datetime.now())
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"✅ Analyse exportée dans : {filename}")
        except Exception as e:
            print(f"❌ Erreur lors de l'export : {e}")


def load_text_from_file(filename: str) -> str:
    """
    Charge un texte depuis un fichier.
    
    Args:
        filename: Nom du fichier
        
    Returns:
        Contenu du fichier
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {filename}")
        return ""
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")
        return ""


def display_stats(analyzer: TextAnalyzer) -> None:
    """Affiche les statistiques de base."""
    stats = analyzer.basic_stats()
    
    print("\n📊 STATISTIQUES DE BASE")
    print("=" * 40)
    print(f"📝 Caractères (total)     : {stats['characters_total']:,}")
    print(f"🔤 Caractères (sans espaces): {stats['characters_no_spaces']:,}")
    print(f"📖 Mots                  : {stats['words']:,}")
    print(f"🆕 Mots uniques          : {stats['unique_words']:,}")
    print(f"📄 Phrases               : {stats['sentences']:,}")
    print(f"📑 Paragraphes           : {stats['paragraphs']:,}")


def display_readability(analyzer: TextAnalyzer) -> None:
    """Affiche les métriques de lisibilité."""
    readability = analyzer.readability_score()
    
    print("\n📚 LISIBILITÉ")
    print("=" * 40)
    print(f"📏 Mots/phrase (moyenne)   : {readability['avg_words_per_sentence']}")
    print(f"🔤 Caractères/mot (moyenne): {readability['avg_chars_per_word']}")
    print(f"🎯 Complexité              : {readability['complexity']}")


def display_word_frequency(analyzer: TextAnalyzer, top_n: int = 10) -> None:
    """Affiche la fréquence des mots."""
    freq = analyzer.word_frequency(top_n)
    
    print(f"\n🔝 TOP {top_n} DES MOTS LES PLUS FRÉQUENTS")
    print("=" * 50)
    
    for i, (word, count) in enumerate(freq, 1):
        percentage = (count / len(analyzer.words)) * 100
        print(f"{i:2d}. {word:<15} : {count:3d} fois ({percentage:.1f}%)")


def main():
    """Fonction principale avec interface interactive."""
    print("📝 ANALYSEUR DE TEXTE - MÉTHODE MARKOVA")
    print("=" * 50)
    
    analyzer = None
    
    while True:
        print("\n🎯 OPTIONS:")
        print("1. 📝 Saisir du texte manuellement")
        print("2. 📁 Charger depuis un fichier")
        print("3. 📊 Voir statistiques de base")
        print("4. 📚 Voir lisibilité")
        print("5. 🔝 Top mots fréquents")
        print("6. 🔍 Rechercher un motif")
        print("7. 🎯 Densité de mots-clés")
        print("8. 💾 Exporter l'analyse")
        print("0. 🚪 Quitter")
        print("-" * 50)
        
        choice = input("👉 Votre choix : ").strip()
        
        try:
            if choice == "0":
                print("👋 À bientôt !")
                break
            
            elif choice == "1":
                print("\n📝 Saisissez votre texte (Ctrl+D ou ligne vide pour terminer):")
                lines = []
                try:
                    while True:
                        line = input()
                        if not line:  # Ligne vide = fin
                            break
                        lines.append(line)
                except EOFError:  # Ctrl+D
                    pass
                
                text = '\n'.join(lines)
                if text.strip():
                    analyzer = TextAnalyzer(text)
                    print("✅ Texte chargé et analysé !")
                else:
                    print("❌ Aucun texte saisi")
            
            elif choice == "2":
                filename = input("📁 Nom du fichier : ").strip()
                text = load_text_from_file(filename)
                if text:
                    analyzer = TextAnalyzer(text)
                    print("✅ Fichier chargé et analysé !")
            
            elif choice in ["3", "4", "5", "6", "7", "8"]:
                if not analyzer:
                    print("❌ Veuillez d'abord charger un texte (options 1 ou 2)")
                    continue
                
                if choice == "3":
                    display_stats(analyzer)
                
                elif choice == "4":
                    display_readability(analyzer)
                
                elif choice == "5":
                    try:
                        n = int(input("🔢 Nombre de mots à afficher [10] : ") or "10")
                        display_word_frequency(analyzer, n)
                    except ValueError:
                        display_word_frequency(analyzer)
                
                elif choice == "6":
                    pattern = input("🔍 Motif à rechercher : ").strip()
                    if pattern:
                        case_sensitive = input("🔠 Sensible à la casse ? (o/N) : ").lower() in ['o', 'oui']
                        matches = analyzer.find_patterns(pattern, case_sensitive)
                        
                        if matches and 'error' not in matches[0]:
                            print(f"\n🎯 {len(matches)} correspondance(s) trouvée(s):")
                            for match in matches[:20]:  # Limite à 20 résultats
                                print(f"  📍 Ligne {match['line']}: '{match['text']}'")
                            if len(matches) > 20:
                                print(f"  ... et {len(matches) - 20} autres")
                        elif matches and 'error' in matches[0]:
                            print(f"❌ {matches[0]['error']}")
                        else:
                            print("❌ Aucune correspondance trouvée")
                
                elif choice == "7":
                    keywords_input = input("🎯 Mots-clés (séparés par des virgules) : ").strip()
                    if keywords_input:
                        keywords = [kw.strip() for kw in keywords_input.split(',')]
                        density = analyzer.keyword_density(keywords)
                        
                        print(f"\n🎯 DENSITÉ DES MOTS-CLÉS:")
                        print("=" * 40)
                        for keyword, data in density.items():
                            print(f"'{keyword}': {data['count']} fois ({data['density']}%)")
                
                elif choice == "8":
                    filename = input("💾 Nom du fichier [text_analysis.json] : ").strip()
                    if not filename:
                        filename = "text_analysis.json"
                    analyzer.export_analysis(filename)
            
            else:
                print("❌ Choix invalide")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu !")
            break
        except Exception as e:
            print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    main() 