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
# # 📊 Marketing Analytics — Cours complet (Master 2)
#
# **British International University (BIU)** — Master in Strategic Sales and Marketing (MSSM)
# **Module :** Marketing Analytics · **Volume :** 36 h (16 h cours + 20 h TP) · **ECTS :** 6
# **Enseignant :** [Nom du candidat] — Data Scientist (Finance / Assurance / AML Analytics)
#
# > Ce notebook constitue le **support de cours complet et exécutable** du module. Il suit l'organisation hebdomadaire du syllabus (S1 → S14). Toutes les données sont **100 % synthétiques** (retailer/e-commerce ivoirien fictif « IvoireMarket ») et **reproductibles** (`random_state=42`).
#
# ---
#
# ## 🎯 Objectifs pédagogiques
#
# À l'issue du module, l'étudiant sera capable de :
# 1. **Collecter et structurer** des données clients multi-sources (CRM, transactions, campagnes) en respectant la qualité et la gouvernance (loi ivoirienne n°2013-450).
# 2. **Mener une analyse descriptive** (RFM, segmentation, churn, CLV) et la traduire en indicateurs actionnables.
# 3. **Construire des modèles prédictifs** (régression, classification, clustering) pour le ciblage et le scoring.
# 4. **Évaluer la performance** des campagnes via des tests A/B rigoureux et des métriques de lift/ROI.
# 5. **Communiquer** les résultats via tableaux de bord et recommandations stratégiques argumentées.
# 6. **Distinguer corrélation et causalité**, et identifier les biais fréquents.
#
# ---
#
# ## 📅 Organisation hebdomadaire (rappel)
#
# | Sem. | Thématique | Section notebook |
# |------|-----------|------------------|
# | S1 | Introduction & data pipeline | §1 |
# | S2 | Manipulation de données (pandas) | §2 |
# | S3 | Analyse descriptive & RFM | §3 |
# | S4 | Visualisation & storytelling | §4 |
# | S5 | Segmentation non supervisée | §5 |
# | S6–S7 | Scoring & classification supervisée | §6 |
# | S8 | Prévision de la demande (régression) | §7 |
# | S9 | Web & social analytics | §8 |
# | S10 | Tests A/B & expérimentation | §9 |
# | S11 | Tableaux de bord | §10 |
# | S12 | Attribution & CLV prédictive | §11 |
# | S13–S14 | Projet intégrateur & soutenance | dossier `projets/` |
#
# ---
#
# ## ⚠️ Avertissement éthique et méthodologique
#
# > **Corrélation ≠ causalité.** Tout au long du cours, on distinguera :
# > - une *association* observée dans les données (corrélation) ;
# > - un *lien de cause à effet* démontré par un plan d'expérience (test A/B, randomisation).
# >
# > Les données étant synthétiques, **aucune décision commerciale réelle** ne doit en découler. L'objectif est l'apprentissage de la démarche.

# %% [markdown]
# ---
# # §1. Introduction au marketing analytics (S1)
#
# ## 1.1 Qu'est-ce que le marketing analytics ?
#
# Le **marketing analytics** est l'ensemble des pratiques et techniques permettant de **mesurer, analyser et piloter** la performance marketing à partir des données. Il transforme la donnée brute en **décisions** :
#
# $$\text{Données} \xrightarrow{\text{analyse}} \text{Insights} \xrightarrow{\text{décision}} \text{Action} \xrightarrow{\text{mesure}} \text{Performance}$$
#
# ### Cas d'usage typiques
# | Cas d'usage | Question métier | Technique |
# |-------------|-----------------|-----------|
# | Segmentation | « Quels sont mes groupes de clients ? » | Clustering (K-means, CAH) |
# | Scoring churn | « Qui risque de partir ? » | Classification supervisée |
# | Propension achat | « Qui va acheter ? » | Régression logistique, arbres |
# | Prévision demande | « Combien vais-je vendre ? » | Régression, séries temporelles |
# | Attribution | « Quel canal convertit le mieux ? » | Attribution multi-touch |
# | Tests A/B | « Quelle version performe ? » | Inférence, tests statistiques |
# | CLV | « Combien vaut un client sur sa durée de vie ? » | Modèle CLV |
#
# ## 1.2 La chaîne de valeur de la donnée marketing
#
# 1. **Collecte** : CRM, transactions, web analytics (GA4), réseaux sociaux, Mobile Money.
# 2. **Stockage** : data warehouse, data lake, tables SQL.
# 3. **Nettoyage & intégration** : gestion des doublons, des manquants, jointures.
# 4. **Analyse** : descriptive → prédictive → prescriptive.
# 5. **Restitution** : tableaux de bord, rapports, alertes.
# 6. **Action** : ciblage, personnalisation, automatisation.
#
# ## 1.3 Gouvernance et éthique (contexte ivoirien)
#
# - **Loi n°2013-450** du 19 juin 2013 sur la protection des données personnelles en Côte d'Ivoire (Autorité de protection des données — APD-CI).
# - Principes : **minimisation** (ne collecter que le nécessaire), **finalité**, **consentement**, **sécurité**, **durée de conservation**.
# - Anonymisation / pseudonymisation des identifiants clients.
# - **Biais algorithmiques** : un modèle entraîné sur des données biaisées reproduit et amplifie les biais (ex. exclusion de certaines villes).
# - **Distinction corrélation/causalité** : un panier moyen plus élevé chez les clients VIP *n'explique pas* pourquoi ils sont VIP.

# %% [markdown]
# ---
# # §2. Manipulation de données clients avec pandas (S2)
#
# ## 2.1 Configuration de l'environnement
#
# Nous utilisons un écosystème Python standard pour la data science :
# - `pandas`, `numpy` : manipulation de données tabulaires.
# - `scikit-learn` : machine learning.
# - `matplotlib`, `seaborn`, `plotly` : visualisation.
#
# > 💡 **Bonnes pratiques (PEP8)** : noms de variables explicites (`snake_case`), un import par ligne pour les principaux, `random_state` fixé pour la reproductibilité.

# %%
# Imports standards
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration globale de reproductibilité
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Style graphique
sns.set_theme(style="whitegrid", palette="viridis", context="notebook")
plt.rcParams["figure.figsize"] = (9, 5)
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["figure.dpi"] = 100

# Affichage pandas
pd.set_option("display.max_columns", 50)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

print("Environnement prêt. pandas =", pd.__version__, "| numpy =", np.__version__)

# %% [markdown]
# ## 2.2 Chargement des données
#
# Le dossier `data/` contient 4 jeux de données synthétiques (voir `docs/dictionnaire_donnees.md`).
#
# | Fichier | Lignes | Description |
# |---------|--------|-------------|
# | `clients.csv` | 5 000 | Table client (CRM) |
# | `transactions.csv` | 120 000 | Historique des achats |
# | `campagnes.csv` | 200 | Campagnes marketing + test A/B |
# | `churn_dataset.csv` | 4 944 | Features clients + label churn |

# %%
# Chargement des 4 tables
DATA_DIR = "../data"

clients = pd.read_csv(f"{DATA_DIR}/clients.csv", parse_dates=["date_inscription"])
transactions = pd.read_csv(f"{DATA_DIR}/transactions.csv", parse_dates=["date_transaction"])
campagnes = pd.read_csv(f"{DATA_DIR}/campagnes.csv",
                        parse_dates=["date_debut", "date_fin"])
churn = pd.read_csv(f"{DATA_DIR}/churn_dataset.csv", parse_dates=["derniere_achat"])

print("Dimensions :")
print(f"  clients      : {clients.shape}")
print(f"  transactions : {transactions.shape}")
print(f"  campagnes    : {campagnes.shape}")
print(f"  churn        : {churn.shape}")

# %% [markdown]
# ## 2.3 Qualité des données (Data Quality Assessment)
#
# Avant toute analyse, on **audite** la donnée : structure, types, valeurs manquantes, doublons, bornes. C'est l'étape **QA** (Quality Assurance), non négociable en production.
#
# ### Aperçu des tables

# %%
# Aperçu des 5 premières lignes de chaque table
print("=== CLIENTS ==="); display(clients.head())
print("=== TRANSACTIONS ==="); display(transactions.head())
print("=== CAMPAGNES ==="); display(campagnes.head())


# %%
# Types et valeurs manquantes par table
def audit(df, name):
    miss = df.isna().sum()
    miss = miss[miss > 0]
    print(f"--- {name} ({df.shape[0]} lignes, {df.shape[1]} colonnes) ---")
    print("Types :"); print(df.dtypes)
    print(f"Doublons : {df.duplicated().sum()}")
    if len(miss):
        print("Manquants :"); print(miss)
    else:
        print("Manquants : aucun ✓")
    print()

audit(clients, "clients")
audit(transactions, "transactions")
audit(campagnes, "campagnes")
audit(churn, "churn")

# %%
# Statistiques descriptives numériques
print("=== TRANSACTIONS (numérique) ===")
display(transactions.describe().T)

print("=== CLIENTS (numérique) ===")
display(clients.describe().T)

# %%
# Statistiques descriptives catégorielles
print("=== Variables catégorielles clients ===")
for col in ["genre", "ville", "canal_acquisition", "segment_marketing"]:
    print(f"\n{col}:")
    print(clients[col].value_counts(normalize=True).round(3))

# %% [markdown]
# ### 🔍 Interprétation métier
#
# 1. **Répartition géographique** : ~55 % des clients sont à Abidjan — logique pour un retailer ivoirien (concentration économique). Un ciblage exclusif sur Abidjan ignorerait ~45 % du potentiel hors-capitale.
# 2. **Canaux d'acquisition** : Mobile Money domine (34 %) — reflet de l'adoption forte du Mobile Money (Orange Money / MTN MoMo) en Côte d'Ivoire. À comparer au coût d'acquisition par canal.
# 3. **Segments** : les clients « Nouveau » (35 %) et « Occasionnel » (25 %) représentent 60 % de la base. Fort potentiel de **montée en valeur** via la fidélisation.
# 4. **Valeurs manquantes** : aucune → la donnée est de qualité suffisante pour l'analyse (cas pédagogique idéal ; en production, c'est rare !).

# %% [markdown]
# ## 2.4 Jointures et enrichissement
#
# En pratique, la donnée utile est **éclatée** entre plusieurs tables. On utilise `merge` pour reconstituer une vue analytique.
#
# > 💡 **Bonnes pratiques** : toujours vérifier la **clé de jointure**, le type de jointure (`inner`, `left`), et le nombre de lignes avant/après pour détecter une perte.

# %%
# Vue enrichie : transactions + infos client
tx_clients = transactions.merge(
    clients[["client_id", "genre", "ville", "segment_marketing"]],
    on="client_id", how="left"
)
print(f"Avant jointure : {len(transactions)} transactions")
print(f"Après jointure  : {len(tx_clients)} transactions")
print(f"Clients non matchés : {tx_clients['segment_marketing'].isna().sum()}")
tx_clients.head()

