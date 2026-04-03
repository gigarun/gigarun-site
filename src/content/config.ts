import { defineCollection, z } from 'astro:content';

const services = defineCollection({
  type: 'data',
  schema: z.object({
    titre: z.string(),
    description: z.string(),
    ordre: z.number(),
  }),
});

const tarifs = defineCollection({
  type: 'data',
  schema: z.object({
    nom: z.string(),
    prix: z.string(),
    sous_titre_prix: z.string(),
    recommande: z.boolean(),
    features: z.array(z.string()),
    bouton_texte: z.string(),
    ordre: z.number(),
  }),
});

const temoignages = defineCollection({
  type: 'data',
  schema: z.object({
    nom: z.string(),
    entreprise: z.string(),
    secteur: z.string(),
    texte: z.string(),
    note: z.number(),
  }),
});

export const collections = { services, tarifs, temoignages };
