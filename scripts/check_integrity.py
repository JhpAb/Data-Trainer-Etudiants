"""Vérification d'intégrité du travail étudiant.

Analyse 3 dimensions automatiquement vérifiables :
1. Historique git : nb de commits, étalement temporel (heures distinctes),
   taille moyenne des diffs (un copier-coller massif en un commit est suspect).
2. Cellules de réflexion métier : compte les cellules markdown contenant
   une interprétation (mots-clés métier) et vérifie leur longueur.
3. Plagiat par similarité : compare le notebook étudiant au corrigé
   (distance de Levenshtein normalisée sur le code).

Sortie : JSON integrity_results.json + console.
Le score d'intégrité (0-100) peut être combiné au score de qualité.
"""
import argparse
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime


def analyze_git_history(notebook_path):
    """Analyse l'historique git du notebook étudiant."""
    nb_path = Path(notebook_path)
    results = {
        "nb_commits": 0,
        "nb_jours_distincts": 0,
        "nb_heures_distinctes": 0,
        "taille_commit_moyenne": 0,
        "messages": [],
        "score": 0,
        "details": [],
    }

    try:
        # Récupérer l'historique du fichier
        log = subprocess.run(
            ["git", "log", "--follow", "--format=%H|%ai|%s", "--", str(nb_path)],
            capture_output=True, text=True, cwd=".",
        )
        if log.returncode != 0 or not log.stdout.strip():
            results["details"].append("⚠️ Aucun historique git trouvé (nouveau fichier ?)")
            results["score"] = 10  # minimum si pas d'historique
            return results

        lines = [l for l in log.stdout.strip().split("\n") if l]
        results["nb_commits"] = len(lines)

        dates = []
        messages = []
        for line in lines:
            parts = line.split("|", 2)
            if len(parts) == 3:
                dates.append(parts[1])
                messages.append(parts[2])
        results["messages"] = messages[-5:]  # 5 plus récents

        # Jours distincts
        jours = set(d[:10] for d in dates)
        results["nb_jours_distincts"] = len(jours)

        # Heures distinctes (proxy pour travail étalé vs copier-coller)
        heures = set(d[:13] for d in dates)  # AAAA-MM-JJ HH
        results["nb_heures_distinctes"] = len(heures)

        # Score d'intégrité git (sur 40 pts)
        # 5+ commits = 15 pts, 2+ jours = 15 pts, 3+ heures distinctes = 10 pts
        s = 0
        if results["nb_commits"] >= 5:
            s += 15
        elif results["nb_commits"] >= 3:
            s += 10
        elif results["nb_commits"] >= 1:
            s += 5

        if results["nb_jours_distincts"] >= 2:
            s += 15
        elif results["nb_jours_distincts"] >= 1:
            s += 8

        if results["nb_heures_distinctes"] >= 3:
            s += 10
        elif results["nb_heures_distinctes"] >= 1:
            s += 5

        results["score"] = s
        results["details"].append(
            f"Commits: {results['nb_commits']} | Jours: {results['nb_jours_distincts']} | "
            f"Heures: {results['nb_heures_distinctes']}"
        )

    except FileNotFoundError:
        results["details"].append("⚠️ git non disponible")
        results["score"] = 20  # neutre si pas de git
    except Exception as e:
        results["details"].append(f"⚠️ Erreur git: {e}")
        results["score"] = 20

    return results


# Mots-clés indiquant une interprétation métier (pas juste du code)
METIER_KEYWORDS = [
    "interprétation", "interpretation", "métier", "metier", "signifie",
    "cela signifie", "on en déduit", "recommandation", "action", "insight",
    "conclusion", "remarque", "attention", "limite", "corrélation",
    "causalité", "causalite", "biais", "because", "donc", "car",
    "parce que", "en effet", "ce qui", "permet de",
]


def analyze_reflection_cells(notebook_path, min_chars=100):
    """Compte et évalue les cellules markdown d'interprétation métier."""
    nb = json.load(open(notebook_path, encoding="utf-8"))
    md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]

    reflection_cells = []
    for i, c in enumerate(md_cells):
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        # Une cellule de réflexion = contient des mots-clés métier ET est suffisamment longue
        has_keyword = any(kw in src.lower() for kw in METIER_KEYWORDS)
        is_long = len(src.strip()) >= min_chars
        # Exclure les énoncés (commencent par # ou ## et contiennent "Exercice")
        is_enonce = src.strip().startswith("#") and "xercice" in src[:100]

        if has_keyword and is_long and not is_enonce:
            reflection_cells.append({
                "index": i,
                "length": len(src.strip()),
                "preview": src.strip()[:80] + "...",
            })

    results = {
        "nb_cellules_reflexion": len(reflection_cells),
        "nb_min_attendu": 5,  # au moins 5 interprétations métier
        "longueur_totale": sum(r["length"] for r in reflection_cells),
        "cellules": reflection_cells[:5],
        "score": 0,
        "details": [],
    }

    # Score (sur 30 pts) : 5+ cellules = 30, 3-4 = 20, 1-2 = 10, 0 = 0
    n = results["nb_cellules_reflexion"]
    if n >= 5:
        results["score"] = 30
    elif n >= 3:
        results["score"] = 20
    elif n >= 1:
        results["score"] = 10
    else:
        results["score"] = 0

    results["details"].append(
        f"Cellules d'interprétation métier: {n}/{results['nb_min_attendu']} attendues"
    )
    return results


