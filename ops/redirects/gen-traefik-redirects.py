import re, hashlib

src = open('src/data/legacy-redirects.js', encoding='utf-8').read()
pairs = re.findall(r"^\s*'((?:[^'\\]|\\.)*)':\s*'((?:[^'\\]|\\.)*)',?\s*$", src, re.M)

ascii_pairs = [(o, n) for o, n in pairs if o.isascii() and n.isascii()]
skipped = [(o, n) for o, n in pairs if not (o.isascii() and n.isascii())]
print('total:', len(pairs), 'ascii:', len(ascii_pairs), 'exclues (accents):', len(skipped))


def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


lines = []
lines.append("# Redirections 301 reelles (Traefik) pour les URLs legacy du Joomla.")
lines.append("# Genere depuis src/data/legacy-redirects.js -- SOUS-ENSEMBLE ASCII UNIQUEMENT.")
lines.append("# Les entrees avec caracteres accentues sont volontairement exclues : elles cassaient la")
lines.append("# reponse HTTP (ERR_HTTP_RESPONSE_CODE_FAILURE sur navigateur reel) quand testees le 2026-09-12.")
lines.append("# Cause exacte non identifiee (rollback de securite fait, pas de nouvelle tentative sans")
lines.append("# comprendre). Ces URLs restent sur le fallback Astro meta-refresh existant, fonctionnel.")
lines.append("# Regenerer avec gen_traefik_redirects_ascii.py si legacy-redirects.js change.")
lines.append("http:")
lines.append("  middlewares:")

seen = set()
router_lines = []
for old, new in ascii_pairs:
    slug = hashlib.md5(old.encode()).hexdigest()[:10]
    name = f"legacy-redir-{slug}"
    if name in seen:
        continue
    seen.add(name)
    target = new if new.startswith("http") else f"https://gigarun.re{new}"
    regex = "^https://gigarun\\.re" + re.escape(old) + "/?$"
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
open("/tmp/legacy-redirects-traefik-ascii.yaml", "w", encoding="utf-8").write(out)
print("routers generes:", len(seen))

with open("/tmp/skipped-accented-redirects.txt", "w", encoding="utf-8") as f:
    for o, n in skipped:
        f.write(f"{o} -> {n}\n")
print("liste des exclues ecrite dans /tmp/skipped-accented-redirects.txt")
