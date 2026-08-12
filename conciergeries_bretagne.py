#!/usr/bin/env python3
"""
Conciergeries Bretagne → CSV CRM (Google Sheets ready) via Places API (New).

Usage:
  python conciergeries_bretagne.py
  python conciergeries_bretagne.py --limit 100 --out leads/conciergeries_bretagne_100.csv
  python conciergeries_bretagne.py --push-sheets   # needs GOOGLE_SERVICE_ACCOUNT_JSON + GOOGLE_SHEET_ID
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
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

# Couverture Bretagne (villes + pôles touristiques LCD)
ZONES: dict[str, dict[str, Any]] = {
    "rennes": {"label": "Rennes", "lat": 48.1173, "lng": -1.6778, "radius_m": 12000},
    "saint_malo": {"label": "Saint-Malo", "lat": 48.6493, "lng": -2.0257, "radius_m": 10000},
    "dinard": {"label": "Dinard", "lat": 48.6322, "lng": -2.0603, "radius_m": 8000},
    "dinan": {"label": "Dinan", "lat": 48.4550, "lng": -2.0470, "radius_m": 8000},
    "saint_brieuc": {"label": "Saint-Brieuc", "lat": 48.5140, "lng": -2.7650, "radius_m": 10000},
    "paimpol": {"label": "Paimpol", "lat": 48.7780, "lng": -3.0450, "radius_m": 8000},
    "perros": {"label": "Perros-Guirec", "lat": 48.8150, "lng": -3.4430, "radius_m": 8000},
    "lannion": {"label": "Lannion", "lat": 48.7330, "lng": -3.4550, "radius_m": 9000},
    "morlaix": {"label": "Morlaix", "lat": 48.5770, "lng": -3.8270, "radius_m": 9000},
    "brest": {"label": "Brest", "lat": 48.3904, "lng": -4.4861, "radius_m": 12000},
    "quimper": {"label": "Quimper", "lat": 47.9970, "lng": -4.0970, "radius_m": 11000},
    "concarneau": {"label": "Concarneau", "lat": 47.8750, "lng": -3.9220, "radius_m": 8000},
    "fouesnant": {"label": "Fouesnant", "lat": 47.8930, "lng": -4.0100, "radius_m": 8000},
    "benodet": {"label": "Bénodet", "lat": 47.8750, "lng": -4.1080, "radius_m": 7000},
    "douarnenez": {"label": "Douarnenez", "lat": 48.0930, "lng": -4.3300, "radius_m": 8000},
    "lorient": {"label": "Lorient", "lat": 47.7486, "lng": -3.3703, "radius_m": 12000},
    "quiberon": {"label": "Quiberon", "lat": 47.4840, "lng": -3.1200, "radius_m": 8000},
    "carnac": {"label": "Carnac", "lat": 47.5840, "lng": -3.0780, "radius_m": 8000},
    "auray": {"label": "Auray", "lat": 47.6670, "lng": -2.9830, "radius_m": 8000},
    "vannes": {"label": "Vannes", "lat": 47.6580, "lng": -2.7600, "radius_m": 11000},
    "sarzeau": {"label": "Sarzeau", "lat": 47.5280, "lng": -2.7690, "radius_m": 9000},
    "la_trinite": {"label": "La Trinité-sur-Mer", "lat": 47.5860, "lng": -3.0280, "radius_m": 7000},
    "pontivy": {"label": "Pontivy", "lat": 48.0680, "lng": -2.9650, "radius_m": 9000},
    "guingamp": {"label": "Guingamp", "lat": 48.5630, "lng": -3.1550, "radius_m": 8000},
}

QUERIES = [
    "conciergerie",
    "conciergerie Airbnb",
    "conciergerie location courte durée",
    "gestion locative saisonnière",
    "conciergerie locations vacances",
]

NAME_OK = re.compile(
    r"concierger|airbnb|saisonni|courte\s*dur[eé]e|location\s*vacances|"
    r"gestion\s*locative|property\s*management|check[\s-]?in|clé\s*en\s*main|"
    r"host\s*service|guest\s*ready|keynest|guestly",
    re.I,
)
NAME_NO = re.compile(
    r"h[oô]tel|restaurant|coiffeur|pharmacie|garage|opticien|"
    r"assurance|banque|notaire|avocat|clinique|m[eé]decin",
    re.I,
)
EMAIL_RE = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
)
EMAIL_BAD = re.compile(
    r"(noreply|no-reply|donotreply|example\.com|sentry\.io|wixpress|"
    r"cloudflare|schema\.org|godaddy|wordpress\.com|googleapis|"
    r"png|jpg|jpeg|gif|webp|svg)",
    re.I,
)

CRM_FIELDS = [
    "nom",
    "email",
    "telephone",
    "adresse",
    "ville_zone",
    "site",
    "maps",
    "note",
    "nb_avis",
    "statut",
    "email_source",
    "place_id",
    "lat",
    "lng",
    "statut_crm",
    "date_ajout",
]


def get_api_key() -> str:
    key = os.getenv("GOOGLE_PLACES_API_KEY", "").strip()
    if not key or key == "your_api_key_here":
        print("Erreur: GOOGLE_PLACES_API_KEY manquante (.env)", file=sys.stderr)
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
        "textQuery": f"{query} {zone['label']} Bretagne",
        "languageCode": "fr",
        "regionCode": "FR",
        "pageSize": 20,
        "locationBias": {
            "circle": {
                "center": {"latitude": zone["lat"], "longitude": zone["lng"]},
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
        raise RuntimeError(f"Places API {resp.status_code}: {resp.text[:500]}")
    return resp.json()


def looks_like_conciergerie(name: str, types: list[str], query: str) -> bool:
    if NAME_NO.search(name) and not NAME_OK.search(name):
        return False
    if NAME_OK.search(name):
        return True
    if "concierger" in query.lower() or "airbnb" in query.lower() or "saisonni" in query.lower():
        # Places a renvoyé ça sur une requête conciergerie : on garde sauf bruit évident
        junk_types = {"restaurant", "lodging", "hotel", "gas_station", "bank"}
        if set(types) & junk_types and "travel_agency" not in types and "real_estate_agency" not in types:
            # hôtels / restos sans nom conciergerie
            if not NAME_OK.search(name):
                return False
        return True
    return False


def normalize_place(place: dict[str, Any], zone_key: str, query: str) -> dict[str, Any] | None:
    name = (place.get("displayName") or {}).get("text", "").strip()
    types = place.get("types") or []
    if not name or not looks_like_conciergerie(name, types, query):
        return None
    if place.get("businessStatus") == "CLOSED_PERMANENTLY":
        return None
    loc = place.get("location") or {}
    return {
        "place_id": place.get("id", ""),
        "nom": name,
        "telephone": place.get("nationalPhoneNumber")
        or place.get("internationalPhoneNumber")
        or "",
        "adresse": place.get("formattedAddress", ""),
        "ville_zone": ZONES[zone_key]["label"],
        "site": place.get("websiteUri", "") or "",
        "maps": place.get("googleMapsUri", "") or "",
        "note": place.get("rating", ""),
        "nb_avis": place.get("userRatingCount", ""),
        "statut": place.get("businessStatus", ""),
        "lat": loc.get("latitude", ""),
        "lng": loc.get("longitude", ""),
        "email": "",
        "email_source": "",
        "statut_crm": "a_contacter",
        "date_ajout": time.strftime("%Y-%m-%d"),
        "_query": query,
        "_zone": zone_key,
    }


def fetch_all(api_key: str, sleep_s: float = 0.15) -> list[dict[str, Any]]:
    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    # 2 requêtes suffisent : Places déduplique déjà beaucoup
    queries = QUERIES[:2]
    for zone_key in ZONES:
        before = len(rows)
        for query in queries:
            page_token: str | None = None
            pages = 0
            while True:
                data = search_text(api_key, query, zone_key, page_token)
                for place in data.get("places") or []:
                    pid = place.get("id")
                    if not pid or pid in seen:
                        continue
                    row = normalize_place(place, zone_key, query)
                    if not row:
                        continue
                    seen.add(pid)
                    rows.append(row)
                page_token = data.get("nextPageToken")
                pages += 1
                if not page_token or pages >= 2:
                    break
                time.sleep(sleep_s)
            time.sleep(sleep_s)
        print(f"Zone {ZONES[zone_key]['label']}: +{len(rows) - before} (total {len(rows)})", flush=True)
    return rows


def pick_best_email(emails: list[str]) -> str | None:
    scored: list[tuple[int, str]] = []
    for e in emails:
        e = e.strip(".,;:()[]<>\"' ").lower()
        if len(e) < 6 or EMAIL_BAD.search(e):
            continue
        score = 0
        local = e.split("@", 1)[0]
        if any(x in local for x in ("contact", "info", "hello", "bonjour", "accueil", "resa", "reservation", "concierger")):
            score += 5
        if any(x in local for x in ("admin", "webmaster", "postmaster", "mailer")):
            score -= 3
        scored.append((score, e))
    if not scored:
        return None
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[0][1]


def extract_emails_from_html(html: str) -> list[str]:
    found = set(EMAIL_RE.findall(html))
    soup = BeautifulSoup(html, "lxml")
    for a in soup.select('a[href^="mailto:"]'):
        href = a.get("href", "")
        mail = href.replace("mailto:", "").split("?")[0].strip()
        if mail:
            found.add(mail)
    return list(found)


def fetch_page(session: requests.Session, url: str, timeout: float = 12) -> str | None:
    try:
        r = session.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; LeadResearch/1.0; +business-research)",
                "Accept": "text/html,application/xhtml+xml",
            },
            allow_redirects=True,
        )
        if r.status_code >= 400:
            return None
        ctype = (r.headers.get("Content-Type") or "").lower()
        if "html" not in ctype and "text" not in ctype:
            return None
        return r.text
    except requests.RequestException:
        return None


def discover_contact_urls(base: str, html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    urls: list[str] = []
    keywords = ("contact", "mention", "a-propos", "about", "nous", "reservation", "booking")
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = (a.get_text() or "").lower()
        low = href.lower()
        if any(k in low or k in text for k in keywords):
            full = urljoin(base, href)
            if urlparse(full).scheme in ("http", "https"):
                urls.append(full.split("#")[0])
    # dedupe preserve order
    out: list[str] = []
    seen: set[str] = set()
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out[:4]


def enrich_email(row: dict[str, Any], session: requests.Session | None = None) -> None:
    site = (row.get("site") or "").strip()
    if not site:
        return
    session = session or requests.Session()
    html = fetch_page(session, site)
    if not html:
        return
    emails = extract_emails_from_html(html)
    best = pick_best_email(emails)
    if best:
        row["email"] = best
        row["email_source"] = "site_accueil"
        return
    for url in discover_contact_urls(site, html):
        page = fetch_page(session, url)
        if not page:
            continue
        best = pick_best_email(extract_emails_from_html(page))
        if best:
            row["email"] = best
            row["email_source"] = "page_contact"
            return


def enrich_emails_parallel(rows: list[dict[str, Any]], workers: int = 8) -> None:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    targets = [r for r in rows if (r.get("site") or "").strip()]
    print(f"Enrichissement email: {len(targets)} sites ({workers} workers)", flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(enrich_email, r): r for r in targets}
        for fut in as_completed(futs):
            done += 1
            try:
                fut.result()
            except Exception as e:  # noqa: BLE001
                print(f"  warn email: {e}", flush=True)
            if done % 15 == 0 or done == len(targets):
                n = sum(1 for r in rows if r.get("email"))
                print(f"  emails {done}/{len(targets)} — {n} trouvés", flush=True)


def rank_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def score(r: dict[str, Any]) -> tuple:
        return (
            0 if r.get("email") else 1,
            0 if r.get("telephone") else 1,
            0 if r.get("site") else 1,
            -(float(r["nb_avis"]) if str(r.get("nb_avis") or "").replace(".", "", 1).isdigit() else 0),
            r.get("ville_zone", ""),
            r.get("nom", ""),
        )

    return sorted(rows, key=score)


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CRM_FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in CRM_FIELDS})
    with_mail = sum(1 for r in rows if r.get("email"))
    with_phone = sum(1 for r in rows if r.get("telephone"))
    print(f"OK → {path} ({len(rows)} lignes, {with_mail} emails, {with_phone} tél)")


def push_google_sheets(rows: list[dict[str, Any]]) -> str:
    """Push vers Google Sheets si credentials service account présents."""
    sa_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    sheet_id = os.getenv("GOOGLE_SHEET_ID", "").strip()
    if not sa_path or not sheet_id:
        raise SystemExit(
            "Push Sheets: définir GOOGLE_SERVICE_ACCOUNT_JSON et GOOGLE_SHEET_ID dans .env"
        )
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(sa_path, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)
    try:
        ws = sh.worksheet("Conciergeries Bretagne")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title="Conciergeries Bretagne", rows=200, cols=len(CRM_FIELDS))
    values = [CRM_FIELDS] + [[str(r.get(k, "")) for k in CRM_FIELDS] for r in rows]
    ws.clear()
    ws.update("A1", values, value_input_option="RAW")
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
    print(f"Sheets OK → {url}")
    return url


def write_sheets_import_readme(csv_path: Path, out: Path) -> None:
    raw_hint = (
        "Après push GitHub, dans une Google Sheet vide :\n"
        f'=IMPORTDATA("https://raw.githubusercontent.com/<USER>/<REPO>/<BRANCH>/{csv_path.as_posix()}")\n'
        "ou Fichier → Importer → Upload du CSV."
    )
    out.write_text(
        "# Conciergeries Bretagne — CRM Google Sheets\n\n"
        f"Fichier source : `{csv_path.as_posix()}`\n\n"
        "## Import Google Sheets (sans API)\n"
        "1. Ouvre https://sheets.new\n"
        "2. Fichier → Importer → Téléverser → choisis le CSV\n"
        "3. Séparateur : virgule · Remplacer la feuille\n\n"
        "## Sync auto (IMPORTDATA)\n"
        f"```\n{raw_hint}\n```\n\n"
        "## Push API (optionnel)\n"
        "1. Google Cloud → Service Account + Sheets API + Drive API\n"
        "2. Partage la Sheet avec l'email du service account ( Éditeur )\n"
        "3. `.env` :\n"
        "   `GOOGLE_SERVICE_ACCOUNT_JSON=./service-account.json`\n"
        "   `GOOGLE_SHEET_ID=...`\n"
        "4. `python conciergeries_bretagne.py --push-sheets --skip-fetch` "
        "(ou laisse le scrape tourner puis push)\n\n"
        "Colonnes CRM : nom, email, telephone, adresse, ville_zone, site, maps, "
        "note, nb_avis, statut, email_source, place_id, lat, lng, statut_crm, date_ajout\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scrape conciergeries Bretagne → CRM Sheets")
    p.add_argument("--limit", type=int, default=100, help="Nombre max de fiches (défaut 100)")
    p.add_argument(
        "--out",
        default="leads/conciergeries_bretagne_100.csv",
        help="CSV de sortie",
    )
    p.add_argument("--no-email", action="store_true", help="Skip enrichissement email sites")
    p.add_argument("--push-sheets", action="store_true", help="Pousser vers Google Sheets")
    p.add_argument(
        "--from-csv",
        default="",
        help="Réutiliser un CSV déjà scrapé (skip Places)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out = Path(args.out)

    if args.from_csv:
        with Path(args.from_csv).open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        print(f"Chargé {len(rows)} lignes depuis {args.from_csv}", flush=True)
        if not args.no_email:
            enrich_emails_parallel(rows)
    else:
        api_key = get_api_key()
        rows = fetch_all(api_key)
        print(f"Brut Places : {len(rows)} conciergeries uniques", flush=True)

        # Sauvegarde brute avant emails (reprise possible)
        write_csv(rank_rows(rows), Path("leads/conciergeries_bretagne_raw.csv"))

        if not args.no_email:
            enrich_emails_parallel(rows)
            write_csv(rank_rows(rows), Path("leads/conciergeries_bretagne_all.csv"))

    rows = rank_rows(rows)[: max(1, args.limit)]
    write_csv(rows, out)
    write_sheets_import_readme(out, Path("leads/CONCIERGERIES_SHEETS.md"))

    if args.push_sheets:
        push_google_sheets(rows)

    with_mail = sum(1 for r in rows if r.get("email"))
    print(
        f"Livrable CRM : {len(rows)} conciergeries Bretagne "
        f"({with_mail} avec email) → {out}",
        flush=True,
    )


if __name__ == "__main__":
    main()
