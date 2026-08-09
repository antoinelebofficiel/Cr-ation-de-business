#!/usr/bin/env python3
"""Extraction forcée Lorient La Base — Text Search + Nearby + grille."""

from __future__ import annotations

import csv
import math
import os
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

TEXT_URL = "https://places.googleapis.com/v1/places:searchText"
NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
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

# Grille serrée sur Keroman / La Base
GRID = [
    (47.7292, -3.3695),  # centre
    (47.7305, -3.3725),  # Cité / quais
    (47.7285, -3.3670),  # port / K blocks
    (47.7318, -3.3735),  # Estienne d'Orves
    (47.7328, -3.3720),  # Action Fun / Bourely
    (47.7275, -3.3660),  # Flore
    (47.7332, -3.3730),  # Rooftop / Dordelin
    (47.7300, -3.3655),  # Keroman pêche
]

QUERIES = [
    "restaurant", "bar", "café", "brasserie", "crêperie", "traiteur", "cantine",
    "boutique", "magasin", "concept store", "showroom", "surf shop",
    "hôtel", "musée", "entreprise", "société", "bureau", "atelier",
    "chantier naval", "nautique", "catamaran", "voile", "skipper", "accastillage",
    "composite", "ingénierie", "association", "salle événement", "centre d'affaires",
    "port", "marina", "école de voile", "UCPA", "team", "course au large",
    "La Base Lorient", "Keroman", "Celtic Submarine", "bloc K1", "bloc K2", "bloc K3",
]

NEARBY_TYPE_BATCHES = [
    ["restaurant", "bar", "cafe", "bakery", "meal_takeaway"],
    ["store", "clothing_store", "gift_shop", "shoe_store"],
    ["museum", "tourist_attraction", "visitor_center"],
    ["lodging", "hotel"],
    ["shipyard", "marina", "boat_dealer"],
    ["office", "coworking_space", "point_of_interest"],
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


def normalize(place: dict[str, Any], source: str) -> dict[str, Any] | None:
    if place.get("businessStatus") == "CLOSED_PERMANENTLY":
        return None
    name = (place.get("displayName") or {}).get("text", "")
    if not name:
        return None
    loc = place.get("location") or {}
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
        "statut": place.get("businessStatus", ""),
        "types": "|".join(place.get("types") or []),
        "lat": loc.get("latitude", ""),
        "lng": loc.get("longitude", ""),
        "source": source,
    }


def search_text(key: str, query: str, lat: float, lng: float, radius: float = 900) -> list[dict]:
    body = {
        "textQuery": query,
        "languageCode": "fr",
        "regionCode": "FR",
        "pageSize": 20,
        "locationBias": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": radius,
            }
        },
    }
    out: list[dict] = []
    token = None
    for _ in range(3):
        if token:
            body["pageToken"] = token
        r = requests.post(TEXT_URL, headers=headers(key), json=body, timeout=30)
        if r.status_code != 200:
            print(f"  TEXT fail {r.status_code}: {r.text[:160]}")
            break
        data = r.json()
        out.extend(data.get("places") or [])
        token = data.get("nextPageToken")
        if not token:
            break
        time.sleep(0.25)
    return out


def search_nearby(key: str, lat: float, lng: float, types: list[str], radius: float = 1000) -> list[dict]:
    body = {
        "languageCode": "fr",
        "regionCode": "FR",
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": radius,
            }
        },
        "includedTypes": types,
    }
    r = requests.post(NEARBY_URL, headers=headers(key), json=body, timeout=30)
    if r.status_code != 200:
        print(f"  NEARBY fail {r.status_code}: {r.text[:160]}")
        return []
    return r.json().get("places") or []


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def categorize(row: dict[str, Any]) -> str:
    t = f"{row.get('types','')} {row['nom']}".lower()
    if any(x in t for x in ["restaurant", "bar", "cafe", "café", "brasserie", "crêper", "traiteur", "meal", "cantine", "marmite", "rooftop", "baleine"]):
        return "bar_resto"
    if any(x in t for x in ["store", "shop", "boutique", "clothing", "magasin", "showroom", "gift"]):
        return "commerce"
    if any(x in t for x in ["museum", "tourist", "attraction", "visitor"]):
        return "site_visite"
    if any(x in t for x in ["hotel", "lodging"]):
        return "hotel"
    if any(x in t for x in ["shipyard", "boat", "marina", "nautique", "voile", "chantier", "catamaran"]):
        return "nautique"
    return "entreprise_autre"


