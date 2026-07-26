#!/usr/bin/env python3
"""Valide que le kit opérationnel est prêt pour Phase 0."""

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
    ROOT / "02-offre" / "one-pager.md",
    ROOT / "02-offre" / "pricing.md",
    ROOT / "02-offre" / "mvp" / "agent-prompt-pac.md",
    ROOT / "02-offre" / "mvp" / "agent-prompt-reno.md",
    ROOT / "02-offre" / "mvp" / "agent-prompt-solaire.md",
    ROOT / "02-offre" / "mvp" / "demo-script.md",
    ROOT / "02-offre" / "mvp" / "workflow-spec.md",
    ROOT / "02-offre" / "mvp" / "workflow.n8n.json",
    ROOT / "02-offre" / "mvp" / "onboarding-checklist.md",
    ROOT / "03-demarchage" / "cold-call-script.md",
    ROOT / "03-demarchage" / "perso-volume.md",
    ROOT / "03-demarchage" / "grande-echelle-perso.md",
    ROOT / "03-demarchage" / "sms-scripts.md",
    ROOT / "03-demarchage" / "objections.md",
    ROOT / "03-demarchage" / "close-14j.md",
    ROOT / "03-demarchage" / "daily-ritual.md",
    ROOT / "03-demarchage" / "compliance-b2b.md",
    ROOT / "04-phase0" / "week1-checklist.md",
    ROOT / "04-phase0" / "scorecard.md",
    ROOT / "04-phase0" / "daily-tracker.csv",
    ROOT / "04-phase0" / "call-log-100.csv",
    ROOT / "04-phase0" / "EXECUTE.md",
    ROOT / "05-scale" / "playbook-20k.md",
    ROOT / "05-scale" / "metrics.md",
    ROOT / "05-scale" / "upsells.md",
    ROOT / "05-scale" / "client-roster-20.csv",
    ROOT / "05-scale" / "EXECUTE.md",
    ROOT / "README.md",
    ROOT / "LOUP.md",
]


def score_row(row: dict) -> int | None:
    raw = (row.get("score") or "").strip()
    if raw.isdigit():
        return int(raw)
    pts = 0
    if row.get("pubs_actives") == "oui":
        pts += 2
    elif row.get("pubs_actives") == "a_verifier":
        pts += 1
    if row.get("landing_lead") == "oui":
        pts += 1
    if row.get("avis_google_gt20") == "oui":
        pts += 1
    if row.get("multi_villes") == "oui":
        pts += 1
    return pts if any(row.get(k) in {"oui", "a_verifier", "non"} for k in ("pubs_actives", "landing_lead")) else None


def main() -> int:
    errors = []
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
        if total < 200:
            errors.append(f"ICP rows={total} < 200")
        for row in rows:
            sc = score_row(row)
            tel = (row.get("telephone") or "").strip()
            if sc is not None and sc >= 3 and tel:
                callable_rows += 1

    print("=== Kit Rappel Leads — validation ===")
    print(f"Fichiers requis OK: {len(REQUIRED) - len([e for e in errors if e.startswith('MISSING')])}/{len(REQUIRED)}")
    print(f"Lignes ICP: {total}")
    print(f"Fiches appelables maintenant (score>=3 + tel): {callable_rows}")
    print("Seuil Phase 0 volume appels: remplir slots jusqu'à 40+ fiches score>=3/jour")

    if errors:
        print("ERRORS:")
        for e in errors:
            print(" -", e)
        return 1

    print("STATUS: KIT_READY")
    print("NEXT: 1) enrichir slots Ad Library 2) brancher Vapi/n8n 3) 60 appels/jour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
