# Modèle dimensionnel (Star Schema) — IvoireMarket

**Module Marketing Analytics (BIU / MSSM)** · Données 100 % synthétiques · Reproductible (`random_state=42`)

Ce document décrit le modèle dimensionnel en **schéma en étoile** conçu pour importer les données dans un SGBD (PostgreSQL, MySQL, SQL Server) et les exploiter dans **Power BI** ou **Excel (Power Pivot)**.

---

## 1. Architecture du modèle

```
                  dim_clients
                       │
dim_produits ── fact_transactions ── dim_canaux
                       │
                  dim_temps
                  dim_campagnes  (indépendante, liée aux analyses de campagnes)
```

**Principe** : la table de fait `fact_transactions` est au centre, entourée des dimensions. Les **clés étrangères** (surrogate keys `_key`) relient la fait aux dimensions. Les **mesures quantitatives** sont dans la table de fait ; les **attributs descriptifs** sont dans les dimensions.

---

## 2. Les 5 tables de dimensions

### dim_clients (5 000 lignes)
| Colonne | Type | Rôle |
|---------|------|------|
| `client_key` (PK) | INTEGER | Clé surrogate (1→5000) |
| `client_id_nk` | INTEGER | Clé naturelle source |
| `genre`, `age`, `tranche_age` | VARCHAR/INT | Démographie |
| `ville` | VARCHAR | Géographie (10 villes ivoiriennes) |
| `canal_acquisition` | VARCHAR | Canal d'origine |
| `segment_marketing` | VARCHAR | Segment (Nouveau/Fidèle/VIP...) |
| `date_inscription` | DATE | Ancienneté |
| `statut` | VARCHAR | Actif/Inactif |

### dim_temps (1 095 lignes = 3 ans × 365 jours)
| Colonne | Type | Rôle |
|---------|------|------|
| `date_key` (PK) | INTEGER | Clé intelligible YYYYMMDD |
| `date`, `annee`, `trimestre`, `mois`, `mois_lib`, `semaine_iso`, `jour_semaine`, `jour_lib` | divers | Hiérarchie temporelle |
| `est_weekend`, `est_fin_annee` | SMALLINT | Indicateurs saisonniers |

### dim_produits (8 lignes)
| Colonne | Type | Rôle |
|---------|------|------|
| `produit_key` (PK) | INTEGER | Clé surrogate |
| `categorie_produit` | VARCHAR | Catégorie (Électronique, Mode...) |
| `gamme` | VARCHAR | Premium/Standard/Économique |
| `taux_marge_pct` | NUMERIC | Taux de marge par catégorie |
| `departement` | VARCHAR | Digital/Textile/Grand public |

### dim_canaux (7 lignes)
| Colonne | Type | Rôle |
|---------|------|------|
| `canal_key` (PK) | INTEGER | Clé surrogate |
| `canal` | VARCHAR | Canal (Boutique, Site Web, Mobile Money...) |
| `type_canal` | VARCHAR | Physique/Digital/Mobile Money |
| `est_digital` | SMALLINT | 0/1 |
| `cout_acquisition_moy_fcfa` | INTEGER | Coût d'acquisition |

### dim_campagnes (200 lignes)
| Colonne | Type | Rôle |
|---------|------|------|
| `campagne_key` (PK) | INTEGER | Clé surrogate |
| `campagne_id_nk` | INTEGER | Clé naturelle source |
| `nom_campagne`, `type_campagne`, `cible`, `groupe_test` | VARCHAR | Attributs campagne |
| `date_debut`, `date_fin`, `duree_jours` | DATE/INT | Période |
| `budget_fcfa`, `nb_envois`, `cout_par_envoi_fcfa` | INT/NUMERIC | Coûts |

---

## 3. Table de fait principale — fact_transactions (120 000 lignes)

### Clés étrangères (FK)
| FK | Vers | Cardinalité |
|----|------|-------------|
| `client_key` | dim_clients.client_key | N→1 |
| `date_key` | dim_temps.date_key | N→1 |
| `produit_key` | dim_produits.produit_key | N→1 |
| `canal_key` | dim_canaux.canal_key | N→1 |

### Mesures quantitatives prioritaires
| Mesure | Type | Additivité | Usage analytique |
|--------|------|------------|------------------|
| `ca_brut_fcfa` | INTEGER | Additive | Chiffre d'affaires brut |
| `montant_remise_fcfa` | INTEGER | Additive | Remises accordées |
| `ca_net_fcfa` | INTEGER | Additive | **CA après remise** (KPI principal) |
| `marge_brute_fcfa` | INTEGER | Additive | **Marge brute** (rentabilité) |
| `quantite_vendue` | INTEGER | Additive | Volume vendu |
| `prix_unitaire_net_fcfa` | INTEGER | Semi-additive | Prix moyen |
| `remise_pct` | NUMERIC | Non-additive | Taux de remise moyen |
| `a_eu_remise` | SMALLINT | Additive (count) | % transactions remisées |