# %% [markdown]
# ---
# # §3. Analyse descriptive & RFM (S3)
#
# ## 3.1 KPI marketing fondamentaux
#
# Avant de modéliser, on calcule les **indicateurs clés (KPI)** qui décrivent l'activité :
#
# | KPI | Définition | Question métier |
# |-----|------------|-----------------|
# | **CA** | Chiffre d'affaires total | Combien ai-je vendu ? |
# | **Panier moyen** | CA / nb transactions | Quelle valeur par achat ? |
# | **Fréquence** | Nb achats / période | À quelle fréquence achète-t-on ? |
# | **Taux de conversion** | Conversions / contacts | Quelle efficacité du ciblage ? |
# | **CLV** | Valeur vie client | Combien vaut un client ? |
# | **Churn rate** | % clients perdus | Quelle érosion de la base ? |

# %%
# KPI globaux sur la période
date_ref = transactions["date_transaction"].max()
ca_total = transactions["montant_fcfa"].sum()
nb_tx = len(transactions)
nb_clients_actifs = transactions["client_id"].nunique()
panier_moyen = transactions["montant_fcfa"].mean()
frequence_moy = nb_tx / nb_clients_actifs

print(f"Période d'analyse : {transactions['date_transaction'].min().date()} → {date_ref.date()}")
print(f"CA total             : {ca_total:,.0f} FCFA")
print(f"Nb transactions      : {nb_tx:,}")
print(f"Clients actifs (TX)  : {nb_clients_actifs:,}")
print(f"Panier moyen         : {panier_moyen:,.0f} FCFA")
print(f"Fréquence moyenne    : {frequence_moy:.2f} achats/client")

# %%
# CA mensuel (série temporelle)
ca_mensuel = (transactions
              .set_index("date_transaction")
              .resample("ME")["montant_fcfa"]
              .sum())

fig, ax = plt.subplots(figsize=(11, 5))
ca_mensuel.plot(ax=ax, color="teal", marker="o", linewidth=2)
ax.set_title("Évolution mensuelle du chiffre d'affaires (IvoireMarket)")
ax.set_ylabel("CA mensuel (FCFA)")
ax.set_xlabel("")
ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.show()

# Tendance : croissance ?
print(f"CA dernier mois / premier mois : {ca_mensuel.iloc[-1] / ca_mensuel.iloc[0]:.2f}x")

# %% [markdown]
# ### 🔍 Interprétation métier
# - On observe une **saisonnalité** (pics en fin d'année = fêtes, rentrée scolaire, prime de fin d'année).
# - La tendance globale indique la **croissance** ou **décroissance** de l'activité — base du pilotage stratégique.
# - ⚠️ Une hausse du CA peut masquer une **baisse du panier moyen** compensée par plus de transactions → toujours croiser plusieurs KPI.

# %% [markdown]
# ## 3.2 Segmentation RFM
#
# La **RFM** est une méthode de segmentation valeur/comportement, simple et robuste, basée sur 3 dimensions :
#
# | Dimension | Question | Calcul |
# |----------|----------|--------|
# | **R**écence | « Quand a-t-il acheté pour la dernière fois ? » | Nb de jours depuis dernier achat |
# | **F**réquence | « Combien de fois a-t-il acheté ? » | Nb d'achats sur la période |
# | **M**ontant | « Combien a-t-il dépensé ? » | CA cumulé |
#
# On découpe chaque dimension en **quartiles** (score 1 à 4) puis on combine.

# %%
# Calcul R, F, M par client
date_ref = transactions["date_transaction"].max()

rfm = transactions.groupby("client_id").agg(
    recence=("date_transaction", lambda d: (date_ref - d.max()).days),
    frequence=("transaction_id", "count"),
    montant=("montant_fcfa", "sum")
).reset_index()

print(f"RFM : {rfm.shape[0]} clients")
rfm.describe().T

