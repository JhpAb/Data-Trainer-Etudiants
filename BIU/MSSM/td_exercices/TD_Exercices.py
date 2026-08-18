# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # TD & Exercices — Marketing Analytics
#
# > **À compléter** — Écrivez votre code dans les cellules `# À COMPLÉTER`.
# > Les corrigés sont diffusés par le professeur après rendu.
#
# **BIU** · Master in Strategic Sales and Marketing · Module Marketing Analytics
#
# Ce notebook contient **5 travaux dirigés** et **8 exercices progressifs** avec **corrigés complets** (code + interprétation métier). Les données sont les mêmes que le cours (`../data/`).
#
# > **Consigne** : pour chaque exercice, complète la cellule `# À COMPLÉTER` puis compare avec le corrigé qui suit. Barèmes indicatifs fournis.

# %%
# Imports communs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.figsize"] = (9, 5)

DATA_DIR = "../data"
clients = pd.read_csv(f"{DATA_DIR}/clients.csv", parse_dates=["date_inscription"])
transactions = pd.read_csv(f"{DATA_DIR}/transactions.csv", parse_dates=["date_transaction"])
campagnes = pd.read_csv(f"{DATA_DIR}/campagnes.csv", parse_dates=["date_debut", "date_fin"])
churn = pd.read_csv(f"{DATA_DIR}/churn_dataset.csv", parse_dates=["derniere_achat"])

print("Données chargées ✓")

# %% [markdown]
# ---
# # TD 1 — Qualité des données & manipulation pandas
#
# **Objectif** : auditer et nettoyer un jeu de données marketing.
# **Durée** : 2 h · **Barème** : 20 pts
#
# ## Énoncé
# Le service marketing vous transmet `clients.csv` et `transactions.csv`. Avant toute analyse, on doit s'assurer de la qualité.
#
# ### Exercice 1 (5 pts) — Audit de base
# Calcule pour `clients` : nombre de lignes, nombre de colonnes, nombre de valeurs manquantes par colonne, nombre de doublons sur `client_id`.

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ### Exercice 2 (5 pts) — Jointure et cohérence
# Jointez `transactions` et `clients` sur `client_id`. Vérifiez qu'aucune transaction n'a perdu son client. Combien de clients n'ont effectué AUCUNE transaction ?

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ### Exercice 3 (5 pts) — Création de variables dérivées
# Créez dans `transactions` une colonne `annee` (année de la transaction) et `mois_lib` (nom du mois en français). Calculez le panier moyen par année.

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ### Exercice 4 (5 pts) — Détection d'outliers
# Identifiez les transactions dont le montant dépasse le 99e percentile. Combien y en a-t-il ? S'agit-il d'erreurs ou de clients légitimes (argumentez) ?

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ---
# # TD 2 — Segmentation RFM
#
# **Objectif** : construire une segmentation RFM et proposer des actions.
# **Durée** : 2 h · **Barème** : 20 pts
#
# ## Énoncé
# ### Exercice 5 (8 pts) — Calcul RFM
# À partir de `transactions`, calculez pour chaque client : Récence (jours depuis dernier achat), Fréquence (nb d'achats), Montant (CA cumulé). Date de référence = date max des transactions.

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ### Exercice 6 (12 pts) — Scoring et actions
# 1. (4 pts) Calculez les scores R, F, M en quartiles (4 = meilleur).
# 2. (4 pts) Créez une colonne `segment` avec 4 catégories : Champions, Fidèles, À risque, Perdus.
# 3. (4 pts) Proposez une action marketing pour chaque segment (tableau).

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ---
# # TD 3 — Scoring churn supervisé
#
# **Objectif** : construire et évaluer un modèle de prédiction du churn.
# **Durée** : 2 h · **Barème** : 20 pts
#
# ## Énoncé
# On utilise `churn` (cible = colonne `churn`).
#
# ### Exercice 7 (10 pts) — Pipeline et évaluation
# Construisez un `Pipeline` sklearn (standardisation numériques + OneHot catégorielles + RandomForestClassifier). Séparez train/test (stratifié, `random_state=42`). Affichez l'AUC et la matrice de confusion.

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ### Exercice 8 (10 pts) — Lift et ROI
# 1. (5 pts) Calculez le lift du 1er décile (les 10 % de clients les plus risqués).
# 2. (5 pts) Si une campagne de rétention coûte 5 000 FCFA/client et sauve un client valant 120 000 FCFA (CLV), à partir de quel décile la campagne est-elle rentable ?

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ---
# # TD 4 — Test A/B
#
# **Objectif** : conduire un test A/B et conclure statistiquement.
# **Durée** : 1 h30 · **Barème** : 20 pts
#
# ## Énoncé
# On dispose de `campagnes.csv` (colonne `groupe_test` A/B).
#
# ### Exercice 9 (10 pts) — Test statistique
# 1. (4 pts) Calculez le taux de conversion agrégé par groupe (conversions / envois).
# 2. (6 pts) Effectuez un test Z pour deux proportions. Concluez au seuil α=5 %.

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ### Exercice 10 (10 pts) — Taille d'échantillon
# Calculez la taille d'échantillon nécessaire par groupe pour détecter un lift absolu de +1 point à partir d'un taux de base de 12 %, puissance 80 %, α=5 %.

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ---
# # TD 5 — Prévision de la demande
#
# **Objectif** : prévoir le CA mensuel et évaluer la qualité.
# **Durée** : 1 h30 · **Barème** : 20 pts
#
# ## Énoncé
# ### Exercice 11 (10 pts) — Régression avec saisonnalité
# Construisez une régression linéaire du CA mensuel avec features : tendance (`t`), sin/cos annuels. Split temporel 80/20. Calculez le MAPE sur le test.

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ### Exercice 12 (10 pts) — Prévision à 3 mois
# En utilisant le modèle précédent, prévoyez le CA des 3 mois suivants et visualisez.

# %%
# À COMPLÉTER — Écrivez votre code ici


# %% [markdown]
# ---
# ## 📊 Barème récapitulatif (sur 100 pts)
#
# | TD | Exercices | Points |
# |----|-----------|--------|
# | TD 1 | Ex.1-4 (data QA) | 20 |
# | TD 2 | Ex.5-6 (RFM) | 20 |
# | TD 3 | Ex.7-8 (churn) | 20 |
# | TD 4 | Ex.9-10 (A/B) | 20 |
# | TD 5 | Ex.11-12 (prévision) | 20 |
# | **Total** | | **100** |
#
# > Seuil de validation : 50/100. Mention : ≥16/20 par TD.
