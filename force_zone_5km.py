#!/usr/bin/env python3
"""
Scrape Places ~5 km autour de Lorient La Base / zones commerciales
+ enrichissement dirigeant (interlocuteur) via API Recherche Entreprises.
"""

from __future__ import annotations

import csv
import math
import os
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

TEXT_URL = "https://places.googleapis.com/v1/places:searchText"
GOUV_URL = "https://recherche-entreprises.api.gouv.fr/search"
FIELD_MASK = ",".join(
    [
        "places.id",
        "places.displayName",
        "places.formattedAddress",
        "places.nationalPhoneNumber",
        "places.internationalPhoneNumber",
        "places.websiteUri",
        "places.googleMapsUri",
        "places.rating",
        "places.userRatingCount",
        "places.types",
        "places.businessStatus",
        "places.location",
        "nextPageToken",
    ]
)

# Centre La Base — rayon 5 km
CENTER = (47.7292, -3.3695)
RADIUS_KM = 5.0

# Grille ~5 km (pas ~1.6–2 km)
GRID = [
    (47.7292, -3.3695),  # La Base
    (47.7486, -3.3703),  # Centre Lorient
    (47.7400, -3.3600),  # Est / Perrière
    (47.7350, -3.3900),  # Ouest Ploemeur bord
    (47.7550, -3.3500),  # Nord vers Lanester
    (47.7647, -3.3397),  # Lanester
    (47.7200, -3.3550),  # Sud Keroman / pêche
    (47.7450, -3.3850),  # Nord-ouest
    (47.7150, -3.3800),  # Larmor bord
    (47.7600, -3.3700),  # Nord Lorient
]

QUERIES = [
    "restaurant", "bar", "boutique", "magasin", "coiffeur", "opticien",
    "agence immobilière", "pharmacie", "hôtel", "concession automobile",
    "showroom", "institut de beauté", "commerce", "crêperie", "brasserie",
]


def api_key() -> str:
    key = os.getenv("GOOGLE_PLACES_API_KEY", "").strip()
    if not key:
        raise SystemExit("GOOGLE_PLACES_API_KEY manquante")
    return key


def headers(key: str) -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": FIELD_MASK,
    }


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def normalize(place: dict[str, Any]) -> dict[str, Any] | None:
    if place.get("businessStatus") == "CLOSED_PERMANENTLY":
        return None
    name = (place.get("displayName") or {}).get("text", "")
    if not name:
        return None
    loc = place.get("location") or {}
    try:
        lat = float(loc["latitude"])
        lng = float(loc["longitude"])
    except Exception:
        return None
    dist = haversine(CENTER[0], CENTER[1], lat, lng)
    if dist > RADIUS_KM:
        return None
    return {
        "place_id": place.get("id", ""),
        "nom": name,
        "telephone": place.get("nationalPhoneNumber")
        or place.get("internationalPhoneNumber")
        or "",
        "adresse": place.get("formattedAddress", ""),
        "site": place.get("websiteUri", ""),
        "maps": place.get("googleMapsUri", ""),
        "note": place.get("rating", ""),
        "nb_avis": place.get("userRatingCount", ""),
        "types": "|".join(place.get("types") or []),
        "lat": lat,
        "lng": lng,
        "distance_km": round(dist, 2),
    }


def search_text(key: str, query: str, lat: float, lng: float) -> list[dict]:
    body = {
        "textQuery": query,
        "languageCode": "fr",
        "regionCode": "FR",
        "pageSize": 20,
        "locationBias": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": 2500.0,
            }
        },
    }
    out: list[dict] = []
    token = None
    for _ in range(2):
        if token:
            body["pageToken"] = token
        r = requests.post(TEXT_URL, headers=headers(key), json=body, timeout=30)
        if r.status_code != 200:
            break
        data = r.json()
        out.extend(data.get("places") or [])
        token = data.get("nextPageToken")
        if not token:
            break
        time.sleep(0.2)
    return out


