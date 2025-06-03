#!/usr/bin/env python3
"""
🚀 Framework ETL - Méthode Markova
=================================

Framework d'ingénierie de données pour Extract, Transform, Load (ETL)
avec connecteurs pour SGBD, Parquet, NoSQL et plus encore.

Fonctionnalités :
• Extraction depuis multiples sources (SQL, NoSQL, fichiers)
• Transformations configurables (filtrage, agrégation, nettoyage)
• Chargement vers différentes destinations
• Pipeline configurable avec validation
• Monitoring et logging intégrés

Auteur: Méthode Markova
Niveau: 06 - Mini-projets concrets
"""

import json
import sqlite3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime, timedelta
from pathlib import Path
import logging
import time
import os
import sys

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_framework.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ETL_Framework')


class DataConnector:
    """Classe de base pour tous les connecteurs de données."""
    
    def __init__(self, name: str):
        self.name = name
        self.connection = None
        self.logger = logging.getLogger(f'Connector_{name}')
    
    def connect(self) -> bool:
        """Établit la connexion à la source de données."""
        raise NotImplementedError("Les sous-classes doivent implémenter connect()")
    
    def disconnect(self):
        """Ferme la connexion."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def extract(self, query: str = None, **kwargs) -> pd.DataFrame:
        """Extrait les données de la source."""
        raise NotImplementedError("Les sous-classes doivent implémenter extract()")
    
    def load(self, data: pd.DataFrame, destination: str, **kwargs) -> bool:
        """Charge les données vers la destination."""
        raise NotImplementedError("Les sous-classes doivent implémenter load()")


class SQLiteConnector(DataConnector):
    """Connecteur pour bases de données SQLite."""
    
    def __init__(self, db_path: str):
        super().__init__("SQLite")
        self.db_path = db_path
    
    def connect(self) -> bool:
        """Connexion à la base SQLite."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.logger.info(f"Connexion SQLite établie : {self.db_path}")
            return True
        except Exception as e:
            self.logger.error(f"Erreur connexion SQLite : {e}")
            return False
    
    def extract(self, query: str = None, table: str = None, **kwargs) -> pd.DataFrame:
        """Extrait des données depuis SQLite."""
        if not self.connection:
            if not self.connect():
                return pd.DataFrame()
        
        try:
            if query:
                df = pd.read_sql_query(query, self.connection)
            elif table:
                df = pd.read_sql_query(f"SELECT * FROM {table}", self.connection)
            else:
                # Liste toutes les tables
                tables = pd.read_sql_query(
                    "SELECT name FROM sqlite_master WHERE type='table'", 
                    self.connection
                )
                print("📋 Tables disponibles :", tables['name'].tolist())
                return pd.DataFrame()
            
            self.logger.info(f"Extraction réussie : {len(df)} lignes")
            return df
            
        except Exception as e:
            self.logger.error(f"Erreur extraction SQLite : {e}")
            return pd.DataFrame()
    
    def load(self, data: pd.DataFrame, table_name: str, **kwargs) -> bool:
        """Charge des données vers SQLite."""
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            if_exists = kwargs.get('if_exists', 'append')
            data.to_sql(table_name, self.connection, if_exists=if_exists, index=False)
            self.logger.info(f"Chargement réussi : {len(data)} lignes vers {table_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur chargement SQLite : {e}")
            return False