def in_labase(row: dict[str, Any]) -> bool:
    center = (47.7292, -3.3695)
    try:
        dist = haversine(center[0], center[1], float(row["lat"]), float(row["lng"]))
    except Exception:
        dist = 999
    row["distance_km"] = round(dist, 2)
    addr = f"{row.get('adresse','')} {row.get('nom','')}".lower()
    keys = (
        "base", "keroman", "estienne", "roland morillot", "sous-marin", "sous marin",
        "bourely", "dordelin", "rallier", "romazotti", "papin", "venus",
        "celtic submarine", "l'herminier", "verrière", "verriere", "pourquoi pas",
        "cité de la voile", "cite de la voile", "flore", "course au large",
    )
    exclude = ("alsace lorraine", "aristide briand", "lazare carnot", "interceltique", "fontaines")
    if any(x in addr for x in exclude) and not any(k in addr for k in keys):
        return False
    return dist <= 1.35 or any(k in addr for k in keys)


def main() -> None:
    key = api_key()
    seen: dict[str, dict[str, Any]] = {}

    print("=== FORCE TEXT + GRILLE ===")
    for i, (lat, lng) in enumerate(GRID):
        for q in QUERIES:
            places = search_text(key, f"{q} Lorient La Base", lat, lng)
            for p in places:
                row = normalize(p, f"text:{q}")
                if row and row["place_id"] and row["place_id"] not in seen:
                    seen[row["place_id"]] = row
            time.sleep(0.12)
        print(f"  grille {i+1}/{len(GRID)} → {len(seen)} fiches")

    print("=== FORCE NEARBY ===")
    for i, (lat, lng) in enumerate(GRID[:5]):
        for batch in NEARBY_TYPE_BATCHES:
            places = search_nearby(key, lat, lng, batch)
            for p in places:
                row = normalize(p, f"nearby:{','.join(batch[:2])}")
                if row and row["place_id"] and row["place_id"] not in seen:
                    seen[row["place_id"]] = row
            time.sleep(0.15)
        print(f"  nearby {i+1}/5 → {len(seen)} fiches")

    kept = []
    for row in seen.values():
        if not in_labase(row):
            continue
        # drop empty landmarks
        if not row["telephone"] and row["nom"] in {
            "Pointe de Keroman", "K2", "K3", "K4", "La Base - K3", "La Base - Cité de la Voile"
        }:
            continue
        row["categorie"] = categorize(row)
        row["statut_appel"] = "a_appeler"
        kept.append(row)

    prio = {"bar_resto": 0, "commerce": 1, "site_visite": 2, "hotel": 3, "nautique": 4, "entreprise_autre": 5}
    kept.sort(key=lambda r: (prio.get(r["categorie"], 9), 0 if r["telephone"] else 1, r.get("distance_km", 99), r["nom"]))

    Path("leads").mkdir(exist_ok=True)
    fields = [
        "categorie", "nom", "telephone", "adresse", "site", "maps",
        "note", "nb_avis", "distance_km", "place_id", "source", "statut_appel",
    ]
    out = Path("leads/entreprises_la_base.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(kept)

    with_phone = sum(1 for r in kept if r["telephone"])
    print(f"\nDONE → {out}")
    print(f"TOTAL {len(kept)} | avec téléphone {with_phone}")
    from collections import Counter
    print(Counter(r["categorie"] for r in kept))


if __name__ == "__main__":
    main()