# %%
# Scores RFM en quartiles (4 = le mieux)
# Récence : plus c'est petit, mieux c'est → on inverse le rang
rfm["R_score"] = pd.qcut(rfm["recence"], 4, labels=[4, 3, 2, 1]).astype(int)
rfm["F_score"] = pd.qcut(rfm["frequence"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
rfm["M_score"] = pd.qcut(rfm["montant"], 4, labels=[1, 2, 3, 4]).astype(int)

# Score combiné (ex: 444 = meilleur client)
rfm["RFM_score"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)
rfm["RFM_total"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

rfm.head(10)


# %%
# Catégorisation métier des segments RFM
def segment_rfm(row):
    r, f, m = row["R_score"], row["F_score"], row["M_score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3:
        return "Fidèles"
    elif r >= 4 and f <= 2:
        return "Nouveaux"
    elif r <= 2 and f >= 3:
        return "À risque (churn)"
    elif r <= 2 and f <= 2:
        return "Perdus"
    else:
        return "Potentiels"

rfm["segment_rfm"] = rfm.apply(segment_rfm, axis=1)

seg_counts = rfm["segment_rfm"].value_counts()
print("Répartition des segments RFM :")
print(seg_counts)
print(f"\nPart des Champions : {seg_counts.get('Champions', 0)/len(rfm):.1%}")

# %%
# Visualisation des segments RFM
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Pie chart des segments
seg_counts.plot(kind="barh", ax=axes[0], color=sns.color_palette("viridis", len(seg_counts)))
axes[0].set_title("Répartition des segments RFM")
axes[0].set_xlabel("Nombre de clients")

# Heatmap R vs F
rfm_pivot = rfm.groupby(["R_score", "F_score"]).size().unstack().fillna(0)
sns.heatmap(rfm_pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=axes[1])
axes[1].set_title("Densité R × F")
axes[1].set_xlabel("F_score"); axes[1].set_ylabel("R_score")
plt.tight_layout(); plt.show()

# %% [markdown]
# ### 🔍 Interprétation métier & actions
#
# | Segment | Caractéristique | Action marketing |
# |---------|-----------------|------------------|
# | **Champions** (R↑ F↑ M↑) | Meilleurs clients | **Récompenser**, programme VIP, cross-sell |
# | **Fidèles** (R↑ F↑) | Achètent régulièrement | Upsell, parrainage |
# | **Nouveaux** (R↑ F↓) | Premiers achats | **Onboarding**, nudge 2e achat |
# | **À risque** (R↓ F↑) | Anciens bons clients | **Réactivation** ciblée, offre |
# | **Perdus** (R↓ F↓ M↓) | Désengagés | Win-back ou abandon |
#
# > 💡 **Levier stratégique** : déplacer des clients des segments « À risque » vers « Fidèles » via une **campagne de réactivation** mesurée (test A/B, voir §9). C'est précisément ce que résout le marketing analytics.

# %% [markdown]
# ## 3.3 Customer Lifetime Value (CLV) — approche historique
#
# La **CLV** (Valeur Vie Client) est la valeur nette qu'un client génère sur toute sa relation avec l'entreprise. C'est l'indicateur roi pour décider **combien investir** pour acquérir un client.
#
# ### Formule simple (CLV historique agrégée)
#
# $$CLV = \text{Panier moyen} \times \text{Fréquence} \times \text{Durée de vie (années)} \times \text{Marge}$$
#
# > ⚠️ Il s'agit d'une **estimation historique agrégée**, pas d'une prédiction individuelle. La CLV prédictive (modélisée) est vue en §11.

# %%
# CLV historique agrégée
panier_moyen = transactions["montant_fcfa"].mean()
frequence_annuelle = transactions.groupby("client_id").size().mean() / 3  # 3 ans
duree_vie_ans = 5        # hypothèse métier
marge_pct = 0.30         # marge brute 30 %

clv_agregee = panier_moyen * frequence_annuelle * duree_vie_ans * marge_pct
print(f"Panier moyen       : {panier_moyen:,.0f} FCFA")
print(f"Fréquence annuelle : {frequence_annuelle:.2f} achets/an")
print(f"Durée de vie       : {duree_vie_ans} ans")
print(f"Marge              : {marge_pct:.0%}")
print(f"\n>>> CLV agrégée estimée : {clv_agregee:,.0f} FCFA / client")

# Coût d'acquisition acceptable (règle CLV / CAC >= 3)
cac_max = clv_agregee / 3
print(f">>> CAC max recommandé (CLV/CAC=3) : {cac_max:,.0f} FCFA")

# %%
# CLV par segment RFM (historique, par segment)
clv_segment = (rfm.groupby("segment_rfm")
               .apply(lambda g: g["montant"].mean() * (g["frequence"].mean()/3) * duree_vie_ans * marge_pct,
                      include_groups=False)
               .round(0)
               .sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(10, 5))
clv_segment.plot(kind="bar", ax=ax, color="steelblue")
ax.set_title("CLV historique estimée par segment RFM")
ax.set_ylabel("CLV (FCFA)")
ax.set_xlabel("")
for i, v in enumerate(clv_segment):
    ax.text(i, v, f"{v:,.0f}", ha="center", va="bottom", fontsize=9)
plt.xticks(rotation=20)
plt.tight_layout(); plt.show()

print("CLV par segment :"); print(clv_segment)

# %% [markdown]
# ### 🔍 Interprétation métier
# - Les **Champions** ont une CLV bien supérieure aux autres : ils justifient un **investissement marketing prioritaire** (programme de fidélité, service dédié).
# - Le ratio **CLV/CAC ≥ 3** est une règle pragmatique : si je dépense plus d'un tiers de la CLV pour acquérir, je détruis de la valeur.
# - ⚠️ La CLV historique **sous-estime** la valeur des nouveaux clients (durée de vie non écoulée) → d'où l'intérêt de la **CLV prédictive** (§11).
#
# > **Corrélation ≠ causalité** : les Champions ont une CLV élevée *parce qu'ils achètent beaucoup* — ce n'est pas le programme VIP qui les a rendus Champions, c'est l'inverse. Pour mesurer l'effet *causal* d'un programme, il faut un **test A/B randomisé** (§9).

# %% [markdown]
# ---
# # §4. Visualisation & storytelling data (S4)
#
# ## 4.1 Principes de la visualisation (Tufte / Few)
#
# La visualisation sert à **communiquer** un message, pas à décorer. Principes clés :
#
# 1. **Adéquat au message** : comparer des montants → barres ; des tendances → lignes ; des distributions → histogrammes/boxplots ; des compositions → parts empilées.
# 2. **Maximiser le ratio données-encre** : pas de fioritures (3D, ombres), axes propres.
# 3. **Une idée par graphique** : un titre qui répond à la question métier.
# 4. **Hiérarchie visuelle** : l'œil doit aller à l'essentiel (couleur contrastée sur le point clé).
# 5. **Étiqueter** plutôt qu'utiliser une légende éloignée quand possible.
#
# > ❌ À éviter : camemberts pour > 5 catégories, axes tronqués, double axe trompeur, couleurs arc-en-ciel pour des données ordonnées.

# %%
# 4.2 CA par canal d'achat
ca_canal = transactions.groupby("canal_achat")["montant_fcfa"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(9, 5))
ca_canal.plot(kind="bar", ax=ax, color=sns.color_palette("viridis", len(ca_canal)))
ax.set_title("Chiffre d'affaires par canal d'achat")
ax.set_ylabel("CA (FCFA)")
ax.set_xlabel("")
for i, v in enumerate(ca_canal):
    ax.text(i, v, f"{v/1e6:.1f}M", ha="center", va="bottom", fontsize=9)
plt.xticks(rotation=15)
plt.tight_layout(); plt.show()

print("Part par canal :")
print((ca_canal / ca_canal.sum()).round(3))

# %% [markdown]
# ### 🔍 Interprétation métier
# - La **boutique physique** reste un canal fort en Côte d'Ivoire (préférence pour le tactile, confiance).
# - **Application Mobile** et **Mobile Money USSD** captent une part significative → investissement digital rentable.
# - ⚠️ Un canal à faible CA n'est pas forcément à abandonner : il peut avoir un **coût d'acquisition faible** ou servir de **porte d'entrée** (cf. attribution multi-touch, §11).

# %%
# 4.3 Distribution des montants (histogramme + log scale)
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# Échelle linéaire
axes[0].hist(transactions["montant_fcfa"], bins=50, color="teal", edgecolor="white")
axes[0].set_title("Distribution des montants (linéaire)")
axes[0].set_xlabel("Montant (FCFA)"); axes[0].set_ylabel("Nb transactions")
axes[0].axvline(transactions["montant_fcfa"].mean(), color="red", linestyle="--",
                label=f"Moyenne {transactions['montant_fcfa'].mean():,.0f}")
axes[0].legend()

# Échelle log (la distribution est asymétrique)
axes[1].hist(np.log1p(transactions["montant_fcfa"]), bins=50, color="darkorange", edgecolor="white")
axes[1].set_title("Distribution des montants (log)")
axes[1].set_xlabel("log(1 + montant)"); axes[1].set_ylabel("Nb transactions")
plt.tight_layout(); plt.show()

print(f"Skewness : {transactions['montant_fcfa'].skew():.2f} (>0 = asymétrie à droite)")

# %% [markdown]
# ### 🔍 Interprétation métier
# - La distribution des montants est **asymétrique à droite** (skewness > 0) : beaucoup de petits paniers, peu de très gros. Typique du retail.
# - La transformation **log** rend la distribution plus proche d'une gaussienne → utile pour les modèles linéaires (régression, §7).
# - ⚠️ Les **valeurs extrêmes** (gros paniers) ne sont pas des erreurs : ce sont des clients B2B ou des achats VIP. Ne pas les supprimer aveuglément.

# %%
# 4.4 CA par catégorie et mois (heatmap saisonnalité)
ca_cat_month = (transactions
                .assign(mois=transactions["date_transaction"].dt.to_period("M").astype(str))
                .groupby(["mois", "categorie_produit"])["montant_fcfa"].sum()
                .unstack(fill_value=0))

fig, ax = plt.subplots(figsize=(13, 6))
sns.heatmap(ca_cat_month.T / 1e6, cmap="YlGnBu", annot=False, cbar_kws={"label": "CA (M FCFA)"}, ax=ax)
ax.set_title("CA mensuel par catégorie de produit (saisonnalité)")
ax.set_xlabel("Mois"); ax.set_ylabel("")
plt.tight_layout(); plt.show()

# %% [markdown]
# ### 🔍 Interprétation métier
# - La heatmap révèle la **saisonnalité par catégorie** : « Électronique » pic en fin d'année (fêtes), « Mode » aux rentrées, « Alimentaire » plus régulier.
# - Ces patrons guident le **planning des campagnes** et la **gestion des stocks** : anticiper les pics évite les ruptures et les surstocks.

# %%
# 4.5 Panier moyen par segment marketing (boxplot)
tx_seg = transactions.merge(clients[["client_id", "segment_marketing"]], on="client_id")

fig, ax = plt.subplots(figsize=(10, 5))
order = ["Nouveau", "Occasionnel", "Régulier", "Fidèle", "VIP"]
sns.boxplot(data=tx_seg, x="segment_marketing", y="montant_fcfa",
            order=order, showfliers=False, ax=ax, palette="viridis")
ax.set_title("Panier par segment marketing (sans valeurs extrêmes)")
ax.set_xlabel(""); ax.set_ylabel("Montant transaction (FCFA)")
plt.tight_layout(); plt.show()

# Tableau récapitulatif
tx_seg.groupby("segment_marketing")["montant_fcfa"].agg(["count", "mean", "median"]).reindex(order)

# %% [markdown]
# ### 🔍 Interprétation métier
# - Le panier moyen **croît avec la fidélité** : VIP > Fidèle > Régulier > Occasionnel > Nouveau. Logique : la confiance et l'engagement augmentent la valeur du panier.
# - ⚠️ **Corrélation, pas causalité** : le fait d'être VIP n'augmente pas mécaniquement le panier. Les VIP *sont* les clients qui dépensent le plus (sélection). On ne peut conclure à l'effet du programme VIP que par un test A/B randomisé.

# %%
# 4.6 Visualisation interactive avec plotly (top clients par CA)
import plotly.express as px

top_clients = (rfm.nlargest(20, "montant")
               .merge(clients[["client_id", "ville"]], on="client_id")
               .sort_values("montant", ascending=True))

fig = px.bar(top_clients, x="montant", y="client_id", orientation="h",
             color="ville", title="Top 20 clients par CA (interactif)",
             labels={"montant": "CA (FCFA)", "client_id": "Client ID"},
             hover_data=["frequence", "recence"])
fig.update_layout(height=550, yaxis_title="Client ID", showlegend=True)
fig.show()

# %% [markdown]
# ### 💡 Pourquoi plotly ?
# - **Interactivité** : survol (tooltips), zoom, filtres — idéal pour l'exploration et les tableaux de bord exécutifs.
# - En production, on privilégie `plotly` pour le web et `matplotlib`/`seaborn` pour les rapports PDF statiques.
#
# > 📖 **Référence** : Edward Tufte, *The Visual Display of Quantitative Information* (1983) — la bible du data viz.

# %% [markdown]
# ---
# # §5. Segmentation non supervisée (clustering) (S5)
#
# ## 5.1 Pourquoi le clustering ?
#
# La segmentation RFM (§3) repose sur des **règles métier** (quartiles). Le **clustering** découvre des groupes **à partir des données**, sans règle préétablie — utile quand :
# - on a plus de 3 dimensions (RFM + démographie + comportement web...) ;
# - on cherche des profils naturels non triviaux.
#
# ### Algorithmes courants
# | Algorithme | Type | Force | Faiblesse |
# |-----------|------|--------|-----------|
# | **K-means** | Partitions | Rapide, simple | Suppose des clusters sphériques |
# | **CAH** (Classification Ascendante Hiérarchique) | Hiérarchique | Dendrogramme lisible | O(n²) → lent sur gros volumes |
# | **DBSCAN** | Densité | Détecte le bruit, formes arbitraires | Sensible aux paramètres |
# | **Gaussian Mixture** | Probabiliste | Clusters souples (ellipsoïdes) | Suppose une distribution gaussienne |
#
# > ⚠️ **Standardisation obligatoire** : K-means et CAH utilisent des distances euclidiennes. Si une variable est en milliers et l'autre en unités, elle domine.

# %%
# 5.2 Préparation des features clients pour le clustering
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# On part du RFM et on ajoute des features comportementales
features = rfm[["recence", "frequence", "montant"]].copy()
# Transformation log sur le montant (asymétrique)
features["log_montant"] = np.log1p(features["montant"])
features = features[["recence", "frequence", "log_montant"]]

print("Features pour le clustering :")
print(features.describe().T)

# %%
# 5.3 Standardisation (z-score)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)
X_scaled = pd.DataFrame(X_scaled, columns=features.columns, index=features.index)

print("Après standardisation (moyenne ~0, écart-type ~1) :")
X_scaled.describe().T[["mean", "std"]]

# %%
# 5.4 Choix du nombre de clusters : méthode du coude + silhouette
inertias = []
silhouettes = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

axes[0].plot(list(K_range), inertias, "o-", color="teal")
axes[0].set_title("Méthode du coude (inertie)")
axes[0].set_xlabel("Nombre de clusters k"); axes[0].set_ylabel("Inertie intra-cluster")
axes[0].axvline(4, color="red", linestyle="--", alpha=0.5, label="k=4")
axes[0].legend()

axes[1].plot(list(K_range), silhouettes, "o-", color="darkorange")
axes[1].set_title("Score de silhouette")
axes[1].set_xlabel("Nombre de clusters k"); axes[1].set_ylabel("Silhouette (↑ = mieux)")
axes[1].axvline(4, color="red", linestyle="--", alpha=0.5, label="k=4")
axes[1].legend()

plt.tight_layout(); plt.show()

best_k = list(K_range)[int(np.argmax(silhouettes))]
print(f"k avec meilleur silhouette : {best_k}")
print(f"Silhouette à k=4 : {silhouettes[2]:.3f}")

# %% [markdown]
# ### 🔍 Interprétation
# - **Coude** : le point où l'inertie cesse de baisser fortement → compromis parcimonie/explication.
# - **Silhouette** ∈ [-1, 1] : mesure la cohésion intra-cluster vs la séparation inter-cluster. Plus proche de 1 = mieux.
# - On retient souvent **k=4** comme bon compromis métier (segments actionnables).

# %%
# 5.5 K-means final à k=4
K_FINAL = 4
kmeans = KMeans(n_clusters=K_FINAL, random_state=RANDOM_STATE, n_init=10)
rfm["cluster"] = kmeans.fit_predict(X_scaled)

# Profiling des clusters : moyennes par cluster
profile = rfm.groupby("cluster").agg(
    nb_clients=("client_id", "count"),
    recence_moy=("recence", "mean"),
    frequence_moy=("frequence", "mean"),
    montant_moy=("montant", "mean"),
).round(0)
profile["part_clients_%"] = (profile["nb_clients"] / profile["nb_clients"].sum() * 100).round(1)
profile = profile.sort_values("montant_moy", ascending=False)
print("Profil des clusters :"); display(profile)

# %%
# 5.6 Visualisation des clusters (pairs plot sur features standardisées)
X_plot = X_scaled.copy()
X_plot["cluster"] = rfm["cluster"].values

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
pairs = [("recence", "frequence"), ("recence", "log_montant"), ("frequence", "log_montant")]
for ax, (x, y) in zip(axes, pairs):
    sns.scatterplot(data=X_plot, x=x, y=y, hue="cluster", palette="viridis",
                    alpha=0.5, s=15, ax=ax, legend=False)
    ax.set_title(f"{x} vs {y}")
plt.suptitle("Segments clients (K-means, k=4) sur features standardisées", y=1.02)
plt.tight_layout(); plt.show()


# %%
# 5.7 Interprétation métier des clusters (nommage)
# Logique : récence basse = récent ; fréquence haute = fréquent ; montant = valeur
def nommer_cluster(g):
    r, f, m = g["recence"].mean(), g["frequence"].mean(), g["montant"].mean()
    if r < rfm["recence"].median() and f > rfm["frequence"].median() and m > rfm["montant"].median():
        return "Champions"
    elif r < rfm["recence"].median() and f > rfm["frequence"].median():
        return "Fidèles"
    elif r > rfm["recence"].median() and f < rfm["frequence"].median():
        return "Endormis"
    else:
        return "Potentiels"

noms_clusters = rfm.groupby("cluster").apply(nommer_cluster, include_groups=False)
rfm["cluster_nom"] = rfm["cluster"].map(noms_clusters)
print(noms_clusters)
print("\nRépartition :")
print(rfm["cluster_nom"].value_counts(normalize=True).round(3))

# %% [markdown]
# ### 🔍 Interprétation métier & actions
#
# Le clustering confirme et enrichit la segmentation RFM :
#
# | Cluster | Profil | Action |
# |---------|--------|--------|
# | **Champions** | Récents, fréquents, gros CA | Programme VIP, cross-sell premium |
# | **Fidèles** | Récents et fréquents, CA moyen | Upsell, parrainage, fidélisation |
# | **Potentiels** | Récents mais peu fréquents | Onboarding, nudge 2e achat |
# | **Endormis** | Anciens, peu fréquents | Réactivation ou win-back |
#
# > 💡 **K-means vs RFM** : le clustering trouve des groupes *naturels* sans règle arbitraire. Il peut révéler des segments inattendus (ex. « gros acheteurs récents mais ponctuels »). À combiner avec l'expertise métier pour le nommage.
# >
# > ⚠️ **Limite** : K-means suppose des clusters sphériques et de taille comparable. Pour des formes complexes, préférer DBSCAN ou Gaussian Mixture.

# %%
# 5.8 (Bonus) Classification Ascendante Hiérarchique (CAH) - échantillon
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

# CAH sur un échantillon (lent sinon)
sample = X_scaled.sample(n=500, random_state=RANDOM_STATE)
Z = linkage(sample, method="ward")

fig, ax = plt.subplots(figsize=(12, 5))
dendrogram(Z, truncate_mode="level", p=5, ax=ax, color_threshold=30)
ax.set_title("Dendrogramme CAH (échantillon 500 clients)")
ax.set_xlabel("Clients"); ax.set_ylabel("Distance")
plt.axhline(30, color="red", linestyle="--", alpha=0.5)
plt.tight_layout(); plt.show()

print("La CAH propose une hiérarchie de regroupements ; on coupe au niveau souhaité.")

# %% [markdown]
# ### 💡 Quand utiliser CAH vs K-means ?
# - **CAH** : petit volume, besoin d'un dendrogramme (visualisation de la hiérarchie), nombre de clusters non connu à l'avance.
# - **K-means** : gros volume, clusters sphériques, k connu. Plus rapide.

# %% [markdown]
# ---
# # §6. Scoring & classification supervisée (S6)
#
# ## 6.1 Du descriptif au prédictif
#
# Jusqu'ici : **analyser** le passé (descriptif). Maintenant : **prédir** l'avenir (prédictif).
#
# Le **scoring** consiste à attribuer à chaque client une **probabilité** qu'un événement se produise (churn, achat, défaut...). C'est la base du **ciblage** marketing.
#
# ### Cadre formel (classification binaire supervisée)
#
# Soit $y \in \{0, 1\}$ la cible (ex. 1 = churn) et $X$ les features. On cherche $f: X \to [0, 1]$ telle que $\hat{p} = f(X)$ estime $P(y=1 | X)$.
#
# | Élément | Rôle |
# |---------|------|
# | **Features** $X$ | Variables explicatives (récence, fréquence, panier, ville...) |
# | **Cible** $y$ | Variable à prédire (churn = 1/0) |
# | **Train set** | Pour entraîner $f$ |
# | **Test set** | Pour évaluer la capacité de généralisation |
# | **Métriques** | AUC, précision, rappel, lift |
#
# > ⚠️ **Fuite de données (data leakage)** : ne jamais inclure dans $X$ une variable qui *révèle* $y$ (ex. « date de résiliation » pour prédire le churn). Toujours se demander : « cette info serait-elle disponible au moment de la prédiction ? »

# %%
# 6.2 Préparation du dataset de scoring churn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, roc_curve)

print("Dataset churn :"); print(f"  {churn.shape[0]} clients, {churn.shape[1]} variables")
print(f"  Taux de churn : {churn['churn'].mean():.2%}")
print("\nColonnes :", list(churn.columns))
churn.head()

# %%
# 6.3 Séparation features / cible
y = churn["churn"]
X = churn.drop(columns=["client_id", "churn", "derniere_achat"])

num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
print("Numériques :", num_cols)
print("Catégorielles :", cat_cols)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y)
print(f"\nTrain : {X_train.shape[0]} | Test : {X_test.shape[0]}")
print(f"Taux churn train : {y_train.mean():.2%} | test : {y_test.mean():.2%}")

# %% [markdown]
# ## 6.2 Prétraitement (pipeline)
#
# On encapsule le prétraitement dans un **`Pipeline`** sklearn pour éviter les fuites et garantir la reproductibilité :
# - **Standardisation** des numériques (z-score).
# - **One-Hot Encoding** des catégorielles.

# %%
# 6.4 Prétraitement (ColumnTransformer)
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
])

pipe_logreg = Pipeline([
    ("preproc", preprocessor),
    ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, class_weight="balanced")),
])
pipe_logreg.fit(X_train, y_train)
proba_logreg = pipe_logreg.predict_proba(X_test)[:, 1]
auc_logreg = roc_auc_score(y_test, proba_logreg)
print(f"Régression logistique - AUC : {auc_logreg:.3f}")

