# Changelog — gigarun-site

Historique des évolutions du site gigarun.re. Format libre, une entrée par changement notable
(pas les correctifs de typo ou de style mineurs).

## [1.4.0] — 2026-09-12
- Google Rich Results Test passé sur un guide (TechArticle) : schema valide, 5 problèmes non
  critiques remontés (dates sans heure/fuseau, champ `image` absent). Corrigés sur les 43
  articles + 42 guides : `datePublished`/`dateModified` en ISO 8601 complet (+04:00, heure La
  Réunion), `image` ajouté (og-default.png).

## [1.3.1] — 2026-09-12
- Badge hero : "La Réunion · DSI Externalisé" → "La Réunion · DSI Externalisé · Infogérant".

## [1.3.0] — 2026-09-12
- Numéro de version affiché en pied de page (lien discret, cohérent avec ce fichier).
- Ce fichier créé (rétroactif pour 1.0.0 à 1.2.0).

## [1.2.0] — 2026-09-12
- Schema `TechArticle` (schema.org) ajouté sur les 42 guides techniques : headline/description
  repris du contenu existant, auteur Thomas Cassen, `datePublished`/`dateModified` = dates
  réelles des fichiers sources OneDrive.

## [1.1.0] — 2026-09-12
- `knowsAbout` ajouté au schema `ProfessionalService` (entités : infogérance, cybersécurité,
  DSI partagée, développement web, cloud, sauvegarde/PRA).
- Auteur des 43 articles de blog : `Organization` anonyme → `Person` Thomas Cassen (E-E-A-T).

## [1.0.0] — 2026-09-10
- Cutover DNS : gigarun.re sert le nouveau site Astro en production (remplace le Joomla
  compromis). 141 URLs migrées, 153 redirections legacy, sitemap resoumis Search Console.
- Formulaires (contact, devis) opérationnels via webhook n8n.
- Fix bandeau cookies / boutons flottants sur mobile (z-index).

<!-- Ajouter les nouvelles entrées EN HAUT (plus récent en premier), format [version] — date. -->
