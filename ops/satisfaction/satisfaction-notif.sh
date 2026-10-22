#!/bin/bash
# Tire le resume des avis a relire depuis tca@10.0.0.82 (cle restreinte : commande forcee, lecture seule du resume) puis notifie.
# Cron : /etc/cron.d/satisfaction-notif, 03:40 UTC, juste avant le rapport quotidien de 04:00 UTC.
set -euo pipefail
R=$(ssh -i /root/.ssh/satisfaction-82 -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=15 tca@10.0.0.82 resume)
printf '%s' "$R" | /opt/satisfaction-notif/notifier.py --resume -
