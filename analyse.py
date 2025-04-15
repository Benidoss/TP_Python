import sqlite3
import pandas as pd
import numpy as np

# Connexion à la base de données SQLite
conn = sqlite3.connect('ventes_magasin.db')

# Charger les données des ventes (nous utilisons la même requête SQL que précédemment)
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

# Charger les données dans un DataFrame Pandas
ventes_df = pd.read_sql_query(sql_query, conn)

# Fermeture de la connexion SQLite
conn.close()

# Convertir la colonne 'date_commande' en datetime
ventes_df['date_commande'] = pd.to_datetime(ventes_df['date_commande'])

# 1. Chiffre d'affaires total
chiffre_affaires_total = ventes_df['montant_total'].sum()
print(f"Chiffre d'affaires total: {chiffre_affaires_total:.2f} €")

# 2. Chiffre d'affaires moyen par mois
ventes_df['mois'] = ventes_df['date_commande'].dt.to_period('M')
ca_moyen_par_mois = ventes_df.groupby('mois')['montant_total'].mean()
print("\nChiffre d'affaires moyen par mois:")
print(ca_moyen_par_mois)

# 3. Chiffre d'affaires moyen par jour
ventes_df['jour'] = ventes_df['date_commande'].dt.date
ca_moyen_par_jour = ventes_df.groupby('jour')['montant_total'].mean()
print("\nChiffre d'affaires moyen par jour:")
print(ca_moyen_par_jour.head())

# 4. Produits les plus vendus (par quantité totale)
produits_par_quantite = ventes_df.groupby('produit_libele')['quantiteTotale'].sum().sort_values(ascending=False)
print("\nTop 5 des produits les plus vendus (par quantité):")
print(produits_par_quantite.head())

# 5. Produits les plus vendus (par chiffre d'affaires)
produits_par_ca = ventes_df.groupby('produit_libele')['montant_total'].sum().sort_values(ascending=False)
print("\nTop 5 des produits les plus vendus (par chiffre d'affaires):")
print(produits_par_ca.head())

# 6. Analyse par client : Chiffre d'affaires par client
ca_par_client = ventes_df.groupby('client_nom')['montant_total'].sum().sort_values(ascending=False)
print("\nTop 5 des clients ayant généré le plus de chiffre d'affaires:")
print(ca_par_client.head(5))

# 7. Analyse par client : Nombre de transactions par client
transactions_par_client = ventes_df.groupby('client_nom')['id_vente'].count().sort_values(ascending=False)
print("\nTop 5 des clients ayant effectué le plus de transactions:")
print(transactions_par_client.head(5))

# 8. Statistiques descriptives générales sur les ventes
statistiques_ventes = ventes_df['montant_total'].describe()
print("\nStatistiques descriptives des ventes (montant total):")
print(statistiques_ventes)

# 9. Calcul du panier moyen par vente
panier_moyen = ventes_df['montant_total'].mean()
print(f"\nPanier moyen par vente: {panier_moyen:.2f} €")
