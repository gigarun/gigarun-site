#!/usr/bin/env bash
# Filet apres un Redeploy fait depuis le dashboard Coolify (qui ne purge pas Cloudflare et ne previent pas IndexNow).
# Cron toutes les 5 min sur tca@10.0.0.82 : si le dernier deploiement de gigarun-site est "finished" et pas encore traite,
# purge le cache Cloudflare puis soumet le sitemap a IndexNow. ops/deploy-prod.sh note son deploiement dans le meme fichier
# d'etat pour ne pas etre double. Idempotent : un doublon ne coute rien.
set -euo pipefail
cd "$(dirname "$0")/.."
exec 9>/tmp/gigarun-post-deploy.lock; flock -n 9 || exit 0
source ~/.gigarun-secrets/coolify-prod.env
set -a; source ~/.gigarun-secrets/cloudflare.env; set +a
ZONE=d8bd99d9e0779ea27319e74061000514
APP=1gxs3w0apyf0fquezj8ovh4e
STATE=~/.gigarun-last-deploy

read -r uuid st < <(curl -s --max-time 20 -H "Authorization: Bearer $COOLIFY_TOKEN" "$COOLIFY_URL/api/v1/deployments/applications/$APP?skip=0&take=1" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); d=d if isinstance(d,list) else d['deployments']; print(d[0]['deployment_uuid'], d[0]['status'])")
[ "$uuid" = "$(cat "$STATE" 2>/dev/null)" ] && exit 0
case "$st" in
  finished) ;;
  failed|cancelled*) echo "$(date -Is) $uuid $st : ignore"; echo "$uuid" > "$STATE"; exit 0;;
  *) exit 0;;   # en file / en cours : on repasse dans 5 min
esac

sleep 5  # laisse Traefik basculer sur le nouveau conteneur
curl -s -X POST -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  --data '{"purge_everything":true}' "https://api.cloudflare.com/client/v4/zones/$ZONE/purge_cache" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('purge Cloudflare:', 'ok' if d.get('success') else d)"
python3 ops/indexnow/submit.py
echo "$uuid" > "$STATE"
echo "$(date -Is) $uuid traite"
