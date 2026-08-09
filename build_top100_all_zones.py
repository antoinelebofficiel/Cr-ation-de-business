#!/usr/bin/env python3
"""Scrape toutes les zones Lorient + enrichissement dirigeants → top 100 équilibré."""

from __future__ import annotations

import csv
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from dotenv import load_dotenv
import os

load_dotenv()

from places_lorient import ZONES, FIELD_MASK, API_URL, search_text, normalize_place, get_api_key

GOUV_URL = "https://recherche-entreprises.api.gouv.fr/search"

QUERIES = [
    "restaurant", "bar", "boutique", "magasin", "coiffeur", "opticien",
    "agence immobilière", "pharmacie", "hôtel", "concession automobile",
    "showroom", "institut de beauté", "commerce", "crêperie",
]

ZONE_QUOTA = {
    "centre": 22,
    "lanester": 18,
    "labase": 16,
    "ploemeur": 12,
    "larmor": 10,
    "caudan": 12,
    "hennebont": 10,
}  # total 100


def categorize(row: dict[str, Any]) -> str:
    t = f"{row.get('types', '')} {row['nom']}".lower()
    if any(x in t for x in ["car_dealer", "concession"]):
        return "concession"
    if any(x in t for x in ["restaurant", "bar", "cafe", "café", "brasserie", "crêper", "bakery", "meal"]):
        return "bar_resto"
    if any(x in t for x in ["hotel", "lodging"]):
        return "hotel"
    if any(x in t for x in ["store", "shop", "boutique", "clothing", "optician", "beauty", "florist", "pharmacy", "real_estate", "hair"]):
        return "commerce"
    if any(x in t for x in ["museum", "tourist"]):
        return "site_visite"
    return "entreprise_autre"


