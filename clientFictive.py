import sqlite3
import random

from faker import Faker

# La fonction Faker() permet de générer des données fictives.
fake = Faker()

# Connexion à la base de données SQLite.
conn = sqlite3.connect('ventes_magasin.db')
cursor = conn.cursor()

# Création des données fictives.
clients_fictifs = []
for _ in range(100):  # On génère 10 clients fictifs
    nom = fake.last_name()
    prenom = fake.first_name()
    phone = random.randint(600000000, 699999999)  # Génère un numéro de téléphone valide.
    ville = fake.city()
    quartier = fake.word()
    clients_fictifs.append((nom, prenom, phone, ville, quartier))

# Insertion des données fictives dans la table Clients
cursor.executemany('''
    INSERT INTO Clients (nom, prenom, phone, ville, quartier) 
    VALUES (?, ?, ?, ?, ?)
''', clients_fictifs)

# Valider l'insertion
conn.commit()

# Vérifier l'insertion (affichage des clients insérés)
cursor.execute('SELECT * FROM Clients')
clients_insères = cursor.fetchall()
for client in clients_insères:
    print(client)

# Fermeture de la connexion
conn.close()
