# 🚀 Guide du Framework ETL - Méthode Markova

## Vue d'ensemble

Le Framework ETL est un système complet d'ingénierie de données qui permet d'extraire, transformer et charger des données entre différentes sources. Il illustre les concepts fondamentaux du traitement de données à grande échelle.

## 🎯 Objectifs d'apprentissage

- **Architecture modulaire** : Comprendre la séparation des responsabilités
- **Connecteurs de données** : Interfacer avec différentes sources (SQL, NoSQL, fichiers)
- **Pipelines ETL** : Orchestrer des flux de transformation de données
- **Gestion d'erreurs** : Robustesse et monitoring
- **Performance** : Optimisation et métriques

## 📋 Fonctionnalités principales

### 🔌 Connecteurs disponibles

1. **SQLiteConnector** - Bases de données relationnelles
2. **ParquetConnector** - Fichiers colonnaires haute performance
3. **JSONConnector** - Documents NoSQL et APIs
4. **Architecture extensible** - Facile d'ajouter de nouveaux connecteurs

### 🔄 Transformations supportées

- **Filtrage** : Sélection de lignes selon des critères
- **Agrégation** : Regroupement et calculs statistiques
- **Nettoyage** : Gestion des valeurs manquantes et doublons
- **Colonnes calculées** : Expressions et formules personnalisées
- **Transformations custom** : Fonctions Python arbitraires

### 📊 Monitoring et métriques

- Logs détaillés de chaque étape
- Métriques de performance (temps, volumes)
- Statut d'exécution en temps réel
- Traçabilité complète des pipelines

## 🚀 Installation et démarrage

### Prérequis
```bash
pip install pandas pyarrow
```

### Lancement rapide
```bash
python 07_etl_framework.py
```

## 💡 Exemples d'utilisation

### 1. Pipeline basique : SQLite → Parquet

```python
# Créer le framework
framework = ETLFramework()

# Configurer les connecteurs
sqlite_conn = SQLiteConnector("data.db")
parquet_conn = ParquetConnector("output")

# Créer le pipeline
pipeline = framework.create_pipeline("export_sales")
pipeline.set_source(sqlite_conn).set_target(parquet_conn)
pipeline.add_filter("amount > 100")

# Exécuter
framework.run_pipeline("export_sales", 
                      extract_params={'table': 'sales'},
                      load_params={'file_name': 'sales_filtered.parquet'})
```

### 2. Pipeline avec agrégation

```python
pipeline = framework.create_pipeline("monthly_summary")
pipeline.set_source(sqlite_conn).set_target(json_conn)
pipeline.add_aggregation(
    group_by=['month', 'region'],
    agg_config={'revenue': 'sum', 'transactions': 'count'}
)
```

### 3. Transformation personnalisée

```python
def calculate_profit_margin(data):
    data['profit_margin'] = (data['revenue'] - data['cost']) / data['revenue'] * 100
    return data

pipeline.add_transformation(calculate_profit_margin)
```

## 🏗️ Architecture du système

### Composants principaux

1. **DataConnector** (classe abstraite)
   - Interface unifiée pour toutes les sources
   - Méthodes : `connect()`, `extract()`, `load()`

2. **ETLPipeline**
   - Orchestration des étapes ETL
   - Gestion des métriques et erreurs
   - Chaînage des transformations

3. **DataTransformer**
   - Bibliothèque de transformations courantes
   - Extensible avec fonctions custom

4. **ETLFramework**
   - Point d'entrée principal
   - Gestion des connecteurs et pipelines
   - Interface utilisateur

### Flux de données

```
Source → Extract → Transform → Load → Destination
  ↓         ↓         ↓         ↓         ↓
SQLite   Pandas    Filter    Pandas   Parquet
          DF      Aggregate   DF      /JSON
```

## 🎓 Concepts avancés

### 1. Gestion des erreurs

- **Retry automatique** : Nouvelles tentatives sur échec temporaire
- **Validation des données** : Vérification de la cohérence
- **Rollback** : Annulation en cas d'erreur critique

### 2. Performance

- **Traitement par chunks** : Gestion de gros volumes
- **Parallélisation** : Exécution simultanée de pipelines
- **Cache** : Réutilisation de résultats intermédiaires

### 3. Monitoring

- **Logs structurés** : Format standardisé pour l'analyse
- **Métriques temps réel** : Suivi de l'avancement
- **Alertes** : Notification en cas de problème

## 🔧 Extensions possibles

### Nouveaux connecteurs

```python
class PostgreSQLConnector(DataConnector):
    def __init__(self, connection_string):
        super().__init__("PostgreSQL")
        self.conn_string = connection_string
    
    def connect(self):
        # Implémentation PostgreSQL
        pass
```

### Transformations avancées

- **Machine Learning** : Intégration scikit-learn
- **Géospatial** : Traitement de données GPS
- **Time Series** : Analyse temporelle

### Intégrations

- **Apache Airflow** : Orchestration avancée
- **Apache Spark** : Traitement distribué
- **Cloud Storage** : AWS S3, Google Cloud Storage

## 📚 Exercices pratiques

### Niveau débutant
1. Créer un pipeline simple CSV → JSON
2. Ajouter un filtre sur les données
3. Calculer des statistiques de base

### Niveau intermédiaire
1. Pipeline multi-étapes avec agrégations
2. Gestion d'erreurs personnalisée
3. Transformation de données temporelles

### Niveau avancé
1. Pipeline temps réel avec monitoring
2. Optimisation des performances
3. Intégration de nouveaux connecteurs

## 🐛 Dépannage

### Erreurs courantes

1. **Module non trouvé** : `pip install pandas pyarrow`
2. **Fichier non trouvé** : Vérifier les chemins
3. **Mémoire insuffisante** : Traiter par chunks

### Performance

- **Données volumineuses** : Utiliser Parquet avec compression
- **Requêtes lentes** : Optimiser les filtres SQL
- **Transformations coûteuses** : Paralléliser le traitement

## 🌟 Bonnes pratiques

1. **Validation** : Toujours valider les données d'entrée
2. **Documentation** : Commenter les transformations complexes
3. **Tests** : Tester avec des jeux de données variés
4. **Versioning** : Garder un historique des pipelines
5. **Monitoring** : Surveiller les performances en production

## 📖 Ressources supplémentaires

- **Pandas Documentation** : https://pandas.pydata.org/
- **Apache Arrow/Parquet** : https://arrow.apache.org/
- **Data Engineering** : "Designing Data-Intensive Applications"
- **ETL Best Practices** : "The Data Warehouse Toolkit"

---

🎯 **Objectif** : Maîtriser les fondamentaux de l'ingénierie de données et comprendre comment construire des systèmes robustes de traitement de données.

Ce framework est une base solide pour apprendre les concepts ETL avant de passer à des solutions industrielles comme Apache Airflow, Spark ou des services cloud. 