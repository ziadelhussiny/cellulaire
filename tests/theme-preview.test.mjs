import test from 'node:test';
import assert from 'node:assert/strict';
import {renderPage,server} from '../tools/preview.mjs';
import {products,signatureSet} from '../tools/fixtures.mjs';

test('reference pages render usable product links, section content and contact inputs',async()=>{
  for(const path of ['/','/pages/our-story','/pages/contact']) {
    const {html}=await renderPage(new URL(path,'http://127.0.0.1:9292'));
    assert.match(html,/<h1>/);assert.match(html,/\/pages\/contact/);assert.doesNotMatch(html,/\{%|\{\{/);
    assert.equal([...html.matchAll(/<title>/g)].length,1,'One usable document title');
    assert.doesNotMatch(html,/<title>\s*(?:–|&ndash;)/);
  }
  const {html}=await renderPage(new URL('/pages/contact','http://127.0.0.1:9292'));
  assert.match(html,/name="contact\[email\]"/);assert.match(html,/name="contact\[body\]"/);
});

test('bundled resource handles resolve native products, signature set and skin collections',async()=>{
  const {html}=await renderPage(new URL('/','http://127.0.0.1:9292'));
  for(const name of ['night','hydration','sun','brightening']){
    assert.ok(html.includes(`/collections/${name}`));
    assert.ok(html.includes(`/products/${name}-face-mist`));
  }
  assert.match(html,/name="id" value="104"/);
  assert.ok(html.includes('$95.00'));
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

test('known products retain their matching bundled photos in gallery and bag without Shopify media',async()=>{
  for(const product of [...products,signatureSet]) {
    const expected=product.featured_image.src;
    const original={image:product.featured_image,images:product.images,variantImages:product.variants.map(v=>v.featured_image)};
    try {
      product.featured_image=undefined;product.images=[];
      product.variants.forEach(v=>{v.featured_image=undefined;});
      const detail=await renderPage(new URL(product.url,'http://127.0.0.1:9292'));
      const gallery=detail.html.split('class="product-gallery"')[1].split('class="product-information"')[0];
      assert.ok(gallery.includes(`src="${expected}"`),product.handle+' gallery');
      assert.ok(gallery.includes('data-main-image'),product.handle+' gallery remains addressable');
      const bag=await renderPage(new URL('/cart','http://127.0.0.1:9292'),[{id:product.variants[0].id,quantity:1}]);
      const line=bag.html.split('class="cart-line"')[1].split('</article>')[0];
      assert.ok(line.includes(`src="${expected}"`),product.handle+' bag');
      assert.doesNotMatch(line,/<img src=""/);
    } finally {
      product.featured_image=original.image;product.images=original.images;
      product.variants.forEach((v,i)=>{v.featured_image=original.variantImages[i];});
    }
  }
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
