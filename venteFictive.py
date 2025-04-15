import sqlite3
import random
from faker import Faker

# Générateur de données fictives
fake = Faker()

# Connexion à la base de données SQLite
conn = sqlite3.connect('ventes_magasin.db')  # Remplacez par le nom de votre base de données
cursor = conn.cursor()

# Nombre de ventes à générer
nombre_ventes = 150

# Définir les différents statuts de vente
statuts = ['Passée', 'Annulée', 'En attente de validation']

# Génération des ventes fictives
ventes_fictives = []

# Récupérer les IDs des commandes existantes
cursor.execute('SELECT id_commande FROM Commandes')
ids_commandes = [commande[0] for commande in cursor.fetchall()]

# Générer les ventes fictives
for _ in range(nombre_ventes):
    id_commande = random.choice(ids_commandes)  # Choisir une commande au hasard
    date_enregistrement = fake.date_this_year()  # Date d'enregistrement fictive cette année
    statut_vente = random.choice(statuts)  # Statut de vente choisi aléatoirement parmi les options

    ventes_fictives.append((id_commande, date_enregistrement, statut_vente))

# Insertion des données dans la table Ventes
cursor.executemany('''
    INSERT INTO Ventes (id_commande, date_enregistrement, statut_vente) 
    VALUES (?, ?, ?)
''', ventes_fictives)

# Valider les insertions
conn.commit()

# Vérification (affichage de quelques ventes insérées)
cursor.execute('SELECT * FROM Ventes LIMIT 5')
ventes_inserees = cursor.fetchall()
print("Ventes insérées:")
for vente in ventes_inserees:
    print(vente)

# Fermeture de la connexion
conn.close()