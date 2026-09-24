import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import { LEGACY_REDIRECTS } from './src/data/legacy-redirects.js';

export default defineConfig({
  site: 'https://gigarun.re',
  output: 'static',
  redirects: LEGACY_REDIRECTS,
  integrations: [
    sitemap(),
  ],
  vite: {
    plugins: [tailwindcss()],
    preview: {
      allowedHosts: true,
    },
  },
});
