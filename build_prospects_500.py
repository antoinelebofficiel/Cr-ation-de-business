#!/usr/bin/env python3
"""
Scrape multi-zones Lorient → devis vitrine → filtre >= 120 € HT/mois → jusqu'à 500 prospects
+ enrichissement interlocuteur (dirigeant).
"""

from __future__ import annotations

import csv
import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

from places_lorient import ZONES, search_text, normalize_place, get_api_key

GOUV_URL = "https://recherche-entreprises.api.gouv.fr/search"
MIN_DEVIS = 120
TARGET = 500

# Requêtes orientées vitrines "moyennes / grosses" (évite le long-tail 65€)
QUERIES = [
    "concession automobile", "garage automobile", "showroom", "concessionnaire",
    "hôtel", "hotel", "magasin", "boutique", "centre commercial",
    "opticien", "agence immobilière", "pharmacie", "restaurant",
    "brasserie", "coiffeur", "institut de beauté", "surf shop",
    "supermarché", "hypermarché", "grande surface", "retail park",
    "décoration", "ameublement", "sport", "prêt-à-porter",
]


def categorize(row: dict[str, Any]) -> str:
    t = f"{row.get('types', '')} {row['nom']}".lower()
    if any(x in t for x in ["car_dealer", "concession", "garage"]):
        return "concession"
    if any(x in t for x in ["hotel", "lodging"]):
        return "hotel"
    if any(x in t for x in ["restaurant", "bar", "cafe", "café", "brasserie", "crêper", "meal"]):
        return "bar_resto"
    if any(x in t for x in ["store", "shop", "boutique", "clothing", "optician", "beauty", "pharmacy", "real_estate", "hair", "supermarket"]):
        return "commerce"
    return "entreprise_autre"


def estimate_devis(r: dict[str, Any]) -> dict[str, Any]:
    nom = (r.get("nom") or "").lower()
    cat = r.get("categorie") or categorize(r)
    adresse = (r.get("adresse") or "").lower()
    zone = r.get("zone") or ""
    euro_m2 = 7.5
    complexite = 1.05 if zone == "centre" else 1.0
    note: list[str] = []

    is_moto = any(x in nom for x in ["moto", "yamaha", "scooter", "motos"])
    is_big = any(
        x in nom
        for x in ["peugeot", "renault", "kia", "mercedes", "lexus", "bmw", "citroen", "citroën", "volkswagen", "toyota", "ford", "hyundai", "nissan", "opel", "dacia", "seat", "skoda"]
    ) and not is_moto
    if __import__("re").search(r"\baudi\b", nom) and "audiopro" not in nom:
        is_big = True
    is_garage = any(
        x in nom
        for x in [
            "garage", "récup", "recup", "global cars", "idéal autos", "ideal autos",
            "coin de l'auto", "calvez", "vda", "belle occasion", "fast car", "ewigo",
            "occasion", "autopuzz", "distinxion",
        ]
    )
    is_mid_auto = any(x in nom for x in ["maxus", "transakauto", "smart", "shad", "allannic", "cobredia"]) or (
        cat == "concession" and not is_big and not is_moto and not is_garage
    )

    if is_big:
        surface, passages, freq = 70, 2, "bi-mensuel"
        note.append("showroom marque")
    elif is_moto:
        surface, passages, freq = 25, 1, "mensuel"
        note.append("concession moto")
    elif is_garage:
        surface, passages, freq = 28, 1, "mensuel"
        note.append("garage / VO")
    elif is_mid_auto:
        surface, passages, freq = 40, 2, "bi-mensuel"
        note.append("showroom auto moyen")
    elif cat == "hotel" or any(x in nom for x in ["hôtel", "hotel", "mercure", "ibis", "best western", "kyriad", "premieres classes", "première classe"]):
        surface, passages, freq = 22, 2, "bi-mensuel"
        note.append("hôtel baies")
        complexite *= 1.1
    elif any(x in nom for x in ["fnac", "monoprix", "stokomani", "b&m", "botanic", "lidl", "leclerc", "carrefour", "intermarché", "intermarche", "super u", "auchan", "grande récré", "grande recre", "decathlon", "leroy merlin", "but ", "conforama", "cultura"]):
        surface, passages, freq = 35, 2, "bi-mensuel"
        note.append("grande façade retail")
        complexite *= 1.05
    elif any(x in nom for x in ["mango", "jules", "undiz", "caroll", "temps des cerises", "promod", "pimkie", "celio", "zara", "h&m", "hm ", "kiabi", "orchestra"]) or "centre commercial" in adresse or "galerie" in adresse or "geant" in adresse or "géant" in adresse:
        surface, passages, freq = 16, 1, "mensuel"
        note.append("boutique CC / enseigne")
    elif any(x in nom for x in ["action fun", "oss 56", "escale marine", "surf", "nautic", "nautique"]):
        surface, passages, freq = 12, 1, "mensuel"
        note.append("magasin nautique")
    elif any(x in nom for x in ["restaurant", "brasserie", "crêper", "creper", "pizza", "burger", "café", "cafe ", "bar "]):
        # restos: only keep if likely larger baies
        surface, passages, freq = 14, 1, "mensuel"
        note.append("resto / bar baies")
        if any(x in nom for x in ["mcdonald", "burger king", "kfc", "quick"]):
            surface, passages, freq = 25, 2, "bi-mensuel"
            note.append("resto chaîne")
    elif any(x in nom for x in ["optic", "pharmacie", "immobilier", "foncia", "orpi", "century", "laforêt", "laforet", "square habitat", "era "]):
        surface, passages, freq = 12, 1, "mensuel"
        note.append("agence / optique / pharma")
    elif any(x in nom for x in ["coiff", "salon", "hair", "look", "barber", "institut", "beauté", "beaute", "esthét"]):
        surface, passages, freq = 8, 1, "mensuel"
        note.append("salon / institut")
    else:
        # commerce générique: assume small unless avis élevés (proxy taille)
        try:
            avis = float(r.get("nb_avis") or 0)
        except Exception:
            avis = 0
        if avis >= 200:
            surface, passages, freq = 16, 1, "mensuel"
            note.append("commerce fort trafic")
        elif avis >= 50:
            surface, passages, freq = 12, 1, "mensuel"
            note.append("commerce moyen")
        else:
            surface, passages, freq = 7, 1, "mensuel"
            note.append("petit commerce")

    prix = surface * euro_m2 * complexite
    if is_big:
        prix = max(220, min(prix, 380))
    elif is_mid_auto and not is_garage:
        prix = max(160, min(prix, 280))
    elif is_garage:
        prix = max(140, min(prix, 240))
    else:
        prix = max(65, min(prix, 320))

    devis = prix * passages
    step = 5 if devis < 150 else 10
    devis = int(round(devis / step) * step)
    ponctuel = int(round(prix * 1.35 / 5) * 5)

    return {
        "categorie": cat,
        "surface_vitrine_m2_est": int(round(surface)),
        "frequence": freq,
        "passages_par_mois": passages,
        "devis_mensuel_ht_eur": devis,
        "devis_ponctuel_ht_eur": ponctuel,
        "devis_engagement_3mois_ht_eur": devis * 3,
        "hypothese": "; ".join(note),
        "confiance_devis": "moyenne" if surface <= 20 else "faible (à valider sur place)",
    }


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
        return "", ""
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
    bad = ("deloitte", "ernst", "mazars", "forvis", "kpmg")
    if any(b in interlocuteur.lower() for b in bad):
        return {}
    return {
        "interlocuteur": interlocuteur,
        "qualite_dirigeant": qualite,
        "qui_demander": qualite or "Gérant / propriétaire",
        "siren": best.get("siren") or "",
        "raison_sociale": best.get("nom_complet") or "",
    }


