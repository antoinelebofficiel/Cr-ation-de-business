#!/usr/bin/env python3
"""
Google Places API (New) → liste d'appels B2B vitres (Lorient & agglo).

Usage:
  1. cp .env.example .env  # puis colle ta clé
  2. python3 -m venv .venv && source .venv/bin/activate
  3. pip install -r requirements.txt
  4. python places_lorient.py
  5. python places_lorient.py --zone centre --query "coiffeur"
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://places.googleapis.com/v1/places:searchText"
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

# Zones utiles pour remplir des tournées (pas toute l'agglo d'un coup)
ZONES: dict[str, dict[str, Any]] = {
    "centre": {
        "label": "Centre-ville Lorient",
        "lat": 47.7486,
        "lng": -3.3703,
        "radius_m": 1800,
    },
    "lanester": {
        "label": "Lanester",
        "lat": 47.7647,
        "lng": -3.3397,
        "radius_m": 2500,
    },
    "ploemeur": {
        "label": "Ploemeur",
        "lat": 47.7361,
        "lng": -3.4278,
        "radius_m": 2500,
    },
    "larmor": {
        "label": "Larmor-Plage",
        "lat": 47.7069,
        "lng": -3.3819,
        "radius_m": 2000,
    },
    "caudan": {
        "label": "Caudan / Kerpont",
        "lat": 47.8100,
        "lng": -3.3400,
        "radius_m": 3000,
    },
    "hennebont": {
        "label": "Hennebont",
        "lat": 47.8050,
        "lng": -3.2780,
        "radius_m": 2500,
    },
}

# Requêtes "vitrine image" + quelques whales
DEFAULT_QUERIES = [
    "boutique",
    "coiffeur",
    "institut de beauté",
    "opticien",
    "agence immobilière",
    "pharmacie",
    "bijouterie",
    "fleuriste",
    "concession automobile",
    "hôtel",
    "showroom",
]


def get_api_key() -> str:
    key = os.getenv("GOOGLE_PLACES_API_KEY", "").strip()
    if not key or key == "your_api_key_here":
        print(
            "Erreur: GOOGLE_PLACES_API_KEY manquante.\n"
            "1) Google Cloud Console → activer Places API (New)\n"
            "2) Créer une clé API + billing\n"
            "3) cp .env.example .env puis coller la clé",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def search_text(
    api_key: str,
    query: str,
    zone_key: str,
    page_token: str | None = None,
) -> dict[str, Any]:
    zone = ZONES[zone_key]
    body: dict[str, Any] = {
        "textQuery": f"{query} {zone['label']}",
        "languageCode": "fr",
        "regionCode": "FR",
        "pageSize": 20,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": zone["lat"],
                    "longitude": zone["lng"],
                },
                "radius": float(zone["radius_m"]),
            }
        },
    }
    if page_token:
        body["pageToken"] = page_token

    resp = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": FIELD_MASK,
        },
        json=body,
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Places API {resp.status_code}: {resp.text}")
    return resp.json()


def normalize_place(place: dict[str, Any], zone_key: str, query: str) -> dict[str, Any]:
    name = (place.get("displayName") or {}).get("text", "")
    loc = place.get("location") or {}
    types = place.get("types") or []
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
        "types": "|".join(types),
        "lat": loc.get("latitude", ""),
        "lng": loc.get("longitude", ""),
        "zone": zone_key,
        "query": query,
        "priorite": "A" if place.get("nationalPhoneNumber") else "C",
        "statut_appel": "a_appeler",
    }


def fetch_zone(
    api_key: str,
    zone_key: str,
    queries: list[str],
    sleep_s: float = 0.35,
) -> list[dict[str, Any]]:
    seen: set[str] = set()
    rows: list[dict[str, Any]] = []

    for query in queries:
        page_token: str | None = None
        pages = 0
        while True:
            data = search_text(api_key, query, zone_key, page_token)
            for place in data.get("places") or []:
                pid = place.get("id")
                if not pid or pid in seen:
                    continue
                # Ignore fermés définitivement
                if place.get("businessStatus") == "CLOSED_PERMANENTLY":
                    continue
                seen.add(pid)
                rows.append(normalize_place(place, zone_key, query))

            page_token = data.get("nextPageToken")
            pages += 1
            if not page_token or pages >= 3:  # ~60 résultats max / requête
                break
            time.sleep(sleep_s)
        time.sleep(sleep_s)
        print(f"  [{zone_key}] {query}: {len(rows)} fiches cumulées")

    return rows


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("Aucune fiche à écrire.")
        return
    # Priorité: téléphone présent d'abord
    rows = sorted(rows, key=lambda r: (0 if r["telephone"] else 1, r["zone"], r["nom"]))
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    with_phone = sum(1 for r in rows if r["telephone"])
    print(f"OK → {path} ({len(rows)} fiches, {with_phone} avec téléphone)")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scrape Google Places → CSV appels Lorient")
    p.add_argument(
        "--zone",
        choices=["all", *ZONES.keys()],
        default="centre",
        help="Zone tournée (défaut: centre)",
    )
    p.add_argument(
        "--query",
        action="append",
        dest="queries",
        help="Requête Maps (répétable). Défaut: pack vitrines",
    )
    p.add_argument(
        "--out",
        default="output/leads_places.csv",
        help="Fichier CSV de sortie",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    api_key = get_api_key()
    queries = args.queries or DEFAULT_QUERIES
    zones = list(ZONES.keys()) if args.zone == "all" else [args.zone]

    all_rows: list[dict[str, Any]] = []
    seen: set[str] = set()

    for zone_key in zones:
        print(f"Zone {zone_key} — {ZONES[zone_key]['label']}")
        rows = fetch_zone(api_key, zone_key, queries)
        for row in rows:
            if row["place_id"] in seen:
                continue
            seen.add(row["place_id"])
            all_rows.append(row)

    write_csv(all_rows, Path(args.out))


if __name__ == "__main__":
    main()
