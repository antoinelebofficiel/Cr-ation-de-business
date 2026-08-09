#!/usr/bin/env python3
"""Enrichit interlocuteur/dirigeant pour tous les prospects du CSV 500."""

from __future__ import annotations

import csv
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests

GOUV_URL = "https://recherche-entreprises.api.gouv.fr/search"
IN_PATH = Path("leads/prospects_500_min120.csv")
OUT_PATH = IN_PATH


def clean_name(name: str) -> str:
    name = re.sub(r"\s*[\|\-–].*$", "", name)
    name = re.sub(
        r"\b(SARL|SAS|EURL|SASU|SCI|SA|SPA|SELARL|SNC)\b",
        "",
        name,
        flags=re.I,
    )
    name = re.sub(r"\b(lorient|lanester|ploemeur|larmor|caudan|hennebont|guidel|quéven|queven)\b", "", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip()


def extract_cp(adresse: str) -> str:
    m = re.search(r"\b56\d{3}\b", adresse or "")
    return m.group(0) if m else ""


def format_dirigeant(d: dict) -> tuple[str, str]:
    if not d or d.get("type_dirigeant") == "personne morale":
        return "", ""
    prenoms = (d.get("prenoms") or "").strip()
    nom = (d.get("nom") or "").strip()
    prenom = prenoms.split()[0].title() if prenoms else ""
    full = f"{prenom} {nom.title()}".strip()
    return full, (d.get("qualite") or "").strip()


def pick_dirigeant(dirigeants: list[dict]) -> dict | None:
    prefer = ("gérant", "gerant", "président", "president", "directeur", "associé")
    phys = [d for d in dirigeants if d.get("type_dirigeant") != "personne morale"]
    for d in phys:
        qual = (d.get("qualite") or "").lower()
        if any(p in qual for p in prefer):
            return d
    return phys[0] if phys else None


def search_gouv(queries: list[str], cp: str) -> dict | None:
    for q in queries:
        if not q or len(q) < 3:
            continue
        urls = []
        if cp:
            urls.append(f"{GOUV_URL}?q={quote(q)}&code_postal={cp}&per_page=8")
        urls.append(f"{GOUV_URL}?q={quote(q)}&departement=56&per_page=8")
        for url in urls:
            try:
                r = requests.get(url, timeout=25, headers={"Accept": "application/json"})
                if r.status_code != 200:
                    continue
                results = r.json().get("results") or []
            except Exception:
                continue
            for item in results:
                if item.get("etat_administratif") == "C":
                    continue
                chosen = pick_dirigeant(item.get("dirigeants") or [])
                if not chosen:
                    continue
                name, qual = format_dirigeant(chosen)
                if not name:
                    continue
                bad = ("deloitte", "ernst", "mazars", "forvis", "kpmg", "pricewater", "pwc")
                if any(b in name.lower() for b in bad):
                    continue
                return {
                    "interlocuteur": name,
                    "qualite_dirigeant": qual,
                    "qui_demander": qual or "Gérant / propriétaire",
                    "siren": item.get("siren") or "",
                    "raison_sociale": item.get("nom_complet") or item.get("nom_raison_sociale") or "",
                }
            time.sleep(0.05)
        time.sleep(0.05)
    return None


def query_variants(nom: str) -> list[str]:
    base = clean_name(nom)
    variants = [nom.strip(), base]
    # first meaningful tokens
    tokens = [t for t in re.split(r"[\s,/]+", base) if len(t) > 2]
    if len(tokens) >= 2:
        variants.append(" ".join(tokens[:3]))
        variants.append(" ".join(tokens[:2]))
    if tokens:
        variants.append(tokens[0])
    # dedupe preserve order
    out = []
    seen = set()
    for v in variants:
        v = v.strip()
        key = v.lower()
        if v and key not in seen:
            seen.add(key)
            out.append(v)
    return out[:6]


def main() -> None:
    rows = list(csv.DictReader(IN_PATH.open(encoding="utf-8")))
    fields = list(rows[0].keys())
    missing_before = sum(1 for r in rows if not (r.get("interlocuteur") or "").strip())
    print(f"Total {len(rows)} | sans dirigeant: {missing_before}", flush=True)

    filled = 0
    refreshed = 0
    still_missing = 0

    for i, r in enumerate(rows, 1):
        had = bool((r.get("interlocuteur") or "").strip())
        # Always try if missing; also retry if had but no siren (weak)
        should = (not had) or (had and not (r.get("siren") or "").strip())
        if not should and had:
            if i % 50 == 0:
                print(f"  {i}/{len(rows)} skip (déjà OK)", flush=True)
            continue

        info = search_gouv(query_variants(r["nom"]), extract_cp(r.get("adresse", "")))
        if info:
            r.update(info)
            if had:
                refreshed += 1
            else:
                filled += 1
        else:
            if not (r.get("interlocuteur") or "").strip():
                r["qui_demander"] = r.get("qui_demander") or "Gérant / propriétaire"
                still_missing += 1

        if i % 25 == 0 or i == len(rows):
            ok = sum(1 for x in rows if (x.get("interlocuteur") or "").strip())
            print(
                f"  {i}/{len(rows)} | avec nom={ok} | +{filled} nouveaux | retry={refreshed} | encore vides={still_missing}",
                flush=True,
            )
        time.sleep(0.08)

    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    # sync top100
    top = Path("leads/top100_prospects.csv")
    with top.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows[:100])

    ok = sum(1 for r in rows if (r.get("interlocuteur") or "").strip())
    print(f"\nDONE → {OUT_PATH}", flush=True)
    print(f"Avec dirigeant: {ok}/{len(rows)}", flush=True)
    print(f"Nouveaux remplis: {filled} | encore sans: {len(rows)-ok}", flush=True)


if __name__ == "__main__":
    main()
