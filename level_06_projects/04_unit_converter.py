#!/usr/bin/env python3
"""
📏 Convertisseur d'Unités - Méthode Markova
============================================

Un convertisseur d'unités universel qui gère :
- Longueurs (mètres, pieds, pouces, etc.)
- Poids (kilogrammes, livres, onces, etc.)
- Températures (Celsius, Fahrenheit, Kelvin)
- Volumes (litres, gallons, etc.)
- Surfaces et plus !

Auteur: Méthode Markova
Niveau: 06 - Mini-projets concrets
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class ConversionResult:
    """Résultat d'une conversion."""
    value: float
    from_unit: str
    to_unit: str
    category: str
    
    def __str__(self) -> str:
        return f"{self.value:.6g} {self.to_unit}"


class UnitConverter:
    """Convertisseur d'unités universel."""
    
    def __init__(self):
        """Initialise le convertisseur avec toutes les unités."""
        self.conversions = {
            "longueur": {
                "name": "Longueur",
                "base_unit": "mètre",
                "units": {
                    # Vers mètres
                    "millimètre": 0.001,
                    "mm": 0.001,
                    "centimètre": 0.01,
                    "cm": 0.01,
                    "décimètre": 0.1,
                    "dm": 0.1,
                    "mètre": 1.0,
                    "m": 1.0,
                    "kilomètre": 1000.0,
                    "km": 1000.0,
                    
                    # Unités impériales
                    "pouce": 0.0254,
                    "inch": 0.0254,
                    "in": 0.0254,
                    "pied": 0.3048,
                    "foot": 0.3048,
                    "ft": 0.3048,
                    "yard": 0.9144,
                    "yd": 0.9144,
                    "mile": 1609.344,
                    "mi": 1609.344,
                    
                    # Unités nautiques
                    "mile nautique": 1852.0,
                    "nm": 1852.0,
                }
            },
            
            "poids": {
                "name": "Poids/Masse",
                "base_unit": "kilogramme",
                "units": {
                    # Vers kilogrammes
                    "milligramme": 0.000001,
                    "mg": 0.000001,
                    "gramme": 0.001,
                    "g": 0.001,
                    "kilogramme": 1.0,
                    "kg": 1.0,
                    "tonne": 1000.0,
                    "t": 1000.0,
                    
                    # Unités impériales
                    "once": 0.0283495,
                    "oz": 0.0283495,
                    "livre": 0.453592,
                    "lb": 0.453592,
                    "lbs": 0.453592,
                    "stone": 6.35029,
                    "st": 6.35029,
                }
            },
            
            "volume": {
                "name": "Volume",
                "base_unit": "litre",
                "units": {
                    # Vers litres
                    "millilitre": 0.001,
                    "ml": 0.001,
                    "centilitre": 0.01,
                    "cl": 0.01,
                    "décilitre": 0.1,
                    "dl": 0.1,
                    "litre": 1.0,
                    "l": 1.0,
                    
                    # Unités US
                    "once liquide US": 0.0295735,
                    "fl oz": 0.0295735,
                    "tasse US": 0.236588,
                    "cup": 0.236588,
                    "pinte US": 0.946353,
                    "pint": 0.946353,
                    "quart US": 0.946353,
                    "gallon US": 3.78541,
                    "gal": 3.78541,
                    
                    # Unités UK
                    "gallon UK": 4.54609,
                    "gallon imperial": 4.54609,
                }
            },
            
            "surface": {
                "name": "Surface",
                "base_unit": "mètre carré",
                "units": {
                    # Vers mètres carrés
                    "millimètre carré": 0.000001,
                    "mm²": 0.000001,
                    "centimètre carré": 0.0001,
                    "cm²": 0.0001,
                    "mètre carré": 1.0,
                    "m²": 1.0,
                    "hectare": 10000.0,
                    "ha": 10000.0,
                    "kilomètre carré": 1000000.0,
                    "km²": 1000000.0,
                    
                    # Unités impériales
                    "pouce carré": 0.00064516,
                    "in²": 0.00064516,
                    "pied carré": 0.092903,
                    "ft²": 0.092903,
                    "yard carré": 0.836127,
                    "yd²": 0.836127,
                    "acre": 4046.86,
                    "mile carré": 2589988.11,
                }
            },
            
            "vitesse": {
                "name": "Vitesse",
                "base_unit": "mètre par seconde",
                "units": {
                    # Vers m/s
                    "mètre par seconde": 1.0,
                    "m/s": 1.0,
                    "kilomètre par heure": 0.277778,
                    "km/h": 0.277778,
                    "kph": 0.277778,
                    "mile par heure": 0.44704,
                    "mph": 0.44704,
                    "nœud": 0.514444,
                    "knot": 0.514444,
                    "kt": 0.514444,
                }
            }
        }
    
    def get_categories(self) -> List[str]:
        """Retourne la liste des catégories disponibles."""
        return list(self.conversions.keys())
    
    def get_units(self, category: str) -> List[str]:
        """
        Retourne la liste des unités pour une catégorie.
        
        Args:
            category: Catégorie d'unités
            
        Returns:
            Liste des unités disponibles
        """
        if category not in self.conversions:
            return []
        return list(self.conversions[category]["units"].keys())
    
    def convert(self, value: float, from_unit: str, to_unit: str, category: str = None) -> ConversionResult:
        """
        Convertit une valeur d'une unité à une autre.
        
        Args:
            value: Valeur à convertir
            from_unit: Unité source
            to_unit: Unité cible
            category: Catégorie (optionnel, détectée automatiquement)
            
        Returns:
            Résultat de la conversion
            
        Raises:
            ValueError: Si les unités ne sont pas trouvées ou incompatibles
        """
        # Détecte automatiquement la catégorie si non spécifiée
        if category is None:
            category = self._find_category(from_unit, to_unit)
        
        if category not in self.conversions:
            raise ValueError(f"Catégorie inconnue : {category}")
        
        category_data = self.conversions[category]
        units = category_data["units"]
        
        # Normalise les noms d'unités (insensible à la casse)
        from_unit_key = self._normalize_unit_name(from_unit, units)
        to_unit_key = self._normalize_unit_name(to_unit, units)
        
        if from_unit_key not in units:
            raise ValueError(f"Unité source inconnue : {from_unit} (catégorie: {category})")
        
        if to_unit_key not in units:
            raise ValueError(f"Unité cible inconnue : {to_unit} (catégorie: {category})")
        
        # Conversion via l'unité de base
        base_value = value * units[from_unit_key]
        result_value = base_value / units[to_unit_key]
        
        return ConversionResult(
            value=result_value,
            from_unit=from_unit,
            to_unit=to_unit,
            category=category
        )
    
    def _find_category(self, from_unit: str, to_unit: str) -> str:
        """
        Trouve la catégorie contenant les deux unités.
        
        Args:
            from_unit: Unité source
            to_unit: Unité cible
            
        Returns:
            Nom de la catégorie
            
        Raises:
            ValueError: Si aucune catégorie commune n'est trouvée
        """
        for category, data in self.conversions.items():
            units = data["units"]
            from_normalized = self._normalize_unit_name(from_unit, units)
            to_normalized = self._normalize_unit_name(to_unit, units)
            
            if from_normalized in units and to_normalized in units:
                return category
        
        raise ValueError(f"Impossible de trouver une catégorie commune pour {from_unit} et {to_unit}")
    
    def _normalize_unit_name(self, unit_name: str, units_dict: Dict[str, float]) -> str:
        """
        Normalise le nom d'unité (insensible à la casse).
        
        Args:
            unit_name: Nom de l'unité à normaliser
            units_dict: Dictionnaire des unités de la catégorie
            
        Returns:
            Nom normalisé ou original si non trouvé
        """
        # Recherche exacte d'abord
        if unit_name in units_dict:
            return unit_name
        
        # Recherche insensible à la casse
        unit_lower = unit_name.lower()
        for unit_key in units_dict.keys():
            if unit_key.lower() == unit_lower:
                return unit_key
        
        return unit_name  # Retourne l'original si non trouvé


