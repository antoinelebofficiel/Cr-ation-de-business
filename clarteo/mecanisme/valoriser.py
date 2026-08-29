#!/usr/bin/env python3
"""Lit carnet.csv. Une tournée est vendable à 10× MRR si les seuils sont tenus."""

import csv
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

CARNET = Path(__file__).resolve().parent / "carnet.csv"
OUT = Path(__file__).resolve().parent / "tournees.csv"

MULTIPLE = 10
MIN_CONTRATS = 6
MIN_MRR = 500
MIN_SEPA = 0.80
MIN_MOIS = 3


def parse_date(s):
    s = (s or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def main():
    by = defaultdict(list)
    with CARNET.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by[r["tournee_id"]].append(r)

    km_map = {}
    if OUT.exists():
        with OUT.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                km_map[r.get("tournee_id", "")] = r.get("km", "")

    today = date.today()
    rows = []
    total_mrr = 0
    total_prix = 0
    for tid in sorted(by):
        shops = by[tid]
        contrats = [s for s in shops if s.get("statut", "").strip().lower() == "contrat"]
        mrr = 0
        sepa_ok = 0
        ages = []
        for s in contrats:
            try:
                mrr += float(str(s.get("prix_mois", "0")).replace(",", ".") or 0)
            except ValueError:
                pass
            if str(s.get("sepa", "")).strip().lower() in ("oui", "1", "sepa", "virement"):
                sepa_ok += 1
            d = parse_date(s.get("date_contrat"))
            if d:
                ages.append((today.year - d.year) * 12 + today.month - d.month)

        n = len(contrats)
        sepa_rate = (sepa_ok / n) if n else 0
        median_age = sorted(ages)[len(ages) // 2] if ages else 0
        vendable = (
            n >= MIN_CONTRATS
            and mrr >= MIN_MRR
            and sepa_rate >= MIN_SEPA
            and median_age >= MIN_MOIS
        )
        prix = int(round(mrr * MULTIPLE)) if vendable else 0
        total_mrr += mrr
        total_prix += prix
        meta = shops[0]
        rows.append(
            {
                "tournee_id": tid,
                "jour": meta.get("jour", ""),
                "zone": meta.get("zone", ""),
                "ilot": meta.get("ilot", ""),
                "cibles": len(shops),
                "km": km_map.get(tid, ""),
                "contrats": n,
                "mrr": int(mrr),
                "vendable": "oui" if vendable else "non",
                "prix_cession": prix,
            }
        )

    fields = [
        "tournee_id",
        "jour",
        "zone",
        "ilot",
        "cibles",
        "km",
        "contrats",
        "mrr",
        "vendable",
        "prix_cession",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"MRR carnet {int(total_mrr)} €  |  cessible {total_prix} €  ({MULTIPLE}×)")
    for r in rows:
        flag = "VENDABLE" if r["vendable"] == "oui" else "—"
        print(
            f"{r['tournee_id']}  {r['jour']:3}  contrats {r['contrats']:2}  "
            f"MRR {r['mrr']:5} €  {flag}  {r['prix_cession'] or '—'}  {r['ilot'][:48]}"
        )


if __name__ == "__main__":
    main()
