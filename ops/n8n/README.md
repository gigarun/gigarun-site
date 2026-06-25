# Backend formulaires — n8n (devis + contact)

Les formulaires du site (calculateurs de devis + contact) sont **statiques** : ils POSTent un JSON
sur un **webhook n8n**. Ce webhook envoie l'email + le PDF de devis, puis (plus tard) crée le prospect
dans Dolibarr.

## 1. Câblage côté site

L'URL du webhook se renseigne via la variable d'environnement **`PUBLIC_FORMS_WEBHOOK`**
(Coolify → Environment, ou `.env` en dev). Tant qu'elle est vide, les formulaires affichent un
succès « gracieux » et loggent le payload en console (aucun envoi).

```
PUBLIC_FORMS_WEBHOOK=https://n8n.gigarun.xxx/webhook/formulaires-gigarun
```

> Décision infra à prendre : sur quelle instance n8n exposer ce webhook public
> (n8n dédié gigarun recommandé, pas l'instance vetilog). Doit être joignable depuis Internet (HTTPS).

## 2. Contrat de payload (ce que le site envoie)

Toujours `POST application/json`. Champ discriminant : `type`.

### `type: "contact"`
```json
{ "type": "contact",
  "contact": { "nom": "...", "coordonnees": "email ou tel", "message": "..." },
  "page": "https://gigarun.re/contact" }
```

### `type: "devis-infogerance"`
```json
{ "type": "devis-infogerance",
  "tier": "or",
  "parc": { "postes": 10, "serveurs": 1, "nas": 1, "peripheriques": 10, "sites": 1 },
  "options": [ { "code": "m365_standard", "label": "...", "prix": 14.65, "qty": 10, "total": 146.5 } ],
  "base_ht": 705, "remise_ht": 0, "engagement_36_mois": false,
  "total_ht_mois": 705, "tva_ht": 59.93, "total_ttc_mois": 764.93,
  "contact": { "societe": "...", "nom": "...", "email": "...", "telephone": "...", "message": "..." },
  "page": "..." }
```

### `type: "devis-erp"`
```json
{ "type": "devis-erp",
  "offre": "Offre avancee - 25 utilisateurs max", "mensuel_ht": 180, "duree_mois": 12,
  "total_ht": 2160, "tva_ht": 183.6, "total_ttc": 2343.6,
  "contact": { "societe": "...", "siret": "...", "nom": "...", "email": "...", "telephone": "...", "message": "..." },
  "page": "..." }
```

## 3. Workflow n8n (design)

`workflow-formulaires-gigarun.json` = squelette importable. Chaîne :

1. **Webhook** (POST `/formulaires-gigarun`, réponse via « Respond to Webhook »).
2. **Switch** sur `{{$json.type}}` → 3 branches (contact / devis-infogerance / devis-erp).
3. **Code** : construit le sujet + le corps HTML récapitulatif (tableau du devis, totaux HT/TVA/TTC).
4. **Email** (SMTP OVH — creds ci-dessous) :
   - notification interne → `contact@gigarun.net`
   - accusé + devis → l'email du prospect (pour les devis).
5. **PDF** (devis uniquement) : HTTP Request vers **Gotenberg** (`/forms/chromium/convert/html`,
   conteneur Docker `gotenberg/gotenberg`) qui transforme l'HTML du devis en PDF, joint à l'email.
   Alternative : node communautaire `n8n-nodes-puppeteer`.
6. **Respond to Webhook** : `{ "ok": true }`.
7. *(Plus tard, non urgent)* **Dolibarr** : HTTP Request `POST /api/index.php/thirdparties`
   puis `/proposals` (token API dans la mémoire `reference_dolibarr_ovh` — NE PAS régénérer, partagé Pennylane).

### Credentials SMTP (déjà en mémoire `reference_smtp_ovh`)
- Hôte `ssl0.ovh.net`, port `465` (SSL), user `contact@gigarun.net`.

## 4. Sécurité
- Le site fait déjà un anti-spam (captcha mathématique) côté client.
- Ajouter côté n8n : vérif `type` connu, rate-limit (n8n ou Caddy/Traefik devant), et idéalement un
  champ honeypot + un secret partagé en header si besoin.

## 5. Reste à décider (Thomas)
- Instance n8n + URL publique du webhook → renseigner `PUBLIC_FORMS_WEBHOOK`.
- PDF : déployer Gotenberg (recommandé) ou puppeteer.
- Dolibarr : activer la création de prospect+devis (phase 2).
