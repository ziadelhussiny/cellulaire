import { selectVariant, productError } from './cellulaire-commerce.js';

const root = document.documentElement.dataset.root || '/';
function init(scope = document) {
  scope.querySelectorAll('[data-menu-toggle]').forEach(button => {
    if (button.dataset.ready) return; button.dataset.ready='true';
    const menu=document.getElementById(button.getAttribute('aria-controls'));
    button.addEventListener('click', () => {
      const expanded=button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded',String(expanded)); menu.hidden=!expanded;
      if (expanded) menu.querySelector('a')?.focus();
    });
    menu.addEventListener('keydown', event => { if(event.key==='Escape') { menu.hidden=true;button.setAttribute('aria-expanded','false');button.focus(); } });
    menu.addEventListener('focusout', () => { queueMicrotask(() => {if(!menu.contains(document.activeElement) && document.activeElement!==button){menu.hidden=true;button.setAttribute('aria-expanded','false');}}); });
  });
  scope.querySelectorAll('[data-topic]').forEach(button => button.addEventListener('click', () => {
    const subject=document.querySelector('[name="contact[Subject]"]');
    if(subject){subject.value=button.dataset.topic;subject.focus();document.getElementById('ContactForm').scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});}
  }));
  scope.querySelectorAll('[data-message]').forEach(field => field.addEventListener('input', () => {document.querySelector('[data-counter]').textContent=`${field.value.length}/500`;}));
  scope.querySelectorAll('[data-product-form]').forEach(form => {
    if(form.dataset.ready)return;form.dataset.ready='true';
    const variantData=form.querySelector('[data-variants]');
    const variants=variantData?JSON.parse(variantData.textContent):[];
    const button=form.querySelector('[type="submit"]');const status=form.querySelector('[data-form-status]');
    form.querySelectorAll('[data-option]').forEach(select => select.addEventListener('change', () => {
      const variant=selectVariant(variants,[...form.querySelectorAll('[data-option]')].map(input=>input.value));
      form.querySelector('[name="id"]').value=variant?.id || '';
      button.disabled=!variant?.available;button.textContent=variant?(variant.available?'Add to bag':'Sold out'):'Unavailable';
      const price=document.querySelector('[data-product-price]');
      if(price && variant)price.textContent=new Intl.NumberFormat(document.documentElement.lang,{style:'currency',currency:document.documentElement.dataset.currency}).format(variant.price/100);
      if(variant){const url=new URL(location.href);url.searchParams.set('variant',variant.id);history.replaceState({},'',url);const img=document.querySelector('[data-main-image]');if(img && variant.featured_image?.src){img.src=variant.featured_image.src;img.removeAttribute('srcset');}}
    }));
    form.addEventListener('submit',async event => {
      if(!window.fetch || !form.querySelector('[name="id"]').value)return;
      event.preventDefault();const label=button.textContent;button.disabled=true;button.textContent='Adding…';status.textContent='';
      const controls=[...form.querySelectorAll('[data-option], [name="quantity"]')];
      const payload=new FormData(form);controls.forEach(control=>{control.disabled=true;});
      try {
        const response=await fetch(root+'cart/add.js',{method:'POST',body:payload,headers:{Accept:'application/json'}});
        const result=await response.json();if(!response.ok)throw new Error(productError(result));
        status.innerHTML='Added to your bag. ';const link=document.createElement('a');link.href=root+'cart';link.textContent='View bag →';status.append(link);
        // Adding succeeded even if refreshing the badge is temporarily unavailable.
        try {const cartResponse=await fetch(root+'cart.js');if(cartResponse.ok){const cart=await cartResponse.json();document.querySelectorAll('[data-cart-count]').forEach(count=>{count.textContent=cart.item_count;});}} catch { /* The bag page still reads Shopify's authoritative cart. */ }
      } catch(error){status.textContent=error.message || 'Please try again.';}
      finally{button.disabled=false;button.textContent=label;controls.forEach(control=>{control.disabled=false;});}
    });
  });
  scope.querySelectorAll('[data-thumbnail]').forEach(button => button.addEventListener('click', () => {
    const image=document.querySelector('[data-main-image]');image.src=button.dataset.thumbnail;image.removeAttribute('srcset');image.alt=button.querySelector('img').alt;
    scope.querySelectorAll('[data-thumbnail]').forEach(other=>other.setAttribute('aria-pressed',String(other===button)));
  }));
  scope.querySelectorAll('[data-review-next], [data-review-prev]').forEach(button => button.addEventListener('click',()=>{
    const section=button.closest('[data-reviews]');const reviews=[...section.querySelectorAll('blockquote')];let index=reviews.findIndex(review=>!review.hidden);
    reviews[index].hidden=true;index=(index+(button.hasAttribute('data-review-next')?1:-1)+reviews.length)%reviews.length;reviews[index].hidden=false;
  }));
}
init();document.addEventListener('shopify:section:load',event=>init(event.target));
