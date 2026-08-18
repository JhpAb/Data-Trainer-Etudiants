"""Script de tests unitaires pour le TD Marketing Analytics.

Rejoue le notebook étudiant (TD_Exercices.ipynb) dans un namespace unique,
puis vérifie que les variables et résultats attendus sont présents et corrects.

Usage :
    python scripts/test_td.py [--notebook td_exercices/TD_Exercices.ipynb]

Sortie : JSON avec le détail de chaque test (pass/fail + message),
écrit dans tests_results.json et affiché sur stdout.
"""
import argparse
import json
import sys
import os
import io
import contextlib
import traceback
from pathlib import Path


def run_notebook_cells(notebook_path):
    """Exécute toutes les cellules de code d'un notebook et retourne le namespace."""
    nb_path = Path(notebook_path).resolve()
    nb = json.load(open(nb_path, encoding="utf-8"))
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    ns = {}
    # Imports de base toujours disponibles
    exec(
        "import pandas as pd\nimport numpy as np\n"
        "import matplotlib\nmatplotlib.use('Agg')\n"
        "import matplotlib.pyplot as plt\nimport seaborn as sns\n",
        ns,
    )
    # Changer le répertoire de travail vers le dossier du notebook
    # pour que les chemins relatifs (../data, etc.) fonctionnent correctement
    original_cwd = os.getcwd()
    nb_dir = nb_path.parent
    os.chdir(nb_dir)
    errors = []
    try:
        for i, cell in enumerate(code_cells):
            src = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
            # Sauter les cellules vides (placeholder "# À COMPLÉTER")
            if src.strip() in ("", "# À COMPLÉTER — Écrivez votre code ici",
                               "# À COMPLÉTER — Écrivez votre code ici\n"):
                continue
            try:
                # Capturer les print pour ne pas polluer la sortie
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(src, ns)
            except Exception as e:
                tb = traceback.format_exc()
                errors.append({"cell_index": i, "error": str(e), "traceback": tb})
    finally:
        os.chdir(original_cwd)
    return ns, errors


class TestResult:
    def __init__(self, name, points, passed=True, message=""):
        self.name = name
        self.points = points
        self.passed = passed
        self.message = message

    def to_dict(self):
        return {
            "test": self.name,
            "points_max": self.points,
            "passed": self.passed,
            "message": self.message,
        }


def check(name, points, ns, var_name, expected=None, tol=None, condition=None):
    """Vérifie qu'une variable existe et (option) correspond à la valeur attendue."""
    if var_name not in ns:
        return TestResult(name, points, False, f"Variable '{var_name}' non définie.")
    val = ns[var_name]
    if expected is not None:
        if tol is not None:
            if isinstance(val, (int, float)) and abs(val - expected) <= tol:
                return TestResult(name, points, True, f"{var_name} = {val:.4f} (attendu ~{expected})")
            return TestResult(name, points, False, f"{var_name} = {val} (attendu ~{expected} ± {tol})")
        if val == expected:
            return TestResult(name, points, True, f"{var_name} = {val}")
        return TestResult(name, points, False, f"{var_name} = {val} (attendu {expected})")
    if condition is not None:
        if condition(val):
            return TestResult(name, points, True, f"{var_name} présent ✓")
        return TestResult(name, points, False, f"{var_name} = {val} (condition non vérifiée)")
    return TestResult(name, points, True, f"{var_name} défini ✓")


def check_any(name, points, ns, var_names, expected=None, tol=None, condition=None):
    """Vérifie qu'au moins une des variables candidate existe."""
    for vn in var_names:
        if vn in ns:
            return check(name, points, ns, vn, expected=expected, tol=tol, condition=condition)
    return TestResult(name, points, False, f"Aucune variable parmi {var_names} non définie.")


