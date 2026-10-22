#!/usr/bin/env python3
"""Previent Thomas quand des commentaires de satisfaction attendent une relecture (a lancer sur Nestor).

Entree : le resume produit par satisfaction_json.py --resume (ids, mois, note, alertes : JAMAIS le texte des commentaires).
Sorties :
- Telegram + mail, une seule fois par avis (etat des ids deja signales) ;
- fragment HTML pour le rapport quotidien (section EXTRA), present tant qu'un avis attend, supprime sinon.
Meme mecanique que /opt/gsc-gigarun/gsc-hebdo.py. Bibliotheque standard uniquement.
Usage : notifier.py --resume fichier.json|-  [--dry-run]
"""
import argparse, html, json, os, subprocess, sys, urllib.request
from email.message import EmailMessage

CSS = ("body{font-family:Arial,sans-serif;font-size:14px;color:#333}h2{color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:5px}"
       "table{border-collapse:collapse;width:100%;margin-bottom:16px}th{background:#3498db;color:#fff;padding:8px;text-align:left}"
       "td{padding:7px 10px;border-bottom:1px solid #eee}")


def fragment(attente):
    lignes = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s / 5</td><td>%s</td></tr>" % (
            x["id"], html.escape(x["mois"]), x["note"], html.escape(", ".join(x["alertes"]) or "aucune"))
        for x in attente)
    return ("<h2>💬 Avis clients à relire (support)</h2><table><tr><th>N°</th><th>Mois</th><th>Note</th><th>Alertes du filtre</th></tr>%s</table>"
            "<p>Dites à Claude lesquels publier (ou écarter) : il met à jour <code>ops/satisfaction/avis-valides.json</code> du dépôt gigarun-site.</p>") % lignes


def telegram(env, texte):
    cfg = dict(l.strip().split("=", 1) for l in open(env, encoding="utf-8") if "=" in l and not l.startswith("#"))
    req = urllib.request.Request("https://api.telegram.org/bot%s/sendMessage" % cfg["TELEGRAM_BOT_TOKEN"],
                                 data=json.dumps({"chat_id": cfg["TELEGRAM_CHAT_ID"], "text": texte}).encode(),
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=30).read()


def mail(dest, sujet, frag):
    corps = "<html><head><meta charset='UTF-8'><style>%s</style></head><body>%s<p style='font-size:12px;color:#999'>Généré par Nestor - GiGaRuN</p></body></html>\n" % (CSS, frag)
    m = EmailMessage()
    m["To"], m["Subject"] = dest, sujet
    m.set_content(corps, subtype="html", charset="utf-8", cte="base64")
    subprocess.run(["/usr/sbin/sendmail", "-t"], input=m.as_bytes(), check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", required=True, help="fichier JSON ou - pour stdin")
    ap.add_argument("--etat", default="/var/lib/gigarun-report/satisfaction-etat.json")
    ap.add_argument("--out", default="/var/lib/gigarun-report/satisfaction.html")
    ap.add_argument("--telegram-env", default="/home/tca/exocortex/credentials/telegram.env")
    ap.add_argument("--mail", default="thomas@gigarun.eu")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    data = json.load(sys.stdin if a.resume == "-" else open(a.resume, encoding="utf-8"))
    attente = data["en_attente"]
    deja = set(json.load(open(a.etat))["notifies"]) if os.path.exists(a.etat) else set()
    nouveaux = [x for x in attente if x["id"] not in deja]
    frag = fragment(attente) if attente else ""
    tg = "Support : %d nouveau(x) commentaire(s) client à relire avant publication (n° %s). Dis-moi lesquels publier ou écarter." % (
        len(nouveaux), ", ".join(str(x["id"]) for x in nouveaux))
    if a.dry_run:
        print("nouveaux:", [x["id"] for x in nouveaux], "| attente:", len(attente))
        print(tg if nouveaux else "(pas de notification)")
        print(frag or "(pas de fragment : le fichier serait supprime)")
        return
    if frag:
        open(a.out, "w", encoding="utf-8").write(frag)
    elif os.path.exists(a.out):
        os.remove(a.out)
    if nouveaux:
        erreurs = []
        for nom, f in (("telegram", lambda: telegram(a.telegram_env, tg)),
                       ("mail", lambda: mail(a.mail, "[Support] %d avis client à relire" % len(nouveaux), frag))):
            try:
                f()
            except Exception as e:
                erreurs.append("%s: %s" % (nom, e))
        if erreurs:  # l'etat n'est pas mis a jour : la notification sera retentee au prochain passage
            print("ERREURS " + " | ".join(erreurs), file=sys.stderr)
            sys.exit(1)
    json.dump({"notifies": sorted(deja | {x["id"] for x in attente})}, open(a.etat, "w"))
    print("ok", len(attente), "en attente,", len(nouveaux), "nouveau(x)")


if __name__ == "__main__":
    main()
