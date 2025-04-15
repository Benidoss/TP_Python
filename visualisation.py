import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connexion à la base de données SQLite
conn = sqlite3.connect('ventes_magasin.db')

# Charger les données des ventes avec le statut
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
'''

# Charger les données dans un DataFrame Pandas
ventes_df = pd.read_sql_query(sql_query, conn)

# Fermeture de la connexion SQLite
conn.close()

# Convertir la colonne 'date_enregistrement' en datetime
ventes_df['date_enregistrement'] = pd.to_datetime(ventes_df['date_enregistrement'])

# --- 1. Evolution temporelle des ventes ---
ventes_df['mois'] = ventes_df['date_enregistrement'].dt.to_period('M')
chiffre_affaires_mensuel = ventes_df.groupby('mois')['montant_total'].sum()

# --- 2. Répartition des ventes par produit ---
ventes_par_produit = ventes_df.groupby('produit_libele')['montant_total'].sum().sort_values(ascending=False).head(10)

# --- 3. Répartition des ventes par statut ---
ventes_par_statut = ventes_df['statut_vente'].value_counts()

# Créer la figure avec 3 sous-graphes
fig, axs = plt.subplots(3, 1, figsize=(10, 18))

# --- Graphique 1 : Evolution du chiffre d'affaires mensuel ---
axs[0].plot(chiffre_affaires_mensuel.index.astype(str), chiffre_affaires_mensuel.values, marker='o', color='b', linestyle='-', linewidth=2)
axs[0].set_title("Évolution du Chiffre d'Affaires Mensuel", fontsize=16)
axs[0].set_xlabel("Mois", fontsize=12)
axs[0].set_ylabel("Chiffre d'Affaires (€)", fontsize=12)
axs[0].tick_params(axis='x', rotation=45)

# --- Graphique 2 : Répartition des ventes par produit ---
axs[1].barh(ventes_par_produit.index, ventes_par_produit.values, color=sns.color_palette('Set2', len(ventes_par_produit)))
axs[1].set_title("Top 10 des Produits par Chiffre d'Affaires", fontsize=16)
axs[1].set_xlabel("Chiffre d'Affaires (€)", fontsize=12)
axs[1].set_ylabel("Produits", fontsize=12)

# --- Graphique 3 : Répartition des ventes par statut ---
axs[2].pie(ventes_par_statut, labels=ventes_par_statut.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2', len(ventes_par_statut)))
axs[2].set_title("Répartition des Ventes par Statut", fontsize=16)
axs[2].axis('equal')  # Assurer que le graphique est circulaire

# Ajuster l'agencement et afficher
plt.tight_layout()
plt.show()