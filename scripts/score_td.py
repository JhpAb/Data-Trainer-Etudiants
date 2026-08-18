"""Calcule le score final et génère un badge + résumé pour la CI.

Lit tests_results.json (produit par test_td.py), calcule :
- note /100 et /20
- mention (Insuffisant / Passable / Assez bien / Bien / Très bien)
- badge SVG couleur (rouge/orange/vert)
- résumé markdown pour le commentaire de commit / PR

Usage :
    python scripts/score_td.py --input tests_results.json --output score_summary.md
"""
import argparse
import json
from pathlib import Path


def mention_from_score(score_100):
    """Retourne (mention, couleur_badge) selon le score /100."""
    if score_100 >= 80:
        return "Très bien", "brightgreen"
    elif score_100 >= 70:
        return "Bien", "green"
    elif score_100 >= 60:
        return "Assez bien", "yellow"
    elif score_100 >= 50:
        return "Passable", "orange"
    else:
        return "Insuffisant", "red"


def make_badge_svg(score_100, mention, color):
    """Génère un badge SVG style shields.io."""
    label = "Note TD"
    value = f"{score_100}/100 ({mention})"
    # Largeurs approximatives
    label_w = 65
    value_w = max(80, len(value) * 7)
    total_w = label_w + value_w
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="{total_w}" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <path fill="#555" d="M0 0h{label_w}v20H0z"/>
    <path fill="#{color}" d="M{label_w} 0h{value_w}v20H{label_w}z"/>
    <path fill="url(#b)" d="M0 0h{total_w}v20H0z"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_w//2}" y="15">{label}</text>
    <text x="{label_w + value_w//2}" y="15">{value}</text>
  </g>
