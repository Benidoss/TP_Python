import sqlite3
import random
from faker import Faker

# La fonction Faker() permet de générer des données fictives.
fake = Faker()

# Connexion à la base de données SQLite
conn = sqlite3.connect('ventes_magasin.db')
cursor = conn.cursor()

# Nombre de commandes à générer
nombre_commandes = 150

# Génération des commandes fictives
commandes_fictives = []

# Récupérer les IDs des clients existants
cursor.execute('SELECT id_client FROM Clients')
ids_clients = [client[0] for client in cursor.fetchall()]

# Récupérer les IDs des produits existants
cursor.execute('SELECT id_produit FROM Produits')
ids_produits = [produit[0] for produit in cursor.fetchall()]

# Générer les commandes fictives
for _ in range(nombre_commandes):
    id_client = random.choice(ids_clients)  # Choisir un client au hasard
    id_produit = random.choice(ids_produits)  # Choisir un produit au hasard
    quantite_totale = random.randint(1, 5)  # Quantité aléatoire entre 1 et 5
    montant_total = 0

    # Récupérer le prix unitaire du produit choisi
    cursor.execute('SELECT prix_uni FROM Produits WHERE id_produit = ?', (id_produit,))
    prix_unitaire = cursor.fetchone()[0]
    
    montant_total = quantite_totale * prix_unitaire  # Calcul du montant total pour la commande
    
    # Génération d'une date de commande aléatoire dans l'année
    date_commande = fake.date_this_year()

    # Récupérer le libellé du produit
    cursor.execute('SELECT libele FROM Produits WHERE id_produit = ?', (id_produit,))
    libele_produit = cursor.fetchone()[0]

    # Récupérer le nom et prénom du client
    cursor.execute('SELECT nom, prenom FROM Clients WHERE id_client = ?', (id_client,))
    client_data = cursor.fetchone()
    nom_client = client_data[0]
    prenom_client = client_data[1]

    commandes_fictives.append((
        id_client, nom_client, prenom_client, 
        id_produit, libele_produit, 
        date_commande, quantite_totale, montant_total
    ))

# Insertion des commandes dans la table Commandes
cursor.executemany('''
    INSERT INTO Commandes (id_client, nom, prenom, id_produit, libele, date_commande, quantiteTotale, montant_total) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', commandes_fictives)

# Valider les insertions
conn.commit()

# Vérification (affichage de quelques commandes insérées)
cursor.execute('SELECT * FROM Commandes LIMIT 5')
commandes_inserees = cursor.fetchall()
print("Commandes insérées:")
for commande in commandes_inserees:
    print(commande)

# Fermeture de la connexion
conn.close()