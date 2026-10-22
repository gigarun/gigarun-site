#!/usr/bin/env python3
"""Genere satisfaction.json (stats + avis anonymises) pour la page support de gigarun.re.

Source : table hesk_ai_satisfaction du plugin SmartDesk IA (HESK). LECTURE SEULE.
Sortie : aggregats uniquement, aucune donnee identifiante (ni client, ni agent, ni ticket, ni date precise).

Regles de publication :
- delai : les reponses de moins de DELAI_H heures ne sont pas comptees (pas de correlation avec un incident du jour) ;
- les commentaires ne sortent QUE s'ils sont dans avis-valides.json (relecture humaine) ;
- tous les avis valides sont publies, quelle que soit la note (pas de tri sur les bonnes notes) ;
- note moyenne masquee sous MIN_REPONSES reponses ;
- si la base est injoignable, l'ancien fichier est conserve (code retour 1).

Usage : satisfaction_json.py [--out chemin] [--selftest]
Connexion : SAT_DB_HOST/PORT/USER/PASS/NAME (defaut : copie locale hesk_local).
Produit aussi avis-a-relire.json (a cote du script, JAMAIS a publier) : candidats a valider.
"""
import argparse, datetime as dt, json, os, re, sys, tempfile

DELAI_H = 72
MIN_REPONSES = 10
MOIS_MIN_REPONSES = 3
HERE = os.path.dirname(os.path.abspath(__file__))
RE_PII = re.compile(r"[\w.+-]+@[\w-]+\.\w+|https?://|www\.|(?:\+?\d[\s.-]?){8,}|\b[A-Z0-9]{3}-[A-Z0-9]{3}-[A-Z0-9]{4}\b")
STOP = {"client", "general", "interne", "support", "gigarun", "cabinet", "societe", "sarl", "holding", "bureaux", "objets", "docteurs",
        "des", "les", "pas", "service", "services", "technique", "techniques", "pieces", "location", "auto", "centre", "sud", "nord"}


def tokens(texts):
    """Mots >= 3 lettres des noms (agents, clients, societes) : a ne jamais laisser dans un avis."""
    out = set()
    for t in texts:
        for w in re.findall(r"[^\W\d_]{3,}", (t or "").lower()):
            if w not in STOP:
                out.add(w)
    return out


def hits(texte, deny):
    """Raisons pour lesquelles un commentaire n'est pas publiable tel quel."""
    r = []
    if RE_PII.search(texte):
        r.append("email/telephone/url/ticket")
    mots = set(re.findall(r"[^\W\d_]{3,}", texte.lower()))
    noms = sorted(mots & deny)
    if noms:
        r.append("nom: " + ",".join(noms))
    return r


def mois(d):
    return d.strftime("%Y-%m")