class TemperatureConverter:
    """Convertisseur spécialisé pour les températures."""
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convertit Celsius vers Fahrenheit."""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convertit Fahrenheit vers Celsius."""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """Convertit Celsius vers Kelvin."""
        return celsius + 273.15
    
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Convertit Kelvin vers Celsius."""
        return kelvin - 273.15
    
    @staticmethod
    def fahrenheit_to_kelvin(fahrenheit: float) -> float:
        """Convertit Fahrenheit vers Kelvin."""
        celsius = TemperatureConverter.fahrenheit_to_celsius(fahrenheit)
        return TemperatureConverter.celsius_to_kelvin(celsius)
    
    @staticmethod
    def kelvin_to_fahrenheit(kelvin: float) -> float:
        """Convertit Kelvin vers Fahrenheit."""
        celsius = TemperatureConverter.kelvin_to_celsius(kelvin)
        return TemperatureConverter.celsius_to_fahrenheit(celsius)
    
    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> ConversionResult:
        """
        Convertit entre unités de température.
        
        Args:
            value: Valeur à convertir
            from_unit: Unité source (C, F, K)
            to_unit: Unité cible (C, F, K)
            
        Returns:
            Résultat de la conversion
        """
        # Normalise les unités
        unit_map = {
            'c': 'celsius', 'celsius': 'celsius', '°c': 'celsius',
            'f': 'fahrenheit', 'fahrenheit': 'fahrenheit', '°f': 'fahrenheit',
            'k': 'kelvin', 'kelvin': 'kelvin'
        }
        
        from_norm = unit_map.get(from_unit.lower(), from_unit.lower())
        to_norm = unit_map.get(to_unit.lower(), to_unit.lower())
        
        # Matrice de conversion
        conversion_map = {
            ('celsius', 'fahrenheit'): cls.celsius_to_fahrenheit,
            ('fahrenheit', 'celsius'): cls.fahrenheit_to_celsius,
            ('celsius', 'kelvin'): cls.celsius_to_kelvin,
            ('kelvin', 'celsius'): cls.kelvin_to_celsius,
            ('fahrenheit', 'kelvin'): cls.fahrenheit_to_kelvin,
            ('kelvin', 'fahrenheit'): cls.kelvin_to_fahrenheit,
        }
        
        if from_norm == to_norm:
            result_value = value
        else:
            conversion_func = conversion_map.get((from_norm, to_norm))
            if not conversion_func:
                raise ValueError(f"Conversion impossible : {from_unit} vers {to_unit}")
            result_value = conversion_func(value)
        
        return ConversionResult(
            value=result_value,
            from_unit=from_unit,
            to_unit=to_unit,
            category="température"
        )


def display_categories(converter: UnitConverter) -> None:
    """Affiche les catégories disponibles."""
    print("\n📏 CATÉGORIES DISPONIBLES:")
    print("=" * 40)
    
    for i, category in enumerate(converter.get_categories(), 1):
        name = converter.conversions[category]["name"]
        print(f"{i}. {name} ({category})")
    
    print("6. 🌡️  Température")


def display_units(converter: UnitConverter, category: str) -> None:
    """Affiche les unités d'une catégorie."""
    if category not in converter.conversions:
        print(f"❌ Catégorie inconnue : {category}")
        return
    
    category_data = converter.conversions[category]
    print(f"\n📐 UNITÉS - {category_data['name'].upper()}:")
    print("=" * 50)
    
    units = list(category_data["units"].keys())
    
    # Affiche en colonnes
    for i in range(0, len(units), 3):
        row_units = units[i:i+3]
        print("  ".join(f"{unit:<15}" for unit in row_units))


