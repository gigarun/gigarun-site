// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import node from '@astrojs/node';
import keystatic from '@keystatic/astro';
import react from '@astrojs/react';

export default defineConfig({
  output: 'server',
  adapter: node({ mode: 'standalone' }),
  integrations: [react(), keystatic()],
  vite: {
    plugins: [tailwindcss()],
    preview: {
      allowedHosts: ['gigarun.local', 'localhost'],
    },
  },
});
