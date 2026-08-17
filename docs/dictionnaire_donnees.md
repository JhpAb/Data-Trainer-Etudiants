# Dictionnaire de données — Datasets Marketing Analytics

**Contexte métier :** Retailer/e-commerce ivoirien fictif **« IvoireMarket »** opérant à Abidjan et dans les grandes villes de Côte d'Ivoire. Toutes les données sont **100% synthétiques**, générées par `scripts/generate_datasets.py` avec `random_state=42` pour reproductibilité.

---

## 1. `clients.csv` — Table client (CRM)

| Variable | Type | Description | Valeurs / domaine |
|----------|------|-------------|-------------------|
| `client_id` | int | Identifiant unique client | 1 → 5 000 |
| `genre` | str | Sexe du client | `F`, `M` |
| `age` | int | Âge (années) | 18 → 75 |
| `ville` | str | Ville de résidence | 10 villes ivoiriennes (Abidjan = 55 %) |
| `canal_acquisition` | str | Canal d'acquisition initial | Mobile Money, Boutique, Site Web, Réseaux sociaux, Partenaire |
| `date_inscription` | date | Date d'inscription | 2022-01-01 → 2024-12-31 |
| `segment_marketing` | str | Segment marketing initial | Nouveau, Occasionnel, Régulier, Fidèle, VIP |
| `actif` | int | Statut actif (1) / inactif (0) | 0/1 (≈ 78 % actifs) |

---

## 2. `transactions.csv` — Table des transactions (≈ 120 000 lignes)

| Variable | Type | Description | Valeurs / domaine |
|----------|------|-------------|-------------------|
| `transaction_id` | int | Identifiant unique transaction | 1 → 120 000 |
| `client_id` | int | Clé étrangère → `clients.client_id` | |
| `date_transaction` | date | Date d'achat | 2022-01-01 → 2024-12-31 |
| `categorie_produit` | str | Catégorie achetée | 8 catégories |
| `canal_achat` | str | Canal d'achat | Boutique, Site Web, Application Mobile, Mobile Money USSD |
| `montant_fcfa` | float | Montant en FCFA | ~5 000 → ~500 000 |
| `quantite` | int | Nombre d'unités | 1 → 5 |
| `remise_pct` | float | Remise appliquée | 0 → 0.20 |

> Note : Le montant dépend de la catégorie (multiplicateur catégoriel × log-normale) pour refléter des paniers réalistes.

---

## 3. `campagnes.csv` — Campagnes marketing + test A/B (200 campagnes)

| Variable | Type | Description | Valeurs / domaine |
|----------|------|-------------|-------------------|
| `campagne_id` | int | Identifiant campagne | 1 → 200 |
| `nom_campagne` | str | Nom interne | Camp_001 → Camp_200 |
| `type_campagne` | str | Canal de la campagne | Email, SMS, WhatsApp, Push App, Réseaux sociaux |
| `date_debut` / `date_fin` | date | Période | 2022 → 2024 |
| `cible` | str | Segment ciblé | Tous, Fidèles, Nouveaux, Inactifs, VIP |
| `budget_fcfa` | float | Budget campagne | 50 000 → 2 000 000 |
| `groupe_test` | str | Groupe A/B | `A` (contrôle), `B` (variation avec offre incitative) |
| `nb_envois` | int | Volume d'envois | 500 → 20 000 |
| `taux_conversion` | float | Taux de conversion observé | ~0.10 → 0.20 |

> **Effet à découvrir :** Le groupe B (offre incitative) a un taux de conversion moyen ≈ 15,3 % vs 11,3 % pour le groupe A.

---

## 4. `churn_dataset.csv` — Dataset de scoring churn (4 944 lignes)

Issu de l'agrégation des transactions par client + features dérivées.

| Variable | Type | Description | Source |
|----------|------|-------------|--------|
| `client_id` | int | Clé | clients |
| `genre`, `age`, `ville`, `canal_acquisition`, `segment_marketing` | divers | Features démographiques | clients |
| `nb_achats` | int | Nombre total d'achats | transactions |
| `ca_total` | float | Chiffre d'affaires cumulé | transactions |
| `panier_moyen` | float | Panier moyen | transactions |
| `derniere_achat` | date | Dernier achat | transactions |
| `recence_jours` | int | Récence (jours depuis dernier achat) | dérivé |
| `frequence_mensuelle` | float | Fréquence d'achat mensuelle | dérivé |
| `churn` | int | **Variable cible** (1 = churn, 0 = actif) | dérivé (≈ 29 % churn) |

> Le label `churn` synthétise un risque de désengagement : récence > 90 j, faible fréquence, faible panier + bruit contrôlé. Taux de churn ≈ 29 %.

---

## Notes de gouvernance

- **Données 100% synthétiques** : aucun client réel, aucun chiffre d'affaires réel.
- **Monnaie** : Franc CFA (FCFA, XOF).
- **Reproductibilité** : `random_state=42` partout ; relancer `python3 scripts/generate_datasets.py` régénère des données identiques.
- **Conformité** : bien que fictives, la structure respecte les principes de la loi ivoirienne n°2013-450 sur la protection des données personnelles (minimisation, anonymisation des identifiants).
