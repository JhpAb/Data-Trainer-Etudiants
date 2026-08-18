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
# # 📊 Démo — Requêtes analytiques sur le schéma en étoile (Power BI / Excel)
#
# **BIU / MSSM — Module Marketing Analytics**
#
# Ce notebook démontre **5 requêtes analytiques types** sur le modèle dimensionnel `data/dw/`, en montrant à chaque fois :
# 1. la **requête SQL** (à exécuter dans un SGBD ou Power BI),
# 2. son **équivalent pandas** (pour comprendre / valider en Python),
# 3. la **mesure DAX** correspondante (Power BI / Excel Power Pivot).
#
# > Les données sont 100 % synthétiques. Voir `docs/modele_dimensionnel.md` pour le schéma complet.

# %%
# Configuration
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.figsize"] = (9, 5)

# Chargement des tables du DW (schéma en étoile)
DW_DIR = "../data/dw"
dim_clients = pd.read_csv(f"{DW_DIR}/dim_clients.csv")
dim_temps = pd.read_csv(f"{DW_DIR}/dim_temps.csv", parse_dates=["date"])
dim_produits = pd.read_csv(f"{DW_DIR}/dim_produits.csv")
dim_canaux = pd.read_csv(f"{DW_DIR}/dim_canaux.csv")
fact = pd.read_csv(f"{DW_DIR}/fact_transactions.csv")
print("DW chargé ✓")

# %% [markdown]
# ---
# ## Requête 1 — CA net par mois et par canal
#
# **SQL** (vue `v_ca_mensuel_canal` du schéma) :
# ```sql
# SELECT t.annee, t.mois, t.mois_lib, c.canal,
#        SUM(f.ca_net_fcfa) AS ca_net
# FROM fact_transactions f
# JOIN dim_temps t   ON f.date_key   = t.date_key
# JOIN dim_canaux c  ON f.canal_key  = c.canal_key
# GROUP BY t.annee, t.mois, t.mois_lib, c.canal;
# ```
#
# **DAX** (Power BI) :
# ```dax
# CA Net = SUM(fact_transactions[ca_net_fcfa])
# -- Visuel : ligne (CA net) × mois (axe X) × canal (légende)
# ```

# %%
# Équivalent pandas + visualisation (ce que produirait le visuel Power BI)
ca_mois_canal = (fact
    .merge(dim_temps[["date_key","annee","mois","mois_lib"]], on="date_key")
    .merge(dim_canaux[["canal_key","canal"]], on="canal_key")
    .groupby(["annee","mois","mois_lib","canal"])["ca_net_fcfa"].sum()
    .reset_index())
ca_mois_canal["periode"] = ca_mois_canal["annee"].astype(str) + "-" + ca_mois_canal["mois"].astype(str).str.zfill(2)

pivot = ca_mois_canal.pivot(index="periode", columns="canal", values="ca_net_fcfa").fillna(0)

fig, ax = plt.subplots(figsize=(12,5))
pivot.plot(ax=ax, linewidth=2)
ax.set_title("CA net mensuel par canal (visuel équivalent Power BI)")
ax.set_ylabel("CA net (FCFA)"); ax.set_xlabel("Période")
ax.legend(title="Canal", fontsize=8)
plt.tight_layout(); plt.show()

print("Top 3 canaux par CA net cumulé :")
print(pivot.sum().sort_values(ascending=False).head(3).apply(lambda x: f"{x:,.0f} FCFA"))

# %% [markdown]
# ---
# ## Requête 2 — Top 10 clients par CA net
#
# **SQL** :
# ```sql
# SELECT cl.client_id_nk, cl.ville, cl.segment_marketing,
#        SUM(f.ca_net_fcfa) AS ca_net, COUNT(*) AS nb_achats
# FROM fact_transactions f
# JOIN dim_clients cl ON f.client_key = cl.client_key
# GROUP BY cl.client_id_nk, cl.ville, cl.segment_marketing
# ORDER BY ca_net DESC
# LIMIT 10;
# ```
#
# **DAX** :
# ```dax
# CA par client = CALCULATE([CA Net], ALLEXCEPT(fact_transactions, fact_transactions[client_key]))
# -- Visuel : barres horizontales, top N filtre
# ```

