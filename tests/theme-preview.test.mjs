import test from 'node:test';
import assert from 'node:assert/strict';
import {renderPage,server} from '../tools/preview.mjs';

test('reference pages render usable product links, section content and contact inputs',async()=>{
  for(const path of ['/','/pages/our-story','/pages/contact']) {
    const {html}=await renderPage(new URL(path,'http://127.0.0.1:9292'));
    assert.match(html,/<h1>/);assert.match(html,/\/pages\/contact/);assert.doesNotMatch(html,/\{%|\{\{/);
  }
  const {html}=await renderPage(new URL('/pages/contact','http://127.0.0.1:9292'));
  assert.match(html,/name="contact\[email\]"/);assert.match(html,/name="contact\[body\]"/);
});
test('shop, product, search, journal and missing-page routes render expected customer states',async()=>{
  const cases=[['/collections/all','The Face Mist Collection'],['/products/night-face-mist','Night Care Face Mist'],['/search?q=unfindable','No results found'],['/blogs/journal','The Journal'],['/not-a-page',"couldn't find this page"]];
  for(const [path,text] of cases){const {html}=await renderPage(new URL(path,'http://127.0.0.1:9292'));assert.ok(html.includes(text),path);}
});
test('Our Story preserves the reference product order and corresponding photos',async()=>{
  const {html}=await renderPage(new URL('/pages/our-story','http://127.0.0.1:9292'));
  const start=html.indexOf('products--compact');const collection=html.slice(start,html.indexOf('</section>',start));
  const productLinks=[...collection.matchAll(/class="product-card-image" href="([^"]+)"/g)].map(match=>match[1]);
  assert.deepEqual(productLinks,['/products/night-face-mist','/products/brightening-face-mist','/products/sun-face-mist','/products/hydration-face-mist']);
  const productPhotos=[...collection.matchAll(/class="product-card-image"[^>]*>\s*<img src="([^"]+)"/g)].map(match=>match[1]);
  assert.deepEqual(productPhotos,['/assets/cellulaire-product-night.webp','/assets/cellulaire-product-brightening.webp','/assets/cellulaire-product-sun.webp','/assets/cellulaire-product-hydration.webp']);
});
test('preview commerce accepts a real fixture variant and rejects sold-out inventory',async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base='http://127.0.0.1:'+server.address().port;
  try {
    const add=await fetch(base+'/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:100,quantity:2})});
    assert.equal(add.status,200);const cookie=add.headers.get('set-cookie').split(';')[0];
    const cart=await(await fetch(base+'/cart.js',{headers:{cookie}})).json();assert.equal(cart.item_count,2);assert.equal(cart.total_price,5600);
    const unavailable=await fetch(base+'/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json',cookie},body:JSON.stringify({id:200,quantity:1})});assert.equal(unavailable.status,422);
    const unchanged=await(await fetch(base+'/cart.js',{headers:{cookie}})).json();assert.equal(unchanged.item_count,2);
    await fetch(base+'/cart/change?id=100%3Apreview&quantity=0',{headers:{cookie},redirect:'manual'});
    const empty=await(await fetch(base+'/cart.js',{headers:{cookie}})).json();assert.equal(empty.item_count,0);
  } finally {await new Promise(resolve=>server.close(resolve));}
});
