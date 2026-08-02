#!/usr/bin/env python3
"""Valide que le kit Clean&Pro est prêt pour Phase 0."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    ROOT / "01-cible" / "icp-sheet.csv",
    ROOT / "01-cible" / "process-liste.md",
    ROOT / "01-cible" / "scoring.md",
    ROOT / "01-cible" / "fill-slots.md",
    ROOT / "01-cible" / "STATUS.md",
    ROOT / "01-cible" / "queue-a-appeler.csv",
    ROOT / "02-offre" / "one-pager.md",
    ROOT / "02-offre" / "pricing.md",
    ROOT / "02-offre" / "branding.md",
    ROOT / "02-offre" / "landing" / "index.html",
    ROOT / "03-demarchage" / "cold-call-script.md",
    ROOT / "03-demarchage" / "sms-scripts.md",
    ROOT / "03-demarchage" / "objections.md",
    ROOT / "03-demarchage" / "close-contrat.md",
    ROOT / "03-demarchage" / "daily-ritual.md",
    ROOT / "03-demarchage" / "meta-ads.md",
    ROOT / "03-demarchage" / "compliance.md",
    ROOT / "04-phase0" / "week1-checklist.md",
    ROOT / "04-phase0" / "scorecard.md",
    ROOT / "04-phase0" / "daily-tracker.csv",
    ROOT / "04-phase0" / "call-log-100.csv",
    ROOT / "04-phase0" / "EXECUTE.md",
    ROOT / "05-ops" / "modele-ops.md",
    ROOT / "05-ops" / "recruter-prestataires.md",
    ROOT / "05-ops" / "checklist-intervention.md",
    ROOT / "05-ops" / "assurance-legal.md",
    ROOT / "06-scale" / "playbook-20k.md",
    ROOT / "06-scale" / "metrics.md",
    ROOT / "06-scale" / "upsells.md",
    ROOT / "06-scale" / "client-roster.csv",
    ROOT / "06-scale" / "objectifs.md",
    ROOT / "06-scale" / "EXECUTE.md",
    ROOT / "README.md",
    ROOT / "LOUP.md",
    ROOT / "DECISION-CLEAN-AND-PRO.md",
]


def score_row(row: dict) -> int | None:
    raw = (row.get("score") or "").strip()
    if raw.isdigit():
        return int(raw)
    pts = 0
    mapping = {
        "vitrine_grande": 2,
        "rue_passante": 1,
        "salete_visible": 1,
        "avis_ou_enseigne": 1,
    }
    seen = False
    for key, val in mapping.items():
        v = (row.get(key) or "").strip()
        if v in {"oui", "non", "a_verifier"}:
            seen = True
        if v == "oui":
            pts += val
    return pts if seen else None


def main() -> int:
    errors: list[str] = []
    for path in REQUIRED:
        if not path.exists():
            errors.append(f"MISSING {path.relative_to(ROOT)}")

    icp = ROOT / "01-cible" / "icp-sheet.csv"
    callable_rows = 0
    total = 0
    if icp.exists():
        with icp.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        total = len(rows)
        if total < 100:
            errors.append(f"ICP rows={total} < 100")
        for row in rows:
            sc = score_row(row)
            tel = (row.get("telephone") or "").strip()
            if sc is not None and sc >= 3 and tel:
                callable_rows += 1

    landing = ROOT / "02-offre" / "landing" / "index.html"
    if landing.exists():
        html = landing.read_text(encoding="utf-8")
        if "Clean&Pro" not in html and "Clean&amp;Pro" not in html:
            errors.append("Landing missing brand Clean&Pro")

    print("=== Kit Clean&Pro Nettoyage Vitres — validation ===")
    print(
        f"Fichiers requis OK: "
        f"{len(REQUIRED) - len([e for e in errors if e.startswith('MISSING')])}/{len(REQUIRED)}"
    )
    print(f"Lignes ICP: {total}")
    print(f"Fiches appelables maintenant (score>=3 + tel): {callable_rows}")
    print("Seuil Phase 0: zone figée + 1 prestataire + 40 fiches score>=3/jour")

    if errors:
        print("ERRORS:")
        for e in errors:
            print(" -", e)
        return 1

    print("STATUS: KIT_READY")
    print("NEXT: 1) figer zone 2) recruter 1 prestataire 3) 30 appels + ads 30€/j")
    return 0


if __name__ == "__main__":
    sys.exit(main())
