// Pages à ne pas indexer : guides d'exploitation internes (outils, infrastructure, stack de GiGaRuN).
// Elles restent accessibles par leur lien et utiles à l'équipe, mais ne doivent ni apparaître dans Google ni
// diluer le sujet du site (TPE/PME réunionnaises). Utilisé par Layout.astro (meta robots) et astro.config.mjs (sitemap).
export const NOINDEX_PATHS = new Set([
  '/guides/exocortex/',
  '/guides/guide-exocortex-bootstrap/',
  '/guides/guide-exocortex-copilote-metier/',
  '/guides/guide-exocortex-sync-multimachine/',
  '/guides/guide-coolify-astro-directus/',
  '/guides/guide-coolify-astro-strapi/',
  '/guides/guide-deploiement-agent-zabbix/',
  '/guides/guide-deploiement-dolibarr23/',
  '/guides/guide-github-claude-code/',
  '/guides/guide-github-desktop/',
  '/guides/guide-maitrise-claude-code/',
  '/guides/guide-multiagent-ollama/',
  '/guides/guide-virtualhosts-virtualmin-dolibarr/',
  '/guides/guide-backup-restic-dolibarr/',
  '/guides/guide-rustdesk-service/',
]);
