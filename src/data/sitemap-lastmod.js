// lastmod du sitemap : uniquement des dates REELLES lues dans les sources des pages
// (dateModified du JSON-LD, ou prop `modifie` de ResumeCitable, a defaut sa date par defaut).
// Une page sans date connue n'a pas de lastmod : mieux vaut rien qu'une date fausse (Google l'ignore sinon).
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const RACINE = 'src/pages';
const DEFAUT_RESUME = (readFileSync('src/components/ResumeCitable.astro', 'utf8').match(/modifie\s*=\s*'(\d{4}-\d{2}-\d{2})'/) || [])[1];

function fichiers(dir) {
  return readdirSync(dir).flatMap((n) => {
    const p = join(dir, n);
    return statSync(p).isDirectory() ? fichiers(p) : p.endsWith('.astro') ? [p] : [];
  });
}

function urlDe(f) {
  let r = f.slice(RACINE.length).replaceAll('\\', '/').replace(/\.astro$/, '').replace(/\/index$/, '');
  return 'https://gigarun.re' + r + '/';
}

export const LASTMOD = new Map();
for (const f of fichiers(RACINE)) {
  if (f.includes('[')) continue;
  const s = readFileSync(f, 'utf8');
  const ld = s.match(/"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})/);
  const prop = s.match(/modifie\s*=\s*["'](\d{4}-\d{2}-\d{2})["']/);
  const date = (ld && ld[1]) || (prop && prop[1]) || (s.includes('<ResumeCitable') ? DEFAUT_RESUME : null);
  if (date) LASTMOD.set(urlDe(f), date);
}
