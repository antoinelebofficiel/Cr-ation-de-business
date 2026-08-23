#!/usr/bin/env python3
"""Liste du jour pour faire basculer UNE tournée. 4 créneaux le même matin = créée."""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARNET = Path(__file__).resolve().parent / "carnet.csv"
CIBLES = ROOT / "cibles-commerces.csv"
OUT = Path(__file__).resolve().parent / "aujourdhui.csv"

TIP = 4
SLOTS = ["08:30", "09:10", "09:50", "10:30", "11:10", "11:50"]

# Plus le score est bas, plus tu frappes tôt (gérant sur place, vitre lue).
RANG = [
    ("bakery", 1),
    ("pastry", 1),
    ("pharmacy", 1),
    ("hair", 1),
    ("florist", 1),
    ("restaurant", 2),
    ("pizza", 2),
    ("cafe", 2),
    ("bar", 2),
    ("clothing", 3),
    ("jewelry", 3),
    ("store", 4),
    ("real_estate", 6),
    ("insurance", 6),
    ("bank", 9),
    ("atm", 9),
]


def types_index():
    by_pair = {}
    by_tel = {}
    with CIBLES.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_pair[(r["nom"], r["tel"])] = r.get("types", "")
            if r.get("tel"):
                by_tel[r["tel"]] = r.get("types", "")
    return by_pair, by_tel


def rang(types):
    t = (types or "").lower()
    best = 5
    for key, n in RANG:
        if key in t:
            best = min(best, n)
    return best


def load_carnet():
    with CARNET.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pick(rows, arg):
    by = {}
    for r in rows:
        by.setdefault(r["tournee_id"], []).append(r)

    if arg:
        tid = arg.upper() if arg.upper().startswith("T") else None
        if tid and tid in by:
            return tid, by[tid]
        jour = arg[:3].capitalize()
        for tid, shops in by.items():
            if shops[0]["jour"] == jour:
                actifs = [s for s in shops if s["statut"] not in ("contrat", "perdu")]
                poses = [s for s in shops if s["statut"] in ("premier", "contrat")]
                if len(poses) < TIP and actifs:
                    return tid, shops

    for tid in sorted(by):
        shops = by[tid]
        poses = [s for s in shops if s["statut"] in ("premier", "contrat")]
        if len(poses) < TIP:
            return tid, shops
    return None, []


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    rows = load_carnet()
    by_pair, by_tel = types_index()
    tid, shops = pick(rows, arg)
    if not shops:
        print("Toutes les tournées ont déjà 4 stops. Passe à la conversion SEPA.")
        return

    meta = shops[0]
    poses = [s for s in shops if s["statut"] in ("premier", "contrat")]
    morts = [s for s in shops if s["statut"] == "perdu"]
    ouverts = [s for s in shops if s["statut"] in ("cible", "premier") or s["statut"] == ""]
    # portes = encore à frapper
    portes = [s for s in shops if s["statut"] == "cible"]
    for s in portes:
        s["_types"] = by_pair.get((s["commerce"], s["tel"])) or by_tel.get(s["tel"], "")
        s["_rang"] = rang(s["_types"])
    portes.sort(key=lambda s: (s["_rang"], int(s["ordre"] or 0)))

    manque = max(0, TIP - len(poses))
    jour = meta["jour"]
    ilot = meta["ilot"]
    zone = meta["zone"]

    print(f"{tid}  {jour}  {zone}")
    print(f"{ilot}")
    print(f"Posés {len(poses)}/{TIP}  —  il en faut encore {manque} demain matin.")
    print()
    print("PHRASE (porte et appel, telle quelle)")
    print(
        f"Clartéo, vitrines. Je passe {jour} matin sur {ilot.split(' / ')[0]}. "
        f"Premier passage 49 €, sans engagement. Je vous glisse à {{heure}} ?"
    )
    print()
    print("ORDRE — tu frappes dans cet ordre, tu n’inventes pas de 13e commerce.")
    fields = [
        "ordre_blitz",
        "tournee_id",
        "heure_proposee",
        "commerce",
        "tel",
        "adresse",
        "statut",
        "rang",
        "action",
    ]
    out_rows = []
    for i, s in enumerate(portes):
        heure = SLOTS[i] if i < len(SLOTS) else SLOTS[-1]
        action = "PORTE puis appel si fermé"
        if s["_rang"] >= 9:
            action = "DERNIER — banque, 30 s, si non tu passes"
        elif s["_rang"] >= 6:
            action = "Après les commerces qui décident sur place"
        out_rows.append(
            {
                "ordre_blitz": i + 1,
                "tournee_id": tid,
                "heure_proposee": heure,
                "commerce": s["commerce"],
                "tel": s["tel"],
                "adresse": s["adresse"],
                "statut": s["statut"],
                "rang": s["_rang"],
                "action": action,
            }
        )
        print(f"  {i+1:2}. {heure}  {s['commerce'][:42]:42}  {s['tel']}  {action}")

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    print()
    print("J0  8h30–11h  les portes ci-dessus. Photo de LEUR vitre en arrivant.")
    print(f"    Tu t’arrêtes dès que tu as {manque} OUI pour {jour} matin.")
    print("J0  14h–17h  tu rappelles uniquement les fermés / NRP de CETTE liste.")
    print(f"J1  {SLOTS[0]}  tu laves les OUI sur la place. Van visible.")
    print("    Entre deux baies tu refrappes le voisin : « je suis en face, 20 min, 49 € ».")
    print("J1  soir      « Je signe » + jour fixe + SEPA. Statut → premier puis contrat.")
    print("J2  s’il manque des stops : même place, tu ne changes pas d’îlot.")
    print()
    print(f"Écrit : {OUT.name}")
    print("Interdit : appeler T02, suivre un lead hors îlot, envoyer un mail.")


if __name__ == "__main__":
    main()
