export const productDefinitions=[
  ['night','Night Care Face Mist','Repair. Renew. Rebalance.'],
  ['hydration','Hydration Face Mist','Refresh. Hydrate. Plump.'],
  ['sun','Sun Protection Face Mist','Defend. Soothe. Glow.'],
  ['brightening','Brightening Face Mist','Even. Brighten. Illuminate.']
];
export const products=productDefinitions.map(([name,title,description],i)=>{
  const image={src:`/assets/cellulaire-product-${name}.webp`,alt:title,width:158,height:134};
  const variant={id:100+i,title:'Default Title',options:['Default Title'],available:true,price:2800,featured_image:image};
  return {id:10+i,handle:name+'-face-mist',url:'/products/'+name+'-face-mist',object_type:'product',title,vendor:'Cellulaire',price:2800,available:true,has_only_default_variant:true,featured_image:image,images:[image],variants:[variant],selected_or_first_available_variant:variant,options_with_values:[],description:`<p>${description} An elevated everyday face mist ritual.</p>`,metafields:{custom:{short_description:description}}};
});
const sizeVariant={id:200,title:'100 ml',options:['100 ml'],available:false,price:4800};
export const optionsProduct={...products[1],id:99,handle:'hydration-options',url:'/products/hydration-options',has_only_default_variant:false,variants:[{...products[1].variants[0],id:199,title:'50 ml',options:['50 ml']},sizeVariant],options_with_values:[{name:'Size',values:[{value:'50 ml',toString(){return this.value},selected:true},{value:'100 ml',toString(){return this.value},selected:false}]}]};
export const signatureSet={...products[0],id:14,handle:'signature-set',title:'The Signature Set',url:'/products/signature-set',price:9500,compare_at_price:11200,featured_image:{src:'/assets/cellulaire-routine.webp',alt:'All four face mists'},images:[{src:'/assets/cellulaire-routine.webp',alt:'All four face mists'}],variants:[{id:104,title:'Default Title',options:['Default Title'],available:true,price:9500}],selected_or_first_available_variant:{id:104,available:true,price:9500}};
export const allProducts=[...products,optionsProduct,signatureSet];
export const collections={all:{title:'The Face Mist Collection',url:'/collections/all',description:'<p>Four targeted formulas. One elevated routine.</p>',products,products_count:4,sort_by:'manual',sort_options:[{value:'manual',name:'Featured'},{value:'price-ascending',name:'Price: Low to high'},{value:'price-descending',name:'Price: High to low'},{value:'title-ascending',name:'Alphabetically: A–Z'}]}};
products.forEach((product,i)=>{collections[productDefinitions[i][0]]={...collections.all,title:product.title.replace(' Face Mist',''),url:'/collections/'+productDefinitions[i][0],products:[product],products_count:1};});
export const article={title:'An Elevated Everyday Ritual',url:'/blogs/journal/an-elevated-everyday-ritual',object_type:'article',published_at:'2026-09-01',image:{src:'/assets/cellulaire-brand-4.webp',alt:'Cellulaire face mist collection'},excerpt_or_content:'Discover the four face mists and build your everyday skincare ritual.',content:'<p>From our signature face mists to every skincare essential, Cellulaire brings thoughtful formulation and a refined sensory experience to everyday care.</p>'};
export const blog={title:'The Journal',url:'/blogs/journal',articles:[article]};
export function makeCart(lines=[]) {
  const items=lines.map(line=>{
    const product=allProducts.find(p=>p.variants.some(v=>v.id===line.id));const variant=product.variants.find(v=>v.id===line.id);
    return {key:`${line.id}:preview`,product,variant,image:product.featured_image,url:product.url,quantity:line.quantity,properties:{},final_price:variant.price,final_line_price:variant.price*line.quantity};
  });
  return {items,item_count:items.reduce((sum,item)=>sum+item.quantity,0),total_price:items.reduce((sum,item)=>sum+item.final_line_price,0),currency:{iso_code:'USD'},cart_level_discount_applications:[],note:''};
}
