import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import { LEGACY_REDIRECTS } from './src/data/legacy-redirects.js';
import { NOINDEX_PATHS } from './src/data/noindex-paths.js';

export default defineConfig({
  site: 'https://gigarun.re',
  output: 'static',
  redirects: LEGACY_REDIRECTS,
  integrations: [
    sitemap({ filter: (page) => !NOINDEX_PATHS.has(new URL(page).pathname.replace(/\/?$/, '/')) }),
  ],
  vite: {
    plugins: [tailwindcss()],
    preview: {
      allowedHosts: true,
    },
  },
});
