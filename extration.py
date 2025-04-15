import sqlite3
import pandas as pd

# Connexion à la base de données SQLite
conn = sqlite3.connect('ventes_magasin.db')

# Charger les commandes passées avec leurs informations de vente
# Requête SQL pour obtenir les ventes passées, les clients et les produits
sql_query = '''
    SELECT
        v.id_vente,
        c.nom AS client_nom,
        c.prenom AS client_prenom,
        p.libele AS produit_libele,
        co.date_commande,
        co.quantiteTotale,
        co.montant_total,
        v.date_enregistrement,
        v.statut_vente
    FROM Ventes v
    JOIN Commandes co ON v.id_commande = co.id_commande
    JOIN Clients c ON co.id_client = c.id_client
    JOIN Produits p ON co.id_produit = p.id_produit
    WHERE v.statut_vente = 'Passée';  -- Filtre pour les commandes passées
'''

# Charger les résultats de la requête SQL dans un DataFrame Pandas
ventes_df = pd.read_sql_query(sql_query, conn)

# Vérification des 30 premières lignes du DataFrame
print(ventes_df.head(30))

# Fermeture de la connexion SQLite
conn.close()