class ParquetConnector(DataConnector):
    """Connecteur pour fichiers Parquet."""
    
    def __init__(self, base_path: str = "data"):
        super().__init__("Parquet")
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def connect(self) -> bool:
        """Vérifie l'accès au répertoire."""
        try:
            if self.base_path.exists() and self.base_path.is_dir():
                self.logger.info(f"Accès Parquet configuré : {self.base_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Erreur accès Parquet : {e}")
            return False
    
    def extract(self, file_name: str, **kwargs) -> pd.DataFrame:
        """Lit un fichier Parquet."""
        try:
            file_path = self.base_path / file_name
            if not file_path.suffix:
                file_path = file_path.with_suffix('.parquet')
            
            if not file_path.exists():
                self.logger.warning(f"Fichier non trouvé : {file_path}")
                return pd.DataFrame()
            
            df = pd.read_parquet(file_path)
            self.logger.info(f"Lecture Parquet réussie : {len(df)} lignes depuis {file_name}")
            return df
            
        except Exception as e:
            self.logger.error(f"Erreur lecture Parquet : {e}")
            return pd.DataFrame()
    
    def load(self, data: pd.DataFrame, file_name: str, **kwargs) -> bool:
        """Écrit vers un fichier Parquet."""
        try:
            file_path = self.base_path / file_name
            if not file_path.suffix:
                file_path = file_path.with_suffix('.parquet')
            
            # Options de compression
            compression = kwargs.get('compression', 'snappy')
            
            data.to_parquet(file_path, compression=compression, index=False)
            self.logger.info(f"Écriture Parquet réussie : {len(data)} lignes vers {file_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur écriture Parquet : {e}")
            return False
    
    def list_files(self) -> List[str]:
        """Liste les fichiers Parquet disponibles."""
        try:
            return [f.name for f in self.base_path.glob("*.parquet")]
        except Exception:
            return []


class JSONConnector(DataConnector):
    """Connecteur pour fichiers JSON (simulant NoSQL)."""
    
    def __init__(self, base_path: str = "data"):
        super().__init__("JSON")
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def connect(self) -> bool:
        """Vérifie l'accès au répertoire."""
        return self.base_path.exists() and self.base_path.is_dir()
    
    def extract(self, file_name: str, **kwargs) -> pd.DataFrame:
        """Lit un fichier JSON."""
        try:
            file_path = self.base_path / file_name
            if not file_path.suffix:
                file_path = file_path.with_suffix('.json')
            
            if not file_path.exists():
                return pd.DataFrame()
            
            df = pd.read_json(file_path, **kwargs)
            self.logger.info(f"Lecture JSON réussie : {len(df)} lignes")
            return df
            
        except Exception as e:
            self.logger.error(f"Erreur lecture JSON : {e}")
            return pd.DataFrame()
    
    def load(self, data: pd.DataFrame, file_name: str, **kwargs) -> bool:
        """Écrit vers un fichier JSON."""
        try:
            file_path = self.base_path / file_name
            if not file_path.suffix:
                file_path = file_path.with_suffix('.json')
            
            orient = kwargs.get('orient', 'records')
            data.to_json(file_path, orient=orient, indent=2, force_ascii=False)
            self.logger.info(f"Écriture JSON réussie : {len(data)} lignes")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur écriture JSON : {e}")
            return False


class DataTransformer:
    """Classe pour les transformations de données."""
    
    def __init__(self):
        self.logger = logging.getLogger('DataTransformer')
    
    def filter_data(self, data: pd.DataFrame, condition: str) -> pd.DataFrame:
        """Filtre les données selon une condition."""
        try:
            filtered = data.query(condition)
            self.logger.info(f"Filtrage : {len(data)} -> {len(filtered)} lignes")
            return filtered
        except Exception as e:
            self.logger.error(f"Erreur filtrage : {e}")
            return data
    
    def aggregate_data(self, data: pd.DataFrame, group_by: List[str], 
                      agg_config: Dict[str, str]) -> pd.DataFrame:
        """Agrège les données."""
        try:
            grouped = data.groupby(group_by).agg(agg_config).reset_index()
            self.logger.info(f"Agrégation : {len(data)} -> {len(grouped)} lignes")
            return grouped
        except Exception as e:
            self.logger.error(f"Erreur agrégation : {e}")
            return data
    
    def clean_data(self, data: pd.DataFrame, **options) -> pd.DataFrame:
        """Nettoie les données."""
        try:
            cleaned = data.copy()
            
            # Supprime les doublons
            if options.get('remove_duplicates', False):
                cleaned = cleaned.drop_duplicates()
            
            # Gère les valeurs manquantes
            if options.get('fill_na'):
                cleaned = cleaned.fillna(options['fill_na'])
            elif options.get('drop_na', False):
                cleaned = cleaned.dropna()
            
            # Convertit les types
            if options.get('convert_types'):
                for col, dtype in options['convert_types'].items():
                    if col in cleaned.columns:
                        cleaned[col] = pd.to_datetime(cleaned[col]) if dtype == 'datetime' else cleaned[col].astype(dtype)
            
            self.logger.info(f"Nettoyage : {len(data)} -> {len(cleaned)} lignes")
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Erreur nettoyage : {e}")
            return data
    
    def add_computed_columns(self, data: pd.DataFrame, 
                           computations: Dict[str, str]) -> pd.DataFrame:
        """Ajoute des colonnes calculées."""
        try:
            result = data.copy()
            for col_name, expression in computations.items():
                result[col_name] = result.eval(expression)
            
            self.logger.info(f"Ajout de {len(computations)} colonnes calculées")
            return result
            
        except Exception as e:
            self.logger.error(f"Erreur colonnes calculées : {e}")
            return data


