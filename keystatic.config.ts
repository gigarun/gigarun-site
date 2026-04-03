import { config, fields, singleton, collection } from '@keystatic/core';

export default config({
  storage: {
    kind: 'local',
  },
  ui: {
    brand: {
      name: 'Gigarun CMS',
    },
  },
  singletons: {
    hero: singleton({
      label: 'Page d\'accueil — Hero',
      path: 'src/content/hero/',
      schema: {
        badge: fields.text({ label: 'Badge (ex: La Réunion · DSI Externalisé)' }),
        titre_ligne1: fields.text({ label: 'Titre ligne 1' }),
        titre_ligne2: fields.text({ label: 'Titre ligne 2 (accentué)' }),
        sous_titre: fields.text({ label: 'Sous-titre', multiline: true }),
        cta_principal: fields.text({ label: 'Bouton principal' }),
        cta_secondaire: fields.text({ label: 'Bouton secondaire' }),
        stat1_chiffre: fields.text({ label: 'Stat 1 — Chiffre (ex: 15+)' }),
        stat1_label: fields.text({ label: 'Stat 1 — Label (ex: Années d\'expérience)' }),
        stat2_chiffre: fields.text({ label: 'Stat 2 — Chiffre' }),
        stat2_label: fields.text({ label: 'Stat 2 — Label' }),
        stat3_chiffre: fields.text({ label: 'Stat 3 — Chiffre' }),
        stat3_label: fields.text({ label: 'Stat 3 — Label' }),
        stat4_chiffre: fields.text({ label: 'Stat 4 — Chiffre' }),
        stat4_label: fields.text({ label: 'Stat 4 — Label' }),
      },
    }),
    contact: singleton({
      label: 'Informations de contact',
      path: 'src/content/contact/',
      schema: {
        telephone: fields.text({ label: 'Téléphone' }),
        email: fields.text({ label: 'Email' }),
        adresse: fields.text({ label: 'Adresse' }),
      },
    }),
  },
  collections: {
    services: collection({
      label: 'Services',
      path: 'src/content/services/*',
      schema: {
        titre: fields.text({ label: 'Titre du service' }),
        description: fields.text({ label: 'Description courte', multiline: true }),
        ordre: fields.integer({ label: 'Ordre d\'affichage' }),
      },
    }),
    temoignages: collection({
      label: 'Témoignages clients',
      path: 'src/content/temoignages/*',
      schema: {
        nom: fields.text({ label: 'Nom du client' }),
        entreprise: fields.text({ label: 'Entreprise' }),
        secteur: fields.text({ label: 'Secteur d\'activité' }),
        texte: fields.text({ label: 'Témoignage', multiline: true }),
        note: fields.integer({ label: 'Note /5' }),
      },
    }),
    tarifs: collection({
      label: 'Forfaits',
      path: 'src/content/tarifs/*',
      schema: {
        nom: fields.text({ label: 'Nom de l\'offre' }),
        prix: fields.text({ label: 'Prix (ex: 15€ ou Sur devis)' }),
        sous_titre_prix: fields.text({ label: 'Sous-titre prix (ex: /poste/mois)' }),
        recommande: fields.checkbox({ label: 'Offre recommandée ?' }),
        features: fields.array(
          fields.text({ label: 'Feature' }),
          { label: 'Fonctionnalités incluses', itemLabel: props => props.value }
        ),
        bouton_texte: fields.text({ label: 'Texte du bouton' }),
        ordre: fields.integer({ label: 'Ordre d\'affichage' }),
      },
    }),
  },
});
