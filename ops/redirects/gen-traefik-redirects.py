import re, hashlib
from urllib.parse import quote

src = open('src/data/legacy-redirects.js', encoding='utf-8').read()
pairs = re.findall(r"^\s*'((?:[^'\\]|\\.)*)':\s*'((?:[^'\\]|\\.)*)',?\s*$", src, re.M)
print('paires trouvees:', len(pairs))


def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


lines = []
lines.append("# Redirections 301 reelles (Traefik) pour les URLs legacy du Joomla.")
lines.append("# Genere depuis src/data/legacy-redirects.js par ops/redirects/gen-traefik-redirects.py")
lines.append("# (source de verite unique). Complete la version Astro statique (meta-refresh) par un")
lines.append("# vrai HTTP 301/308 au niveau du reverse proxy.")
lines.append("#")
lines.append("# IMPORTANT (decouvert le 2026-09-12) : Traefik lit le chemin sous DEUX representations")
lines.append("# differentes selon le contexte -- la regle du routeur (Path()) voit le chemin DECODE")
lines.append("# (Unicode brut, ex: /securite-accentue), alors que le middleware redirectRegex")
lines.append("# reconstruit l'URL complete et la voit PERCENT-ENCODEE (ex: %C3%A9). Utiliser la")
lines.append("# meme representation aux deux endroits casse soit le matching (silencieux, retombe")
lines.append("# sur le fallback Astro), soit la reponse HTTP elle-meme (ERR_HTTP_RESPONSE_CODE_FAILURE)."
             )
lines.append("# D'ou : Path() en Unicode decode, regex en percent-encode. Regenerer ce fichier avec")
lines.append("# gen-traefik-redirects.py si legacy-redirects.js change.")
lines.append("http:")
lines.append("  middlewares:")

seen = set()
router_lines = []
for old, new in pairs:
    slug = hashlib.md5(old.encode()).hexdigest()[:10]
    name = f"legacy-redir-{slug}"
    if name in seen:
        continue
    seen.add(name)
    target = new if new.startswith("http") else f"https://gigarun.re{new}"
    old_enc = quote(old, safe='/-_.~,')
    regex = "^https://gigarun\\.re" + re.escape(old_enc) + "/?$"
    lines.append(f"    {name}:")
    lines.append("      redirectRegex:")
    lines.append(f"        regex: {yaml_str(regex)}")
    lines.append(f"        replacement: {yaml_str(target)}")
    lines.append("        permanent: true")

    rule = "Host(`gigarun.re`) && Path(`" + old + "`)"
    router_lines.append(f"    {name}:")
    router_lines.append("      entryPoints:")
    router_lines.append("        - https")
    router_lines.append(f"      rule: {yaml_str(rule)}")
    router_lines.append("      middlewares:")
    router_lines.append(f"        - {name}")
    router_lines.append("      service: noop@internal")
    router_lines.append("      priority: 100")
    router_lines.append("      tls:")
    router_lines.append("        certresolver: letsencrypt")

lines.append("  routers:")
lines.extend(router_lines)

out = "\n".join(lines) + "\n"
open("/tmp/legacy-redirects-traefik-final.yaml", "w", encoding="utf-8").write(out)
print("routers generes:", len(seen))