# %%
# 6.5 Modèle 2 : Forêt aléatoire
pipe_rf = Pipeline([
    ("preproc", preprocessor),
    ("clf", RandomForestClassifier(n_estimators=300, max_depth=10,
                                    random_state=RANDOM_STATE, class_weight="balanced",
                                    n_jobs=-1)),
])
pipe_rf.fit(X_train, y_train)
proba_rf = pipe_rf.predict_proba(X_test)[:, 1]
auc_rf = roc_auc_score(y_test, proba_rf)
print(f"Forêt aléatoire - AUC : {auc_rf:.3f}")

# %%
# 6.6 Comparaison visuelle : courbes ROC
fpr_l, tpr_l, _ = roc_curve(y_test, proba_logreg)
fpr_r, tpr_r, _ = roc_curve(y_test, proba_rf)

fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(fpr_l, tpr_l, label=f"Régression logistique (AUC={auc_logreg:.3f})")
ax.plot(fpr_r, tpr_r, label=f"Forêt aléatoire (AUC={auc_rf:.3f})")
ax.plot([0, 1], [0, 1], "k--", alpha=0.3, label="Aléatoire (AUC=0.5)")
ax.set_title("Courbes ROC - Prédiction du churn")
ax.set_xlabel("Taux de faux positifs"); ax.set_ylabel("Taux de vrais positifs")
ax.legend(loc="lower right")
plt.tight_layout(); plt.show()

print(f"Meilleur modèle : {'Forêt aléatoire' if auc_rf > auc_logreg else 'Régression logistique'}")

# %% [markdown]
# ### 🔍 Interprétation métier
# - **AUC** (Area Under ROC Curve) ∈ [0.5, 1] : 0.5 = aléatoire, 1 = parfait. Un AUC > 0.7 est déjà exploitable.
# - La **forêt aléatoire** surpasse souvent la régression logistique car elle capte les **interactions non linéaires** (ex. effet combiné récence × fréquence).
# - Mais la **régression logistique reste intéressante** pour l'**interprétabilité** (coefficients lisibles). En compliance (AML), on privilégie souvent des modèles explicables.

# %%
# 6.7 Matrice de confusion + rapport de classification (modèle retenu)
best_pipe = pipe_rf if auc_rf >= auc_logreg else pipe_logreg
best_name = "Forêt aléatoire" if auc_rf >= auc_logreg else "Régression logistique"
y_pred = best_pipe.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
            xticklabels=["Actif", "Churn"], yticklabels=["Actif", "Churn"])
ax.set_title(f"Matrice de confusion ({best_name})")
ax.set_xlabel("Prédit"); ax.set_ylabel("Réel")
plt.tight_layout(); plt.show()

print(classification_report(y_test, y_pred, target_names=["Actif", "Churn"]))


# %% [markdown]
# ### 🔍 Lecture de la matrice de confusion
# | | Prédit Actif | Prédit Churn |
# |---|---|---|
# | **Réel Actif** | Vrais Négatifs (OK) | Faux Positifs (offre inutile) |
# | **Réel Churn** | Faux Négatifs (client perdu !) | Vrais Positifs (réussite) |
#
# - **Rappel (recall)** = VP / (VP + FN) : parmi les churners réels, combien a-t-on détectés ? Critique si rater un churn coûte cher.
# - **Précision** = VP / (VP + FP) : parmi les clients ciblés, combien churnent vraiment ? Critique si l'action de rétention coûte cher.
# - Le **compromis précision/rappel** dépend du **coût métier** : une campagne de rétention à 5 000 FCFA/client supporte un FP ; une offre premium à 100 000 FCFA non.

# %%
# 6.8 Courbe de lift : valeur du ciblage
def lift_curve(y_true, y_proba, n_bins=10):
    df = pd.DataFrame({"y": y_true.values, "p": y_proba}).sort_values("p", ascending=False)
    df["decile"] = pd.qcut(df["p"].rank(method="first"), n_bins, labels=False)
    base_rate = df["y"].mean()
    lift = df.groupby("decile")["y"].mean() / base_rate
    return lift, base_rate

lift, base = lift_curve(y_test, best_pipe.predict_proba(X_test)[:, 1])

fig, ax = plt.subplots(figsize=(8, 5))
lift.plot(kind="bar", ax=ax, color="teal")
ax.axhline(1, color="red", linestyle="--", label=f"Hasard (base rate {base:.2%})")
ax.set_title("Courbe de lift par décile (modèle retenu)")
ax.set_xlabel("Décile (0 = plus risqué)"); ax.set_ylabel("Lift (× le taux de base)")
ax.legend()
plt.tight_layout(); plt.show()

print(f"Sur le 1er décile (10% les plus risqués) : {lift.iloc[0]:.2f}x plus de churners qu'au hasard")

# %% [markdown]
# ### 🔍 Interprétation métier — le lift, indicateur ROI
#
# Le **lift** mesure le **gain du ciblage** par rapport au hasard :
# - Lift = 2 sur le 1er décile ⇒ en ciblant les 10 % les plus risqués, on touche **2× plus** de churners qu'en ciblant au hasard.
# - ⇒ **ROI de la campagne de rétention multiplié** : on agit sur les clients qui en ont vraiment besoin.
# - C'est l'argument **business** d'un modèle prédictif : transformer la donnée en économie.

# %%
# 6.9 Importance des variables (forêt aléatoire)
ohe = best_pipe.named_steps["preproc"].named_transformers_["cat"]
cat_features = ohe.get_feature_names_out(cat_cols).tolist()
all_features = num_cols + cat_features

importances = best_pipe.named_steps["clf"].feature_importances_
feat_imp = pd.Series(importances, index=all_features).sort_values(ascending=True).tail(15)