def score(r: dict[str, Any]) -> float:
    s = float(r.get("devis_mensuel_ht_eur") or 0)
    if r.get("telephone"):
        s += 30
    if r.get("interlocuteur"):
        s += 20
    try:
        s += min(10, float(r.get("nb_avis") or 0) / 50)
    except Exception:
        pass
    return s


def main() -> None:
    key = get_api_key()
    by_zone: dict[str, dict[str, dict]] = {z: {} for z in ZONES}

    print("=== SCRAPE MULTI-ZONES ===", flush=True)
    for zone_key in ZONES:
        for q in QUERIES:
            token = None
            pages = 0
            while True:
                data = search_text(key, q, zone_key, token)
                for place in data.get("places") or []:
                    if place.get("businessStatus") == "CLOSED_PERMANENTLY":
                        continue
                    row = normalize_place(place, zone_key, q)
                    if not row.get("place_id") or not row.get("telephone"):
                        continue
                    by_zone[zone_key][row["place_id"]] = row
                token = data.get("nextPageToken")
                pages += 1
                if not token or pages >= 3:
                    break
                time.sleep(0.12)
            time.sleep(0.04)
        print(f"  {zone_key}: {len(by_zone[zone_key])}", flush=True)

    # merge unique, keep first zone by priority
    zone_priority = ["labase", "centre", "lanester", "hennebont", "caudan", "ploemeur", "larmor"]
    global_map: dict[str, dict] = {}
    for z in zone_priority:
        for pid, row in by_zone[z].items():
            if pid not in global_map:
                global_map[pid] = row

    print(f"Uniques avec téléphone: {len(global_map)}", flush=True)

    candidates = []
    for row in global_map.values():
        row["categorie"] = categorize(row)
        est = estimate_devis(row)
        row.update(est)
        if row["devis_mensuel_ht_eur"] >= MIN_DEVIS:
            candidates.append(row)

    print(f"Après filtre devis >= {MIN_DEVIS} €: {len(candidates)}", flush=True)

    # sort and take pool for enrichment (all if <=600, else top 600 by score)
    candidates.sort(key=score, reverse=True)
    pool = candidates[: max(TARGET + 150, TARGET)]

    print(f"=== ENRICHISSEMENT DIRIGEANTS ({len(pool)}) ===", flush=True)
    for i, r in enumerate(pool, 1):
        info = lookup_dirigeant(r["nom"], r["adresse"])
        r["interlocuteur"] = info.get("interlocuteur", "")
        r["qualite_dirigeant"] = info.get("qualite_dirigeant", "")
        r["qui_demander"] = info.get("qui_demander", "Gérant / propriétaire")
        r["siren"] = info.get("siren", "")
        r["raison_sociale"] = info.get("raison_sociale", "")
        r["statut_appel"] = "a_appeler"
        if i % 40 == 0 or i == len(pool):
            ok = sum(1 for x in pool[:i] if x.get("interlocuteur"))
            print(f"  {i}/{len(pool)} interlocuteurs={ok}", flush=True)
        time.sleep(0.07)

    # Prefer those with interlocuteur, still fill to TARGET
    pool.sort(key=lambda r: (-(1 if r.get("interlocuteur") else 0), -score(r), r["nom"]))
    # diversify a bit by zone
    selected: list[dict] = []
    seen = set()
    zone_counts: dict[str, int] = defaultdict(int)
    soft_cap = {
        "centre": 110,
        "lanester": 90,
        "labase": 80,
        "ploemeur": 60,
        "larmor": 50,
        "caudan": 60,
        "hennebont": 50,
    }

    def try_add(r: dict) -> bool:
        key = (r["nom"].lower()[:50], r["telephone"][-8:])
        if key in seen:
            return False
        z = r.get("zone", "")
        if zone_counts[z] >= soft_cap.get(z, 80) and len(selected) < TARGET * 0.85:
            return False
        seen.add(key)
        zone_counts[z] += 1
        selected.append(r)
        return True

    for r in pool:
        if len(selected) >= TARGET:
            break
        try_add(r)

    # fill remaining ignoring soft caps
    if len(selected) < TARGET:
        for r in pool:
            if len(selected) >= TARGET:
                break
            key = (r["nom"].lower()[:50], r["telephone"][-8:])
            if key in seen:
                continue
            seen.add(key)
            selected.append(r)

    # also pull from leftover candidates not in pool if still short
    if len(selected) < TARGET:
        for r in candidates:
            if len(selected) >= TARGET:
                break
            key = (r["nom"].lower()[:50], r["telephone"][-8:])
            if key in seen:
                continue
            r.setdefault("interlocuteur", "")
            r.setdefault("qualite_dirigeant", "")
            r.setdefault("qui_demander", "Gérant / propriétaire")
            r.setdefault("siren", "")
            r.setdefault("raison_sociale", "")
            r["statut_appel"] = "a_appeler"
            seen.add(key)
            selected.append(r)

    selected = selected[:TARGET]
    # final order: devis desc, zone
    selected.sort(key=lambda r: (-r["devis_mensuel_ht_eur"], r.get("zone", ""), r["nom"]))
    for i, r in enumerate(selected, 1):
        r["rang"] = i

    Path("leads").mkdir(exist_ok=True)
    out = Path("leads/prospects_500_min120.csv")
    fields = [
        "rang", "zone", "categorie", "nom", "interlocuteur", "qualite_dirigeant", "qui_demander",
        "telephone", "adresse", "surface_vitrine_m2_est", "frequence", "passages_par_mois",
        "devis_mensuel_ht_eur", "devis_ponctuel_ht_eur", "devis_engagement_3mois_ht_eur",
        "hypothese", "confiance_devis", "siren", "raison_sociale", "site", "maps",
        "note", "nb_avis", "statut_appel",
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(selected)

    # also update top file pointer-style copy name
    with Path("leads/top100_prospects.csv").open("w", newline="", encoding="utf-8") as f:
        # keep top100 as first 100 of this list for compatibility
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(selected[:100])

    total = sum(r["devis_mensuel_ht_eur"] for r in selected)
    print(f"\nDONE → {out}", flush=True)
    print(f"TOTAL {len(selected)} | min devis {MIN_DEVIS} €", flush=True)
    print(f"Interlocuteurs: {sum(1 for r in selected if r.get('interlocuteur'))}", flush=True)
    print(f"Panier moyen: {total // max(len(selected),1)} € | Potentiel: {total} €", flush=True)
    print("Zones:", Counter(r["zone"] for r in selected), flush=True)
    print("Cats:", Counter(r["categorie"] for r in selected), flush=True)
    print("Devis bands:", flush=True)
    for a, b in [(120, 200), (200, 400), (400, 600), (600, 2000)]:
        n = sum(1 for r in selected if a <= r["devis_mensuel_ht_eur"] < b)
        print(f"  {a}-{b-1}: {n}", flush=True)


if __name__ == "__main__":
    main()
