// Source unique des 4 niveaux d'infogérance (Bronze -> Platine).
// Utilisé par /infogerance-contrats (détail) ET la home (teaser) pour ne jamais diverger.
// Rappel 2026-09-09 : la home affichait avant des tarifs "Essentiel/Business/Premium"
// fictifs, sans rapport avec cette grille réelle -> plus jamais deux sources de vérité.
export const CONTRATS = [
  {
    code: "bronze", nom: "BRONZE", couleur: "#CD7F32",
    bg: "rgba(205,127,50,0.08)", border: "rgba(205,127,50,0.25)",
    prix: "dès 25€", unite: "/poste/mois",
    desc: "L'essentiel à distance pour l'entreprise déjà équipée : on surveille et on épaule votre informatique interne.",
    socle: null,
    features: [
      "Monitoring & supervision des équipements",
      "Support & assistance à distance",
      "Mises à jour de sécurité",
      "Rapport d'activité",
    ],
    recommande: false,
  },
  {
    code: "argent", nom: "ARGENT", couleur: "#9B9B9B",
    bg: "rgba(155,155,155,0.08)", border: "rgba(155,155,155,0.25)",
    prix: "dès 30€", unite: "/poste/mois",
    desc: "On ajoute le terrain : interventions et maintenance sur site, déplacements inclus.",
    socle: "Tout BRONZE, plus :",
    features: [
      "Interventions sur site",
      "Maintenance préventive sur site",
      "Supervision des sauvegardes",
      "Main d'œuvre & déplacements inclus",
    ],
    recommande: false,
  },
  {
    code: "or", nom: "OR", couleur: "#FFD700",
    bg: "rgba(255,215,0,0.08)", border: "rgba(255,215,0,0.35)",
    prix: "dès 35€", unite: "/poste/mois",
    desc: "La couverture complète avec pilotage : pièces, réseau et DSI externalisée.",
    socle: "Tout ARGENT, plus :",
    features: [
      "Pièces défectueuses remplacées",
      "Gestion réseau, périphériques & GSM",
      "DSI externalisée",
      "Support prioritaire",
    ],
    recommande: true,
  },
  {
    code: "platine", nom: "PLATINE", couleur: "#E5E4E2",
    bg: "rgba(229,228,226,0.06)", border: "rgba(229,228,226,0.3)",
    prix: "dès 40€", unite: "/poste/mois",
    desc: "Le niveau maximal, orienté sécurité et conformité : RSSI et XDR/SIEM inclus.",
    socle: "Tout OR, plus :",
    features: [
      "RSSI externalisé",
      "XDR + SIEM inclus (postes, serveurs, NAS)",
      "SOC / cyberdéfense 24/7 (option)",
      "Conformité NIS2 accompagnée",
    ],
    recommande: false,
  },
];