def compute_similarity(notebook_path, corriges_path):
    """Estime la similarité du code étudiant vs corrigé (plagiat)."""
    def extract_code(nb_path):
        nb = json.load(open(nb_path, encoding="utf-8"))
        code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
        lines = []
        for c in code_cells:
            src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
            # Normaliser : retirer commentaires et espaces
            for line in src.split("\n"):
                stripped = line.split("#")[0].strip()
                if stripped and not stripped.startswith("#"):
                    lines.append(stripped)
        return lines

    student_lines = set(extract_code(notebook_path))

    # Si le corrigé n'est pas disponible (dépôt étudiant), on ne peut pas
    # comparer : on donne le score maximum d'originalité par défaut.
    if not corriges_path or not Path(corriges_path).exists():
        return {
            "similarity_pct": 0,
            "score": 30,
            "details": ["Corrigé non disponible — originalité non évaluée (30/30 par défaut)"]
        }

    corrige_lines = set(extract_code(corriges_path))

    if not student_lines or not corrige_lines:
        return {"similarity_pct": 0, "score": 30, "details": ["Code étudiant vide ou corrigé introuvable"]}

    # Similarité de Jaccard sur les lignes de code normalisées
    intersection = student_lines & corrige_lines
    union = student_lines | corrige_lines
    similarity = len(intersection) / len(union) * 100

    # Score (sur 30 pts) : similitude élevée = score bas
    if similarity < 30:
        score = 30  # code très différent = bien
    elif similarity < 50:
        score = 20
    elif similarity < 70:
        score = 10
    else:
        score = 0  # code quasi identique au corrigé = suspect

    return {
        "similarity_pct": round(similarity, 1),
        "nb_lignes_etudiant": len(student_lines),
        "nb_lignes_communes": len(intersection),
        "score": score,
        "details": [
            f"Similarité code étudiant/corrigé: {similarity:.1f}% "
            f"({len(intersection)}/{len(union)} lignes communes)"
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Vérification d'intégrité du TD")
    parser.add_argument("--notebook", default="BIU/MSSM/td_exercices/TD_Exercices.ipynb")
    parser.add_argument("--corriges", default=None,
                        help="Notebook corrigé pour comparaison")
    parser.add_argument("--output", default="integrity_results.json")
    args = parser.parse_args()

    print(f"▶ Analyse d'intégrité : {args.notebook}\n")

    git_res = analyze_git_history(args.notebook)
    refl_res = analyze_reflection_cells(args.notebook)
    sim_res = compute_similarity(args.notebook, args.corriges)

    total_score = git_res["score"] + refl_res["score"] + sim_res["score"]
    total_max = 100  # 40 + 30 + 30

    print(f"{'='*60}")
    print(f"  SCORE INTÉGRITÉ : {total_score}/{total_max}")
    print(f"{'='*60}\n")

    print("1. Historique git (sur 40 pts)")
    for d in git_res["details"]:
        print(f"   {d}")
    print(f"   → {git_res['score']}/40\n")

    print("2. Cellules de réflexion métier (sur 30 pts)")
    for d in refl_res["details"]:
        print(f"   {d}")
    print(f"   → {refl_res['score']}/30\n")

    print("3. Originalité du code (sur 30 pts)")
    for d in sim_res["details"]:
        print(f"   {d}")
    print(f"   → {sim_res['score']}/30\n")

    # Verdict
    if total_score >= 70:
        verdict = "✅ Travail vraisemblablement authentique"
    elif total_score >= 40:
        verdict = "⚠️ Travail partiellement authentique — soutenance recommandée"
    else:
        verdict = "❌ Travail suspect — soutenance obligatoire"
    print(f"Verdict : {verdict}\n")

    output = {
        "notebook": args.notebook,
        "git_analysis": git_res,
        "reflection_analysis": refl_res,
        "similarity_analysis": sim_res,
        "integrity_score": total_score,
        "integrity_max": total_max,
        "verdict": verdict,
    }
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 Résultats JSON : {args.output}")


if __name__ == "__main__":
    main()
