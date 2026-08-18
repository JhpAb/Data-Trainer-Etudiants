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
# # 🎯 Projet Final Intégrateur — Template
#
# **IvoireMarket** : churn + allocation budget marketing.
# **Équipe** : [Noms des 3 étudiants] · **Date** : [jj/mm/aaaa]
#
# > Ce template structure votre projet. Remplissez chaque section. Le notebook doit s'exécuter de bout en bout avec `random_state=42`. Voir `Projet_Final_Brief.md` pour le cahier des charges complet et la grille d'évaluation.

# %%
# === CONFIGURATION ===
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
campagnes = pd.read_csv(f"{DATA_DIR}/campagnes.csv", parse_dates=["date_debut","date_fin"])
churn = pd.read_csv(f"{DATA_DIR}/churn_dataset.csv", parse_dates=["derniere_achat"])
print("Données chargées ✓")

# %% [markdown]
# ---
# ## §1. EDA & qualité des données (15 pts)
# *Audit complet : structure, manquants, doublons, bornes, outliers, features dérivées.*

# %%
# TODO : audit qualité + features dérivées (récence, fréquence, panier, variables temporelles)
# ...

# %% [markdown]
# ---
# ## §2. Analyse descriptive & segmentation (15 pts)
# *KPI, RFM, clustering, visualisations.*

# %%
# TODO : KPI globaux, RFM, clustering K-means, profiling segments
# ...

# %% [markdown]
# ---
# ## §3. Modèle de scoring churn (20 pts)
# *Pipeline sklearn, train/test stratifié, AUC, lift, importance variables.*

# %%
# TODO : pipeline (preprocessing + modèle), évaluation, lift
# ...

# %% [markdown]
# **Interprétation métier** : [quels facteurs de churn ? quel ROI d'une campagne de rétention ciblée ?]

# %% [markdown]
# ---
# ## §4. Prévision de la demande (10 pts)
# *Régression saisonnière, MAPE, forecast 3 mois.*

# %%
# TODO : CA mensuel, features temporelles, split temporel, MAPE, forecast
# ...

# %% [markdown]
# ---
# ## §5. Évaluation de campagne & attribution (5 pts)
# *Test A/B, ROI, attribution multi-touch.*

# %%
# TODO : test A/B sur campagnes, calcul ROI, attribution
# ...

# %% [markdown]
# ---
# ## §6. Recommandations stratégiques (15 pts)
# *Synthèse chiffrée, priorisée, avec ROI estimé pour le COMEX.*

# %% [markdown]
# | Recommandation | Segment/canal | Investissement estimé | ROI attendu | Priorité |
# |----------------|---------------|----------------------|------------|----------|
# | 1. ... | ... | ... FCFA | x.x | Haute |
# | 2. ... | ... | ... FCFA | x.x | Moyenne |
# | 3. ... | ... | ... FCFA | x.x | Basse |

# %% [markdown]
# ---
# ## §7. Limites & ouverture
# *[Lister les limites : données synthétiques, hypothèses, biais possibles, pistes d'amélioration]*

# %% [markdown]
# ---
# ## 📚 Références utilisées
# - Provost & Fawcett (2013)
# - Tufféry (2018)
# - ...