### Totaux agrégés (3 ans)
- CA brut total : **3,57 Md FCFA**
- CA net total : **3,31 Md FCFA**
- Marge brute totale : **867 M FCFA**
- Quantité totale : **285 150 unités**

---

## 4. Import dans un SGBD

### Option A — PostgreSQL (recommandé)
```bash
# 1. Créer le schéma et les tables
psql -U user -d mabase -f scripts/dw_schema.sql

# 2. Générer le script de chargement
python3 scripts/dw_import.py --db print-sql > scripts/dw_load.psql

# 3. Charger les données
psql -U user -d mabase -f scripts/dw_load.psql
```

### Option B — MySQL
Adapter le DDL : `SERIAL` → `INT AUTO_INCREMENT`, `NUMERIC` → `DECIMAL`. Charger avec :
```sql
LOAD DATA INFILE '/path/to/dim_clients.csv'
INTO TABLE dim_clients FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 ROWS;
```

### Option C — SQL Server
Utiliser `bcp` ou l'assistant d'import SSMS. Types équivalents : `INT`, `DECIMAL(5,2)`, `DATE`.

---

## 5. Exploitation dans Power BI

### Connexion
1. **Obtenir les données** → PostgreSQL (ou MySQL/SQL Server).
2. Sélectionner les 6 tables (5 dim + 1 fait).
3. **Mode Import** (recommandé pour 120k lignes) ou DirectQuery.

### Modélisation dans Power BI
- Vérifier les **relations** automatiques (Power BI détecte les FK/PK `_key`).
- Définir la **hiérarchie de date** : Année → Trimestre → Mois → Date.
- Définir la **direction du filtre** : 1→N (dimensions filtrent la fait).

### Mesures DAX recommandées
```dax
CA Net = SUM(fact_transactions[ca_net_fcfa])
Marge Brute = SUM(fact_transactions[marge_brute_fcfa])
Taux de Marge % = DIVIDE([Marge Brute], [CA Net])
Panier Moyen = DIVIDE([CA Net], COUNTROWS(fact_transactions))
Quantité Vendue = SUM(fact_transactions[quantite_vendue])
% Transactions Remisées = DIVIDE(
    CALCULATE(COUNTROWS(fact_transactions), fact_transactions[a_eu_remise]=1),
    COUNTROWS(fact_transactions)
)
```

### Visuels types
- CA net par mois (ligne) + par canal (barres empilées).
- Marge brute par catégorie (treemap).
- Top clients par CA (barres horizontales).
- Carte du CA par ville (map ivoirienne).
- Segmenteurs : segment_marketing, gamme, type_canal, annee.

---

## 6. Exploitation dans Excel (Power Pivot)

1. **Power Pivot → Gérer → Obtenir les données externes** → connexion SQL.
2. Importer les 6 tables.
3. Onglet **Diagram View** → créer les relations (glisser-déposer les `_key`).
4. **Hiérarchie** : glisser Année/Trimestre/Mois sous la table dim_temps.
5. Mesures (DAX identique à Power BI) via **Mesures → Nouvelle mesure**.
6. Construire les **Tableaux croisés dynamiques** et graphiques.

### Astuces Excel
- Désactiver le chargement en arrière-plan des tables sources (option Power Pivot).
- Pour 120k lignes, le mode **Import** est instantané.
- Utiliser **Segments** (Slicers) sur segment_marketing / ville / canal pour filtrer.

---

## 7. Vues analytiques pré-construites (dans `dw_schema.sql`)

| Vue | Usage |
|-----|-------|
| `v_ca_mensuel_canal` | CA net + marge + quantité par mois et canal |
| `v_ca_segment_categorie` | CA par segment client × catégorie produit |
| `v_kpi_clients` | RFM-like (récence, fréquence, CA total, panier moyen) |

Ces vues permettent de **contourner** la modélisation Power BI si on préfère une approche par requête SQL directe.

---

## 8. Intégrité référentielle

✅ **0 clé étrangère manquante** dans `fact_transactions` (vérifié au chargement).
✅ Les `date_key` couvrent toute la période des transactions (2022-2024).
✅ Contraintes `UNIQUE` sur les clés naturelles (`client_id_nk`, `categorie_produit`, `canal`, `campagne_id_nk`).
✅ Index sur les FK de la table de fait pour accélérer les jointures analytiques.
