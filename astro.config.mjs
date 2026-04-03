import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import node from '@astrojs/node';
import react from '@astrojs/react';
import keystatic from '@keystatic/astro';

export default defineConfig({
  output: 'server',
  site: 'http://gigarun.local',
  adapter: node({
    mode: 'standalone',
    trustProxy: true,
  }),
  integrations: [react(), keystatic()],
  vite: {
    plugins: [tailwindcss()],
    preview: {
      allowedHosts: ['gigarun.local', 'localhost'],
    },
  },
});
