#!/usr/bin/env python3
"""Recalcule les scores ICP et exporte la file A_APPELER (score>=3)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICP = ROOT / "01-cible" / "icp-sheet.csv"
OUT = ROOT / "01-cible" / "queue-a-appeler.csv"


def compute_score(row: dict) -> int:
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
    return pts


def main() -> int:
    with ICP.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    for row in rows:
        if (row.get("statut") or "").startswith("A_RECHERCHER"):
            continue
        row["score"] = str(compute_score(row))

    with ICP.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    queue = [
        r
        for r in rows
        if (r.get("score") or "").isdigit()
        and int(r["score"]) >= 3
        and (r.get("telephone") or "").strip()
        and r.get("statut") in {"A_APPELER", "RAPPEL_J1", "RAPPEL_J3"}
    ]

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(queue)

    print(f"Updated scores in {ICP}")
    print(f"Queue callables: {len(queue)} → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