class ETLPipeline:
    """Pipeline ETL principal."""
    
    def __init__(self, name: str):
        self.name = name
        self.source_connector = None
        self.target_connector = None
        self.transformer = DataTransformer()
        self.steps = []
        self.logger = logging.getLogger(f'Pipeline_{name}')
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'rows_extracted': 0,
            'rows_loaded': 0,
            'status': 'PENDING'
        }
    
    def set_source(self, connector: DataConnector):
        """Définit la source de données."""
        self.source_connector = connector
        return self
    
    def set_target(self, connector: DataConnector):
        """Définit la cible de données."""
        self.target_connector = connector
        return self
    
    def add_transformation(self, transform_func: Callable, **kwargs):
        """Ajoute une transformation au pipeline."""
        self.steps.append({
            'type': 'transform',
            'function': transform_func,
            'kwargs': kwargs
        })
        return self
    
    def add_filter(self, condition: str):
        """Ajoute un filtre au pipeline."""
        self.steps.append({
            'type': 'filter',
            'condition': condition
        })
        return self
    
    def add_aggregation(self, group_by: List[str], agg_config: Dict[str, str]):
        """Ajoute une agrégation au pipeline."""
        self.steps.append({
            'type': 'aggregate',
            'group_by': group_by,
            'agg_config': agg_config
        })
        return self
    
    def run(self, extract_params: Dict = None, load_params: Dict = None) -> bool:
        """Exécute le pipeline ETL."""
        self.metrics['start_time'] = datetime.now()
        self.metrics['status'] = 'RUNNING'
        
        try:
            # EXTRACT
            self.logger.info(f"🚀 Début du pipeline '{self.name}'")
            
            if not self.source_connector:
                raise ValueError("Aucun connecteur source défini")
            
            extract_params = extract_params or {}
            data = self.source_connector.extract(**extract_params)
            
            if data.empty:
                self.logger.warning("Aucune donnée extraite")
                self.metrics['status'] = 'WARNING'
                return False
            
            self.metrics['rows_extracted'] = len(data)
            self.logger.info(f"✅ Extraction : {len(data)} lignes")
            
            # TRANSFORM
            for step in self.steps:
                if step['type'] == 'transform':
                    data = step['function'](data, **step['kwargs'])
                elif step['type'] == 'filter':
                    data = self.transformer.filter_data(data, step['condition'])
                elif step['type'] == 'aggregate':
                    data = self.transformer.aggregate_data(
                        data, step['group_by'], step['agg_config']
                    )
            
            # LOAD
            if self.target_connector:
                load_params = load_params or {}
                success = self.target_connector.load(data, **load_params)
                
                if success:
                    self.metrics['rows_loaded'] = len(data)
                    self.metrics['status'] = 'SUCCESS'
                    self.logger.info(f"✅ Chargement : {len(data)} lignes")
                else:
                    self.metrics['status'] = 'FAILED'
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur pipeline : {e}")
            self.metrics['status'] = 'FAILED'
            return False
            
        finally:
            self.metrics['end_time'] = datetime.now()
            duration = (self.metrics['end_time'] - self.metrics['start_time']).total_seconds()
            self.logger.info(f"🏁 Pipeline terminé en {duration:.2f}s - Status: {self.metrics['status']}")
    
    def get_metrics(self) -> Dict:
        """Retourne les métriques d'exécution."""
        metrics = self.metrics.copy()
        if metrics['start_time'] and metrics['end_time']:
            metrics['duration_seconds'] = (
                metrics['end_time'] - metrics['start_time']
            ).total_seconds()
        return metrics


