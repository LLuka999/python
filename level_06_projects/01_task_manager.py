#!/usr/bin/env python3
"""
🚀 Gestionnaire de Tâches - Méthode Markova
===========================================

Un gestionnaire de tâches simple mais complet qui permet de :
- Ajouter des tâches avec priorités
- Marquer comme terminé/en cours
- Supprimer des tâches
- Voir les statistiques
- Sauvegarder automatiquement en JSON

Auteur: Méthode Markova
Niveau: 06 - Mini-projets concrets
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


class TaskManager:
    """Gestionnaire de tâches avec persistance JSON."""
    
    def __init__(self, filename: str = "tasks.json"):
        """
        Initialise le gestionnaire de tâches.
        
        Args:
            filename: Nom du fichier de sauvegarde
        """
        self.filename = filename
        self.tasks: List[Dict[str, Any]] = []
        self.load_tasks()
    
    def load_tasks(self) -> None:
        """Charge les tâches depuis le fichier JSON."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
                print(f"✅ {len(self.tasks)} tâche(s) chargée(s)")
            else:
                print("📝 Nouveau fichier de tâches créé")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️  Erreur lors du chargement : {e}")
            self.tasks = []
    
    def save_tasks(self) -> None:
        """Sauvegarde les tâches dans le fichier JSON."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
            print("💾 Tâches sauvegardées")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde : {e}")
    
    def add_task(self, description: str, priority: str = "normale") -> None:
        """
        Ajoute une nouvelle tâche.
        
        Args:
            description: Description de la tâche
            priority: Priorité (haute, normale, basse)
        """
        if not description.strip():
            print("❌ La description ne peut pas être vide")
            return
        
        task = {
            "id": len(self.tasks) + 1,
            "description": description.strip(),
            "priority": priority.lower(),
            "status": "en_cours",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.tasks.append(task)
        self.save_tasks()
        print(f"✅ Tâche ajoutée : {description}")
    
    def complete_task(self, task_id: int) -> None:
        """
        Marque une tâche comme terminée.
        
        Args:
            task_id: ID de la tâche à terminer
        """
        for task in self.tasks:
            if task["id"] == task_id:
                if task["status"] == "terminee":
                    print("ℹ️  Cette tâche est déjà terminée")
                    return
                
                task["status"] = "terminee"
                task["completed_at"] = datetime.now().isoformat()
                self.save_tasks()
                print(f"🎉 Tâche terminée : {task['description']}")
                return
        
        print(f"❌ Aucune tâche trouvée avec l'ID {task_id}")
    
    def delete_task(self, task_id: int) -> None:
        """
        Supprime une tâche.
        
        Args:
            task_id: ID de la tâche à supprimer
        """
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted_task = self.tasks.pop(i)
                self.save_tasks()
                print(f"🗑️  Tâche supprimée : {deleted_task['description']}")
                return
        
        print(f"❌ Aucune tâche trouvée avec l'ID {task_id}")
    
    def list_tasks(self, filter_status: str = "all") -> None:
        """
        Affiche la liste des tâches.
        
        Args:
            filter_status: Filtre par statut (all, en_cours, terminee)
        """
        if not self.tasks:
            print("📭 Aucune tâche trouvée")
            return
        
        # Filtre les tâches selon le statut
        if filter_status == "all":
            filtered_tasks = self.tasks
        else:
            filtered_tasks = [t for t in self.tasks if t["status"] == filter_status]
        
        if not filtered_tasks:
            print(f"📭 Aucune tâche avec le statut : {filter_status}")
            return
        
        print(f"\n📋 Liste des tâches ({filter_status}):")
        print("-" * 60)
        
        for task in filtered_tasks:
            status_icon = "✅" if task["status"] == "terminee" else "⏳"
            priority_icon = {"haute": "🔴", "normale": "🟡", "basse": "🟢"}.get(
                task["priority"], "⚪"
            )
            
            print(f"{status_icon} [{task['id']}] {priority_icon} {task['description']}")
            print(f"    Créée: {task['created_at'][:10]}")
            
            if task["completed_at"]:
                print(f"    Terminée: {task['completed_at'][:10]}")
            
            print()
    
    def show_statistics(self) -> None:
        """Affiche les statistiques des tâches."""
        if not self.tasks:
            print("📊 Aucune statistique disponible")
            return
        
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["status"] == "terminee"])
        in_progress = total - completed
        completion_rate = (completed / total) * 100 if total > 0 else 0
        
        print("\n📊 Statistiques:")
        print("-" * 30)
        print(f"📝 Total de tâches : {total}")
        print(f"✅ Terminées : {completed}")
        print(f"⏳ En cours : {in_progress}")
        print(f"📈 Taux de completion : {completion_rate:.1f}%")
        
        # Statistiques par priorité
        priorities = {}
        for task in self.tasks:
            priority = task["priority"]
            priorities[priority] = priorities.get(priority, 0) + 1
        
        print("\n🎯 Répartition par priorité :")
        for priority, count in priorities.items():
            icon = {"haute": "🔴", "normale": "🟡", "basse": "🟢"}.get(priority, "⚪")
            print(f"  {icon} {priority.title()}: {count}")


def show_menu() -> None:
    """Affiche le menu principal."""
    print("\n" + "="*50)
    print("🚀 GESTIONNAIRE DE TÂCHES - MÉTHODE MARKOVA")
    print("="*50)
    print("1. 📝 Ajouter une tâche")
    print("2. 📋 Voir toutes les tâches") 
    print("3. ⏳ Voir tâches en cours")
    print("4. ✅ Voir tâches terminées")
    print("5. 🎉 Marquer comme terminée")
    print("6. 🗑️  Supprimer une tâche")
    print("7. 📊 Voir les statistiques")
    print("0. 🚪 Quitter")
    print("-" * 50)


def main():
    """Fonction principale avec boucle interactive."""
    manager = TaskManager()
    
    print("🎯 Bienvenue dans votre gestionnaire de tâches !")
    
    while True:
        show_menu()
        
        try:
            choice = input("👉 Votre choix : ").strip()
            
            if choice == "0":
                print("👋 À bientôt ! Restez productif !")
                break
            
            elif choice == "1":
                description = input("📝 Description de la tâche : ")
                print("🎯 Priorité : (1) Haute, (2) Normale, (3) Basse")
                priority_choice = input("👉 Votre choix [2] : ").strip() or "2"
                
                priority_map = {"1": "haute", "2": "normale", "3": "basse"}
                priority = priority_map.get(priority_choice, "normale")
                
                manager.add_task(description, priority)
            
            elif choice == "2":
                manager.list_tasks("all")
            
            elif choice == "3":
                manager.list_tasks("en_cours")
            
            elif choice == "4":
                manager.list_tasks("terminee")
            
            elif choice == "5":
                manager.list_tasks("en_cours")
                try:
                    task_id = int(input("👉 ID de la tâche à terminer : "))
                    manager.complete_task(task_id)
                except ValueError:
                    print("❌ Veuillez entrer un ID valide")
            
            elif choice == "6":
                manager.list_tasks("all")
                try:
                    task_id = int(input("👉 ID de la tâche à supprimer : "))
                    confirm = input("⚠️  Êtes-vous sûr ? (o/N) : ").lower()
                    if confirm in ['o', 'oui', 'y', 'yes']:
                        manager.delete_task(task_id)
                    else:
                        print("❌ Suppression annulée")
                except ValueError:
                    print("❌ Veuillez entrer un ID valide")
            
            elif choice == "7":
                manager.show_statistics()
            
            else:
                print("❌ Choix invalide. Essayez encore.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu. À bientôt !")
            break
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")


if __name__ == "__main__":
    main() 