fig, ax = plt.subplots(figsize=(8, 6))
feat_imp.plot(kind="barh", ax=ax, color="steelblue")
ax.set_title("Top 15 variables explicatives du churn (forêt aléatoire)")
ax.set_xlabel("Importance")
plt.tight_layout(); plt.show()

# %% [markdown]
# ### 🔍 Interprétation métier — facteurs de churn
# - La **récence** est généralement le facteur n°1 du churn : un client qui n'a pas acheté depuis longtemps risque de partir.
# - La **fréquence** et le **panier moyen** suivent : les clients peu engageants churnent davantage.
# - ⚠️ **Corrélation ≠ causalité** : une récence élevée *indique* le churn, elle ne le *cause* pas. Pour réduire le churn, il faut **agir sur les leviers causaux** (qualité de service, prix, expérience) — idéalement identifiés par des **tests A/B** (§9).
#
# > 📖 **Référence** : Tufféry (2018), *Data Mining et Machine Learning*, chap. « Rétention client ».

# %% [markdown]
# ---
# # §7. Prévision de la demande (régression) (S8)
#
# ## 7.1 De la classification à la régression
#
# La **classification** prédit une catégorie (churn oui/non). La **régression** prédit une **quantité continue** (CA, demande, prix). En marketing, on prédit :
# - le **CA** futur d'un client (CLV prédictive) ;
# - la **demande** d'un produit par période (forecasting) ;
# - le **prix optimal** (élasticité-prix).
#
# ### Métriques de régression
# | Métrique | Formule | Interprétation |
# |----------|---------|----------------|
# | **RMSE** | $\sqrt{\frac{1}{n}\sum(y - \hat y)^2}$ | Écart-type de l'erreur (même unité) |
# | **MAE** | $\frac{1}{n}\sum|y - \hat y|$ | Erreur moyenne absolue (robuste aux outliers) |
# | **MAPE** | $\frac{1}{n}\sum\frac{|y - \hat y|}{y}$ | Erreur en % (comparable entre séries) |
# | **R²** | $1 - \frac{SS_{res}}{SS_{tot}}$ | Part de variance expliquée (0 à 1) |
#
# > ⚠️ Le RMSE pénalise davantage les **grandes erreurs** (carré) → utile quand une grosse erreur coûte très cher (rupture de stock).

# %%
# 7.2 Préparation : CA mensuel agrégé (série temporelle)
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

ca_mensuel = (transactions
              .set_index("date_transaction")
              .resample("ME")["montant_fcfa"].sum()
              .reset_index())
ca_mensuel.columns = ["mois", "ca"]
ca_mensuel["mois_lib"] = ca_mensuel["mois"].dt.month
print(f"Période : {ca_mensuel['mois'].min().date()} → {ca_mensuel['mois'].max().date()}")
print(f"Nb points : {len(ca_mensuel)} mois")
ca_mensuel.head()

# %%
# 7.3 Features temporelles : tendance + saisonnalité
ca_mensuel["t"] = np.arange(len(ca_mensuel))
ca_mensuel["sin12"] = np.sin(2 * np.pi * ca_mensuel["mois_lib"] / 12)
ca_mensuel["cos12"] = np.cos(2 * np.pi * ca_mensuel["mois_lib"] / 12)

split_idx = int(len(ca_mensuel) * 0.8)
feat_cols = ["t", "sin12", "cos12"]
train = ca_mensuel.iloc[:split_idx]
test = ca_mensuel.iloc[split_idx:]

print(f"Train : {len(train)} mois (jusqu'à {train['mois'].max().date()})")
print(f"Test  : {len(test)} mois (à partir de {test['mois'].min().date()})")

# %% [markdown]
# ### ⚠️ Principe clé : pas de `shuffle` sur les séries temporelles
#
# Pour évaluer un modèle prédictif temporel, on **préserve l'ordre** : on entraîne sur le passé et on teste sur le futur. Un `train_test_split` aléatoire ferait de la fuite (le modèle « voit » l'avenir).

# %%
# 7.4 Régression linéaire avec tendance + saisonnalité
model_lr = LinearRegression()
model_lr.fit(train[feat_cols], train["ca"])
pred_lr = model_lr.predict(test[feat_cols])

rmse_lr = np.sqrt(mean_squared_error(test["ca"], pred_lr))
mae_lr = mean_absolute_error(test["ca"], pred_lr)
mape_lr = np.mean(np.abs((test["ca"] - pred_lr) / test["ca"])) * 100
r2_lr = r2_score(test["ca"], pred_lr)

print(f"Régression linéaire :")
print(f"  RMSE : {rmse_lr:,.0f} FCFA")
print(f"  MAE  : {mae_lr:,.0f} FCFA")
print(f"  MAPE : {mape_lr:.1f}%")
print(f"  R²   : {r2_lr:.3f}")

# %%
# 7.5 Forêt aléatoire (capture les non-linéarités)
model_rf = RandomForestRegressor(n_estimators=300, random_state=RANDOM_STATE, max_depth=6)
model_rf.fit(train[feat_cols], train["ca"])
pred_rf = model_rf.predict(test[feat_cols])

rmse_rf = np.sqrt(mean_squared_error(test["ca"], pred_rf))
mape_rf = np.mean(np.abs((test["ca"] - pred_rf) / test["ca"])) * 100
print(f"Forêt aléatoire : RMSE={rmse_rf:,.0f} | MAPE={mape_rf:.1f}%")

# %%
# 7.6 Visualisation : prédictions vs réalité
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(ca_mensuel["mois"], ca_mensuel["ca"], label="Réel", color="black", linewidth=2)
ax.plot(test["mois"], pred_lr, label=f"Régression linéaire (MAPE {mape_lr:.1f}%)", color="teal")
ax.plot(test["mois"], pred_rf, label=f"Forêt aléatoire (MAPE {mape_rf:.1f}%)", color="darkorange")
ax.axvline(test["mois"].min(), color="grey", linestyle="--", alpha=0.5, label="Début du test")
ax.set_title("Prévision du CA mensuel (IvoireMarket)")
ax.set_ylabel("CA (FCFA)"); ax.set_xlabel("")
ax.legend()
plt.tight_layout(); plt.show()

# %% [markdown]
# ### 🔍 Interprétation métier
# - Un **MAPE < 15 %** est déjà exploitable pour la planification des stocks et des campagnes.
# - La **régression linéaire avec tendance + saisonnalité** est une baseline robuste et **explicable** (coefficients lisibles).
# - La **forêt aléatoire** peut mieux capter les non-linéarités, mais risque le **surapprentissage** sur de petites séries (peu de mois). Toujours comparer sur le test.
# - ⚠️ Le modèle suppose que les **patterns passés se prolongent**. Un choc exogène (dévaluation, confinement) invalide la prévision → toujours assortir d'une **analyse de scénarios**.

# %%
# 7.7 Prévision à 6 mois (horizon de planification)
horizon = 6
last_t = ca_mensuel["t"].max()
future = pd.DataFrame({
    "t": np.arange(last_t + 1, last_t + 1 + horizon),
    "mois_lib": [(ca_mensuel["mois"].dt.month.iloc[-1] + i - 1) % 12 + 1 for i in range(1, horizon + 1)],
})
future["sin12"] = np.sin(2 * np.pi * future["mois_lib"] / 12)
future["cos12"] = np.cos(2 * np.pi * future["mois_lib"] / 12)
future["mois"] = pd.date_range(start=ca_mensuel["mois"].max() + pd.offsets.MonthEnd(1),
                                periods=horizon, freq="ME")

future["ca_pred"] = model_lr.predict(future[feat_cols])
print("Prévision CA des 6 prochains mois :")
print(future[["mois", "ca_pred"]].to_string(index=False))

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(ca_mensuel["mois"], ca_mensuel["ca"], label="Historique", color="black")
ax.plot(future["mois"], future["ca_pred"], label="Prévision", color="teal", linestyle="--", marker="o")
ax.set_title("Prévision du CA à 6 mois (régression linéaire)")
ax.set_ylabel("CA (FCFA)")
ax.legend()
plt.tight_layout(); plt.show()

# %% [markdown]
# ### 🔍 Interprétation métier & usage
# - La prévision à 6 mois éclaire : la **trésorerie**, le **recrutement** (saisonnalité), la **négociation fournisseurs**, le **planning des campagnes**.
# - ⚠️ Toujours fournir un **intervalle de confiance** en production (bootstrap, quantiles). Une prévision ponctuelle donne une illusion de fausse précision.
# - En marketing analytics, on croise la prévision de **demande** avec le **scoring de propension** pour décider *où* et *quand* lancer les campagnes.

# %% [markdown]
# ---
# # §8. Web & social analytics (S9)
#
# ## 8.1 De la donnée transactionnelle à la donnée digitale
#
# Les données CRM (§3) décrivent *l'achat*. Les données **web/social** décrivent *le parcours* qui mène à l'achat :
# - **Web analytics** : pages vues, sessions, sources de trafic (GA4).
# - **Social analytics** : likes, partages, portée, engagement (Facebook, Instagram, TikTok).
# - **Entonnoir (funnel)** : Visiteurs → Inscrits → Panier → Achat.
#
# > 💡 **KPI digital emblématique** : le **taux de conversion** = achats / visites. En e-commerce, 1-3 % est courant ; au-delà de 5 % c'est excellent.
#
# ## 8.2 Paramètres UTM et sources de trafic
#
# Les **UTM** (Urchin Tracking Module) sont des paramètres d'URL qui identifient la source d'une visite :
# `?utm_source=facebook&utm_medium=cpc&utm_campaign=soldes_2024`
#
# Ils permettent d'**attribuer** une conversion à un canal — base de l'attribution multi-touch (§11).
#
# ## 8.3 Analyse de cohorte (cohortes)
#
# Une **cohorte** = groupe d'utilisateurs partageant un événement commun (ex. inscrits en janvier 2024). On suit leur comportement dans le temps (rétention, CA cumulé).
#
# > La **rétention** est souvent le meilleur indicateur de la santé d'un produit digital. Une courbe de rétention qui se stabilise = un produit qui crée de l'habitude.

# %%
# 8.4 Simulation de données web/social (sessions par jour et source)
rng_web = np.random.default_rng(RANDOM_STATE + 10)

dates = pd.date_range("2024-09-01", periods=90, freq="D")
sources = ["Organic", "Facebook Ads", "Google Ads", "Direct", "Instagram", "WhatsApp"]

base = 500
tendance = np.linspace(0, 200, 90)
hebdo = np.where(dates.dayofweek >= 5, 150, 0)
bruit = rng_web.normal(0, 60, 90)

sessions = pd.DataFrame({
    "date": dates,
    "sessions_total": (base + tendance + hebdo + bruit).clip(min=50).astype(int),
})
repart = np.array([0.30, 0.20, 0.15, 0.15, 0.12, 0.08])
sessions_par_source = []
for i, s in enumerate(sources):
    n = (sessions["sessions_total"] * repart[i] * rng_web.normal(1, 0.08, 90)).astype(int)
    sessions_par_source.append(pd.DataFrame({"date": dates, "source": s, "sessions": n}))
