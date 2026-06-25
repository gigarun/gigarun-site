// Configuration des formulaires (devis + contact).
// Le webhook n8n reçoit les soumissions (email + PDF, puis Dolibarr).
// Renseigner PUBLIC_FORMS_WEBHOOK dans les variables d'environnement Coolify
// quand l'instance n8n et l'URL publique sont décidées.
export const FORMS_WEBHOOK: string = import.meta.env.PUBLIC_FORMS_WEBHOOK || '';

// TVA La Réunion (les prix catalogue sont HT).
export const TVA_REUNION = 0.085;
