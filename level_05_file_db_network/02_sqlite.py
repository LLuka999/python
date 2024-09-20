"""
Utilisation de SQLite en Python
- Création de table
- Insertion
- Requête
- Mise à jour
- Suppression
"""
import sqlite3

# Connexion à la base (fichier local)
conn = sqlite3.connect("exemple.db")
cursor = conn.cursor()

# Création d'une table
cursor.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    age INTEGER
)
""")

# Insertion de données
cursor.execute("INSERT INTO utilisateurs (nom, age) VALUES (?, ?)", ("Alice", 30))
cursor.execute("INSERT INTO utilisateurs (nom, age) VALUES (?, ?)", ("Bob", 25))
conn.commit()

# Requête
cursor.execute("SELECT * FROM utilisateurs")
print("Utilisateurs :")
for row in cursor.fetchall():
    print(row)

# Mise à jour
cursor.execute("UPDATE utilisateurs SET age = ? WHERE nom = ?", (31, "Alice"))
conn.commit()

# Suppression
cursor.execute("DELETE FROM utilisateurs WHERE nom = ?", ("Bob",))
conn.commit()

# Affichage final
cursor.execute("SELECT * FROM utilisateurs")
print("\nAprès mise à jour et suppression :")
for row in cursor.fetchall():
    print(row)

conn.close() 