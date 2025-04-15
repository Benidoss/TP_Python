import sqlite3
import random
from faker import Faker

# La fonction Faker() permet de générer des données fictives.
fake = Faker()

# Connexion à la base de données
conn = sqlite3.connect('ventes_magasin.db')
cursor = conn.cursor()

# Générer des données fictives
produits_fictifs = []
categories = ['Service', 'Électronique', 'Domestique', 'Sports-Loisir', 'Automobile']

for _ in range(200):
    libele = fake.word().capitalize() + " " + fake.word().capitalize()  # Nom fictif de produit
    categorie = random.choice(categories)  # Catégorie aléatoire parmi celles définies
    prix_uni = round(random.uniform(10, 500), 2)  # Prix entre 10 et 500, arrondi à 2 décimales
    stock = random.randint(0, 100)  # Stock aléatoire entre 0 et 100 unités
    produits_fictifs.append((libele, categorie, prix_uni, stock))

# Insertion des données fictives dans la table Produits
cursor.executemany('''
    INSERT INTO Produits (libele, categorie, prix_uni, stock) 
    VALUES (?, ?, ?, ?)
''', produits_fictifs)
# Commit des modifications
conn.commit()
# Vérification de l'insertion (affichage des produits insérés)
cursor.execute('SELECT * FROM Produits')
produits_insérés = cursor.fetchall()
for produit in produits_insérés:
    print(produit)
# Fermeture de la connexion
conn.close()