def run_tests(ns):
    """Exécute tous les tests et retourne la liste des résultats."""
    results = []

    # === TD 1 — Data QA (20 pts) ===
    # Ex.1 (5 pts) : Audit de base
    results.append(check_any("Ex1-nb_lignes", 2, ns, ["n_lignes", "nb_lignes", "nb_clients"],
                             expected=5000))
    results.append(check_any("Ex1-nb_colonnes", 1, ns, ["n_colonnes", "nb_colonnes"],
                             expected=8))
    results.append(check_any("Ex1-doublons", 2, ns, ["doublons", "nb_doublons"],
                             expected=0))

    # Ex.2 (5 pts) : Jointure et cohérence
    results.append(check_any("Ex2-tx_joined", 2, ns, ["tx_clients", "tx_avec_client", "transactions_merged"],
                             condition=lambda v: hasattr(v, "shape") and v.shape[0] == 120000))
    # nb_sans_tx = 56 (clients sans transaction) OU tx_sans_client = 0 (transactions orphelines)
    results.append(check_any("Ex2-sans_client", 2, ns, ["nb_sans_tx", "tx_sans_client", "orphelins"],
                             condition=lambda v: (isinstance(v,(int,float)) and v in (0, 56)) or (hasattr(v,"__len__") and len(v)==0)))
    results.append(check_any("Ex2-cohesion", 1, ns, ["taux_cohesion", "clients_avec_tx"],
                             condition=lambda v: (isinstance(v,(int,float)) and v == 4944) or (isinstance(v,(int,float)) and v == 1.0)))

    # Ex.3 (5 pts) : Variables dérivées
    results.append(check_any("Ex3-panier_annee", 3, ns, ["panier_annee", "panier_moyen"],
                             condition=lambda v: hasattr(v, "__len__") and len(v) == 3))
    results.append(check_any("Ex3-annee_col", 2, ns, ["transactions"],
                             condition=lambda v: hasattr(v, "columns") and "annee" in v.columns))

    # Ex.4 (5 pts) : Outliers
    results.append(check_any("Ex4-outliers", 3, ns, ["outliers", "nb_outliers"],
                             condition=lambda v: (hasattr(v,"shape") and v.shape[0] == 1200) or (isinstance(v,(int,float)) and abs(v-1200)<=100)))
    results.append(check_any("Ex4-seuil", 2, ns, ["seuil"],
                             expected=181764.05, tol=5000))

    # === TD 2 — RFM (20 pts) ===
    # Ex.5 (8 pts) : Calcul RFM
    results.append(check_any("Ex5-rfm", 4, ns, ["rfm"],
                             condition=lambda v: hasattr(v, "shape") and v.shape[0] == 4944))
    results.append(check_any("Ex5-rfm-cols", 2, ns, ["rfm"],
                             condition=lambda v: hasattr(v, "columns") and "recence" in v.columns and "frequence" in v.columns))
    results.append(check_any("Ex5-clients_avec_tx", 2, ns, ["clients_avec_tx", "nb_clients_actifs"],
                             expected=4944, tol=1))

    # Ex.6 (12 pts) : Scoring et actions
    # segment peut être une Series isolée ou une colonne de rfm
    seg_var = ns.get("segment", ns.get("rfm", ns.get("clients", {})).get("segment") if isinstance(ns.get("rfm"), type(ns.get("rfm"))) else None)
    has_seg_col = "rfm" in ns and hasattr(ns["rfm"], "columns") and "segment" in ns["rfm"].columns
    seg_series = ns["rfm"]["segment"] if has_seg_col else ns.get("segment")
    if seg_series is not None and hasattr(seg_series, "value_counts"):
        n_seg = len(seg_series.value_counts())
        has_champ = "Champions" in seg_series.values
        results.append(TestResult("Ex6-segment", 4, n_seg >= 3, f"segment : {n_seg} segments trouvés"))
        results.append(TestResult("Ex6-segments-nb", 4, has_champ, f"'Champions' présent : {has_champ}"))
    else:
        results.append(TestResult("Ex6-segment", 4, False, "segment non défini (ni variable, ni colonne rfm)"))
        results.append(TestResult("Ex6-segments-nb", 4, False, "segment non défini"))
    results.append(check_any("Ex6-rfm-R", 4, ns, ["rfm"],
                             condition=lambda v: hasattr(v, "columns") and "R" in v.columns))

    # === TD 3 — Churn (20 pts) ===
    # Ex.7 (10 pts) : Pipeline et évaluation
    # Le corrigé peut stocker auc dans une variable OU le calculer à la volée
    # On accepte : variable auc/roc_auc OU présence de proba + y_te (AUC calculable)
    if any(vn in ns for vn in ["auc", "roc_auc", "score_auc"]):
        results.append(check_any("Ex7-auc", 5, ns, ["auc", "roc_auc", "score_auc"],
                                 condition=lambda v: isinstance(v, (int, float)) and v > 0.85))
    elif "proba" in ns and "y_te" in ns:
        from sklearn.metrics import roc_auc_score as _ras
        try:
            _auc = _ras(ns["y_te"], ns["proba"])
            results.append(TestResult("Ex7-auc", 5, _auc > 0.85, f"AUC recalculé = {_auc:.3f}"))
        except Exception:
            results.append(TestResult("Ex7-auc", 5, False, "Impossible de calculer l'AUC depuis proba/y_te"))
    else:
        results.append(TestResult("Ex7-auc", 5, False, "auc/proba non définis"))
    results.append(check_any("Ex7-X_tr", 2, ns, ["X_tr", "X_train"],
                             condition=lambda v: hasattr(v, "shape") and v.shape[0] == 3708))
    results.append(check_any("Ex7-base_rate", 3, ns, ["base_rate", "tx_churn"],
                             expected=0.2913, tol=0.05))

    # Ex.8 (10 pts) : Lift et ROI
    # lift_par_decile est une Series de 10 valeurs ; on vérifie sa structure
    results.append(check_any("Ex8-lift", 5, ns, ["lift_top", "lift_decile1", "lift_1", "lift_par_decile", "df_lift"],
                             condition=lambda v: (isinstance(v,(int,float))) or (hasattr(v,"__len__") and len(v) == 10) or (hasattr(v,"shape") and v.shape[0] == 1236)))
    results.append(check_any("Ex8-seuil_roi", 5, ns, ["seuil_roi", "seuil_rentabilite"],
                             expected=0.0417, tol=0.02))

    # === TD 4 — A/B test (20 pts) ===
    # Ex.9 (10 pts) : Test statistique
    results.append(check_any("Ex9-p_A", 3, ns, ["p_A", "taux_A", "conv_A"],
                             expected=0.1166, tol=0.01))
    results.append(check_any("Ex9-p_B", 3, ns, ["p_B", "taux_B", "conv_B"],
                             expected=0.1469, tol=0.01))
    results.append(check_any("Ex9-z", 2, ns, ["z", "z_stat", "zscore"],
                             condition=lambda v: isinstance(v, (int, float)) and abs(v) > 10))
    results.append(check_any("Ex9-pval", 2, ns, ["pval", "p_value", "pvalue"],
                             condition=lambda v: isinstance(v, (int, float)) and v < 0.05))

    # Ex.10 (10 pts) : Taille d'échantillon
    results.append(check_any("Ex10-n", 10, ns, ["n", "n_necessaire", "taille_echantillon"],
                             expected=17164, tol=2000))

    # === TD 5 — Prévision (20 pts) ===
    # Ex.11 (10 pts) : Régression avec saisonnalité
    results.append(check_any("Ex11-mape", 5, ns, ["mape", "mape_test"],
                             condition=lambda v: isinstance(v, (int, float)) and v < 5.0))
    results.append(check_any("Ex11-feats", 5, ns, ["feats", "features"],
                             condition=lambda v: hasattr(v, "__len__") and len(v) == 3))

    # Ex.12 (10 pts) : Prévision à 3 mois
    results.append(check_any("Ex12-fut", 5, ns, ["fut", "future", "prevision"],
                             condition=lambda v: hasattr(v, "shape") and v.shape[0] == 3))
    results.append(check_any("Ex12-ca_pred", 5, ns, ["fut", "future", "prevision"],
                             condition=lambda v: hasattr(v, "columns") and "ca_pred" in v.columns))

    return results