web = pd.concat(sessions_par_source, ignore_index=True)

print(f"Web analytics simulé : {len(web)} lignes ({len(sources)} sources x 90 jours)")
print(web.groupby("source")["sessions"].sum())

# %%
# 8.5 Taux de conversion par source (simulation)
conv_rates = {"Organic": 0.025, "Facebook Ads": 0.018, "Google Ads": 0.030,
              "Direct": 0.045, "Instagram": 0.020, "WhatsApp": 0.060}

web["conversions"] = web.apply(
    lambda r: rng_web.binomial(r["sessions"], conv_rates[r["source"]]), axis=1)
web["taux_conversion"] = web["conversions"] / web["sessions"]

conv_par_source = web.groupby("source").agg(
    sessions=("sessions", "sum"),
    conversions=("conversions", "sum"),
).assign(taux_conv=lambda d: (d["conversions"] / d["sessions"]).round(4))
conv_par_source = conv_par_source.sort_values("taux_conv", ascending=False)
print("Performance par source de trafic :")
display(conv_par_source)

# %%
# 8.6 Visualisation : trafic + taux de conversion par source
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

(web.pivot(index="date", columns="source", values="sessions")
   .rolling(7).mean()
   .plot(ax=axes[0], linewidth=2))
axes[0].set_title("Trafic par source (moyenne mobile 7 j)")
axes[0].set_ylabel("Sessions/jour"); axes[0].legend(fontsize=8)

conv_par_source["taux_conv"].plot(kind="barh", ax=axes[1], color="teal")
axes[1].set_title("Taux de conversion par source")
axes[1].set_xlabel("Taux de conversion")
axes[1].set_ylabel("")
plt.tight_layout(); plt.show()

# %% [markdown]
# ### 🔍 Interprétation métier
# - **WhatsApp** a le meilleur taux de conversion (6 %) — typique en Côte d'Ivoire (canal de confiance, conversation 1-à-1).
# - **Google Ads** convertit mieux que Facebook Ads (intention de recherche = acheteuse).
# - **Direct** = clients qui connaissent déjà la marque → forte conversion.
# - ⚠️ Ne pas confondre **volume** et **qualité** : Facebook Ads génère du volume mais convertit moins → calculer le **CPA** (coût par acquisition) par canal.
# - Le **taux de conversion** seul ne suffit pas : un canal peut convertir à 5 % mais coûter cher en publicité → arbitrer via le **ROAS** (Return On Ad Spend).

# %%
# 8.7 Analyse de cohorte : rétention des inscrits par mois
rng_coh = np.random.default_rng(RANDOM_STATE + 11)
cohortes = pd.date_range("2024-01-01", periods=6, freq="MS")
months_labels = [d.strftime("%Y-%m") for d in cohortes]
n_inscrits = [120, 150, 180, 200, 220, 250]

retenue_base = [1.00, 0.60, 0.45, 0.38, 0.33, 0.30]

matrice = np.zeros((len(cohortes), 6))
for i, n in enumerate(n_inscrits):
    for j in range(6):
        if i + j < 6:
            rate = retenue_base[j] * rng_coh.normal(1, 0.05)
            matrice[i, j] = n * rate

cohort_df = pd.DataFrame(matrice, index=months_labels,
                          columns=[f"M{j}" for j in range(6)])

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(cohort_df, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
ax.set_title("Matrice de cohorte : clients actifs par mois depuis inscription")
ax.set_xlabel("Mois depuis inscription"); ax.set_ylabel("Cohorte d'inscription")
plt.tight_layout(); plt.show()

# %% [markdown]
# ### 🔍 Interprétation métier
# - La **première colonne (M0)** = taille de chaque cohorte (inscrits du mois).
# - En **ligne** : la rétention dans le temps d'une cohorte. La chute M0→M1 (~40 %) est normale (effet « nouveauté »).
# - En **diagonale** : tous les clients actifs à un mois calendaire donné.
# - Une rétention qui se **stabilise** (M3→M5) indique un produit qui fidélise. Si elle chute à 0, le produit ne crée pas d'habitude → enquête (qualité, prix, expérience).
#
# > 📖 **Référence** : Chaffey & Ellis-Chadwick (2019), *Digital Marketing*, chap. « Digital media analytics ».

# %% [markdown]
# ---
# # §9. Tests A/B & expérimentation (S10)
#
# ## 9.1 Pourquoi expérimenter ?
#
# L'observation (§3-§8) révèle des **corrélations**, pas des **causalités**. Pour savoir si une action (nouveau message, offre, design) *cause* une amélioration, il faut une **expérimentation contrôlée** : le **test A/B**.
#
# ### Principe
# 1. Définir une **hypothèse** (ex. « l'offre -10 % augmente le taux de conversion »).
# 2. Répartir **aléatoirement** les utilisateurs en 2 groupes :
#    - **A (contrôle)** : version actuelle.
#    - **B (variant)** : nouvelle version.
# 3. Mesurer la métrique cible sur les deux groupes.
# 4. Tester la **significativité statistique** de la différence.
#
# > ⚠️ Sans randomisation, on ne peut pas conclure : les groupes pourraient différer *avant* l'expérience (biais de sélection).
#
# ## 9.2 Risques d'erreur (statistique)
# | | H0 vraie (pas d'effet) | H0 fausse (effet réel) |
# |---|---|---|
# | Rejeter H0 | **Erreur α (faux positif)** | ✓ Bonne détection (1-β) |
# | Ne pas rejeter H0 | ✓ Bonne décision | **Erreur β (faux négatif)** |
#
# - **α** (seuil de signification) : probabilité de voir un effet là où il n'y en a pas. Généralement 5 %.
# - **β** : probabilité de rater un effet réel. **Puissance** = 1 - β (souvent 80 %).
# - La **taille d'échantillon** se calcule pour garantir α et β voulus.

# %%
# 9.3 Test A/B sur les campagnes (données campagnes.csv)
ab = campagnes.copy()
print(f"Campagnes : {len(ab)}")
print("Effectifs par groupe :")
print(ab["groupe_test"].value_counts())

taux_groupe = ab.groupby("groupe_test")["taux_conversion"].agg(["mean", "count"])
taux_groupe.columns = ["taux_conv_moyen", "nb_campagnes"]
print("\nTaux de conversion moyen par groupe :")
display(taux_groupe)

diff = taux_groupe.loc["B", "taux_conv_moyen"] - taux_groupe.loc["A", "taux_conv_moyen"]
print(f"\nDifférence brute (B - A) : {diff:.4f} (+{diff/taux_groupe.loc['A','taux_conv_moyen']:.1%})")

# %%
# 9.4 Test statistique : comparaison de deux proportions
ab["nb_conversions"] = (ab["nb_envois"] * ab["taux_conversion"]).round().astype(int)

groupe_A = ab[ab["groupe_test"] == "A"]
groupe_B = ab[ab["groupe_test"] == "B"]

conv_A = groupe_A["nb_conversions"].sum()
envoi_A = groupe_A["nb_envois"].sum()
conv_B = groupe_B["nb_conversions"].sum()
envoi_B = groupe_B["nb_envois"].sum()

p_A = conv_A / envoi_A
p_B = conv_B / envoi_B
print(f"Groupe A : {conv_A:,} conv / {envoi_A:,} envois = {p_A:.4f}")
print(f"Groupe B : {conv_B:,} conv / {envoi_B:,} envois = {p_B:.4f}")
print(f"Lift absolu : {p_B - p_A:.4f} ({(p_B - p_A)/p_A:+.2%})")

# %%
# 9.5 Test Z pour deux proportions
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

count = np.array([conv_B, conv_A])
nobs = np.array([envoi_B, envoi_A])
z_stat, p_value = proportions_ztest(count, nobs)

ci_A = proportion_confint(conv_A, envoi_A, alpha=0.05)
ci_B = proportion_confint(conv_B, envoi_B, alpha=0.05)

print(f"Z-statistic : {z_stat:.3f}")
print(f"p-value     : {p_value:.6f}")
print(f"IC 95% A : [{ci_A[0]:.4f} ; {ci_A[1]:.4f}]")
print(f"IC 95% B : [{ci_B[0]:.4f} ; {ci_B[1]:.4f}]")
print("\nDécision (seuil alpha=5%) :")
print("  ✅ Différence significative, on rejette H0 (le variant B est meilleur)."
      if p_value < 0.05 else
      "  ❌ Pas de différence significative, on ne rejette pas H0.")

# %%
# 9.6 Visualisation : taux de conversion + intervalles de confiance
fig, ax = plt.subplots(figsize=(8, 5))
groupes = ["A (contrôle)", "B (offre incitative)"]
means = [p_A, p_B]
yerr = [[p_A - ci_A[0], p_B - ci_B[0]], [ci_A[1] - p_A, ci_B[1] - p_B]]

ax.bar(groupes, means, yerr=yerr, capsize=10, color=["grey", "teal"], alpha=0.8)
ax.set_title("Test A/B : taux de conversion par groupe (IC 95%)")
ax.set_ylabel("Taux de conversion")
for i, m in enumerate(means):
    ax.text(i, m + 0.003, f"{m:.4f}", ha="center", fontsize=11)
ax.set_ylim(0, max(ci_B[1], ci_A[1]) * 1.2)
plt.tight_layout(); plt.show()

print(f"Lift relatif de B vs A : {(p_B - p_A)/p_A:+.2%}")

# %% [markdown]
# ### 🔍 Interprétation métier — le test A/B
# - Si **p-value < 5 %** : la différence est **statistiquement significative**. On peut déployer le variant B avec confiance.
# - Le **lift relatif** (+35 % par exemple) est l'argument business : pour chaque franc dépensé, on gagne X % de conversions en plus.
# - L'**intervalle de confiance** donne l'incertitude : si les IC ne se chevauchent pas, la différence est robuste.
# - ⚠️ **Attention aux pièges** :
#   - **Taille d'échantillon** insuffisante → test non concluant (erreur β).
#   - **Effet peaking** : vérifier le test en continu gonfle les faux positifs (correction de Bonferroni).
#   - **Interactions** : un variant peut marcher sur un segment et pas sur un autre → analyser **par segment**.

# %%
# 9.7 Calcul de la taille d'échantillon nécessaire (power analysis)
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

p_base = 0.12
mde = 0.01
alpha = 0.05
power = 0.80

effect_size = proportion_effectsize(p_base + mde, p_base)
analysis = NormalIndPower()
n_par_groupe = int(np.ceil(analysis.solve_power(effect_size=effect_size, alpha=alpha,
                                                power=power, ratio=1.0)))
print(f"Taux de base : {p_base:.2%}")
print(f"Effet minimal à détecter : +{mde:.2%}")
print(f"Puissance visée : {power:.0%} | Seuil alpha : {alpha:.0%}")
print(f"\n>>> Taille d'échantillon nécessaire : {n_par_groupe:,} utilisateurs PAR groupe")
print(f">>> Soit {2*n_par_groupe:,} utilisateurs au total")
print(f">>> Notre test ({envoi_A+envoi_B:,} envois) : "
      f"{'SUFFISANT ✅' if envoi_A+envoi_B >= 2*n_par_groupe else 'INSUFFISANT ❌'}")

# %% [markdown]
# ### 🔍 Interprétation métier
# - Plus l'**effet attendu est petit**, plus il faut d'utilisateurs pour le détecter (avec puissance).
# - Calculer la taille **avant** de lancer le test évite de conclure à tort « pas d'effet » alors que le test manquait de puissance.
# - En pratique marketing : on cherche des **lifts de 1 à 5 %** → il faut souvent des dizaines de milliers de visiteurs.
#
# > 📖 **Référence** : Kohavi, Tang & Xu (2020), *Trustworthy Online Controlled Experiments* — la référence sur l'expérimentation web.

# %% [markdown]
# ---
# # §10. Tableaux de bord & pilotage (S11)
#
# ## 10.1 Du modèle au pilotage
#
# Un modèle prédictif n'a de valeur que s'il **alimente une décision**. Le **tableau de bord** est l'interface entre la donnée et l'action.
#
# ### Principes d'un bon dashboard
# 1. **One screen, one message** : un dashboard doit répondre à une question principale.
# 2. **Hiérarchie visuelle** : KPIs en haut, détail en bas.
# 3. **Comparaison** : toujours comparer à une référence (vs période précédente, vs objectif, vs benchmark).
# 4. **Drill-down** : du global au détail (ex. CA total -> par canal -> par campagne).
# 5. **Fréquence adaptée** : opérationnel = temps réel/journalier ; stratégique = mensuel.
#
# ### Outils
# | Outil | Usage |
# |-------|-------|
# | **Power BI** | Tableaux de bord corporate, DAX |
# | **Tableau** | Exploration visuelle, drag-and-drop |
# | **plotly Dash** | Dashboards Python custom, intégration ML |
# | **Looker Studio** | Gratuit, intégration Google (GA4) |
#
# > Ici on construit un **mini-dashboard** matplotlib/plotly pour montrer la logique.

# %%
# 10.2 Mini-dashboard synthétique (matplotlib subplots)
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

ax1 = fig.add_subplot(gs[0, :])
ca_mensuel_df = transactions.set_index("date_transaction").resample("ME")["montant_fcfa"].sum()
ca_mensuel_df.plot(ax=ax1, color="teal", linewidth=2)
ax1.set_title("CA mensuel (3 ans)")
ax1.set_ylabel("FCFA"); ax1.set_xlabel("")

ax2 = fig.add_subplot(gs[1, 0])
ca_canal = transactions.groupby("canal_achat")["montant_fcfa"].sum().sort_values()
ca_canal.plot(kind="barh", ax=ax2, color="steelblue")
ax2.set_title("CA par canal"); ax2.set_xlabel("FCFA")

ax3 = fig.add_subplot(gs[1, 1])
rfm["segment_rfm"].value_counts().plot(kind="bar", ax=ax3, color="darkorange", rot=20)
ax3.set_title("Segments RFM"); ax3.set_ylabel("Clients")

ax4 = fig.add_subplot(gs[1, 2])
churn_vals = churn["churn"].value_counts().sort_index()
ax4.pie(churn_vals, labels=["Actif", "Churn"], autopct="%1.1f%%",
        colors=["#66c2a5", "#fc8d62"], startangle=90)
ax4.set_title(f"Taux de churn : {churn['churn'].mean():.1%}")

ax5 = fig.add_subplot(gs[2, 0])
ax5.hist(transactions["montant_fcfa"], bins=40, color="purple", edgecolor="white")
ax5.set_title("Distribution panier"); ax5.set_xlabel("FCFA")

ax6 = fig.add_subplot(gs[2, 1])
transactions.groupby("categorie_produit")["montant_fcfa"].sum().sort_values().plot(
    kind="barh", ax=ax6, color="seagreen")
ax6.set_title("CA par categorie"); ax6.set_xlabel("FCFA")

ax7 = fig.add_subplot(gs[2, 2])
web.groupby("source")["sessions"].sum().sort_values().plot(kind="barh", ax=ax7, color="indianred")
ax7.set_title("Sessions par source"); ax7.set_xlabel("Sessions")

fig.suptitle("Dashboard IvoireMarket - Vue d'ensemble", fontsize=15, y=1.005)
plt.tight_layout(); plt.show()

# %% [markdown]
# ### 🔍 Interprétation stratégique
# Ce dashboard répond en un écran aux questions du COMEX :
# - « Où en est le CA ? » (tendance + saisonnalité)
# - « Quels canaux performants ? » (boutique vs digital)
# - « Quelle est la santé de la base client ? » (segments + churn)
# - « Quels produits/porteurs ? » (catégories)
# - « D'où vient le trafic digital ? » (sources)
#
# > 💡 **Recommandation** : en production, automatiser ce dashboard (Power BI / Dash) avec **refresh quotidien** et **alertes** (ex. churn > seuil).

# %% [markdown]
# ---
# # §11. Attribution & CLV prédictive (S12)
#
# ## 11.1 CLV prédictive (modélisée)
#
# La CLV **historique** (§3.3) s'appuie sur le passé. La CLV **prédictive** projette la valeur future d'un client à partir d'un modèle. Deux grandes familles :
# - **Modèles probabilistes (BG/NBD + Gamma-Gamma)** : adaptés aux données transactionnelles non contractuelles (retail/e-commerce).
# - **Modèles ML (régression)** : prédire directement le CA futur à partir de features.
#
# > Ici, on illustre l'approche ML simple : prédire le CA futur à partir de features RFM passées.

# %%
# 11.2 Préparation des données pour CLV prédictive
# Principe : features à la date T-12mois -> prédire le CA sur les 12 mois suivants
date_split = transactions["date_transaction"].max() - pd.DateOffset(months=12)

tx_past = transactions[transactions["date_transaction"] < date_split]
features_clv = tx_past.groupby("client_id").agg(
    nb_achats=("transaction_id", "count"),
    ca_passe=("montant_fcfa", "sum"),
    panier_moyen=("montant_fcfa", "mean"),
).reset_index()

tx_future = transactions[transactions["date_transaction"] >= date_split]
ca_future = tx_future.groupby("client_id")["montant_fcfa"].sum().rename("ca_futur")

data_clv = features_clv.merge(ca_future, on="client_id", how="left")
data_clv["ca_futur"] = data_clv["ca_futur"].fillna(0)
print(f"Clients pour CLV prédictive : {len(data_clv)}")
print(f"Clients sans achat futur : {(data_clv['ca_futur']==0).sum()} ({(data_clv['ca_futur']==0).mean():.1%})")
data_clv.head()

# %%
# 11.3 Modèle de régression : prédire le CA futur par client
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

X_clv = data_clv[["nb_achats", "ca_passe", "panier_moyen"]]
y_clv = data_clv["ca_futur"]

X_tr, X_te, y_tr, y_te = train_test_split(X_clv, y_clv, test_size=0.25, random_state=RANDOM_STATE)

model_clv = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=RANDOM_STATE)
model_clv.fit(X_tr, y_tr)
pred_clv = model_clv.predict(X_te)

