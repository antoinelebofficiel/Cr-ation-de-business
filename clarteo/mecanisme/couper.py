#!/usr/bin/env python3
"""Coupe 30 îlots denses depuis cibles-commerces.csv → carnet.csv + tournees.csv."""

import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "cibles-commerces.csv"
OUT_CARNET = Path(__file__).resolve().parent / "carnet.csv"
OUT_TOUR = Path(__file__).resolve().parent / "tournees.csv"

JOUR = {
    "Lorient-centre": "Lun",
    "Lorient-Keroman": "Lun",
    "Lorient-Merville": "Lun",
    "Lanester": "Mar",
    "Caudan": "Mar",
    "Ploemeur": "Mer",
    "Larmor-Plage": "Mer",
    "Guidel": "Mer",
    "Queven": "Jeu",
    "Hennebont": "Jeu",
    "Inzinzac": "Jeu",
    "Auray": "Ven",
    "Port-Louis": "Ven",
    "Plouay": "Ven",
}

SIZE = 12
KEEP = 30


def diag(group):
    lats = [float(x["lat"]) for x in group]
    lngs = [float(x["lng"]) for x in group]
    mid = sum(lats) / len(lats)
    dlat = (max(lats) - min(lats)) * 111
    dlng = (max(lngs) - min(lngs)) * 111 * math.cos(math.radians(mid))
    return max((dlat**2 + dlng**2) ** 0.5, 0.05)


def label(group):
    seen = []
    for x in group:
        bit = x["adresse"].split(",")[0].strip()[:42]
        if bit and bit not in seen:
            seen.append(bit)
        if len(seen) == 2:
            break
    return " / ".join(seen)


def load():
    rows = []
    with SRC.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("chaine", "").strip().lower() != "non":
                continue
            if not r.get("tel", "").strip():
                continue
            try:
                float(r["lat"])
                float(r["lng"])
            except (TypeError, ValueError):
                continue
            rows.append(r)
    return rows


def ilots(rows):
    byz = defaultdict(list)
    for r in rows:
        byz[r["zone"]].append(r)
    out = []
    for zone, items in byz.items():
        items.sort(key=lambda x: (float(x["lat"]), float(x["lng"])))
        for i in range(0, len(items), SIZE):
            g = items[i : i + SIZE]
            if len(g) < 8:
                if out and out[-1]["zone"] == zone:
                    out[-1]["shops"].extend(g)
                    out[-1]["n"] = len(out[-1]["shops"])
                    out[-1]["km"] = round(diag(out[-1]["shops"]), 2)
                    out[-1]["ilot"] = label(out[-1]["shops"])
                continue
            out.append(
                {
                    "zone": zone,
                    "n": len(g),
                    "km": round(diag(g), 2),
                    "ilot": label(g),
                    "shops": g,
                }
            )
    out.sort(key=lambda x: x["n"] / x["km"], reverse=True)
    return out[:KEEP]


def write(top):
    carnet_fields = [
        "tournee_id",
        "jour",
        "zone",
        "ilot",
        "ordre",
        "commerce",
        "adresse",
        "tel",
        "lat",
        "lng",
        "statut",
        "contact",
        "prix_mois",
        "frequence",
        "heure",
        "sepa",
        "date_premier",
        "date_contrat",
        "acces",
        "notes",
    ]
    with OUT_CARNET.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=carnet_fields)
        w.writeheader()
        for i, it in enumerate(top, 1):
            tid = f"T{i:02d}"
            jour = JOUR.get(it["zone"], "Ven")
            for n, s in enumerate(it["shops"], 1):
                w.writerow(
                    {
                        "tournee_id": tid,
                        "jour": jour,
                        "zone": it["zone"],
                        "ilot": it["ilot"],
                        "ordre": n,
                        "commerce": s["nom"],
                        "adresse": s["adresse"],
                        "tel": s["tel"],
                        "lat": s["lat"],
                        "lng": s["lng"],
                        "statut": "cible",
                        "contact": "",
                        "prix_mois": "",
                        "frequence": "",
                        "heure": "",
                        "sepa": "",
                        "date_premier": "",
                        "date_contrat": "",
                        "acces": "",
                        "notes": "",
                    }
                )

    tour_fields = [
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
    with OUT_TOUR.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=tour_fields)
        w.writeheader()
        for i, it in enumerate(top, 1):
            w.writerow(
                {
                    "tournee_id": f"T{i:02d}",
                    "jour": JOUR.get(it["zone"], "Ven"),
                    "zone": it["zone"],
                    "ilot": it["ilot"],
                    "cibles": it["n"],
                    "km": it["km"],
                    "contrats": 0,
                    "mrr": 0,
                    "vendable": "non",
                    "prix_cession": 0,
                }
            )


def main():
    force = "--force" in sys.argv
    if OUT_CARNET.exists() and not force:
        with OUT_CARNET.open(newline="", encoding="utf-8") as f:
            if any((r.get("statut") or "").strip().lower() != "cible" for r in csv.DictReader(f)):
                print("carnet.csv a déjà des statuts. Stop. Relance seulement avec --force.")
                sys.exit(1)
    top = ilots(load())
    write(top)
    print(f"{len(top)} tournées → {OUT_CARNET.name}, {OUT_TOUR.name}")
    for i, it in enumerate(top, 1):
        print(f"T{i:02d}  {JOUR.get(it['zone'], '?'):3}  {it['zone']:18}  {it['n']:2}  {it['km']} km  {it['ilot']}")


if __name__ == "__main__":
    main()
