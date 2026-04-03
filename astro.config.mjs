// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  output: 'static',
  server: {
    host: '0.0.0.0',
  },
  vite: {
    preview: {
      allowedHosts: ['gigarun.local', 'localhost'],
    },

    plugins: [tailwindcss()],
  },
});