def main():
    parser = argparse.ArgumentParser(description="Tests automatiques du TD")
    parser.add_argument("--notebook", default="BIU/MSSM/td_exercices/TD_Exercices.ipynb",
                        help="Chemin du notebook à tester")
    parser.add_argument("--output", default="tests_results.json",
                        help="Fichier de sortie JSON")
    args = parser.parse_args()

    nb_path = Path(args.notebook)
    if not nb_path.exists():
        print(f"❌ Notebook introuvable : {nb_path}")
        sys.exit(1)

    print(f"▶ Exécution du notebook : {nb_path}")
    ns, errors = run_notebook_cells(nb_path)

    if errors:
        print(f"\n⚠️  {len(errors)} erreur(s) d'exécution détectée(s) :")
        for e in errors:
            print(f"  Cellule {e['cell_index']} : {e['error']}")

    print(f"\n▶ Lancement des tests...")
    results = run_tests(ns)

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    points_earned = sum(r.points for r in results if r.passed)
    points_max = sum(r.points for r in results)

    print(f"\n{'='*60}")
    print(f"  RÉSULTATS : {passed}/{total} tests réussis")
    print(f"  POINTS    : {points_earned}/{points_max}")
    print(f"{'='*60}\n")

    for r in results:
        status = "✅" if r.passed else "❌"
        print(f"  {status} [{r.points:2d} pts] {r.name:30s} {r.message}")

    # Sortie JSON
    output = {
        "notebook": str(nb_path),
        "exec_errors": errors,
        "tests": [r.to_dict() for r in results],
        "summary": {
            "passed": passed,
            "total": total,
            "points_earned": points_earned,
            "points_max": points_max,
            "score_pct": round(points_earned / points_max * 100, 1) if points_max else 0,
        },
    }
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📄 Résultats JSON écrits : {args.output}")

    # Code de sortie : 0 si au moins 50% des tests passent
    sys.exit(0 if points_earned >= points_max * 0.5 else 1)


if __name__ == "__main__":
    main()