# %%
# Équivalent pandas
top_clients = (fact
    .merge(dim_clients[["client_key","client_id_nk","ville","segment_marketing"]], on="client_key")
    .groupby(["client_id_nk","ville","segment_marketing"])
    .agg(ca_net=("ca_net_fcfa","sum"), nb_achats=("transaction_id","count"))
    .reset_index()
    .sort_values("ca_net", ascending=False)
    .head(10))

fig, ax = plt.subplots(figsize=(10,5))
ax.barh([str(i) for i in top_clients["client_id_nk"]][::-1],
        top_clients["ca_net"][::-1], color="teal")
ax.set_title("Top 10 clients par CA net")
ax.set_xlabel("CA net (FCFA)")
for i, v in enumerate(top_clients["ca_net"][::-1]):
    ax.text(v, i, f" {v/1e6:.1f}M", va="center", fontsize=8)
plt.tight_layout(); plt.show()
top_clients[["client_id_nk","ville","segment_marketing","ca_net","nb_achats"]]

# %% [markdown]
# ---
# ## Requête 3 — Marge brute par catégorie de produit
#
# **SQL** :
# ```sql
# SELECT p.categorie_produit, p.gamme,
#        SUM(f.ca_net_fcfa) AS ca_net, SUM(f.marge_brute_fcfa) AS marge
# FROM fact_transactions f
# JOIN dim_produits p ON f.produit_key = p.produit_key
# GROUP BY p.categorie_produit, p.gamme
# ORDER BY marge DESC;
# ```
#
# **DAX** :
# ```dax
# Marge Brute = SUM(fact_transactions[marge_brute_fcfa])
# Taux Marge % = DIVIDE([Marge Brute], [CA Net])
# ```

# %%
marge_cat = (fact
    .merge(dim_produits[["produit_key","categorie_produit","gamme"]], on="produit_key")
    .groupby(["categorie_produit","gamme"])
    .agg(ca_net=("ca_net_fcfa","sum"), marge=("marge_brute_fcfa","sum"))
    .reset_index())
marge_cat["taux_marge_pct"] = (marge_cat["marge"] / marge_cat["ca_net"] * 100).round(1)
marge_cat = marge_cat.sort_values("marge", ascending=False)

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(marge_cat["categorie_produit"], marge_cat["marge"]/1e6, color="steelblue", label="Marge (M FCFA)")
ax.set_ylabel("Marge brute (M FCFA)")
ax2 = ax.twinx()
ax2.plot(marge_cat["categorie_produit"], marge_cat["taux_marge_pct"], "o-", color="red", label="Taux marge %")
ax2.set_ylabel("Taux de marge (%)")
ax.set_title("Marge brute et taux de marge par catégorie")
plt.xticks(rotation=20)
fig.legend(loc="upper right", bbox_to_anchor=(0.9,0.9))
plt.tight_layout(); plt.show()
marge_cat

# %% [markdown]
# ---
# ## Requête 4 — CA net par segment client et tranche d'âge (analyse croisée)
#
# **SQL** :
# ```sql
# SELECT cl.segment_marketing, cl.tranche_age,
#        SUM(f.ca_net_fcfa) AS ca_net, COUNT(DISTINCT f.client_key) AS nb_clients
# FROM fact_transactions f
# JOIN dim_clients cl ON f.client_key = cl.client_key
# GROUP BY cl.segment_marketing, cl.tranche_age;
# ```
#
# **DAX** :
# ```dax
# CA Net = SUM(fact_transactions[ca_net_fcfa])
# Nb Clients Actifs = DISTINCTCOUNT(fact_transactions[client_key])
# -- Visuel : matrice (segment × tranche_age) ou heatmap
# ```

