// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',
  server: {
    host: '0.0.0.0',
  },
  vite: {
    preview: {
      allowedHosts: ['gigarun.local', 'localhost'],
    },
  },
});