class ETLFramework:
    """Framework ETL principal avec interface utilisateur."""
    
    def __init__(self):
        self.connectors = {}
        self.pipelines = {}
        self.logger = logging.getLogger('ETLFramework')
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Initialise des données d'exemple."""
        # Crée une base SQLite avec des données d'exemple
        db_path = "sample_data.db"
        if not Path(db_path).exists():
            conn = sqlite3.connect(db_path)
            
            # Table des ventes
            sales_data = pd.DataFrame({
                'id': range(1, 101),
                'product': ['Produit_A', 'Produit_B', 'Produit_C'] * 33 + ['Produit_A'],
                'quantity': [i % 10 + 1 for i in range(100)],
                'price': [round(10 + (i % 50) * 0.5, 2) for i in range(100)],
                'date': pd.date_range('2023-01-01', periods=100, freq='D'),
                'region': ['Nord', 'Sud', 'Est', 'Ouest'] * 25
            })
            sales_data.to_sql('sales', conn, if_exists='replace', index=False)
            
            # Table des clients
            clients_data = pd.DataFrame({
                'id': range(1, 51),
                'name': [f'Client_{i}' for i in range(1, 51)],
                'age': [20 + i % 60 for i in range(50)],
                'city': ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice'] * 10,
                'segment': ['Premium', 'Standard', 'Basic'] * 16 + ['Premium', 'Standard']
            })
            clients_data.to_sql('clients', conn, if_exists='replace', index=False)
            
            conn.close()
            self.logger.info("📊 Données d'exemple créées")
    
    def register_connector(self, name: str, connector: DataConnector):
        """Enregistre un connecteur."""
        self.connectors[name] = connector
        self.logger.info(f"📡 Connecteur '{name}' enregistré")
    
    def create_pipeline(self, name: str) -> ETLPipeline:
        """Crée un nouveau pipeline."""
        pipeline = ETLPipeline(name)
        self.pipelines[name] = pipeline
        return pipeline
    
    def run_pipeline(self, name: str, **kwargs) -> bool:
        """Exécute un pipeline par nom."""
        if name not in self.pipelines:
            self.logger.error(f"Pipeline '{name}' non trouvé")
            return False
        
        return self.pipelines[name].run(**kwargs)
    
    def list_connectors(self):
        """Affiche les connecteurs disponibles."""
        print("\n📡 CONNECTEURS DISPONIBLES :")
        print("-" * 40)
        for name, connector in self.connectors.items():
            status = "🟢 Connecté" if connector.connection else "🔴 Déconnecté"
            print(f"• {name:<15} ({connector.__class__.__name__}) - {status}")
    
    def list_pipelines(self):
        """Affiche les pipelines disponibles."""
        print("\n🔄 PIPELINES DISPONIBLES :")
        print("-" * 40)
        for name, pipeline in self.pipelines.items():
            status = pipeline.metrics['status']
            emoji = {'SUCCESS': '✅', 'FAILED': '❌', 'RUNNING': '🔄', 'PENDING': '⏳'}.get(status, '❓')
            print(f"• {name:<20} - {emoji} {status}")
    
    def show_pipeline_metrics(self, name: str):
        """Affiche les métriques d'un pipeline."""
        if name not in self.pipelines:
            print(f"❌ Pipeline '{name}' non trouvé")
            return
        
        metrics = self.pipelines[name].get_metrics()
        print(f"\n📊 MÉTRIQUES DU PIPELINE '{name}' :")
        print("-" * 50)
        print(f"Status           : {metrics['status']}")
        print(f"Lignes extraites : {metrics['rows_extracted']:,}")
        print(f"Lignes chargées  : {metrics['rows_loaded']:,}")
        
        if 'duration_seconds' in metrics:
            print(f"Durée            : {metrics['duration_seconds']:.2f}s")
        
        if metrics['start_time']:
            print(f"Début            : {metrics['start_time'].strftime('%H:%M:%S')}")
        if metrics['end_time']:
            print(f"Fin              : {metrics['end_time'].strftime('%H:%M:%S')}")