# %%
ca_seg_age = (fact
    .merge(dim_clients[["client_key","segment_marketing","tranche_age"]], on="client_key")
    .groupby(["segment_marketing","tranche_age"])
    .agg(ca_net=("ca_net_fcfa","sum"), nb_clients=("client_key","nunique"))
    .reset_index())

pivot_ca = ca_seg_age.pivot(index="segment_marketing", columns="tranche_age", values="ca_net").fillna(0)

fig, ax = plt.subplots(figsize=(9,5))
sns.heatmap(pivot_ca/1e6, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax, cbar_kws={"label":"CA net (M FCFA)"})
ax.set_title("CA net (M FCFA) par segment × tranche d'âge")
plt.tight_layout(); plt.show()

# %% [markdown]
# ---
# ## Requête 5 — KPI clients (récence, fréquence, CA, panier moyen) — vue RFM
#
# **SQL** (vue `v_kpi_clients` du schéma) :
# ```sql
# SELECT cl.client_key, cl.segment_marketing, cl.ville,
#        MAX(t.date) AS derniere_achat,
#        (CURRENT_DATE - MAX(t.date)) AS recence_jours,
#        COUNT(*) AS frequence,
#        SUM(f.ca_net_fcfa) AS ca_total,
#        ROUND(AVG(f.ca_net_fcfa),0) AS panier_moyen
# FROM fact_transactions f
# JOIN dim_clients cl ON f.client_key = cl.client_key
# JOIN dim_temps t    ON f.date_key   = t.date_key
# GROUP BY cl.client_key, cl.segment_marketing, cl.ville;
# ```
#
# **DAX** :
# ```dax
# Récence = DATEDIFF(MAX(dim_temps[date]), TODAY(), DAY)
# Fréquence = COUNTROWS(fact_transactions)
# CA Total = SUM(fact_transactions[ca_net_fcfa])
# Panier Moyen = DIVIDE([CA Total], [Fréquence])
# ```

# %%
# Équivalent pandas
kpi = (fact
    .merge(dim_clients[["client_key","segment_marketing","ville"]], on="client_key")
    .merge(dim_temps[["date_key","date"]], on="date_key")
    .groupby(["client_key","segment_marketing","ville"])
    .agg(derniere_achat=("date","max"), frequence=("transaction_id","count"),
         ca_total=("ca_net_fcfa","sum"), panier_moyen=("ca_net_fcfa","mean"))
    .reset_index())
kpi["recence_jours"] = (dim_temps["date"].max() - kpi["derniere_achat"]).dt.days

# Synthèse par segment
synthese = kpi.groupby("segment_marketing").agg(
    nb_clients=("client_key","count"),
    ca_total_moy=("ca_total","mean"),
    frequence_moy=("frequence","mean"),
    panier_moy=("panier_moyen","mean"),
    recence_moy=("recence_jours","mean")
).round(0).sort_values("ca_total_moy", ascending=False)

print("Synthèse RFM par segment marketing :")
display(synthese)

fig, ax = plt.subplots(figsize=(9,5))
synthese["ca_total_moy"].plot(kind="bar", ax=ax, color="teal")
ax.set_title("CA total moyen par client selon le segment")
ax.set_ylabel("CA moyen (FCFA)"); ax.set_xlabel("")
plt.tight_layout(); plt.show()

# %% [markdown]
# ---
# ## 🎯 Synthèse
#
# Ces 5 requêtes couvrent les analyses marketing fondamentales d'un dashboard Power BI :
# 1. **Tendance** : CA mensuel par canal (ligne)
# 2. **Top clients** : ciblage (barres horizontales, top N)
# 3. **Rentabilité** : marge par catégorie (barres + courbe)
# 4. **Segmentation** : CA segment × âge (heatmap)
# 5. **RFM** : récence, fréquence, valeur (tableau + barres)
#
# > 💡 **Passage à Power BI/Excel** : chaque requête SQL devient une mesure DAX, et chaque visualisation pandas devient un visuel Power BI. Le schéma en étoile garantit que les jointures sont simples et que les filtres (segments) se propagent automatiquement.
