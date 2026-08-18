# 📚 Module Marketing Analytics — Espace Étudiant

**BIU / MSSM — Master Strategic Sales and Marketing**

Bienvenue ! Ce dossier contient **tout ce dont vous avez besoin** pour suivre le module et rendre vos travaux. Aucune autre dépendance externe n'est requise : les datasets sont inclus.

---

## 🚀 Démarrage en 5 minutes

### 1. Cloner le dépôt
```bash
git clone https://github.com/JhpAb/Data-Trainer-Etudiants.git
cd Data-Trainer-Etudiants
```

> 💡 Ce dépôt est **spécifiquement dédié aux étudiants**. Il ne contient aucun corrigé.
> Le dépôt professeur (`Data-Trainer`) est privé et non accessible.

### 2. Installer les dépendances
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
# ou : venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. Lancer Jupyter
```bash
jupyter notebook
# ou, si vous préférez VS Code :
# code .
```

Ouvrez le notebook du cours `cours/Marketing_Analytics_Cours.ipynb` et exécutez les cellules dans l'ordre ( menu **Run > Run All Cells**).

---

## 📂 Contenu de ce dossier

| Dossier | Contenu | Usage |
|---------|---------|-------|
| `cours/` | `Marketing_Analytics_Cours.ipynb` (+ `.py`), `Demo_DW_PowerBI.ipynb` (+ `.py`) | **Support de cours** à exécuter pour suivre les séances S1 à S14 |
| `td_exercices/` | `TD_Exercices.ipynb` (+ `.py`) — **sans corrigés** | **À rendre** — écrivez votre code dans les cellules `# À COMPLÉTER` |
| `projets/` | `Projet_Final_Template.ipynb` (+ `.py`) | **Squelette** du projet final à compléter |
| `data/` | 4 fichiers CSV (sources) + `dw/` (6 fichiers schéma en étoile) | **Datasets** — 100 % synthétiques, déjà prêts |
| `docs/` | `dictionnaire_donnees.md`, `modele_dimensionnel.md` | **Documentation** des données |

---

## 🗂️ Les données

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `data/clients.csv` | 5 000 | Table client (CRM) |
| `data/transactions.csv` | 120 000 | Historique des achats |
| `data/campagnes.csv` | 200 | Campagnes marketing + test A/B |
| `data/churn_dataset.csv` | 4 944 | Features clients + label churn |
| `data/dw/*.csv` | — | Schéma en étoile (5 dimensions + 1 fait) pour Power BI / Excel |

> 📖 Voir `docs/dictionnaire_donnees.md` pour la description de chaque colonne.

---

## ✅ Comment rendre le TD et voir votre note

### Workflow automatique (recommandé)

Le repo est équipé d'une **évaluation automatique** : à chaque push, une GitHub Action rejoue votre notebook, vérifie vos résultats, calcule votre note et l'affiche sur votre repo.

![Note TD](./score_badge.svg)

#### Étapes

1. **Forkez** ce repo (bouton **Fork** en haut à droite sur GitHub).
2. **Clonez** votre fork :
   ```bash
   git clone https://github.com/VOTRE_LOGIN/Data-Trainer-Etudiants.git
   cd Data-Trainer-Etudiants
   ```
3. **Complétez** `BIU/MSSM/td_exercices/TD_Exercices.ipynb` : remplissez toutes les cellules `# À COMPLÉTER`.
4. **Testez en local** avant de pousser (depuis la racine du dépôt) :
   ```bash
   python scripts/test_td.py --notebook BIU/MSSM/td_exercices/TD_Exercices.ipynb
   ```
   Vous verrez votre score immédiatement. Corrigez jusqu'à être satisfait.
5. **Committez et poussez** (depuis la racine du dépôt) :
   ```bash
   git add BIU/MSSM/td_exercices/TD_Exercices.ipynb
   git commit -m "Rendu TD Marketing Analytics"
   git push
   ```
6. **Voyez votre note** : allez sur votre fork sur GitHub → onglet **Actions**. Le workflow
   s'exécute en ~2 min, calcule votre score, et :
   - publie un **badge** (`BIU/MSSM/score_badge.svg`),
   - ajoute un **commentaire détaillé** sur le commit (score par TD, tests réussis/échoués),
   - met à jour `BIU/MSSM/score_summary.md`.

> 💡 Vous pouvez pousser **autant de fois que voulu** avant la deadline. Seul le dernier push compte.

### Barème automatique (sur 100 pts)

| TD | Exercices | Points |
|----|----------|--------|
| TD 1 — Data QA | Ex.1-4 | 20 |
| TD 2 — RFM | Ex.5-6 | 20 |
| TD 3 — Churn | Ex.7-8 | 20 |
| TD 4 — A/B test | Ex.9-10 | 20 |
| TD 5 — Prévision | Ex.11-12 | 20 |
| **Total** | | **100** |

- **Seuil de validation** : 50/100 (10/20)
- Mentions : ≥80 Très bien · ≥70 Bien · ≥60 Assez bien · ≥50 Passable · <50 Insuffisant

### 🔒 Score d'intégrité (40% de la note globale)

Votre note finale combine deux dimensions :

| Dimension | Poids | Ce que ça vérifie |
|-----------|-------|-------------------|
| **Qualité** | 60% | Les résultats sont corrects (tests unitaires) |
| **Intégrité** | 40% | Le travail est authentique |

Le score d'intégrité (sur 100) analyse 3 choses automatiquement :

1. **Historique git (40 pts)** : travail étalé sur plusieurs commits/jours
2. **Cellules de réflexion métier (30 pts)** : interprétations dans des cellules markdown
3. **Originalité du code (30 pts)** : similarité avec le corrigé

#### 💡 Bonnes pratiques pour maximiser votre score d'intégrité

- **Committez régulièrement** (5+ commits sur 2+ jours) plutôt qu'un seul push final
- **Rédigez des interprétations métier** : après chaque exercice, ajoutez une cellule
  markdown avec votre analyse (ce que les chiffres signifient pour IvoireMarket)
- **Écrivez votre code vous-même** : si votre code est identique au corrigé, le score
  d'originalité sera de 0/30
- **Un score d'intégrité < 40 déclenche une soutenance orale obligatoire**

### 🎤 Questions de soutenance

À la fin du TD, une section "Soutenance" contient 3 questions de compréhension.
Répondez-y personnellement (3-5 lignes par question). Ces questions portent sur
**vos choix** et **vos résultats** — pas sur du code générique.

### Rendu alternatif (sans GitHub)

Si vous n'avez pas de compte GitHub : complétez le notebook, exécutez tout (Run All),
exportez en HTML (**File > Download as > HTML**) et déposez le fichier sur la plateforme de l'école.

---

## 💡 Conseils

- **Exécutez le cours d'abord** : il contient les exemples et la théorie dont vous avez besoin pour les TD.
- **Lisez les interprétations métier** dans le cours : elles vous donnent le modèle pour vos propres analyses.
- **Reproductibilité** : un `random_state = 42` est utilisé partout. Gardez-le pour des résultats reproductibles.
- **Corrélation ≠ causalité** : distinguez toujours les deux dans vos interprétations.

---

## ❓ Besoin d'aide ?

- Consultez `docs/dictionnaire_donnees.md` pour comprendre les variables.
- Relisez la section correspondante du cours `cours/Marketing_Analytics_Cours.ipynb`.
- Les corrigés des TD sont diffusés par le professeur **après** la date de rendu.
