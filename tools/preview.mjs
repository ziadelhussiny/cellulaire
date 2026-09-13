// Local QA adapter only. The shipped theme uses Shopify Liquid and real endpoints.
import http from 'node:http';
import path from 'node:path';
import fs from 'node:fs/promises';
import {Liquid} from 'liquidjs';
import {allProducts,products,productDefinitions,collections,blog,article,makeCart,signatureSet} from './fixtures.mjs';
const project=path.resolve(import.meta.dirname,'..');
const snippetRoot=path.join(project,'tmp/liquid');await fs.mkdir(snippetRoot,{recursive:true});
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function preprocess(source) {
  return source.replace(/{%\s*(schema|doc)\s*%}[\s\S]*?{%\s*end\1\s*%}/g,'')
    .replace(/{%\s*form\s+'(\w+)'([^%]*)%}/g,(_,type,attrs)=>{
      const values=[...attrs.matchAll(/([\w-]+):\s*'([^']*)'/g)].map(([,key,value])=>`${key}="${esc(value)}"`).join(' ');
      return `<form method="post" action="${type==='product'?'/cart/add':'/contact'}" ${values}><input type="hidden" name="form_type" value="${type}">`;
    }).replace(/{%\s*endform\s*%}/g,'</form>')
    .replace(/{%\s*paginate\s+[^%]+%}/g,'{% assign paginate = preview_paginate %}')
    .replace(/{%\s*endpaginate\s*%}/g,'')
    .replace(/{%\s*sections\s+'header-group'\s*%}/g,'{{ preview_header }}')
    .replace(/{%\s*sections\s+'footer-group'\s*%}/g,'{{ preview_footer }}');
}
const engine=new Liquid({root:snippetRoot,extname:'.liquid',lenientIf:true,jsTruthy:false});
engine.registerFilter('asset_url',name=>'/assets/'+name);
engine.registerFilter('stylesheet_tag',src=>`<link rel="stylesheet" href="${esc(src)}">`);
engine.registerFilter('image_url',image=>typeof image==='object'?image?.src:image);
engine.registerFilter('image_tag',(src,...args)=>{
  const params=Object.fromEntries(args.filter(Array.isArray));const attrs=Object.entries(params).filter(([key])=>!['widths','sizes'].includes(key)).map(([key,value])=>`${key}="${esc(value)}"`).join(' ');
  return `<img src="${esc(src)}" ${attrs}>`;
});
engine.registerFilter('money',n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(Number(n)/100));
engine.registerFilter('money_without_currency',n=>(Number(n)/100).toFixed(2));
engine.registerFilter('json',object=>JSON.stringify(object));
engine.registerFilter('payment_terms',()=> '');engine.registerFilter('default_errors',v=>esc(v));
engine.registerFilter('metafield_tag',v=>`<p>${esc(v)}</p>`);engine.registerFilter('structured_data',()=> '{}');
engine.registerFilter('default_pagination',()=> '');
for(const name of await fs.readdir(path.join(project,'snippets'))){if(name.startsWith('cellulaire-') || name==='meta-tags.liquid')await fs.writeFile(path.join(snippetRoot,name),preprocess(await fs.readFile(path.join(project,'snippets',name),'utf8')));}
async function renderSection(type,definition,base,id) {
  const raw=await fs.readFile(path.join(project,'sections',type+'.liquid'),'utf8');
  const schema=JSON.parse(raw.match(/{%\s*schema\s*%}([\s\S]*?){%\s*endschema\s*%}/)[1]);
  const settings={...Object.fromEntries(schema.settings.filter(s=>s.default!==undefined).map(s=>[s.id,s.default])),...definition.settings};
  const blocks=(definition.block_order||[]).map((key,i)=>{
    const block=definition.blocks[key];const defaults=schema.blocks?.find(b=>b.type===block.type)?.settings||[];
    const blockSettings={...Object.fromEntries(defaults.filter(s=>s.default!==undefined).map(s=>[s.id,s.default])),...block.settings};
    if(typeof blockSettings.product==='string')blockSettings.product=allProducts.find(product=>product.handle===blockSettings.product);
    if(typeof blockSettings.collection==='string')blockSettings.collection=collections[blockSettings.collection];
    return {...block,id:key,settings:blockSettings,shopify_attributes:''};
  });
  if(typeof settings.product==='string')settings.product=allProducts.find(product=>product.handle===settings.product);
  if(typeof settings.collection==='string')settings.collection=collections[settings.collection];
  // Expand scalar option value fixtures to Shopify's string-like values.
  const context={...base,section:{id,settings,blocks}};
  return `<div class="shopify-section" id="shopify-section-${id}">${await engine.parseAndRender(preprocess(raw),context)}</div>`;
}
async function renderGroup(name,base) {
  const group=JSON.parse(await fs.readFile(path.join(project,'sections',name+'-group.json'),'utf8'));
  return (await Promise.all(group.order.map(id=>renderSection(group.sections[id].type,group.sections[id],base,name+'-'+id)))).join('');
}
export async function renderPage(url,lines=[],form={}) {
  let template='404',page={},product,collection,search={performed:false},pageType='404';
  if(url.pathname==='/'){template='index';pageType='index';}
  else if(url.pathname.startsWith('/pages/')){const handle=url.pathname.split('/')[2];page={handle,title:({'our-story':'Our Story',contact:'Contact Us',faq:'Frequently Asked Questions',science:'Our Science'})[handle]||handle,content:''};template=['our-story','contact','faq','science'].includes(handle)?'page.'+handle:'page';pageType='page';}
  else if(url.pathname.startsWith('/collections/')){collection=collections[url.pathname.split('/')[2]];if(collection){template='collection';pageType='collection';collection={...collection,sort_by:url.searchParams.get('sort_by')||'manual'};if(collection.sort_by==='title-ascending')collection.products=[...collection.products].sort((a,b)=>a.title.localeCompare(b.title));}}
  else if(url.pathname.startsWith('/products/')){product=allProducts.find(p=>p.handle===url.pathname.split('/')[2]);if(product){template='product';pageType='product';const variant=product.variants.find(v=>String(v.id)===url.searchParams.get('variant'))||product.variants[0];product={...product,selected_or_first_available_variant:variant};if(!product.has_only_default_variant){product.options_with_values=[{name:'Size',values:product.variants.map(v=>Object.assign(new String(v.options[0]),{selected:v.id===variant.id}))}];}}}
  else if(url.pathname==='/cart'){template='cart';pageType='cart';}
  else if(url.pathname==='/search'){template='search';pageType='search';const term=url.searchParams.get('q')||'';const results=[...products,article].filter(p=>(p.title+' '+(p.description||p.content)).toLowerCase().includes(term.toLowerCase()));search={performed:!!term,terms:term,results,results_count:results.length};}
  else if(url.pathname==='/blogs/journal'){template='blog';pageType='blog';}
  else if(url.pathname===article.url){template='article';pageType='article';}
  else if(url.pathname==='/collections'){template='list-collections';pageType='list-collections';}
  const base={page,product,collection,search,blog,article,collections,all_products:Object.fromEntries(allProducts.map(product=>[product.handle,product])),cart:makeCart(lines),form,customer:{},request:{locale:{iso_code:'en'},page_type:pageType,origin:url.origin},routes:{root_url:'/',all_products_collection_url:'/collections/all',cart_url:'/cart',cart_change_url:'/cart/change',search_url:'/search',account_url:'/account'},settings:{},shop:{name:'Cellulaire',currency:'USD',policies:[],customer_accounts_enabled:false},page_title:product?.title||collection?.title||page.title|| (template==='index'?'Where Science Meets Luxury':template==='blog'?'The Journal':template==='cart'?'Your Bag':'Cellulaire'),canonical_url:url.href,preview_paginate:{pages:1}};
  const definition=JSON.parse(await fs.readFile(path.join(project,'templates',template+'.json'),'utf8'));
  const body=(await Promise.all(definition.order.map(id=>renderSection(definition.sections[id].type,definition.sections[id],base,id)))).join('');
  const html=await engine.parseAndRender(preprocess(await fs.readFile(path.join(project,'layout/theme.liquid'),'utf8')),{...base,content_for_layout:body,content_for_header:'',preview_header:await renderGroup('header',base),preview_footer:await renderGroup('footer',base)});
  return {html,template};
}
const carts=new Map();
export const server=http.createServer(async(req,res)=>{
  const url=new URL(req.url,'http://127.0.0.1:9292');
  try{
    if(url.pathname.startsWith('/assets/')){const filename=path.resolve(project,'.'+url.pathname);if(!filename.startsWith(path.join(project,'assets')+path.sep))throw new Error('Invalid asset');const bytes=await fs.readFile(filename);res.setHeader('Content-Type',({'css':'text/css','js':'text/javascript','webp':'image/webp','png':'image/png','svg':'image/svg+xml'})[path.extname(filename).slice(1)]||'application/octet-stream');res.end(bytes);return;}
    if(url.pathname==='/favicon.ico'){res.writeHead(204);res.end();return;}
    let session=req.headers.cookie?.match(/cellulaire_preview=([\w-]+)/)?.[1];if(!session){session=crypto.randomUUID();res.setHeader('Set-Cookie',`cellulaire_preview=${session}; Path=/; SameSite=Lax`);}let lines=carts.get(session)||[];
    const json=(data,status=200)=>{res.writeHead(status,{'Content-Type':'application/json'});res.end(JSON.stringify(data));};
    if(url.pathname==='/cart.js'){json(makeCart(lines));return;}
    if(req.method==='POST'){
      const chunks=[];for await(const chunk of req)chunks.push(chunk);const body=Buffer.concat(chunks).toString();let fields;
      if(req.headers['content-type']?.includes('application/json'))fields=JSON.parse(body);
      else if(req.headers['content-type']?.includes('multipart')){fields={};for(const match of body.matchAll(/name="([^"\r\n]+)"\r\n\r\n([^\r\n]*)/g))fields[match[1]]=match[2];}
      else fields=Object.fromEntries(new URLSearchParams(body));
      if(['/cart/add.js','/cart/add'].includes(url.pathname)){
        const id=Number(fields.id),quantity=Number(fields.quantity||1);const variant=allProducts.flatMap(p=>p.variants).find(v=>v.id===id);
        if(!variant?.available||!Number.isInteger(quantity)||quantity<1){json({description:'This variant is unavailable.'},422);return;}
        const existing=lines.find(line=>line.id===id);if(existing)existing.quantity+=quantity;else lines.push({id,quantity});carts.set(session,lines);
        if(url.pathname.endsWith('.js'))json({id,quantity});else{res.writeHead(303,{Location:'/cart'});res.end();}return;
      }
      if(url.pathname==='/cart'){
        const quantities=new URLSearchParams(body).getAll('updates[]');lines=lines.map((line,i)=>({...line,quantity:Number(quantities[i]??line.quantity)})).filter(line=>line.quantity>0);carts.set(session,lines);
        if('checkout' in fields){res.end('<p>Local preview only: live checkout requires the Shopify store.</p><a href="/cart">Return to bag</a>');return;}
        res.writeHead(303,{Location:'/cart'});res.end();return;
      }
      if(url.pathname==='/contact') {const result=await renderPage(new URL('/pages/contact',url),lines,{'posted_successfully?':true});res.setHeader('Content-Type','text/html');res.end(result.html.replace('Thank you. Your message has been sent.','Preview validation passed. No email was sent.'));return;}
    }
    if(url.pathname==='/cart/change'){const key=url.searchParams.get('id');const quantity=Number(url.searchParams.get('quantity'));lines=lines.map(line=>`${line.id}:preview`===key?{...line,quantity}:line).filter(line=>line.quantity>0);carts.set(session,lines);res.writeHead(303,{Location:'/cart'});res.end();return;}
    const result=await renderPage(url,lines);res.writeHead(result.template==='404'?404:200,{'Content-Type':'text/html; charset=utf-8'});res.end(result.html);
  }catch(error){console.error(error);res.writeHead(500);res.end(esc(error.stack));}
});
if(process.argv[1]===import.meta.filename)server.listen(9292,'127.0.0.1',()=>console.log('Cellulaire native-template QA preview: http://127.0.0.1:9292 (fixture data, no live checkout/email)'));
