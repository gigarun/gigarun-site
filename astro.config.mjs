import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://gigarun.re',
  output: 'static',
  integrations: [
    sitemap({
      // Exclut les pages légales/utilitaires sans valeur SEO
      filter: (page) =>
        !/\/(cgl|cgv|confidentialite|mentions-legales|politique-de-divulgation-responsable|fiche-sav)\/?$/.test(page),
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
    preview: {
      allowedHosts: true,
    },
  },
});