def clear_screen():
    """Efface l'écran."""
    os.system('cls' if os.name == 'nt' else 'clear')


def demo_basic_etl():
    """Démonstration ETL basique."""
    print("\n🎯 DÉMONSTRATION ETL BASIQUE")
    print("=" * 50)
    
    # Initialise le framework
    framework = ETLFramework()
    
    # Configure les connecteurs
    sqlite_conn = SQLiteConnector("sample_data.db")
    parquet_conn = ParquetConnector("data")
    json_conn = JSONConnector("data")
    
    framework.register_connector("sqlite", sqlite_conn)
    framework.register_connector("parquet", parquet_conn)
    framework.register_connector("json", json_conn)
    
    # Pipeline 1: SQLite -> Parquet
    print("\n🔄 Pipeline 1: Export des ventes vers Parquet")
    pipeline1 = framework.create_pipeline("sales_to_parquet")
    pipeline1.set_source(sqlite_conn).set_target(parquet_conn)
    pipeline1.add_filter("quantity > 5")
    
    success = framework.run_pipeline(
        "sales_to_parquet",
        extract_params={'table': 'sales'},
        load_params={'file_name': 'sales_filtered.parquet'}
    )
    
    if success:
        print("✅ Pipeline 1 terminé avec succès")
    
    # Pipeline 2: Agrégation et export JSON
    print("\n🔄 Pipeline 2: Agrégation des ventes par région")
    pipeline2 = framework.create_pipeline("sales_aggregation")
    pipeline2.set_source(sqlite_conn).set_target(json_conn)
    pipeline2.add_aggregation(
        group_by=['region', 'product'],
        agg_config={'quantity': 'sum', 'price': 'mean'}
    )
    
    success = framework.run_pipeline(
        "sales_aggregation",
        extract_params={'table': 'sales'},
        load_params={'file_name': 'sales_by_region.json'}
    )
    
    if success:
        print("✅ Pipeline 2 terminé avec succès")
    
    # Affiche les métriques
    framework.show_pipeline_metrics("sales_to_parquet")
    framework.show_pipeline_metrics("sales_aggregation")
    
    input("\n👉 Appuyez sur Entrée pour continuer...")


def demo_advanced_pipeline():
    """Démonstration pipeline avancé."""
    print("\n🚀 DÉMONSTRATION PIPELINE AVANCÉ")
    print("=" * 50)
    
    framework = ETLFramework()
    
    # Connecteurs
    sqlite_conn = SQLiteConnector("sample_data.db")
    parquet_conn = ParquetConnector("data")
    
    framework.register_connector("sqlite", sqlite_conn)
    framework.register_connector("parquet", parquet_conn)
    
    # Pipeline complexe avec transformations personnalisées
    def add_revenue_analysis(data: pd.DataFrame) -> pd.DataFrame:
        """Ajoute une analyse de revenus."""
        data = data.copy()
        data['revenue'] = data['quantity'] * data['price']
        data['month'] = pd.to_datetime(data['date']).dt.month
        data['revenue_category'] = pd.cut(
            data['revenue'], 
            bins=[0, 50, 100, 200, float('inf')], 
            labels=['Faible', 'Moyen', 'Élevé', 'Premium']
        )
        return data
    
    pipeline = framework.create_pipeline("advanced_sales_analysis")
    pipeline.set_source(sqlite_conn).set_target(parquet_conn)
    pipeline.add_transformation(add_revenue_analysis)
    pipeline.add_filter("revenue > 30")
    pipeline.add_aggregation(
        group_by=['region', 'revenue_category'],
        agg_config={'revenue': 'sum', 'quantity': 'count'}
    )
    
    success = framework.run_pipeline(
        "advanced_sales_analysis",
        extract_params={'table': 'sales'},
        load_params={'file_name': 'sales_analysis.parquet'}
    )
    
    if success:
        print("✅ Pipeline avancé terminé avec succès")
        framework.show_pipeline_metrics("advanced_sales_analysis")
    
    input("\n👉 Appuyez sur Entrée pour continuer...")