def display_temperature_units() -> None:
    """Affiche les unités de température."""
    print("\n🌡️  UNITÉS DE TEMPÉRATURE:")
    print("=" * 40)
    print("• Celsius (C, °C)")
    print("• Fahrenheit (F, °F)")
    print("• Kelvin (K)")


def interactive_conversion(converter: UnitConverter, temp_converter: TemperatureConverter) -> None:
    """Interface de conversion interactive."""
    try:
        # Choix de la catégorie
        print("\n🎯 Choisissez une catégorie :")
        display_categories(converter)
        
        category_choice = input("\n👉 Numéro de catégorie : ").strip()
        
        if category_choice == "6":  # Température
            display_temperature_units()
            
            value = float(input("\n🔢 Valeur à convertir : "))
            from_unit = input("📥 Unité source (C/F/K) : ").strip()
            to_unit = input("📤 Unité cible (C/F/K) : ").strip()
            
            result = temp_converter.convert(value, from_unit, to_unit)
            
            print(f"\n✅ RÉSULTAT:")
            print(f"📊 {value} {from_unit} = {result}")
            
        else:
            # Catégories standards
            categories = list(converter.get_categories())
            
            try:
                category_index = int(category_choice) - 1
                if 0 <= category_index < len(categories):
                    category = categories[category_index]
                else:
                    print("❌ Numéro de catégorie invalide")
                    return
            except ValueError:
                print("❌ Veuillez entrer un numéro valide")
                return
            
            display_units(converter, category)
            
            value = float(input("\n🔢 Valeur à convertir : "))
            from_unit = input("📥 Unité source : ").strip()
            to_unit = input("📤 Unité cible : ").strip()
            
            result = converter.convert(value, from_unit, to_unit, category)
            
            print(f"\n✅ RÉSULTAT:")
            print(f"📊 {value} {from_unit} = {result}")
    
    except ValueError as e:
        print(f"❌ Erreur de conversion : {e}")
    except Exception as e:
        print(f"❌ Erreur : {e}")


