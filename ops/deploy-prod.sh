#!/usr/bin/env bash
# Deploiement prod complet de gigarun.re : Coolify -> attente de fin -> purge du cache Cloudflare.
# A lancer depuis tca@10.0.0.82 (les deux fichiers de secrets y sont). Le webhook GitHub ne deploie QUE le dev.
# La purge est indispensable : le HTML est mis en cache 1 h chez Cloudflare (regle "Cache Rules").
set -euo pipefail
source ~/.gigarun-secrets/coolify-prod.env
set -a; source ~/.gigarun-secrets/cloudflare.env; set +a
ZONE=d8bd99d9e0779ea27319e74061000514
APP=1gxs3w0apyf0fquezj8ovh4e
api() { python3 -c "import json,sys; print(json.load(sys.stdin)$1)"; }

dep=$(curl -s -X POST -H "Authorization: Bearer $COOLIFY_TOKEN" "$COOLIFY_URL/api/v1/deploy?uuid=$APP" | api "['deployments'][0]['deployment_uuid']")
echo "deploiement en file: $dep"

st=""
for _ in $(seq 1 72); do
  st=$(curl -s -H "Authorization: Bearer $COOLIFY_TOKEN" "$COOLIFY_URL/api/v1/deployments/$dep" | api ".get('status','')")
  [ "$st" = finished ] && break
  case "$st" in failed|cancelled*) echo "ECHEC du deploiement (statut: $st)"; exit 1;; esac
  sleep 5
done
[ "$st" = finished ] || { echo "delai depasse (statut: $st)"; exit 1; }
sleep 5  # laisse Traefik basculer sur le nouveau conteneur

curl -s -X POST -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  --data '{"purge_everything":true}' "https://api.cloudflare.com/client/v4/zones/$ZONE/purge_cache" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('purge cache Cloudflare:', 'ok' if d.get('success') else d)"
echo "termine. Option : python3 ops/indexnow/submit.py"