def categorize(row: dict[str, Any]) -> str:
    t = f"{row.get('types', '')} {row['nom']}".lower()
    if any(x in t for x in ["restaurant", "bar", "cafe", "café", "brasserie", "crêper", "bakery", "meal"]):
        return "bar_resto"
    if any(x in t for x in ["car_dealer", "concession"]):
        return "concession"
    if any(x in t for x in ["store", "shop", "boutique", "clothing", "optician", "beauty", "florist", "pharmacy", "real_estate", "hair"]):
        return "commerce"
    if any(x in t for x in ["hotel", "lodging"]):
        return "hotel"
    if any(x in t for x in ["museum", "tourist"]):
        return "site_visite"
    return "entreprise_autre"


def clean_query_name(name: str) -> str:
    name = re.sub(r"\s*[-|].*$", "", name)
    name = re.sub(r"\b(SARL|SAS|EURL|SASU|SCI|SA)\b", "", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip()


def extract_cp(adresse: str) -> str:
    m = re.search(r"\b56\d{3}\b", adresse or "")
    return m.group(0) if m else "56100"


def format_dirigeant(d: dict[str, Any]) -> tuple[str, str]:
    """Retourne (interlocuteur, qualite)."""
    if not d:
        return "", ""
    if d.get("type_dirigeant") == "personne morale":
        return (d.get("denomination") or "").strip(), d.get("qualite") or "Dirigeant personne morale"
    prenoms = (d.get("prenoms") or "").strip()
    nom = (d.get("nom") or "").strip()
    # Premier prénom seulement pour l'appel
    prenom = prenoms.split()[0].title() if prenoms else ""
    nom_fmt = nom.title() if nom else ""
    full = f"{prenom} {nom_fmt}".strip()
    qualite = (d.get("qualite") or "Dirigeant").strip()
    return full, qualite


def lookup_dirigeant(nom: str, adresse: str) -> dict[str, str]:
    q = clean_query_name(nom)
    cp = extract_cp(adresse)
    params = f"q={quote(q)}&code_postal={cp}&per_page=5"
    try:
        r = requests.get(f"{GOUV_URL}?{params}", timeout=20, headers={"Accept": "application/json"})
        if r.status_code != 200:
            return {}
        results = r.json().get("results") or []
    except Exception:
        return {}

    if not results:
        # retry without CP
        try:
            r = requests.get(
                f"{GOUV_URL}?q={quote(q)}&departement=56&per_page=5",
                timeout=20,
                headers={"Accept": "application/json"},
            )
            results = r.json().get("results") or [] if r.status_code == 200 else []
        except Exception:
            results = []

    if not results:
        return {}

    # pick best: active + has dirigeants
    best = None
    for item in results:
        if item.get("etat_administratif") == "C":
            continue
        if item.get("dirigeants"):
            best = item
            break
    if not best:
        best = results[0]

    dirigeants = best.get("dirigeants") or []
    # Prefer Gérant / Président / Directeur
    prefer = ("gérant", "gerant", "président", "president", "directeur", "associé")
    chosen = None
    for d in dirigeants:
        qual = (d.get("qualite") or "").lower()
        if any(p in qual for p in prefer) and d.get("type_dirigeant") != "personne morale":
            chosen = d
            break
    if not chosen and dirigeants:
        chosen = next((d for d in dirigeants if d.get("type_dirigeant") != "personne morale"), dirigeants[0])

    interlocuteur, qualite = format_dirigeant(chosen or {})
    siege = best.get("siege") or {}
    return {
        "interlocuteur": interlocuteur,
        "qualite_dirigeant": qualite,
        "siren": best.get("siren") or "",
        "raison_sociale": best.get("nom_complet") or best.get("nom_raison_sociale") or "",
        "naf": best.get("activite_principale") or "",
        "siege_api": siege.get("adresse") or "",
    }


def pitch_qui_demander(categorie: str, qualite: str) -> str:
    if categorie in ("bar_resto", "commerce", "concession", "hotel"):
        return qualite or "Gérant / propriétaire"
    if categorie == "site_visite":
        return "Responsable site / services généraux"
    return "Gérant ou responsable entretien / services généraux"


def main() -> None:
    key = api_key()
    seen: dict[str, dict[str, Any]] = {}

    print(f"=== PLACES 5 km autour La Base ({RADIUS_KM} km) ===", flush=True)
    for i, (lat, lng) in enumerate(GRID):
        for q in QUERIES:
            for p in search_text(key, f"{q} Lorient", lat, lng):
                row = normalize(p)
                if row and row["place_id"] not in seen:
                    seen[row["place_id"]] = row
            time.sleep(0.05)
        print(f"  point {i+1}/{len(GRID)} → {len(seen)} fiches dans le rayon", flush=True)

    rows = list(seen.values())
    for r in rows:
        r["categorie"] = categorize(r)

    # Prioritize enrichment for commercial targets first
    enrich_order = {"concession": 0, "bar_resto": 1, "commerce": 2, "hotel": 3, "site_visite": 4, "entreprise_autre": 5}
    rows.sort(key=lambda r: (enrich_order.get(r["categorie"], 9), r.get("distance_km", 99)))

    print(f"=== ENRICHISSEMENT DIRIGEANTS ({len(rows)} fiches) ===", flush=True)
    enriched = 0
    for i, r in enumerate(rows, 1):
        info = lookup_dirigeant(r["nom"], r["adresse"])
        r["interlocuteur"] = info.get("interlocuteur", "")
        r["qualite_dirigeant"] = info.get("qualite_dirigeant", "")
        r["qui_demander"] = pitch_qui_demander(r["categorie"], r.get("qualite_dirigeant", ""))
        r["siren"] = info.get("siren", "")
        r["raison_sociale"] = info.get("raison_sociale", "")
        r["statut_appel"] = "a_appeler"
        if r["interlocuteur"]:
            enriched += 1
        if i % 20 == 0 or i == len(rows):
            print(f"  {i}/{len(rows)} — interlocuteurs trouvés: {enriched}", flush=True)
        time.sleep(0.08)

    prio = {
        "concession": 0,
        "bar_resto": 1,
        "commerce": 2,
        "hotel": 3,
        "site_visite": 4,
        "entreprise_autre": 5,
    }
    rows.sort(
        key=lambda r: (
            prio.get(r["categorie"], 9),
            0 if r.get("interlocuteur") else 1,
            0 if r.get("telephone") else 1,
            r.get("distance_km", 99),
            r["nom"],
        )
    )

    Path("leads").mkdir(exist_ok=True)
    out = Path("leads/zone_5km_interlocuteurs.csv")
    fields = [
        "categorie",
        "nom",
        "interlocuteur",
        "qualite_dirigeant",
        "qui_demander",
        "telephone",
        "adresse",
        "distance_km",
        "siren",
        "raison_sociale",
        "site",
        "maps",
        "note",
        "nb_avis",
        "place_id",
        "statut_appel",
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    with_phone = sum(1 for r in rows if r.get("telephone"))
    with_person = sum(1 for r in rows if r.get("interlocuteur"))
    print(f"\nDONE → {out}")
    print(f"TOTAL {len(rows)} | téléphone {with_phone} | interlocuteur {with_person}")
    print(Counter(r["categorie"] for r in rows))

    print("\n=== TOP A APPELER (avec nom) ===")
    n = 0
    for r in rows:
        if not r.get("interlocuteur") or not r.get("telephone"):
            continue
        if r["categorie"] not in ("bar_resto", "commerce", "concession", "hotel"):
            continue
        print(
            f"{r['categorie'][:10]:10} | Demander {r['interlocuteur']} ({r['qualite_dirigeant']}) "
            f"| {r['nom'][:35]:35} | {r['telephone']}"
        )
        n += 1
        if n >= 40:
            break


if __name__ == "__main__":
    main()