def quick_conversion_examples() -> None:
    """Affiche des exemples de conversions courantes."""
    converter = UnitConverter()
    temp_converter = TemperatureConverter()
    
    print("\n🚀 EXEMPLES DE CONVERSIONS:")
    print("=" * 50)
    
    examples = [
        # Longueur
        (100, "cm", "m", "longueur"),
        (5, "ft", "m", "longueur"),
        (1, "mile", "km", "longueur"),
        
        # Poids
        (70, "kg", "lb", "poids"),
        (1, "t", "kg", "poids"),
        
        # Volume
        (1, "gal", "l", "volume"),
        (500, "ml", "cup", "volume"),
        
        # Surface
        (1, "hectare", "m²", "surface"),
        (100, "ft²", "m²", "surface"),
    ]
    
    for value, from_unit, to_unit, category in examples:
        try:
            result = converter.convert(value, from_unit, to_unit, category)
            print(f"• {value} {from_unit} = {result}")
        except Exception as e:
            print(f"• Erreur: {value} {from_unit} → {to_unit}: {e}")
    
    # Exemples température
    print("\n🌡️  Températures :")
    temp_examples = [
        (0, "C", "F"),
        (100, "C", "F"),
        (32, "F", "C"),
        (273.15, "K", "C"),
    ]
    
    for value, from_unit, to_unit in temp_examples:
        try:
            result = temp_converter.convert(value, from_unit, to_unit)
            print(f"• {value}°{from_unit} = {result}")
        except Exception as e:
            print(f"• Erreur: {value}°{from_unit} → °{to_unit}: {e}")


def main():
    """Fonction principale avec interface interactive."""
    converter = UnitConverter()
    temp_converter = TemperatureConverter()
    
    print("📏 CONVERTISSEUR D'UNITÉS - MÉTHODE MARKOVA")
    print("=" * 60)
    
    while True:
        print("\n🎯 OPTIONS:")
        print("1. 🔄 Convertir des unités")
        print("2. 📋 Voir toutes les catégories")
        print("3. 📐 Voir unités d'une catégorie")
        print("4. 🚀 Exemples de conversions")
        print("5. 🌡️  Conversion de température")
        print("0. 🚪 Quitter")
        print("-" * 50)
        
        choice = input("👉 Votre choix : ").strip()
        
        try:
            if choice == "0":
                print("👋 À bientôt !")
                break
            
            elif choice == "1":
                interactive_conversion(converter, temp_converter)
            
            elif choice == "2":
                display_categories(converter)
                display_temperature_units()
            
            elif choice == "3":
                display_categories(converter)
                category_input = input("\n👉 Nom de la catégorie : ").strip().lower()
                
                if category_input in converter.get_categories():
                    display_units(converter, category_input)
                elif category_input in ["température", "temperature", "temp"]:
                    display_temperature_units()
                else:
                    print("❌ Catégorie non trouvée")
            
            elif choice == "4":
                quick_conversion_examples()
            
            elif choice == "5":
                display_temperature_units()
                
                try:
                    value = float(input("\n🔢 Valeur : "))
                    from_unit = input("📥 De (C/F/K) : ").strip()
                    to_unit = input("📤 Vers (C/F/K) : ").strip()
                    
                    result = temp_converter.convert(value, from_unit, to_unit)
                    print(f"\n✅ {value}°{from_unit} = {result}")
                    
                except ValueError as e:
                    print(f"❌ Erreur : {e}")
            
            else:
                print("❌ Choix invalide")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu !")
            break
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")


if __name__ == "__main__":
    main() 