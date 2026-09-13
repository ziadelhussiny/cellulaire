import {renderPage} from './preview.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
const routes=['/','/pages/our-story','/pages/contact','/pages/science','/pages/faq','/collections/all','/products/night-face-mist','/cart','/search?q=mist','/blogs/journal','/blogs/journal/an-elevated-everyday-ritual'];
const links=new Set(),assets=new Set();
for(const route of routes){const {html}=await renderPage(new URL(route,'http://127.0.0.1:9292'));for(const [,href] of html.matchAll(/href="([^"]+)"/g)){if(href.startsWith('/')&&!href.startsWith('/assets/'))links.add(href);}for(const [,src] of html.matchAll(/(?:src|href)="(\/assets\/[^"?]+)"/g))assets.add(src);}
const failures=[];
for(const link of links){const {template}=await renderPage(new URL(link,'http://127.0.0.1:9292'));if(template==='404')failures.push(link);}
for(const asset of assets){try{await fs.access(path.join(import.meta.dirname,'..',asset));}catch{failures.push(asset);}}
const result={scope:'Local native templates with separate fixtures; store resources still require live verification',pages:routes.length,internalLinks:links.size,assets:assets.size,failures};
await fs.mkdir(path.join(import.meta.dirname,'../output'),{recursive:true});await fs.writeFile(path.join(import.meta.dirname,'../output/link-audit.json'),JSON.stringify(result,null,2));console.log(result);if(failures.length)process.exit(1);