def interface_connecteurs(framework: ETLFramework):
    """Interface de gestion des connecteurs."""
    while True:
        clear_screen()
        print("📡 GESTION DES CONNECTEURS")
        print("=" * 40)
        
        framework.list_connectors()
        
        print("\n🎯 OPTIONS :")
        print("1. Ajouter connecteur SQLite")
        print("2. Ajouter connecteur Parquet")
        print("3. Ajouter connecteur JSON")
        print("4. Tester connexion")
        print("0. Retour au menu principal")
        
        choix = input("\n👉 Votre choix : ").strip()
        
        if choix == "0":
            break
        elif choix == "1":
            nom = input("📝 Nom du connecteur : ").strip()
            db_path = input("📂 Chemin de la base SQLite : ").strip()
            if nom and db_path:
                conn = SQLiteConnector(db_path)
                framework.register_connector(nom, conn)
                print(f"✅ Connecteur '{nom}' ajouté")
        elif choix == "2":
            nom = input("📝 Nom du connecteur : ").strip()
            data_path = input("📂 Répertoire des données (défaut: data) : ").strip() or "data"
            if nom:
                conn = ParquetConnector(data_path)
                framework.register_connector(nom, conn)
                print(f"✅ Connecteur '{nom}' ajouté")
        elif choix == "3":
            nom = input("📝 Nom du connecteur : ").strip()
            data_path = input("📂 Répertoire des données (défaut: data) : ").strip() or "data"
            if nom:
                conn = JSONConnector(data_path)
                framework.register_connector(nom, conn)
                print(f"✅ Connecteur '{nom}' ajouté")
        elif choix == "4":
            nom = input("📡 Nom du connecteur à tester : ").strip()
            if nom in framework.connectors:
                if framework.connectors[nom].connect():
                    print(f"✅ Connexion '{nom}' réussie")
                else:
                    print(f"❌ Échec connexion '{nom}'")
            else:
                print(f"❌ Connecteur '{nom}' non trouvé")
        
        if choix != "0":
            input("\n👉 Appuyez sur Entrée pour continuer...")


def interface_pipelines(framework: ETLFramework):
    """Interface de gestion des pipelines."""
    while True:
        clear_screen()
        print("🔄 GESTION DES PIPELINES")
        print("=" * 40)
        
        framework.list_pipelines()
        
        print("\n🎯 OPTIONS :")
        print("1. Créer pipeline simple")
        print("2. Exécuter pipeline")
        print("3. Voir métriques pipeline")
        print("4. Supprimer pipeline")
        print("0. Retour au menu principal")
        
        choix = input("\n👉 Votre choix : ").strip()
        
        if choix == "0":
            break
        elif choix == "1":
            nom = input("📝 Nom du pipeline : ").strip()
            if nom:
                pipeline = framework.create_pipeline(nom)
                
                # Configuration source
                print("\n📡 Connecteurs disponibles :")
                for name in framework.connectors.keys():
                    print(f"• {name}")
                
                source = input("🔍 Connecteur source : ").strip()
                target = input("🎯 Connecteur cible : ").strip()
                
                if source in framework.connectors and target in framework.connectors:
                    pipeline.set_source(framework.connectors[source])
                    pipeline.set_target(framework.connectors[target])
                    
                    # Ajouter un filtre optionnel
                    filtre = input("🔍 Filtre optionnel (ex: quantity > 5) : ").strip()
                    if filtre:
                        pipeline.add_filter(filtre)
                    
                    print(f"✅ Pipeline '{nom}' créé")
                else:
                    print("❌ Connecteur(s) invalide(s)")
        
        elif choix == "2":
            nom = input("🚀 Nom du pipeline à exécuter : ").strip()
            if nom in framework.pipelines:
                # Paramètres d'extraction
                table = input("📋 Table/fichier source : ").strip()
                destination = input("🎯 Destination : ").strip()
                
                extract_params = {'table': table} if table else {}
                load_params = {'table_name': destination} if destination else {}
                
                if framework.run_pipeline(nom, extract_params=extract_params, load_params=load_params):
                    print(f"✅ Pipeline '{nom}' exécuté avec succès")
                else:
                    print(f"❌ Échec du pipeline '{nom}'")
            else:
                print(f"❌ Pipeline '{nom}' non trouvé")
        
        elif choix == "3":
            nom = input("📊 Nom du pipeline : ").strip()
            if nom in framework.pipelines:
                framework.show_pipeline_metrics(nom)
            else:
                print(f"❌ Pipeline '{nom}' non trouvé")
        
        elif choix == "4":
            nom = input("🗑️ Nom du pipeline à supprimer : ").strip()
            if nom in framework.pipelines:
                del framework.pipelines[nom]
                print(f"✅ Pipeline '{nom}' supprimé")
            else:
                print(f"❌ Pipeline '{nom}' non trouvé")
        
        if choix != "0":
            input("\n👉 Appuyez sur Entrée pour continuer...")


