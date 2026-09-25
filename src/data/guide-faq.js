// FAQ affichées en fin de guide (composant GuideFaq.astro) et publiées en JSON-LD FAQPage.
// Chaque réponse renvoie aux sections réelles du guide : ne rien promettre qu'il ne contient pas.
export const GUIDE_FAQ = {
  'guide-mfa-microsoft-authenticator': [
    { q: 'Pourquoi activer la MFA sur Microsoft 365 ?',
      a: "Un mot de passe seul peut être volé, deviné ou réutilisé sur un autre site. Avec la MFA, un second facteur est demandé, par exemple une approbation sur votre téléphone : un mot de passe dérobé ne suffit plus pour ouvrir votre compte." },
    { q: "Faut-il obligatoirement l'application Microsoft Authenticator ?",
      a: "Non, d'autres méthodes existent (voir la section « Méthodes alternatives » de ce guide). L'application reste la plus simple au quotidien : une approbation en un geste, sans recopier de code." },
    { q: 'Que faire si je change de téléphone ?',
      a: "Préparez le changement avant de vous séparer de l'ancien téléphone : la section « Changer de téléphone » décrit la marche à suivre. Si vous n'y avez plus accès, demandez à votre administrateur de réinitialiser vos méthodes d'authentification." },
    { q: 'Comment savoir si mon entreprise est correctement protégée ?',
      a: "La MFA est une première protection essentielle mais pas la seule. Notre diagnostic gratuit examine l'exposition publique de votre nom de domaine, et un audit permet d'aller plus loin." },
  ],
  'guide-restauration-fichiers': [
    { q: 'Comment récupérer un fichier supprimé par erreur ?',
      a: "Cela dépend de l'endroit où se trouvait le fichier : corbeille Windows, corbeille OneDrive, historique des versions, corbeille SharePoint ou Teams, ou e-mail supprimé. Ce guide vous fait choisir la bonne méthode selon votre cas." },
    { q: "Combien de temps un fichier supprimé reste-t-il récupérable ?",
      a: "Le délai dépend de la méthode et de votre abonnement : la section « Récapitulatif des délais » les rassemble. Plus vous agissez tôt, plus vos chances de récupération sont grandes." },
    { q: "Et si le fichier n'est dans aucune corbeille ?",
      a: "La corbeille n'est pas une sauvegarde. Si le fichier n'apparaît nulle part, seule une vraie sauvegarde de vos données peut le restaurer : vérifiez que Microsoft 365 et vos serveurs sont bien sauvegardés." },
  ],
  'guide-ia-pour-pme': [
    { q: "L'IA est-elle utile pour une petite entreprise ?",
      a: "Oui pour les tâches répétitives (rédaction, synthèse, tri d'informations), à condition de partir d'un cas d'usage précis et de garder une relecture humaine. Ce guide détaille des cas d'usage concrets et un plan d'action pour démarrer." },
    { q: 'Puis-je confier des données clients à un outil comme ChatGPT ?',
      a: "Pas sans précautions : des données personnelles ou confidentielles saisies dans un outil grand public peuvent vous exposer. Voir la section « Sécurité & confidentialité » ; privilégiez des comptes professionnels et un cadre d'usage écrit." },
    { q: "Par quel outil commencer ?",
      a: "Si vous utilisez déjà Microsoft 365, Microsoft Copilot est une porte d'entrée naturelle (section « Commencer avec Microsoft Copilot »). L'important est de tester un cas d'usage à petite échelle avant de généraliser." },
    { q: "Existe-t-il une IA qui reste chez moi, sans envoyer de données à l'extérieur ?",
      a: "Oui : une IA hébergée dans vos locaux ou chez un hébergeur de confiance, comme notre solution Nestor. Contactez-nous pour voir si elle correspond à votre besoin." },
  ],
  'guide-bonnes-pratiques-onedrive': [
    { q: 'Pourquoi partager un lien OneDrive plutôt qu’envoyer une pièce jointe ?',
      a: "Un lien évite de multiplier les copies d'un fichier, permet de choisir qui peut le consulter ou le modifier, et de retirer l'accès ensuite (section « Gérer et révoquer les partages »)." },
    { q: 'Comment choisir les bons droits de partage ?',
      a: "Donnez le droit minimum nécessaire (lecture seule si la personne n'a pas besoin de modifier). La section « Paramètres de partage : choisir les bons droits » explique les options une par une." },
    { q: "OneDrive ne se synchronise pas correctement, que faire ?",
      a: "La section « Dépannage » de ce guide recense les cas courants. Si le problème persiste, notre équipe peut intervenir." },
  ],
  'guide-stockage-fichiers-teams-share-point-one-drive': [
    { q: 'Où sont stockés les fichiers partagés dans Microsoft Teams ?',
      a: "Les fichiers d'un canal standard sont stockés dans un site SharePoint, ceux des canaux privés ont leur propre espace, et ceux des conversations privées (chats) sont dans le OneDrive de la personne qui les a envoyés." },
    { q: "Comment accéder au site SharePoint d'un canal Teams ?",
      a: "Le guide décrit deux méthodes dans la section « Comment accéder au site SharePoint d'un canal »." },
    { q: 'Quelle différence entre SharePoint et OneDrive dans Teams ?',
      a: "SharePoint sert au stockage partagé des équipes et des canaux, OneDrive au stockage personnel de chacun. Le « Comparatif rapide » de ce guide résume où va chaque type de fichier." },
  ],
};
