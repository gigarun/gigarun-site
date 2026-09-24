#!/usr/bin/env python3
"""Soumet les URLs du site a IndexNow (Bing, Yandex, Naver, Seznam).
Usage (depuis la racine du repo, apres un deploiement prod) :
  python3 ops/indexnow/submit.py            # toutes les URLs du sitemap
  python3 ops/indexnow/submit.py URL [URL]  # seulement ces URLs
La cle est le fichier public/<32 hex>.txt (public par conception d IndexNow)."""
import glob, json, re, sys, urllib.request

HOST = "gigarun.re"
keys = [re.search(r"([0-9a-f]{32})\.txt$", f).group(1) for f in glob.glob("public/*.txt") if re.search(r"/[0-9a-f]{32}\.txt$", f)]
assert len(keys) == 1, "il faut exactement une cle public/<32 hex>.txt"
key = keys[0]
urls = sys.argv[1:] or re.findall(r"<loc>([^<]+)</loc>", urllib.request.urlopen(f"https://{HOST}/sitemap-0.xml").read().decode())
body = json.dumps({"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", body, {"Content-Type": "application/json; charset=utf-8"})
print(len(urls), "URLs soumises ->", urllib.request.urlopen(req).status)
