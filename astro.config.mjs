import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import react from '@astrojs/react';
import writenex from '@writenex/astro';

export default defineConfig({
  output: 'static',
  integrations: [react(), writenex()],
  vite: {
    plugins: [tailwindcss()],
    server: {
      allowedHosts: ['gigarun.local', 'localhost'],
    },
    preview: {
      allowedHosts: ['gigarun.local', 'localhost'],
    },
  },
});