mae_clv = mean_absolute_error(y_te, pred_clv)
r2_clv = r2_score(y_te, pred_clv)
print(f"CLV prédictive (Gradient Boosting) :")
print(f"  MAE : {mae_clv:,.0f} FCFA")
print(f"  R²  : {r2_clv:.3f}")

# %%
# 11.4 Visualisation : prédiction vs réalité (top clients)
resultats = pd.DataFrame({"reel": y_te, "predit": pred_clv}).sort_values("reel", ascending=False)

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(resultats["reel"], resultats["predit"], alpha=0.3, s=12, color="teal")
lim = max(resultats["reel"].max(), resultats["predit"].max())
ax.plot([0, lim], [0, lim], "r--", alpha=0.5, label="Prediction parfaite")
ax.set_title("CLV prédictive : CA futur prédit vs réel")
ax.set_xlabel("CA réel (12 mois)"); ax.set_ylabel("CA prédit")
ax.legend()
plt.tight_layout(); plt.show()

print(f"CA futur total réel    : {y_te.sum():,.0f} FCFA")
print(f"CA futur total prédit  : {pred_clv.sum():,.0f} FCFA")

# %% [markdown]
# ### 🔍 Interprétation métier
# - Le modèle identifie les clients à **fort potentiel futur** avant même qu'ils ne dépensent -> ciblage **proactif** (offres, service VIP).
# - ⚠️ Le R² peut être modéré : prédire un comportement individuel est difficile. L'agrégat (CA total prédit) est souvent plus fiable que l'individu.
# - La CLV prédictive guide le **CAC max acceptable** : si je sais qu'un client vaut 150 000 FCFA sur 12 mois, je peux investir jusqu'à 50 000 FCFA pour l'acquérir (ratio 3:1).
#
# ## 11.2 Attribution multi-touch
#
# L'**attribution** répond à : « quel canal mérite la conversion ? ». Modèles courants :
# - **Last-click** : 100 % au dernier canal (simple mais injuste pour les canaux de découverte).
# - **First-click** : 100 % au premier canal.
# - **Linéaire** : répartition égale entre tous les canaux du parcours.
# - **Data-driven** (Markov, Shapley) : basé sur les données.

# %%
# 11.5 Attribution linéaire simulée (parcours multi-canal)
rng_att = np.random.default_rng(RANDOM_STATE + 20)
canaux_parcours = ["Organic", "Facebook Ads", "Google Ads", "Direct", "Email", "WhatsApp"]
n_parcours = 2000

parcours = []
for _ in range(n_parcours):
    k = rng_att.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
    canaux = rng_att.choice(canaux_parcours, size=k, replace=False)
    parcours.append(list(canaux))

credit = {c: 0.0 for c in canaux_parcours}
for p in parcours:
    poids = 1.0 / len(p)
    for c in p:
        credit[c] += poids

attrib = pd.Series(credit).sort_values(ascending=False)
print("Attribution linéaire (conversions créditées par canal) :")
print(attrib.round(1))

# %%
# 11.6 Comparaison : Last-click vs Linéaire
last_click = {c: 0 for c in canaux_parcours}
for p in parcours:
    last_click[p[-1]] += 1