def moy(vals):
    vals = [v for v in vals if v is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


def construire(rows, envoyees, valides, deny, now, ecartes=frozenset()):
    """rows : reponses completees (dicts). Retourne (public, a_relire)."""
    cut = now - dt.timedelta(hours=DELAI_H)
    ok = [r for r in rows if r["completed_at"] <= cut]
    n = len(ok)
    par_mois = {}
    for r in ok:
        par_mois.setdefault(mois(r["completed_at"]), []).append(r["rating_overall"])
    debut = mois(cut.replace(day=1) - dt.timedelta(days=1) - dt.timedelta(days=335))
    serie = [{"mois": m, "reponses": len(v), "note": moy(v) if len(v) >= MOIS_MIN_REPONSES else None}
             for m, v in sorted(par_mois.items()) if m >= debut]
    reco = [r["would_recommend"] for r in ok if r["would_recommend"] is not None]
    avis, relire = [], []
    for r in ok:
        txt = (r["comment"] or "").strip()
        if not txt:
            continue
        v = valides.get(r["id"])
        if v is None and r["id"] in ecartes:  # decision prise : ne pas publier, ne plus signaler
            continue
        if v is None:
            relire.append({"id": r["id"], "mois": mois(r["completed_at"]), "note": r["rating_overall"],
                           "texte": txt, "alertes": hits(txt, deny)})
            continue
        v, force = v
        pb = [h for h in hits(v, deny) if not (force and h.startswith("nom:"))]  # force = relu a la main, faux positif de nom
        if pb:
            raise SystemExit(f"avis valide {r['id']} refuse ({'; '.join(pb)}) : corriger avis-valides.json")
        avis.append({"mois": mois(r["completed_at"]), "note": r["rating_overall"], "texte": v})
    public = {
        "genere_le": now.strftime("%Y-%m-%d"),
        "delai_publication_h": DELAI_H,
        "enquetes_envoyees": envoyees,
        "reponses": n,
        "taux_reponse": round(100 * n / envoyees) if envoyees else None,
        "note_moyenne": moy([r["rating_overall"] for r in ok]) if n >= MIN_REPONSES else None,
        "satisfaits_pct": round(100 * sum(r["rating_overall"] >= 4 for r in ok) / n) if n >= MIN_REPONSES else None,
        "recommandent_pct": round(100 * sum(reco) / len(reco)) if len(reco) >= MIN_REPONSES else None,
        "criteres": {k: moy([r[c] for r in ok]) for k, c in
                     (("rapidite", "rating_speed"), ("qualite", "rating_quality"), ("amabilite", "rating_friendliness"))}
        if n >= MIN_REPONSES else None,
        "repartition": {str(i): sum(r["rating_overall"] == i for r in ok) for i in range(1, 6)},
        "par_mois": serie,
        "avis": sorted(avis, key=lambda a: a["mois"], reverse=True),
        "regle": "Avis anonymisés, publiés après relecture. Aucun avis n'est écarté en raison de sa note.",
    }
    return public, relire


def lire_base():
    import pymysql
    c = pymysql.connect(host=os.getenv("SAT_DB_HOST", "127.0.0.1"), port=int(os.getenv("SAT_DB_PORT", "3306")),
                        user=os.getenv("SAT_DB_USER", "root"), password=os.getenv("SAT_DB_PASS", ""),
                        database=os.getenv("SAT_DB_NAME", "hesk_local"), charset="utf8mb4",
                        cursorclass=pymysql.cursors.DictCursor, connect_timeout=15, read_timeout=60)
    with c, c.cursor() as q:
        q.execute("SELECT id, rating_overall, rating_speed, rating_quality, rating_friendliness, would_recommend, comment, completed_at "
                  "FROM hesk_ai_satisfaction WHERE survey_type='ticket' AND completed_at IS NOT NULL AND rating_overall BETWEEN 1 AND 5")
        rows = q.fetchall()
        q.execute("SELECT COUNT(*) n FROM hesk_ai_satisfaction WHERE survey_type='ticket' AND email_sent_at IS NOT NULL "
                  "AND email_sent_at <= UTC_TIMESTAMP() - INTERVAL %s HOUR", (DELAI_H,))
        envoyees = q.fetchone()["n"]
        noms = []
        for sql in ("SELECT name, user, nickname FROM hesk_users", "SELECT name FROM hesk_customers",
                    "SELECT DISTINCT name, u_name FROM hesk_tickets", "SELECT name FROM hesk_categories"):
            q.execute(sql)
            for r in q.fetchall():
                noms.extend(str(v) for v in r.values() if v)
    return rows, envoyees, tokens(noms)


def ecrire(chemin, data):
    os.makedirs(os.path.dirname(os.path.abspath(chemin)), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(chemin)), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    os.replace(tmp, chemin)  # remplacement atomique : le site ne lit jamais un fichier a moitie ecrit


def selftest():
    d = tokens(["Gilles Barbe", "Client 02", "SCM Docteurs Kolbe"])
    assert hits("Merci Gilles pour la rapidite", d) == ["nom: gilles"]
    assert hits("ecrire a jean@x.fr", d) and hits("appelez le 0262 96 72 91", d) and hits("ticket 8AG-LBN-371E", d)
    assert hits("Toujours tres reactif, merci.", d) == []
    now = dt.datetime(2026, 10, 22, 12)
    mk = lambda i, h, note, c="": dict(id=i, rating_overall=note, rating_speed=note, rating_quality=note, rating_friendliness=note,
                                      would_recommend=1, comment=c, completed_at=now - dt.timedelta(hours=h))
    rows = [mk(i, 100 + i * 24, 5, "Tres bien" if i == 1 else "") for i in range(12)] + [mk(99, 5, 1, "trop recent")]
    p, r = construire(rows, 50, {1: ("Tres bien", False)}, d, now)
    assert p["reponses"] == 12 and p["taux_reponse"] == 24 and p["note_moyenne"] == 5.0   # reponse recente (<72h) ignoree
    assert len(p["avis"]) == 1 and r == [] and "id" not in p["avis"][0]
    p2, r2 = construire(rows[:5], 50, {}, d, now)
    assert p2["note_moyenne"] is None and len(r2) == 1                                     # sous le seuil + commentaire a relire
    assert construire(rows[:5], 50, {}, d, now, {1})[1] == []                              # avis ecarte : plus signale
    try:
        construire(rows, 50, {1: ("Merci Gilles", False)}, d, now); raise AssertionError("aurait du refuser")
    except SystemExit:
        pass
    assert construire(rows, 50, {1: ("Merci Gilles", True)}, d, now)[0]["avis"]            # force : nom relu a la main
    try:
        construire(rows, 50, {1: ("ecrire a jean@x.fr", True)}, d, now); raise AssertionError("force ne leve pas un contact")
    except SystemExit:
        pass
    print("selftest OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "out", "satisfaction.json"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--relire", default=os.path.join(HERE, "avis-a-relire.json"), help="candidats a relire (texte brut : jamais dans le depot)")
    ap.add_argument("--resume", help="resume des avis en attente SANS texte (ids, mois, note, alertes), pour la notification")
    ap.add_argument("--env", help="fichier KEY=VALUE avec SAT_DB_* (hors depot, chmod 600)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.env:
        for l in open(a.env, encoding="utf-8-sig"):
            k, s, v = l.strip().partition("=")
            if s and not k.startswith("#"):
                os.environ[k.strip()] = v.strip().strip("\"'")
    try:
        rows, envoyees, deny = lire_base()
    except Exception as e:
        print(f"base injoignable, fichier precedent conserve : {e}", file=sys.stderr)
        sys.exit(1)
    p_valides = os.path.join(HERE, "avis-valides.json")
    valides = {}
    if os.path.exists(p_valides):
        valides = {int(x["id"]): (x["texte"].strip(), bool(x.get("force"))) for x in json.load(open(p_valides, encoding="utf-8"))}
    p_ecartes = os.path.join(HERE, "avis-ecartes.json")
    ecartes = {int(i) for i in json.load(open(p_ecartes, encoding="utf-8"))} if os.path.exists(p_ecartes) else set()
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    public, relire = construire(rows, envoyees, valides, deny, now, ecartes)
    ecrire(a.out, public)
    ecrire(a.relire, relire)
    if a.resume:  # sans le texte des commentaires : seul fichier destine a sortir du serveur (notification)
        ecrire(a.resume, {"genere_le": now.strftime("%Y-%m-%d"), "en_attente": [
            {"id": x["id"], "mois": x["mois"], "note": x["note"], "alertes": x["alertes"]} for x in relire]})
    print(f"{a.out} : {public['reponses']} reponses, {len(public['avis'])} avis publies, {len(relire)} a relire")


if __name__ == "__main__":
    main()
