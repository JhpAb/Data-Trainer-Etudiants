# Data-Trainer — Espace Étudiant

Dépôt public contenant les **supports de cours, TD et datasets** pour les formations en Data Science, Marketing Analytics et Finance dispensées dans plusieurs établissements.

---

## 🏫 Établissements et programmes disponibles

| Établissement | Programme | Module | Niveau | Statut |
|---------------|-----------|--------|--------|--------|
| **BIU** (British International University) | MSSM — Master Strategic Sales & Marketing | Marketing Analytics | Master 2 | ✅ Disponible |
| _Autres établissements à venir_ | | | | 🚧 |

---

## 🚀 Comment commencer

### 1. Cloner le dépôt

```bash
git clone https://github.com/JhpAb/Data-Trainer-Etudiants.git
cd Data-Trainer-Etudiants
```

### 2. Aller dans votre établissement / programme

```bash
# Exemple : étudiant BIU / MSSM
cd BIU/MSSM
```

### 3. Installer les dépendances

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
# ou : venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 4. Lancer Jupyter

```bash
jupyter notebook
```

Ouvrez le notebook du cours (`cours/`) ou le TD (`td_exercices/`) et suivez les instructions.

---

## 📂 Structure du dépôt

```
Data-Trainer-Etudiants/
├── README.md                    ← Ce fichier (sommaire général)
├── BIU/                         ← British International University
│   └── MSSM/                    ← Master Strategic Sales & Marketing
│       ├── cours/               ← Support de cours (notebooks)
│       ├── td_exercices/        ← TD à compléter (sans corrigés)
│       ├── projets/             ← Projet final (template)
│       ├── data/                ← Datasets synthétiques
│       ├── docs/                ← Dictionnaire de données, documentation
│       ├── README.md            ← Guide spécifique au module
│       └── requirements.txt
├── .github/workflows/           ← CI : évaluation automatique des TD
└── scripts/                     ← Scripts d'évaluation (tests + score)
```

---

## 🔐 Sécurité des corrigés

Ce dépôt est **public** et ne contient **aucun corrigé**. Les corrigés sont stockés dans le dépôt privé `Data-Trainer` et ne sont diffusés par le professeur qu'après la date de rendu.

---

## ❓ Besoin d'aide ?

- Consultez le `README.md` de votre établissement (ex. `BIU/MSSM/README.md`).
- Consultez `docs/dictionnaire_donnees.md` pour comprendre les variables.
- Relisez la section correspondante du cours dans `cours/`.
