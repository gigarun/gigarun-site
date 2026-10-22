#!/usr/bin/env bash
# Mise a jour hebdomadaire des stats de satisfaction du site (page /support-infogerance/).
# Cron (tca@10.0.0.82) : cd ~/gigarun-satisfaction && git pull -q --ff-only && ops/satisfaction/run.sh
# Lit HESK en lecture seule, ecrit src/data/satisfaction.json, commit + push (le dev se redeploie seul).
# Le deploiement PROD n'a lieu que si SAT_DEPLOY_PROD=1 dans ~/.gigarun-secrets/satisfaction.env.
set -euo pipefail
cd "$(dirname "$0")/../.."
ENV=~/.gigarun-secrets/satisfaction.env
OUT=src/data/satisfaction.json

python3 ops/satisfaction/satisfaction_json.py --env "$ENV" --out "$OUT" \
  --relire ~/.gigarun-satisfaction-a-relire.json   # texte brut des commentaires : hors depot

if git diff --quiet -- "$OUT"; then echo "$(date -Is) inchange"; exit 0; fi
git add "$OUT"
git commit -q -m "data: statistiques de satisfaction (mise a jour automatique)" -- "$OUT"
git push -q origin HEAD:main
echo "$(date -Is) pousse $(git log -1 --format=%h)"

if grep -q '^SAT_DEPLOY_PROD=1' "$ENV"; then ops/deploy-prod.sh; fi