compa = pd.DataFrame({
    "Last_click": pd.Series(last_click),
    "Lineaire": attrib,
}).fillna(0)
compa = compa.sort_values("Lineaire", ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
compa.plot(kind="bar", ax=ax, color=["grey", "teal"])
ax.set_title("Attribution : Last-click vs Linéaire")
ax.set_ylabel("Conversions créditées"); ax.set_xlabel("")
plt.xticks(rotation=15)
plt.tight_layout(); plt.show()

print(compa)

# %% [markdown]
# ### 🔍 Interprétation métier
# - Le **last-click** sous-estime les canaux de **découverte** (Organic, Facebook Ads) qui amènent le client mais ne le convertissent pas directement.
# - L'attribution **linéaire** est plus juste mais ignore l'**ordre** des canaux.
# - L'attribution **data-driven** (modèles de Markov) mesure l'**effet réel** de chaque canal (retrait = combien de conversions perdues ?) -> c'est la méthode à privilégier quand on a les données.
# - ⚠️ L'attribution reste une **modélisation** : aucune méthode n'est parfaite. Le test A/B incrémental (§9) reste la preuve de causalité ultime.

# %% [markdown]
# ---
# # §10bis. Du dataframe au modèle dimensionnel (schéma en étoile)
#
# ## 10bis.1 Pourquoi un modèle dimensionnel ?
#
# Jusqu'ici, nous avons travaillé sur des **dataframes plats** (`clients.csv`, `transactions.csv`...) chargés en pandas. C'est parfait pour l'analyse en Python. Mais pour alimenter un **SGBD** (PostgreSQL, MySQL, SQL Server) puis un outil de **Business Intelligence** (Power BI, Excel/Power Pivot, Tableau), on adopte une modélisation spécifique : le **schéma en étoile** (Kimball).
#
# ### Principes du schéma en étoile
# 1. **Table(s) de fait** au centre : contiennent les **mesures quantitatives** (CA, quantité) + les **clés étrangères** vers les dimensions.
# 2. **Tables de dimensions** autour : contiennent les **attributs descriptifs** (nom du client, catégorie, mois...).
# 3. **Clés surrogate** (synthétiques) : on remplace les clés naturelles par des entiers auto-incrémentés (`client_key`, `date_key`...). Cela isole le modèle des changements de source.
# 4. **Granularité** unique par table de fait (ici : 1 ligne = 1 transaction).
#
# ```
#                   dim_clients
#                        │
# dim_produits ── fact_transactions ── dim_canaux
#                        │
#                   dim_temps
# ```
#
# > 💡 **Bénéfice** : en BI, les jointures sont prévisibles (toujours dimension → fait), les agrégations sont rapides, et l'utilisateur métier navigue naturellement (ex. « CA par ville et par mois » = filtre dim_clients.ville × dim_temps.mois, mesure SUM(ca_net)).
#
# ## 10bis.2 Correspondance : sources plates → modèle dimensionnel
#
# Nous avons généré ce modèle à partir des sources existantes (script `scripts/dw_build_dim.py` + `dw_build_fact.py`). Voici le mapping :
#
# | Source (plat) | → | Table DW | Type |
# |---------------|---|-----------|------|
# | `clients.csv` | → | `dim_clients` (+ tranche_age, statut dérivés) | Dimension |
# | dates des transactions | → | `dim_temps` (annee, mois, weekend...) | Dimension |
# | `categorie_produit` de transactions | → | `dim_produits` (+ gamme, marge) | Dimension |
# | `canal_achat` / `canal_acquisition` | → | `dim_canaux` (+ type, coût) | Dimension |
# | `campagnes.csv` | → | `dim_campagnes` (+ durée, coût par envoi) | Dimension |
# | `transactions.csv` | → | `fact_transactions` (mesures + FK) | **Fait** |

# %%
# 10bis.3 Démonstration : charger le DW en pandas et faire une analyse "à la BI"
# Le DW vit dans data/dw/ (généré par scripts/dw_build_dim.py + dw_build_fact.py)
DW_DIR = "../data/dw"

dim_clients_dw = pd.read_csv(f"{DW_DIR}/dim_clients.csv")
dim_temps_dw = pd.read_csv(f"{DW_DIR}/dim_temps.csv", parse_dates=["date"])
dim_produits_dw = pd.read_csv(f"{DW_DIR}/dim_produits.csv")
dim_canaux_dw = pd.read_csv(f"{DW_DIR}/dim_canaux.csv")
fact_tx = pd.read_csv(f"{DW_DIR}/fact_transactions.csv")

print("Tables DW chargées :")
print(f"  dim_clients  : {dim_clients_dw.shape}")
print(f"  dim_temps    : {dim_temps_dw.shape}")
print(f"  dim_produits : {dim_produits_dw.shape}")
print(f"  dim_canaux   : {dim_canaux_dw.shape}")
print(f"  fact_tx      : {fact_tx.shape}")

# %%
# 10bis.4 Requête analytique "à la BI" : CA net par ville et par année
# Équivalent d'un tableau croisé dynamique / d'un visuel Power BI
ca_ville_annee = (fact_tx
    .merge(dim_clients_dw[["client_key", "ville"]], on="client_key")
    .merge(dim_temps_dw[["date_key", "annee"]], on="date_key")
    .groupby(["ville", "annee"])["ca_net_fcfa"]
    .sum()
    .unstack(fill_value=0)
)

print("CA net (FCFA) par ville × année :")
display(ca_ville_annee.head(6).map(lambda x: f"{x:,.0f}"))

# Vérification d'intégrité : aucune FK orpheline
fk_ok = all(
    fact_tx[fk].isin(keys).all()
    for fk, keys in [
        ("client_key", dim_clients_dw["client_key"]),
        ("date_key", dim_temps_dw["date_key"]),
        ("produit_key", dim_produits_dw["produit_key"]),
        ("canal_key", dim_canaux_dw["canal_key"]),
    ]
)
statut = "OK (0 orphelin)" if fk_ok else "KO"
print("\nIntégrité référentielle :", statut)


# %% [markdown]
# ### 🔍 Interprétation métier
# - Le passage au modèle dimensionnel **ne change pas les chiffres** (CA net total identique), mais il **structure** la donnée pour la BI.
# - La jointure `fact × dim_clients × dim_temps` est l'équivalent pandas d'un **tableau croisé dynamique** Excel ou d'un visuel Power BI « CA par ville et par année ».
# - ⚠️ **Le DW est dérivé des sources** : si on régénère `data/*.csv` (`generate_datasets.py`), il faut **régénérer le DW** (`dw_build_dim.py` puis `dw_build_fact.py`) pour garder la cohérence.
#
# ## 10bis.3 Mesures calculées (équivalent DAX)
#
# En Power BI / Excel, on définit des **mesures DAX**. Voici les équivalents pandas et DAX :
#
# | Mesure | pandas | DAX (Power BI/Excel) |
# |--------|--------|----------------------|
# | CA net | `fact_tx['ca_net_fcfa'].sum()` | `CA Net = SUM(fact_transactions[ca_net_fcfa])` |
# | Marge brute | `fact_tx['marge_brute_fcfa'].sum()` | `Marge Brute = SUM(fact_transactions[marge_brute_fcfa])` |
# | Taux de marge % | `marge / ca_net` | `Taux Marge % = DIVIDE([Marge Brute], [CA Net])` |
# | Panier moyen | `ca_net / nb_tx` | `Panier Moyen = DIVIDE([CA Net], COUNTROWS(fact_transactions))` |
#
# > 📖 **Référence** : Ralph Kimball, *The Data Warehouse Toolkit* (2013) — la bible de la modélisation dimensionnelle.
# > Le fichier `docs/modele_dimensionnel.md` détaille le schéma complet et le guide Power BI/Excel.

# %% [markdown]
# ---
# # §12. Synthèse, limites & bonnes pratiques (S13-S14)
#
# ## 12.1 Synthèse de la chaîne de valeur marketing analytics
#
# ```
# Données (CRM, web, social)
#     ↓ Nettoyage & intégration (§2)
# Analyse descriptive (KPI, RFM, CLV historique) (§3)
#     ↓ Visualisation & storytelling (§4)
# Segmentation (RFM, clustering) (§5)
#     ↓ Modélisation prédictive
# Scoring (churn, propension) (§6) + Prévision demande (§7)
#     ↓ Digital analytics
# Web/social analytics (§8) + Tests A/B (§9)
#     ↓ Restitution & action
# Tableaux de bord (§10) + CLV prédictive & attribution (§11)
#     ↓ Décision
# Ciblage, personnalisation, optimisation budget marketing
# ```
#
# ## 12.2 Rappel : corrélation ≠ causalité
#
# | Symptôme | Erreur fréquente | Bonne pratique |
# |----------|-----------------|----------------|
# | « Les VIP dépensent plus -> le programme VIP augmente les ventes » | Inversion cause/effet (sélection) | Test A/B randomisé |
# | « Le CA baisse le lundi -> c'est à cause de la pluie » | Corrélation fallacieuse | Vérifier un mécanisme causal |
# | « Le modèle a 95 % d'accuracy -> il est bon » | Surapprentissage (test = train) | Split train/test, validation croisée |
# | « Plus de features = meilleur modèle » | Surajustement, fuite de données | Parcimonie, sélection de variables |
#
# ## 12.3 Limites des approches vues
#
# | Méthode | Limite | Mitigation |
# |---------|--------|------------|
# | RFM | Règles arbitraires (quartiles) | Compléter par clustering |
# | K-means | Clusters sphériques | DBSCAN / Gaussian Mixture |
# | Régression logistique | Hypothèse de linéarité | Forêt aléatoire, gradient boosting |
# | Tests A/B | Effet peaking, interactions | Bonferroni, analyse par segment |
# | Prévision temporelle | Suppose continuité | Scénarios, intervalles de confiance |
#
# ## 12.4 Checklist bonnes pratiques (récapitulatif)
#
# ✅ **Reproductibilité** : `random_state` fixé, données versionnées.
# ✅ **Qualité des données** : audit (manquants, doublons, bornes) avant toute analyse.
# ✅ **Séparation train/test** : pas de fuite de données (surtout temporelle).
# ✅ **Standardisation** : pour les modèles basés sur des distances.
# ✅ **Interprétabilité** : un modèle compréhensible vaut mieux qu'un modèle opaque (sauf gain net prouvé).
# ✅ **Évaluation** : choisir la métrique selon le **coût métier** (rappel vs précision).
# ✅ **Éthique & conformité** : minimisation des données, loi ivoirienne n°2013-450, vigilance sur les biais.
# ✅ **Communication** : transformer les chiffres en **recommandations actionnables** avec un ROI chiffré.
#
# ## 12.5 Références clés du module
#
# 1. Provost & Fawcett (2013), *Data Science for Business*.
# 2. Tufféry (2018), *Data Mining et Machine Learning* (3e éd.).
# 3. Chaffey & Ellis-Chadwick (2019), *Digital Marketing* (7e éd.).
# 4. Géron (2022), *Hands-On Machine Learning* (3e éd.).
# 5. Kohavi, Tang & Xu (2020), *Trustworthy Online Controlled Experiments*.
# 6. Jodelet & Lévesque (2021), *Marketing Analytics* (Dunod).
#
# ---
#
# ## 🎯 Conclusion du cours
#
# Le marketing analytics n'est pas une fin en soi : c'est un **levier de décision**. La valeur se crée quand la donnée devient une **recommandation argumentée** qui change une action marketing :
# - cibler le **bon** client (scoring),
# - au **bon** moment (prévision),
# - sur le **bon** canal (attribution),
# - avec la **bonne** offre (test A/B),
# - et le **bon** message (segmentation).
#
# La maîtrise technique (Python, modèles) est nécessaire mais **insuffisante** : c'est la **pensée analytique** — articuler donnée, modèle et métier — qui fait la différence. C'est l'objectif de ce module.