def clean_query_name(name: str) -> str:
    name = re.sub(r"\s*[-|].*$", "", name)
    name = re.sub(r"\b(SARL|SAS|EURL|SASU|SCI|SA)\b", "", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip()


def extract_cp(adresse: str) -> str:
    m = re.search(r"\b56\d{3}\b", adresse or "")
    return m.group(0) if m else ""


def format_dirigeant(d: dict[str, Any]) -> tuple[str, str]:
    if not d:
        return "", ""
    if d.get("type_dirigeant") == "personne morale":
        return (d.get("denomination") or "").strip(), d.get("qualite") or ""
    prenoms = (d.get("prenoms") or "").strip()
    nom = (d.get("nom") or "").strip()
    prenom = prenoms.split()[0].title() if prenoms else ""
    return f"{prenom} {nom.title()}".strip(), (d.get("qualite") or "").strip()


def lookup_dirigeant(nom: str, adresse: str) -> dict[str, str]:
    q = clean_query_name(nom)
    cp = extract_cp(adresse)
    urls = []
    if cp:
        urls.append(f"{GOUV_URL}?q={quote(q)}&code_postal={cp}&per_page=5")
    urls.append(f"{GOUV_URL}?q={quote(q)}&departement=56&per_page=5")
    results: list[dict] = []
    for url in urls:
        try:
            r = requests.get(url, timeout=20, headers={"Accept": "application/json"})
            if r.status_code == 200:
                results = r.json().get("results") or []
                if results:
                    break
        except Exception:
            continue
    if not results:
        return {}
    best = None
    for item in results:
        if item.get("etat_administratif") == "C":
            continue
        if item.get("dirigeants"):
            best = item
            break
    best = best or results[0]
    dirigeants = best.get("dirigeants") or []
    prefer = ("gérant", "gerant", "président", "president", "directeur")
    chosen = None
    for d in dirigeants:
        if d.get("type_dirigeant") == "personne morale":
            continue
        qual = (d.get("qualite") or "").lower()
        if any(p in qual for p in prefer):
            chosen = d
            break
    if not chosen:
        chosen = next((d for d in dirigeants if d.get("type_dirigeant") != "personne morale"), None)
    interlocuteur, qualite = format_dirigeant(chosen or {})
    # Filter audit firms as fake contacts
    bad = ("deloitte", "ernst", "mazars", "forvis", "kpmg")
    if any(b in interlocuteur.lower() for b in bad):
        return {}
    return {
        "interlocuteur": interlocuteur,
        "qualite_dirigeant": qualite,
        "siren": best.get("siren") or "",
        "raison_sociale": best.get("nom_complet") or "",
    }


def is_noise(r: dict[str, Any]) -> bool:
    nom = (r.get("nom") or "").lower()
    inter = (r.get("interlocuteur") or "").lower()
    if any(x in nom for x in ["france travail", "parking indigo", "atm ", "la poste "]):
        return True
    if any(x in inter for x in ["deloitte", "ernst", "mazars", "forvis"]):
        return True
    return False


def score(r: dict[str, Any]) -> float:
    s = 0.0
    if r.get("telephone"):
        s += 40
    if r.get("interlocuteur"):
        s += 30
    cat = r.get("categorie")
    s += {"concession": 25, "commerce": 20, "hotel": 18, "bar_resto": 15, "site_visite": 10}.get(cat, 5)
    try:
        avis = float(r.get("nb_avis") or 0)
        note = float(r.get("note") or 0)
        if avis >= 15 and note >= 3.8:
            s += 5
    except Exception:
        pass
    # prefer local indés over national chains slightly for closeability
    nom = (r.get("nom") or "").lower()
    if any(x in nom for x in ["carrefour", "leclerc", "zara", "promod", "pimkie", "foot locker"]):
        s -= 8
    return s


def main() -> None:
    key = get_api_key()
    by_zone: dict[str, dict[str, dict]] = {z: {} for z in ZONES}

    print("=== SCRAPE TOUTES ZONES ===", flush=True)
    for zone_key in ZONES:
        for q in QUERIES:
            page_token = None
            pages = 0
            while True:
                data = search_text(key, q, zone_key, page_token)
                for place in data.get("places") or []:
                    row = normalize_place(place, zone_key, q)
                    pid = row["place_id"]
                    if not pid or place.get("businessStatus") == "CLOSED_PERMANENTLY":
                        continue
                    if not row.get("telephone"):
                        continue
                    by_zone[zone_key][pid] = row
                page_token = data.get("nextPageToken")
                pages += 1
                if not page_token or pages >= 2:
                    break
                time.sleep(0.15)
            time.sleep(0.05)
        print(f"  {zone_key}: {len(by_zone[zone_key])} avec téléphone", flush=True)

    # flatten unique (prefer first zone assignment by priority density)
    zone_priority = ["labase", "centre", "lanester", "hennebont", "caudan", "ploemeur", "larmor"]
    global_seen: dict[str, dict] = {}
    for z in zone_priority:
        for pid, row in by_zone[z].items():
            if pid not in global_seen:
                row["categorie"] = categorize(row)
                global_seen[pid] = row

    rows = list(global_seen.values())
    print(f"=== ENRICHISSEMENT ({len(rows)}) ===", flush=True)
    # Enrich all candidates that might enter top (cap for speed: enrich per zone top pools)
    enrich_pool = []
    for z in ZONES:
        pool = [r for r in rows if r["zone"] == z]
        pool.sort(key=lambda r: -score({**r, "interlocuteur": ""}))
        enrich_pool.extend(pool[: max(ZONE_QUOTA[z] * 3, 40)])
    # unique
    enrich_ids = {r["place_id"] for r in enrich_pool}
    enrich_list = [r for r in rows if r["place_id"] in enrich_ids]
    print(f"  pool enrichi: {len(enrich_list)}", flush=True)

    for i, r in enumerate(enrich_list, 1):
        info = lookup_dirigeant(r["nom"], r["adresse"])
        r["interlocuteur"] = info.get("interlocuteur", "")
        r["qualite_dirigeant"] = info.get("qualite_dirigeant", "")
        r["qui_demander"] = info.get("qualite_dirigeant") or "Gérant / propriétaire"
        r["siren"] = info.get("siren", "")
        r["raison_sociale"] = info.get("raison_sociale", "")
        if i % 30 == 0 or i == len(enrich_list):
            ok = sum(1 for x in enrich_list if x.get("interlocuteur"))
            print(f"  {i}/{len(enrich_list)} interlocuteurs={ok}", flush=True)
        time.sleep(0.07)

    # Select by zone quota
    selected: list[dict] = []
    seen_keys = set()
    for z, quota in ZONE_QUOTA.items():
        pool = [r for r in enrich_list if r["zone"] == z and not is_noise(r)]
        # also allow non-enriched from zone if short
        if len(pool) < quota:
            extra = [r for r in rows if r["zone"] == z and r["place_id"] not in {p["place_id"] for p in pool}]
            for r in extra:
                r.setdefault("interlocuteur", "")
                r.setdefault("qualite_dirigeant", "")
                r.setdefault("qui_demander", "Gérant / propriétaire")
                r.setdefault("siren", "")
                r.setdefault("raison_sociale", "")
            pool.extend(extra)
        pool = [r for r in pool if not is_noise(r)]
        pool.sort(key=lambda r: -score(r))
        added = 0
        for r in pool:
            key = (r["nom"].lower()[:45], r["telephone"][-8:])
            if key in seen_keys:
                continue
            seen_keys.add(key)
            selected.append(r)
            added += 1
            if added >= quota:
                break
        print(f"  quota {z}: {added}/{quota}", flush=True)

    # fill if < 100
    if len(selected) < 100:
        rest = sorted(enrich_list, key=lambda r: -score(r))
        for r in rest:
            if is_noise(r):
                continue
            key = (r["nom"].lower()[:45], r["telephone"][-8:])
            if key in seen_keys:
                continue
            seen_keys.add(key)
            selected.append(r)
            if len(selected) >= 100:
                break

    # order by zone then score
    zorder = {z: i for i, z in enumerate(ZONE_QUOTA)}
    selected.sort(key=lambda r: (zorder.get(r["zone"], 99), -score(r), r["nom"]))
    selected = selected[:100]

    Path("leads").mkdir(exist_ok=True)
    out = Path("leads/top100_prospects.csv")
    fields = [
        "rang", "zone", "categorie", "nom", "interlocuteur", "qualite_dirigeant",
        "qui_demander", "telephone", "adresse", "siren", "site", "maps",
        "note", "nb_avis", "statut_appel",
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for i, r in enumerate(selected, 1):
            row = dict(r)
            row["rang"] = i
            row["statut_appel"] = "a_appeler"
            w.writerow(row)

    print(f"\nDONE → {out} ({len(selected)})", flush=True)
    print("Zones:", Counter(r["zone"] for r in selected), flush=True)
    print("Cats:", Counter(r["categorie"] for r in selected), flush=True)
    print("Interlocuteurs:", sum(1 for r in selected if r.get("interlocuteur")), flush=True)
    for r in selected:
        who = r.get("interlocuteur") or "Gérant sur place"
        print(f"{r.get('rang', selected.index(r)+1):3}. [{r['zone']}] Demander {who} | {r['nom']} | {r['telephone']}")


if __name__ == "__main__":
    main()