def main():
    """Interface principale du framework ETL."""
    framework = ETLFramework()
    
    # Initialise les connecteurs par défaut
    sqlite_conn = SQLiteConnector("sample_data.db")
    parquet_conn = ParquetConnector("data")
    json_conn = JSONConnector("data")
    
    framework.register_connector("sqlite_default", sqlite_conn)
    framework.register_connector("parquet_default", parquet_conn)
    framework.register_connector("json_default", json_conn)
    
    while True:
        clear_screen()
        print("🚀 FRAMEWORK ETL - MÉTHODE MARKOVA")
        print("=" * 60)
        print("Framework d'ingénierie de données avec connecteurs multiples")
        print()
        
        print("🎯 MENU PRINCIPAL :")
        print("1. 🎬 Démonstration ETL basique")
        print("2. 🚀 Démonstration pipeline avancé")
        print("3. 📡 Gestion des connecteurs")
        print("4. 🔄 Gestion des pipelines")
        print("5. 📊 Voir tous les métriques")
        print("6. 📁 Explorer les fichiers générés")
        print("0. 🚪 Quitter")
        print("-" * 60)
        
        choix = input("👉 Votre choix : ").strip()
        
        try:
            if choix == "0":
                clear_screen()
                print("👋 Merci d'avoir utilisé le Framework ETL !")
                print("🚀 Continuez à explorer l'ingénierie de données !")
                break
            
            elif choix == "1":
                demo_basic_etl()
            
            elif choix == "2":
                demo_advanced_pipeline()
            
            elif choix == "3":
                interface_connecteurs(framework)
            
            elif choix == "4":
                interface_pipelines(framework)
            
            elif choix == "5":
                clear_screen()
                print("📊 MÉTRIQUES DE TOUS LES PIPELINES")
                print("=" * 50)
                for name in framework.pipelines.keys():
                    framework.show_pipeline_metrics(name)
                    print()
                input("\n👉 Appuyez sur Entrée pour continuer...")
            
            elif choix == "6":
                clear_screen()
                print("📁 FICHIERS GÉNÉRÉS")
                print("=" * 30)
                
                data_path = Path("data")
                if data_path.exists():
                    files = list(data_path.glob("*"))
                    if files:
                        for file in files:
                            size = file.stat().st_size
                            print(f"📄 {file.name:<25} ({size:,} octets)")
                    else:
                        print("📭 Aucun fichier généré")
                else:
                    print("📭 Répertoire 'data' non trouvé")
                
                print(f"\n🗄️ Base SQLite : sample_data.db")
                if Path("sample_data.db").exists():
                    size = Path("sample_data.db").stat().st_size
                    print(f"   Taille : {size:,} octets")
                
                input("\n👉 Appuyez sur Entrée pour continuer...")
            
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
    # Vérification des dépendances
    try:
        import pandas as pd
        import pyarrow as pa
        import pyarrow.parquet as pq
        main()
    except ImportError as e:
        print("❌ Dépendance manquante :")
        print(f"   {e}")
        print("\n💡 Installez les dépendances avec :")
        print("   pip install pandas pyarrow") 