</svg>'''
    return svg


def make_markdown_summary(results, score_100, score_20, mention, integrity_data=None):
    """Génère un résumé markdown pour le commentaire de commit/PR."""
    lines = []
    lines.append(f"## 📊 Évaluation automatique du TD\n")
    emoji = "🟢" if score_100 >= 50 else "🔴"
    lines.append(f"### {emoji} Note : **{score_100}/100** ({score_20}/20) — {mention}\n")

    summary = results.get("summary", {})
    lines.append(f"- **Tests réussis** : {summary.get('passed',0)}/{summary.get('total',0)}")
    lines.append(f"- **Points** : {summary.get('points_earned',0)}/{summary.get('points_max',100)}\n")

    # Erreurs d'exécution
    errors = results.get("exec_errors", [])
    if errors:
        lines.append(f"### ⚠️ Erreurs d'exécution ({len(errors)})\n")
        for e in errors[:5]:
            lines.append(f"- Cellule {e['cell_index']} : `{e['error'][:80]}`")
        if len(errors) > 5:
            lines.append(f"- ... et {len(errors)-5} autre(s)")
        lines.append("")

    # Détail par TD
    tests = results.get("tests", [])
    td_names = {
        "Ex1": "TD1 — Data QA", "Ex2": "TD1 — Data QA", "Ex3": "TD1 — Data QA",
        "Ex4": "TD1 — Data QA",
        "Ex5": "TD2 — RFM", "Ex6": "TD2 — RFM",
        "Ex7": "TD3 — Churn", "Ex8": "TD3 — Churn",
        "Ex9": "TD4 — A/B test", "Ex10": "TD4 — A/B test",
        "Ex11": "TD5 — Prévision", "Ex12": "TD5 — Prévision",
    }
    td_scores = {}
    for t in tests:
        prefix = t["test"][:3]
        td = td_names.get(prefix, "Autre")
        if td not in td_scores:
            td_scores[td] = {"earned": 0, "max": 0}
        td_scores[td]["earned"] += t["points_max"] if t["passed"] else 0
        td_scores[td]["max"] += t["points_max"]

    lines.append("### 📋 Score par TD\n")
    lines.append("| TD | Points | Note /20 |")
    lines.append("|----|--------|----------|")
    for td, sc in td_scores.items():
        note_20 = round(sc["earned"] / sc["max"] * 20, 1) if sc["max"] else 0
        status = "✅" if sc["earned"] >= sc["max"] * 0.5 else "❌"
        lines.append(f"| {td} | {sc['earned']}/{sc['max']} | {note_20} {status} |")
    lines.append("")

    lines.append("### 🔍 Détail des tests\n")
    lines.append("| Test | Points | Statut | Détail |")
    lines.append("|------|--------|--------|--------|")
    for t in tests:
        status = "✅" if t["passed"] else "❌"
        lines.append(f"| {t['test']} | {t['points_max']} | {status} | {t['message'][:60]} |")

    # Section intégrité
    if integrity_data:
        lines.append("\n### 🔒 Analyse d'intégrité\n")
        int_score = integrity_data.get("integrity_score", 0)
        verdict = integrity_data.get("verdict", "")
        lines.append(f"- **Score d'intégrité** : {int_score}/100")
        lines.append(f"- **Verdict** : {verdict}\n")

        git_a = integrity_data.get("git_analysis", {})
        if git_a:
            lines.append(f"- Historique git : {git_a.get('nb_commits',0)} commits, "
                         f"{git_a.get('nb_jours_distincts',0)} jour(s) distinct(s) "
                         f"({git_a.get('score',0)}/40 pts)")

        refl_a = integrity_data.get("reflection_analysis", {})
        if refl_a:
            lines.append(f"- Cellules de réflexion métier : "
                         f"{refl_a.get('nb_cellules_reflexion',0)}/{refl_a.get('nb_min_attendu',5)} "
                         f"({refl_a.get('score',0)}/30 pts)")

        sim_a = integrity_data.get("similarity_analysis", {})
        if sim_a:
            lines.append(f"- Originalité du code : "
                         f"{sim_a.get('similarity_pct',0)}% de similarité avec le corrigé "
                         f"({sim_a.get('score',0)}/30 pts)")
        lines.append("")

    lines.append("\n---")
    lines.append("_Score global = Qualité (60%) + Intégrité (40%). "
    "Seuil de validation : 50/100. "
    "Si le score d'intégrité < 40, une soutenance orale est obligatoire._")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Scoring automatique du TD")
    parser.add_argument("--input", default="tests_results.json")
    parser.add_argument("--output", default="score_summary.md")
    parser.add_argument("--badge", default="score_badge.svg")
    parser.add_argument("--integrity", default=None,
                        help="Fichier JSON des résultats d'intégrité (optionnel)")
    args = parser.parse_args()

    results = json.loads(Path(args.input).read_text(encoding="utf-8"))
    summary = results.get("summary", {})
    quality_score = summary.get("score_pct", 0)

    # Score d'intégrité (optionnel)
    integrity_score = None
    integrity_data = None
    if args.integrity and Path(args.integrity).exists():
        integrity_data = json.loads(Path(args.integrity).read_text(encoding="utf-8"))
        integrity_score = integrity_data.get("integrity_score", 0)

    # Score global = Qualité (60%) + Intégrité (40%)
    if integrity_score is not None:
        score_100 = round(quality_score * 0.6 + integrity_score * 0.4, 1)
    else:
        score_100 = quality_score

    score_20 = round(score_100 / 5, 1)
    mention, color = mention_from_score(score_100)

    # Badge SVG
    svg = make_badge_svg(score_100, mention, color)
    Path(args.badge).write_text(svg, encoding="utf-8")

    # Résumé markdown
    md = make_markdown_summary(results, score_100, score_20, mention, integrity_data)
    Path(args.output).write_text(md, encoding="utf-8")

    print(f"Note qualité : {quality_score}/100")
    if integrity_score is not None:
        print(f"Note intégrité : {integrity_score}/100")
        print(f"Score global : {score_100}/100 (qualité 60% + intégrité 40%)")
    else:
        print(f"Score global : {score_100}/100 (qualité seule)")
    print(f"({score_20}/20) — {mention}")
    print(f"Badge SVG : {args.badge}")
    print(f"Résumé MD : {args.output}")


if __name__ == "__main__":
    main()
