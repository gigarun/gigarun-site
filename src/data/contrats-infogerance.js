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
    descLongue: "Supervision proactive du réseau, des postes et des applications pour anticiper les incidents, télémaintenance pour l'administration complète du parc, plateforme de suivi transparente des interventions et support technique réactif à distance. Les interventions physiques restent rares et exceptionnelles : elles sont facturées au tarif horaire ou prises en charge par votre équipe interne. Ce niveau convient si vous disposez déjà d'un référent technique capable d'intervenir sur site — GiGaRuN le guide à distance lors des opérations qui l'exigent.",
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
    descLongue: "Reprend l'intégralité du socle Bronze et y ajoute les interventions et la maintenance préventive sur site, sans limite de nombre, main d'œuvre et déplacements inclus. GiGaRuN prend alors en charge 100% de la maintenance et de l'infogérance du parc, en lien avec votre référent technique interne informé des opérations terminées et en cours. Ce niveau convient si vous ne disposez pas en interne d'une personne capable d'intervenir physiquement.",
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
    descLongue: "Reprend l'intégralité du socle Argent et ajoute le remplacement des pièces défectueuses (hors consommables), la gestion et la supervision du réseau — périphériques, mobilité, GSM, sécurisation BYOD à la demande — ainsi qu'une DSI externalisée en charge de la gouvernance des prestataires, des domaines et des messageries. Ce niveau convient si vous voulez externaliser en totalité l'infogérance, la maintenance et le pilotage stratégique de votre SI.",
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
    descLongue: "Reprend l'intégralité du socle Or et ajoute un RSSI externalisé rattaché à la direction générale de l'entreprise, avec Extended Detection and Response (XDR) + SIEM, chiffrement des postes, contrôle RGPD des données et reporting avancé, complété d'une option SOC en cyberdéfense active 24/7/365. Le forfait inclut aussi des sessions de sensibilisation du personnel, des tests d'intrusion et des audits d'infrastructure — le RSSI n'est pas limité à l'informatique : l'organisation, les ressources humaines et la sécurité physique entrent aussi dans la gestion des risques.",
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
