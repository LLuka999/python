#!/usr/bin/env python3
"""
👥 Carnet d'Adresses - Méthode Markova
======================================

Un carnet d'adresses complet avec :
- Base de données SQLite pour la persistance
- Gestion complète des contacts (CRUD)
- Recherche et filtrage avancés
- Export/Import des données
- Interface utilisateur intuitive

Auteur: Méthode Markova
Niveau: 06 - Mini-projets concrets
"""

import sqlite3
import json
import csv
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import os


@dataclass
class Contact:
    """Représente un contact avec toutes ses informations."""
    id: Optional[int] = None
    nom: str = ""
    prenom: str = ""
    telephone: str = ""
    email: str = ""
    adresse: str = ""
    ville: str = ""
    code_postal: str = ""
    pays: str = ""
    profession: str = ""
    entreprise: str = ""
    notes: str = ""
    date_creation: Optional[str] = None
    date_modification: Optional[str] = None
    
    def nom_complet(self) -> str:
        """Retourne le nom complet."""
        return f"{self.prenom} {self.nom}".strip()
    
    def __str__(self) -> str:
        """Représentation string du contact."""
        return f"{self.nom_complet()} ({self.telephone})"


class AddressBookDB:
    """Gestionnaire de base de données pour le carnet d'adresses."""
    
    def __init__(self, db_path: str = "carnet_adresses.db"):
        """
        Initialise la base de données.
        
        Args:
            db_path: Chemin vers le fichier de base de données
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self) -> None:
        """Initialise la structure de la base de données."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    telephone TEXT,
                    email TEXT,
                    adresse TEXT,
                    ville TEXT,
                    code_postal TEXT,
                    pays TEXT,
                    profession TEXT,
                    entreprise TEXT,
                    notes TEXT,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Index pour optimiser les recherches
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_nom_prenom 
                ON contacts(nom, prenom)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_email 
                ON contacts(email)
            """)
            
            conn.commit()
    
    def ajouter_contact(self, contact: Contact) -> int:
        """
        Ajoute un nouveau contact.
        
        Args:
            contact: Contact à ajouter
            
        Returns:
            ID du contact créé
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO contacts (
                    nom, prenom, telephone, email, adresse, ville,
                    code_postal, pays, profession, entreprise, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contact.nom, contact.prenom, contact.telephone, contact.email,
                contact.adresse, contact.ville, contact.code_postal, contact.pays,
                contact.profession, contact.entreprise, contact.notes
            ))
            
            contact_id = cursor.lastrowid
            conn.commit()
            return contact_id
    
    def modifier_contact(self, contact: Contact) -> bool:
        """
        Modifie un contact existant.
        
        Args:
            contact: Contact avec les nouvelles données
            
        Returns:
            True si le contact a été modifié, False sinon
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE contacts SET
                    nom = ?, prenom = ?, telephone = ?, email = ?,
                    adresse = ?, ville = ?, code_postal = ?, pays = ?,
                    profession = ?, entreprise = ?, notes = ?,
                    date_modification = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (
                contact.nom, contact.prenom, contact.telephone, contact.email,
                contact.adresse, contact.ville, contact.code_postal, contact.pays,
                contact.profession, contact.entreprise, contact.notes, contact.id
            ))
            
            success = cursor.rowcount > 0
            conn.commit()
            return success
    
    def supprimer_contact(self, contact_id: int) -> bool:
        """
        Supprime un contact.
        
        Args:
            contact_id: ID du contact à supprimer
            
        Returns:
            True si le contact a été supprimé, False sinon
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            
            success = cursor.rowcount > 0
            conn.commit()
            return success
    
    def obtenir_contact(self, contact_id: int) -> Optional[Contact]:
        """
        Récupère un contact par son ID.
        
        Args:
            contact_id: ID du contact
            
        Returns:
            Contact trouvé ou None
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_contact(row)
            return None
    
    def lister_contacts(self, tri: str = "nom") -> List[Contact]:
        """
        Liste tous les contacts.
        
        Args:
            tri: Champ de tri (nom, prenom, date_creation)
            
        Returns:
            Liste des contacts triés
        """
        valid_sorts = ["nom", "prenom", "date_creation", "date_modification"]
        if tri not in valid_sorts:
            tri = "nom"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM contacts ORDER BY {tri}, prenom")
            rows = cursor.fetchall()
            
            return [self._row_to_contact(row) for row in rows]
    
    def rechercher_contacts(self, terme: str) -> List[Contact]:
        """
        Recherche des contacts par terme.
        
        Args:
            terme: Terme de recherche
            
        Returns:
            Liste des contacts correspondants
        """
        terme_like = f"%{terme}%"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM contacts 
                WHERE nom LIKE ? OR prenom LIKE ? OR telephone LIKE ? 
                   OR email LIKE ? OR entreprise LIKE ? OR ville LIKE ?
                ORDER BY nom, prenom
            """, (terme_like, terme_like, terme_like, terme_like, terme_like, terme_like))
            
            rows = cursor.fetchall()
            return [self._row_to_contact(row) for row in rows]
    
    def obtenir_statistiques(self) -> Dict[str, any]:
        """
        Calcule des statistiques sur le carnet d'adresses.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Nombre total de contacts
            cursor.execute("SELECT COUNT(*) FROM contacts")
            total = cursor.fetchone()[0]
            
            # Contacts avec email
            cursor.execute("SELECT COUNT(*) FROM contacts WHERE email != ''")
            avec_email = cursor.fetchone()[0]
            
            # Contacts avec téléphone
            cursor.execute("SELECT COUNT(*) FROM contacts WHERE telephone != ''")
            avec_telephone = cursor.fetchone()[0]
            
            # Villes les plus représentées
            cursor.execute("""
                SELECT ville, COUNT(*) as count 
                FROM contacts 
                WHERE ville != '' 
                GROUP BY ville 
                ORDER BY count DESC 
                LIMIT 5
            """)
            villes_top = cursor.fetchall()
            
            # Entreprises les plus représentées
            cursor.execute("""
                SELECT entreprise, COUNT(*) as count 
                FROM contacts 
                WHERE entreprise != '' 
                GROUP BY entreprise 
                ORDER BY count DESC 
                LIMIT 5
            """)
            entreprises_top = cursor.fetchall()
            
            return {
                "total_contacts": total,
                "avec_email": avec_email,
                "avec_telephone": avec_telephone,
                "taux_email": (avec_email / total * 100) if total > 0 else 0,
                "taux_telephone": (avec_telephone / total * 100) if total > 0 else 0,
                "villes_top": villes_top,
                "entreprises_top": entreprises_top
            }
    
    def _row_to_contact(self, row: sqlite3.Row) -> Contact:
        """Convertit une ligne de base de données en Contact."""
        return Contact(
            id=row["id"],
            nom=row["nom"],
            prenom=row["prenom"],
            telephone=row["telephone"] or "",
            email=row["email"] or "",
            adresse=row["adresse"] or "",
            ville=row["ville"] or "",
            code_postal=row["code_postal"] or "",
            pays=row["pays"] or "",
            profession=row["profession"] or "",
            entreprise=row["entreprise"] or "",
            notes=row["notes"] or "",
            date_creation=row["date_creation"],
            date_modification=row["date_modification"]
        )


class AddressBook:
    """Carnet d'adresses principal avec interface utilisateur."""
    
    def __init__(self, db_path: str = "carnet_adresses.db"):
        """Initialise le carnet d'adresses."""
        self.db = AddressBookDB(db_path)
    
    def valider_email(self, email: str) -> bool:
        """
        Valide le format d'un email.
        
        Args:
            email: Email à valider
            
        Returns:
            True si l'email est valide, False sinon
        """
        if not email:
            return True  # Email optionnel
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def valider_telephone(self, telephone: str) -> bool:
        """
        Valide le format d'un numéro de téléphone.
        
        Args:
            telephone: Numéro à valider
            
        Returns:
            True si le numéro est valide, False sinon
        """
        if not telephone:
            return True  # Téléphone optionnel
        
        # Supprime les espaces et caractères spéciaux pour la validation
        clean_phone = re.sub(r'[^\d+]', '', telephone)
        # Accepte les numéros de 8 à 15 chiffres (avec éventuel +)
        return len(clean_phone) >= 8 and len(clean_phone) <= 16
    
    def saisir_contact(self, contact: Optional[Contact] = None) -> Optional[Contact]:
        """
        Interface de saisie/modification d'un contact.
        
        Args:
            contact: Contact existant à modifier (None pour nouveau)
            
        Returns:
            Contact saisi ou None si annulé
        """
        if contact is None:
            contact = Contact()
            mode = "NOUVEAU"
        else:
            mode = "MODIFICATION"
        
        print(f"\n📝 {mode} CONTACT")
        print("=" * 40)
        print("(Appuyez sur Entrée pour garder la valeur actuelle)")
        
        # Champs obligatoires
        while True:
            nom = input(f"👤 Nom [{contact.nom}] : ").strip()
            if nom:
                contact.nom = nom
                break
            elif contact.nom:
                break
            else:
                print("❌ Le nom est obligatoire")
        
        while True:
            prenom = input(f"👤 Prénom [{contact.prenom}] : ").strip()
            if prenom:
                contact.prenom = prenom
                break
            elif contact.prenom:
                break
            else:
                print("❌ Le prénom est obligatoire")
        
        # Téléphone avec validation
        while True:
            telephone = input(f"📞 Téléphone [{contact.telephone}] : ").strip()
            if telephone:
                if self.valider_telephone(telephone):
                    contact.telephone = telephone
                    break
                else:
                    print("❌ Format de téléphone invalide")
            else:
                if contact.telephone or not telephone:
                    break
        
        # Email avec validation
        while True:
            email = input(f"📧 Email [{contact.email}] : ").strip()
            if email:
                if self.valider_email(email):
                    contact.email = email
                    break
                else:
                    print("❌ Format d'email invalide")
            else:
                break
        
        # Champs optionnels
        champs_optionnels = [
            ("🏠 Adresse", "adresse"),
            ("🏙️  Ville", "ville"),
            ("📮 Code postal", "code_postal"),
            ("🌍 Pays", "pays"),
            ("💼 Profession", "profession"),
            ("🏢 Entreprise", "entreprise"),
            ("📝 Notes", "notes")
        ]
        
        for label, attr in champs_optionnels:
            valeur_actuelle = getattr(contact, attr)
            nouvelle_valeur = input(f"{label} [{valeur_actuelle}] : ").strip()
            if nouvelle_valeur:
                setattr(contact, attr, nouvelle_valeur)
        
        return contact
    
    def afficher_contact(self, contact: Contact, detaille: bool = True) -> None:
        """
        Affiche un contact.
        
        Args:
            contact: Contact à afficher
            detaille: Affichage détaillé ou résumé
        """
        if not detaille:
            print(f"[{contact.id:3d}] {contact.nom_complet():<25} {contact.telephone:<15} {contact.email}")
            return
        
        print(f"\n👤 CONTACT #{contact.id}")
        print("=" * 50)
        print(f"👤 Nom complet     : {contact.nom_complet()}")
        
        if contact.telephone:
            print(f"📞 Téléphone       : {contact.telephone}")
        if contact.email:
            print(f"📧 Email           : {contact.email}")
        if contact.adresse:
            print(f"🏠 Adresse         : {contact.adresse}")
        if contact.ville or contact.code_postal:
            print(f"🏙️  Ville           : {contact.ville} {contact.code_postal}")
        if contact.pays:
            print(f"🌍 Pays            : {contact.pays}")
        if contact.profession:
            print(f"💼 Profession      : {contact.profession}")
        if contact.entreprise:
            print(f"🏢 Entreprise      : {contact.entreprise}")
        if contact.notes:
            print(f"📝 Notes           : {contact.notes}")
        
        print(f"\n📅 Créé le         : {contact.date_creation}")
        if contact.date_modification != contact.date_creation:
            print(f"📅 Modifié le      : {contact.date_modification}")
    
    def lister_contacts_resume(self, contacts: List[Contact]) -> None:
        """Affiche une liste résumée des contacts."""
        if not contacts:
            print("📭 Aucun contact trouvé")
            return
        
        print(f"\n📋 {len(contacts)} CONTACT(S) TROUVÉ(S):")
        print("=" * 80)
        print(f"{'ID':>3} {'Nom complet':<25} {'Téléphone':<15} {'Email'}")
        print("-" * 80)
        
        for contact in contacts:
            self.afficher_contact(contact, detaille=False)
    
    def rechercher_et_afficher(self) -> None:
        """Interface de recherche de contacts."""
        terme = input("🔍 Terme de recherche : ").strip()
        if not terme:
            print("❌ Terme de recherche vide")
            return
        
        contacts = self.db.rechercher_contacts(terme)
        self.lister_contacts_resume(contacts)
        
        if contacts:
            try:
                choix = input("\n👉 ID du contact à voir en détail (Entrée pour annuler) : ").strip()
                if choix:
                    contact_id = int(choix)
                    contact = next((c for c in contacts if c.id == contact_id), None)
                    if contact:
                        self.afficher_contact(contact)
                    else:
                        print("❌ Contact non trouvé dans les résultats")
            except ValueError:
                print("❌ ID invalide")
    
    def exporter_contacts(self, format_export: str = "json") -> None:
        """
        Exporte les contacts.
        
        Args:
            format_export: Format d'export (json, csv)
        """
        contacts = self.db.lister_contacts()
        if not contacts:
            print("❌ Aucun contact à exporter")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            if format_export.lower() == "json":
                filename = f"contacts_export_{timestamp}.json"
                
                contacts_data = []
                for contact in contacts:
                    contact_dict = asdict(contact)
                    contacts_data.append(contact_dict)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(contacts_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ {len(contacts)} contact(s) exporté(s) vers {filename}")
            
            elif format_export.lower() == "csv":
                filename = f"contacts_export_{timestamp}.csv"
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # En-têtes
                    headers = [
                        "ID", "Nom", "Prénom", "Téléphone", "Email", "Adresse",
                        "Ville", "Code postal", "Pays", "Profession", "Entreprise",
                        "Notes", "Date création", "Date modification"
                    ]
                    writer.writerow(headers)
                    
                    # Données
                    for contact in contacts:
                        row = [
                            contact.id, contact.nom, contact.prenom, contact.telephone,
                            contact.email, contact.adresse, contact.ville, contact.code_postal,
                            contact.pays, contact.profession, contact.entreprise,
                            contact.notes, contact.date_creation, contact.date_modification
                        ]
                        writer.writerow(row)
                
                print(f"✅ {len(contacts)} contact(s) exporté(s) vers {filename}")
            
            else:
                print("❌ Format d'export non supporté (json, csv)")
        
        except Exception as e:
            print(f"❌ Erreur lors de l'export : {e}")
    
    def afficher_statistiques(self) -> None:
        """Affiche les statistiques du carnet d'adresses."""
        stats = self.db.obtenir_statistiques()
        
        print("\n📊 STATISTIQUES DU CARNET D'ADRESSES")
        print("=" * 50)
        print(f"📝 Total de contacts    : {stats['total_contacts']}")
        print(f"📧 Avec email          : {stats['avec_email']} ({stats['taux_email']:.1f}%)")
        print(f"📞 Avec téléphone      : {stats['avec_telephone']} ({stats['taux_telephone']:.1f}%)")
        
        if stats['villes_top']:
            print(f"\n🏙️  Top des villes :")
            for ville, count in stats['villes_top']:
                print(f"   • {ville}: {count} contact(s)")
        
        if stats['entreprises_top']:
            print(f"\n🏢 Top des entreprises :")
            for entreprise, count in stats['entreprises_top']:
                print(f"   • {entreprise}: {count} contact(s)")


def main():
    """Fonction principale avec interface interactive."""
    carnet = AddressBook()
    
    print("👥 CARNET D'ADRESSES - MÉTHODE MARKOVA")
    print("=" * 50)
    
    while True:
        print("\n🎯 MENU PRINCIPAL:")
        print("1. 📝 Ajouter un contact")
        print("2. 📋 Lister tous les contacts")
        print("3. 🔍 Rechercher des contacts")
        print("4. 👤 Voir un contact")
        print("5. ✏️  Modifier un contact")
        print("6. 🗑️  Supprimer un contact")
        print("7. 📊 Statistiques")
        print("8. 💾 Exporter les contacts")
        print("0. 🚪 Quitter")
        print("-" * 50)
        
        choix = input("👉 Votre choix : ").strip()
        
        try:
            if choix == "0":
                print("👋 À bientôt !")
                break
            
            elif choix == "1":
                contact = carnet.saisir_contact()
                if contact:
                    contact_id = carnet.db.ajouter_contact(contact)
                    print(f"✅ Contact ajouté avec l'ID {contact_id}")
                else:
                    print("❌ Ajout annulé")
            
            elif choix == "2":
                contacts = carnet.db.lister_contacts()
                carnet.lister_contacts_resume(contacts)
            
            elif choix == "3":
                carnet.rechercher_et_afficher()
            
            elif choix == "4":
                contact_id = input("👤 ID du contact : ").strip()
                if contact_id.isdigit():
                    contact = carnet.db.obtenir_contact(int(contact_id))
                    if contact:
                        carnet.afficher_contact(contact)
                    else:
                        print("❌ Contact non trouvé")
                else:
                    print("❌ ID invalide")
            
            elif choix == "5":
                contact_id = input("✏️  ID du contact à modifier : ").strip()
                if contact_id.isdigit():
                    contact = carnet.db.obtenir_contact(int(contact_id))
                    if contact:
                        contact_modifie = carnet.saisir_contact(contact)
                        if contact_modifie and carnet.db.modifier_contact(contact_modifie):
                            print("✅ Contact modifié avec succès")
                        else:
                            print("❌ Modification échouée")
                    else:
                        print("❌ Contact non trouvé")
                else:
                    print("❌ ID invalide")
            
            elif choix == "6":
                contact_id = input("🗑️  ID du contact à supprimer : ").strip()
                if contact_id.isdigit():
                    contact = carnet.db.obtenir_contact(int(contact_id))
                    if contact:
                        carnet.afficher_contact(contact)
                        confirmation = input("\n⚠️  Êtes-vous sûr de vouloir supprimer ce contact ? (oui/NON) : ")
                        if confirmation.lower() in ['oui', 'o', 'yes', 'y']:
                            if carnet.db.supprimer_contact(int(contact_id)):
                                print("✅ Contact supprimé avec succès")
                            else:
                                print("❌ Suppression échouée")
                        else:
                            print("❌ Suppression annulée")
                    else:
                        print("❌ Contact non trouvé")
                else:
                    print("❌ ID invalide")
            
            elif choix == "7":
                carnet.afficher_statistiques()
            
            elif choix == "8":
                print("\n💾 Format d'export :")
                print("1. JSON")
                print("2. CSV")
                format_choix = input("👉 Votre choix [1] : ").strip() or "1"
                
                if format_choix == "1":
                    carnet.exporter_contacts("json")
                elif format_choix == "2":
                    carnet.exporter_contacts("csv")
                else:
                    print("❌ Format invalide")
            
            else:
                print("❌ Choix invalide")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu !")
            break
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")


if __name__ == "__main__":
    main() 