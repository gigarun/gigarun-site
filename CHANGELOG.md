# Changelog — gigarun-site

Historique des évolutions du site gigarun.re. Format libre, une entrée par changement notable
(pas les correctifs de typo ou de style mineurs).

## [1.7.0] — 2026-09-12
- Vrais 301 HTTP (Traefik, côté prod) pour 85 des 153 redirections legacy Joomla — remplace le
  meta-refresh Astro pour les URLs sans accent. 68 URLs accentuées exclues (cassaient la réponse
  HTTP côté Traefik, cause non identifiée, rollback fait) — restent sur le fallback existant,
  sans régression. Script : `ops/redirects/gen-traefik-redirects.py`.

## [1.6.3] — 2026-09-12
- Mode clair : la classe Tailwind standard `text-white` (312 occurrences, hors syntaxe crochets
  déjà couverte) n'était pas mappée — texte invisible sur fond clair (repéré sur le bloc
  « Travaillons ensemble » de `/a-propos`, probablement ailleurs aussi). Couverte.
- Vérification systématique : accueil, 42 guides, 43 articles, `/reseau`, `/nestor`,
  `/a-propos` passés en revue (grep exhaustif de toutes les classes couleur + captures d'écran).

## [1.6.2] — 2026-09-12
- Mode clair : bandeau titre des 42 guides illisible (fond sombre en `style=` inline, pas une
  classe Tailwind, donc pas couvert par les règles précédentes). Classe `guide-hero-dark`
  ajoutée pour le cibler, même traitement que le hero (reste sombre, texte clair).

## [1.6.1] — 2026-09-12
- Mode clair : les témoignages (et autres textes en `rgba()` plutôt qu'en hex) restaient
  illisibles — couverture étendue aux variantes `rgba(241,240,247,*)`, `rgba(255,255,255,*)`,
  `rgba(155,153,170,*)` et à quelques couleurs d'accent restées non couvertes (pages
  réseau/cloud/solutions/nestor/infogérance-contrats).
- Lien « Voir nos avis sur Google » corrigé : l'ancien slug `gigarun+ingénierie` ne résolvait
  plus (fiche renommée « gigarun » côté Google, même place_id) — mis à jour vers l'URL qui
  résout réellement.

## [1.6.0] — 2026-09-12
- Toggle « Mode clair » ajouté au panneau accessibilité (même mécanisme que le contraste élevé
  existant). Redéfinit les ~15 classes Tailwind en dur les plus utilisées (texte/fond) via
  sélecteur d'attribut CSS, sans toucher aux ~150 fichiers de pages ni au widget lui-même.
  Bordures/overlays translucides (rgba) non retouchés.

## [1.5.0] — 2026-09-12
- Bloc « Services associés » ajouté sur les 42 guides techniques (lien vers 1-2 pages de
  service pertinentes chacun) — même mécanisme que les 43 articles de blog, absent des guides
  jusqu'ici.

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
