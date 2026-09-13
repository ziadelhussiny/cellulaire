"""Initial native Shopify section/template scaffold. Source strings live here."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def write(path,text):
    (R/path).parent.mkdir(parents=True,exist_ok=True)
    (R/path).write_text(text.strip()+'\n',encoding='utf-8')
def setting(type,id,label,default=None,**kwargs):
    obj=dict(type=type,id=id,label=label,**kwargs)
    if default is not None:obj['default']=default
    return obj
def section(name,title,body,settings=[],blocks=None):
    schema=dict(name=title,settings=settings)
    if blocks:schema.update(blocks=blocks)
    schema['presets']=[dict(name=title)]
    write('sections/'+name+'.liquid',body+'\n{% schema %}\n'+json.dumps(schema,indent=2)+'\n{% endschema %}')
def template(name,items):
    write('templates/'+name+'.json',json.dumps({'sections':{id:{'type':type,**data} for id,type,data in items},'order':[id for id,_,_ in items]},indent=2))

write('layout/theme.liquid','''
<!doctype html>
<html lang="{{ request.locale.iso_code }}" data-root="{{ routes.root_url }}" data-currency="{{ cart.currency.iso_code | default: shop.currency }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="theme-color" content="#181816">
  <meta name="description" content="{{ page_description | default: shop.description | default: shop.name | escape }}">
  <meta property="og:site_name" content="{{ shop.name | escape }}">
  <meta property="og:title" content="{{ page_title | escape }}">
  <meta property="og:url" content="{{ canonical_url }}">
  <meta property="og:type" content="{% if request.page_type == 'product' %}product{% elsif request.page_type == 'article' %}article{% else %}website{% endif %}">
  {% if page_image %}<meta property="og:image" content="https:{{ page_image | image_url: width: 1200 }}">{% endif %}
  <title>{{ page_title | escape }}{% unless page_title contains shop.name %} — {{ shop.name | escape }}{% endunless %}</title>
  <link rel="canonical" href="{{ canonical_url }}">
  {% if settings.favicon != blank %}<link rel="icon" href="{{ settings.favicon | image_url: width: 32 }}">{% endif %}
  {{ 'cellulaire.css' | asset_url | stylesheet_tag }}
  <script type="module" src="{{ 'cellulaire.js' | asset_url }}"></script>
  {{ content_for_header }}
</head>
<body class="template-{{ request.page_type }}">
  <a class="skip-link" href="#MainContent">Skip to content</a>
  {% sections 'header-group' %}
  <main id="MainContent">{{ content_for_layout }}</main>
  {% sections 'footer-group' %}
</body>
</html>
''')
write('snippets/cellulaire-image.liquid','''
{% if image != blank %}
  {{ image | image_url: width: 1800 | image_tag: widths: '320, 640, 960, 1280, 1800', sizes: sizes, loading: loading, alt: alt, class: class }}
{% else %}
  <img src="{{ fallback | asset_url }}" alt="{{ alt | escape }}" class="{{ class }}" loading="{{ loading | default: 'lazy' }}" width="{{ width | default: 800 }}" height="{{ height | default: 500 }}" {% if main %}data-main-image{% endif %}>
{% endif %}
''')
write('snippets/cellulaire-product-asset.liquid','''
{%- case product.handle -%}
{%- when 'night-face-mist' -%}cellulaire-product-night.webp
{%- when 'hydration-face-mist' -%}cellulaire-product-hydration.webp
{%- when 'sun-face-mist' -%}cellulaire-product-sun.webp
{%- when 'brightening-face-mist' -%}cellulaire-product-brightening.webp
{%- when 'signature-set' -%}cellulaire-routine.webp
{%- endcase -%}
''')
write('snippets/cellulaire-icon.liquid','''
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
{% case name %}
{% when 'menu' %}<path d="M4 6h16M4 12h16M4 18h16"/>
{% when 'search' %}<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>
{% when 'bag' %}<path d="M5 7h14l1 14H4L5 7Z"/><path d="M9 8V5a3 3 0 0 1 6 0v3"/>
{% when 'account' %}<circle cx="12" cy="7" r="3.5"/><path d="M4 21v-2a8 8 0 0 1 16 0v2H4Z"/>
{% when 'drop' %}<path d="M12 2s-7 8-7 13a7 7 0 0 0 14 0c0-5-7-13-7-13Z"/><path d="M8 14c0 3 1 4 3 5"/>
{% when 'leaf' %}<path d="M4 20 19 4M4 16C0 8 11 2 21 2c0 10-6 21-15 15M10 13l-1-5M13 10l5 1"/>
{% when 'diamond' %}<path d="m3 7 4-5h10l4 5-9 15L3 7ZM3 7h18M7 2l5 20 5-20M7 7l5-5 5 5"/>
{% when 'heart' %}<path d="M12 21 3 12C-3 5 7-1 12 6c5-7 15-1 9 6l-9 9Z"/>
{% when 'science' %}<path d="M9 2h6M10 2v7l-6 11c-1 2 1 2 2 2h12c2 0 3-1 2-3L14 9V2M8 16h8"/><circle cx="11" cy="18" r=".5"/>
{% when 'mail' %}<rect x="2" y="5" width="20" height="14" rx="1"/><path d="m2 6 10 8 10-8"/>
{% when 'phone' %}<path d="M7 2 3 4c-2 6 8 17 15 18l4-4-5-5-3 3-6-6 3-3-4-5Z"/>
{% when 'clock' %}<circle cx="12" cy="12" r="10"/><path d="M12 5v7l5 3"/>
{% when 'truck' %}<path d="M2 5h12v12H2V5ZM14 10h5l3 5v2h-8M2 10H0"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="18" r="3"/>
{% when 'bottle' %}<path d="M10 2h4v5l3 2v13H7V9l3-2V2ZM10 5h4"/>
{% when 'people' %}<circle cx="12" cy="6" r="3"/><path d="M6 21v-6a6 6 0 0 1 12 0v6H6ZM5 4a3 3 0 0 0 0 6M19 4a3 3 0 0 1 0 6M3 12c-3 2-3 6-2 9M21 12c3 2 3 6 2 9"/>
{% when 'instagram' %}<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17 7h.01"/>
{% when 'tiktok' %}<path d="M14 3v12a4 4 0 1 1-4-4M14 3c0 4 3 6 6 6M14 6c2 3 4 4 6 4"/>
{% when 'facebook' %}<path fill="currentColor" stroke="none" d="M14 22V13h3l.5-4H14V7c0-1 .4-1.5 1.7-1.5H18V2.2L15.5 2C12.5 2 10 3.8 10 7v2H7v4h3v9Z"/>
{% when 'youtube' %}<rect x="2" y="5" width="20" height="14" rx="4" fill="currentColor" stroke="none"/><path d="m10 9 6 3-6 3Z" fill="white" stroke="none"/>
{% when 'whatsapp' %}<path d="m3 21 1.5-5A9 9 0 1 1 8 20Z"/><path d="M9 7c-4 2 3 10 7 8l-2-3-2 1-2-3 1-1-2-2Z"/>
{% else %}<circle cx="12" cy="12" r="9"/><path d="M8 12h8m-4-4 4 4-4 4"/>
{% endcase %}
</svg>
''')
section('cellulaire-header','Cellulaire header','''
<div class="announcement">{{ section.settings.announcement | escape }}<span class="announcement-extra"> &nbsp; | &nbsp; A More Radiant You, Every Day</span></div>
<header class="site-header wrap">
  <button class="icon-button mobile-only" data-menu-toggle aria-expanded="false" aria-controls="MobileMenu" aria-label="Open navigation">{% render 'cellulaire-icon', name: 'menu' %}</button>
  <nav class="desktop-nav" aria-label="Main navigation">
    {% if section.settings.menu != blank %}{% for link in section.settings.menu.links %}<a href="{{ link.url }}" {% if link.current %}aria-current="page"{% endif %}>{{ link.title | escape }}</a>{% endfor %}
    {% else %}<a href="{{ routes.all_products_collection_url }}">Shop</a><a href="{{ routes.root_url }}pages/our-story">Our Story</a><a href="{{ routes.root_url }}pages/science">Science</a>{% endif %}
  </nav>
  <a class="brand" href="{{ routes.root_url }}" aria-label="{{ shop.name | escape }} home">{% if settings.logo != blank %}{{ settings.logo | image_url: width: 600 | image_tag: alt: shop.name, width: 220 }}{% else %}<img src="{{ 'cellulaire-logo.png' | asset_url }}" width="220" height="51" alt="Cellulaire">{% endif %}</a>
  <div class="header-actions"><nav class="desktop-nav" aria-label="Information"><a href="{{ routes.root_url }}blogs/journal">Journal</a><a href="{{ routes.root_url }}pages/faq">Help</a></nav>
    <a class="icon-button" href="{{ routes.search_url }}" aria-label="Search">{% render 'cellulaire-icon', name: 'search' %}</a>
    {% if shop.customer_accounts_enabled %}<a class="icon-button desktop-only" href="{{ routes.account_url }}" aria-label="My account">{% render 'cellulaire-icon', name: 'account' %}</a>{% endif %}
    <a class="icon-button bag" href="{{ routes.cart_url }}" aria-label="Shopping bag">{% render 'cellulaire-icon', name: 'bag' %}<span data-cart-count>{{ cart.item_count }}</span></a>
  </div>
  <nav id="MobileMenu" class="mobile-menu" aria-label="Mobile navigation" hidden>
    {% if section.settings.menu != blank %}{% for link in section.settings.menu.links %}<a href="{{ link.url }}">{{ link.title | escape }}</a>{% endfor %}{% else %}<a href="{{ routes.all_products_collection_url }}">Shop</a><a href="{{ routes.root_url }}pages/our-story">Our Story</a><a href="{{ routes.root_url }}pages/science">Science</a>{% endif %}
    <a href="{{ routes.root_url }}blogs/journal">Journal</a><a href="{{ routes.root_url }}pages/faq">Help</a><a href="{{ routes.root_url }}pages/contact">Contact</a>{% if shop.customer_accounts_enabled %}<a href="{{ routes.account_url }}">My account</a>{% endif %}
  </nav>
</header>
''',[setting('text','announcement','Announcement','Free Shipping on Orders Over $50'),setting('link_list','menu','Main menu')])
section('cellulaire-footer','Cellulaire footer','''
<footer class="site-footer wrap">
  <a href="{{ routes.root_url }}" class="footer-brand"><img src="{{ 'cellulaire-logo.png' | asset_url }}" width="155" height="36" alt="Cellulaire"><span>Skincare for a brighter you</span></a>
  <nav aria-label="Footer navigation">{% if section.settings.menu != blank %}{% for link in section.settings.menu.links %}<a href="{{ link.url }}">{{ link.title | escape }}</a>{% endfor %}{% else %}<a href="{{ routes.all_products_collection_url }}">Shop</a><a href="{{ routes.root_url }}pages/our-story">Our Story</a><a href="{{ routes.root_url }}pages/science">Science</a><a href="{{ routes.root_url }}pages/faq">Help</a><a href="{{ routes.root_url }}pages/contact">Contact</a>{% endif %}</nav>
  <div class="social-links">{% if section.settings.instagram != blank %}<a href="{{ section.settings.instagram }}" aria-label="Instagram">{% render 'cellulaire-icon', name: 'instagram' %}</a>{% endif %}{% if section.settings.tiktok != blank %}<a href="{{ section.settings.tiktok }}" aria-label="TikTok">{% render 'cellulaire-icon', name: 'tiktok' %}</a>{% endif %}{% if section.settings.facebook != blank %}<a href="{{ section.settings.facebook }}" aria-label="Facebook">{% render 'cellulaire-icon', name: 'facebook' %}</a>{% endif %}{% if section.settings.youtube != blank %}<a href="{{ section.settings.youtube }}" aria-label="YouTube">{% render 'cellulaire-icon', name: 'youtube' %}</a>{% endif %}</div>
  <div class="footer-legal"><span>© {{ 'now' | date: '%Y' }} {{ shop.name | escape }}</span>{% for policy in shop.policies %}{% if policy != blank %}<a href="{{ policy.url }}">{{ policy.title | escape }}</a>{% endif %}{% endfor %}</div>
</footer>
''',[setting('link_list','menu','Footer menu'),*[setting('url',id,id.title()) for id in ['instagram','tiktok','facebook','youtube']]])
for group,type in [('header','cellulaire-header'),('footer','cellulaire-footer')]:
    write('sections/'+group+'-group.json',json.dumps({'type':group,'name':group.title(),'sections':{'main':{'type':type,'settings':{}}},'order':['main']},indent=2))

section('cellulaire-hero','Cellulaire hero','''
<section class="hero hero--{{ section.settings.variant }} {% if section.settings.composite_desktop and section.settings.image == blank %}hero--composite-desktop{% endif %} {% if section.settings.composite_mobile and section.settings.mobile_image == blank %}hero--composite{% endif %} wrap">
  <div class="hero-copy">
    {% if section.settings.eyebrow != blank %}<p class="eyebrow">{{ section.settings.eyebrow | escape }}</p>{% endif %}
    <h1>{{ section.settings.heading | escape | newline_to_br }}</h1>
    <p>{{ section.settings.description | escape }}</p>
    {% if section.settings.button_label != blank %}<a class="button" href="{{ section.settings.button_link | default: routes.all_products_collection_url }}">{{ section.settings.button_label | escape }} <span>→</span></a>{% endif %}
  </div>
  {% assign desktop_asset = section.settings.fallback %}{% if section.settings.composite_desktop and section.settings.image == blank %}{% assign desktop_asset = section.settings.composite_fallback %}{% endif %}
  {% assign mobile_asset = section.settings.mobile_fallback %}{% if section.settings.composite_mobile and section.settings.mobile_image == blank and section.settings.mobile_composite_fallback != blank %}{% assign mobile_asset = section.settings.mobile_composite_fallback %}{% endif %}
  <div class="hero-image desktop-only">{% render 'cellulaire-image', image: section.settings.image, fallback: desktop_asset, alt: section.settings.image_alt, loading: 'eager', sizes: '100vw' %}</div>
  <div class="hero-image mobile-only">{% render 'cellulaire-image', image: section.settings.mobile_image, fallback: mobile_asset, alt: section.settings.image_alt, loading: 'eager', sizes: '100vw' %}</div>
</section>
''',[setting('select','variant','Layout','home',options=[dict(value=x,label=x.title()) for x in ['home','about','contact']]),setting('text','eyebrow','Eyebrow'),setting('textarea','heading','Heading','Where Science\nMeets Luxury'),setting('textarea','description','Description','Advanced skincare. Visible results. A refined everyday ritual.'),setting('text','button_label','Button','Shop face mists'),setting('url','button_link','Button link'),setting('image_picker','image','Desktop image'),setting('image_picker','mobile_image','Mobile image'),setting('checkbox','composite_desktop','Use reference desktop banner',False,info='Retains supplied artwork with accessible text and a working button. Upload a clean image for visible editable text.'),setting('text','composite_fallback','Reference desktop banner','cellulaire-hero-banner.webp'),setting('checkbox','composite_mobile','Use reference mobile banner',False,info='Retains supplied artwork with accessible text and a working button. Upload a clean image for visible editable text.'),setting('text','mobile_composite_fallback','Reference mobile banner'),setting('text','fallback','Bundled desktop asset','cellulaire-hero.webp'),setting('text','mobile_fallback','Bundled mobile asset','cellulaire-hero.webp'),setting('text','image_alt','Image description','Cellulaire face mist ritual')])
section('cellulaire-benefits','Cellulaire benefits','''
<section class="benefits wrap" aria-label="Our approach">
{% for block in section.blocks %}<div {{ block.shopify_attributes }}>{% render 'cellulaire-icon', name: block.settings.icon %}<span>{{ block.settings.text | escape | newline_to_br }}</span></div>{% endfor %}
</section>
''',[],[dict(type='benefit',name='Benefit',settings=[setting('text','icon','Icon','drop'),setting('textarea','text','Text','Science-backed\nformulas')])])
section('cellulaire-skin-needs','Shop by skin need','''
<section class="skin-needs wrap inset">
  <div class="skin-needs-intro"><h2>{{ section.settings.heading | escape }}</h2><p>Targeted care for every moment, every skin need.</p><a class="text-link" href="{{ routes.all_products_collection_url }}">Shop all →</a></div>
  <div class="need-grid">{% for block in section.blocks %}{% assign chosen_collection = block.settings.collection %}{% if chosen_collection == blank %}{% assign chosen_collection = collections[block.settings.handle] %}{% endif %}{% assign destination = chosen_collection.url | default: routes.all_products_collection_url %}<a class="need-card need--{{ block.settings.tone }}" href="{{ destination }}" {{ block.shopify_attributes }}>
    {% render 'cellulaire-image', image: block.settings.image, fallback: block.settings.fallback, alt: block.settings.heading, width: 127, height: 95 %}<div><h3>{{ block.settings.heading | escape }}</h3><span>{{ block.settings.description | escape }} →</span></div>
  </a>{% endfor %}</div>
</section>
''',[setting('text','heading','Heading','Shop by Skin Need')],[dict(type='need',name='Skin need',settings=[setting('text','heading','Title','Night Care'),setting('text','description','Description','Repair & renew'),setting('collection','collection','Collection'),setting('text','handle','Fallback collection handle','night'),setting('image_picker','image','Image'),setting('text','fallback','Bundled asset','cellulaire-need-night.webp'),setting('text','tone','Color tone','night')])])
write('snippets/cellulaire-product-card.liquid','''
{% assign destination = product.url | default: routes.all_products_collection_url %}
{% assign title = product.title | default: title %}
{% capture bundled_photo %}{% render 'cellulaire-product-asset', product: product %}{% endcapture %}{% assign bundled_photo = bundled_photo | strip %}{% assign fallback = bundled_photo | default: fallback %}
<article class="product-card">
  <a class="product-card-image" href="{{ destination }}">{% render 'cellulaire-image', image: product.featured_image, fallback: fallback, alt: title, width: 158, height: 134 %}</a>
  <div class="product-card-copy"><h3><a href="{{ destination }}">{% if compact %}{{ title | remove: ' Face Mist' | escape }}{% else %}{{ title | escape }}{% endif %}</a></h3><p>{{ product.metafields.custom.short_description | default: description | escape }}</p>
    {% if product != blank %}<span>{{ product.price | money }}</span>{% endif %}
    {% if compact %}<a class="button" href="{{ destination }}">Shop now →</a>
    {% elsif product != blank and product.has_only_default_variant and product.available %}
      {% form 'product', product, data-product-form: '' %}<input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}"><input type="hidden" name="quantity" value="1"><button class="button" type="submit"><span class="desktop-only">Add to bag</span><span class="mobile-only">Add</span></button><p data-form-status role="status"></p>{% endform %}
    {% else %}<a class="button" href="{{ destination }}">{% if product == blank %}Shop now{% elsif product.available %}Choose options{% else %}View product{% endif %}</a>{% endif %}
  </div>
</article>
''')
section('cellulaire-products','Cellulaire products','''
<section class="products-section wrap inset {% if section.settings.compact %}products--compact{% endif %}">
  <div class="section-heading"><div>{% if section.settings.eyebrow != blank %}<p class="eyebrow">{{ section.settings.eyebrow | escape }}</p>{% endif %}<h2>{{ section.settings.heading | escape }}</h2><p>{{ section.settings.description | escape }}</p></div><a class="text-link" href="{{ section.settings.collection.url | default: routes.all_products_collection_url }}">View all →</a></div>
  <div class="product-grid">
    {% if section.blocks.size > 0 %}{% for block in section.blocks %}{% assign chosen_product = block.settings.product %}{% if chosen_product == blank %}{% assign chosen_product = all_products[block.settings.handle] %}{% endif %}<div {{ block.shopify_attributes }}>{% render 'cellulaire-product-card', product: chosen_product, title: block.settings.title, description: block.settings.description, fallback: block.settings.fallback, compact: section.settings.compact %}</div>{% endfor %}
    {% elsif section.settings.collection != blank %}{% for product in section.settings.collection.products limit: 4 %}{% render 'cellulaire-product-card', product: product, fallback: 'cellulaire-product-night.webp', compact: section.settings.compact %}{% endfor %}
    {% else %}{% for product in collections.all.products limit: 4 %}{% render 'cellulaire-product-card', product: product, fallback: 'cellulaire-product-night.webp', compact: section.settings.compact %}{% endfor %}{% endif %}
  </div>
</section>
''',[setting('text','eyebrow','Eyebrow'),setting('text','heading','Heading','Best Sellers'),setting('text','description','Description','Our most-loved face mists for healthy, radiant skin.'),setting('collection','collection','Collection'),setting('checkbox','compact','Compact cards',False)],[dict(type='product',name='Product',settings=[setting('product','product','Shopify product'),setting('text','handle','Fallback product handle','night-face-mist'),setting('text','title','Fallback title','Night Care Face Mist'),setting('text','description','Short description','Repair. Renew. Rebalance.'),setting('text','fallback','Bundled photo','cellulaire-product-night.webp')])])
section('cellulaire-editorial','Cellulaire editorial','''
<section id="{{ section.settings.anchor | default: section.id }}" class="editorial editorial--{{ section.settings.layout }} wrap {% if section.settings.inset %}inset{% endif %}">
  <div class="editorial-copy">{% if section.settings.eyebrow != blank %}<p class="{% if section.settings.small_eyebrow %}eyebrow{% endif %}">{{ section.settings.eyebrow | escape }}</p>{% endif %}<h2>{{ section.settings.heading | escape | newline_to_br }}</h2><p>{{ section.settings.description | escape }}</p>{% if section.settings.button_label != blank %}<a class="{% if section.settings.layout == 'story' %}button button-outline{% elsif section.settings.layout == 'about-story' %}text-link{% else %}button{% endif %}" href="{{ section.settings.button_link | default: routes.all_products_collection_url }}">{{ section.settings.button_label | escape }} →</a>{% endif %}</div>
  <div class="editorial-image">
    <div {% if section.settings.mobile_fallback != blank or section.settings.mobile_image != blank %}class="desktop-only"{% endif %}>{% render 'cellulaire-image', image: section.settings.image, fallback: section.settings.fallback, alt: section.settings.image_alt %}</div>
    {% if section.settings.mobile_fallback != blank or section.settings.mobile_image != blank %}<div class="mobile-only">{% render 'cellulaire-image', image: section.settings.mobile_image, fallback: section.settings.mobile_fallback, alt: section.settings.image_alt %}</div>{% endif %}
    {% if section.settings.overlay != blank %}<h3 class="image-caption {% if section.settings.composite_image and section.settings.image == blank %}caption-composite-desktop{% endif %} {% if section.settings.composite_image and section.settings.mobile_image == blank %}caption-composite-mobile{% endif %}">{{ section.settings.overlay | escape | newline_to_br }}</h3>{% endif %}
  </div>
  {% if section.settings.aside != blank %}<p class="editorial-aside eyebrow">{{ section.settings.aside | escape | newline_to_br }}</p>{% endif %}
  {% if section.settings.layout == 'story' %}<a class="story-mobile" href="{{ section.settings.button_link | default: routes.all_products_collection_url }}"><img src="{{ 'cellulaire-woman-wide.webp' | asset_url }}" width="148" height="86" alt="A refined skincare ritual"><div><h3>Science<br>In Every Drop</h3><p class="eyebrow">Real results.<br>A brighter you.</p></div></a>{% endif %}
</section>
''',[setting('select','layout','Layout','story',options=[dict(value=x,label=x.title()) for x in ['story','about-story','formulas','mission','cta']]),setting('checkbox','inset','Inset',False),setting('text','anchor','Section anchor'),setting('text','eyebrow','Eyebrow','Our Story'),setting('checkbox','small_eyebrow','Spaced eyebrow',False),setting('textarea','heading','Heading','Exceptional Skincare\nBegins with a Belief'),setting('textarea','description','Description','At Cellulaire, we combine advanced science, carefully selected ingredients, and a commitment to quality to create skincare that delivers real results while offering a luxurious sensory experience.'),setting('text','button_label','Button label','Our story'),setting('url','button_link','Button link'),setting('image_picker','image','Image'),setting('image_picker','mobile_image','Mobile image'),setting('text','mobile_fallback','Bundled mobile asset'),setting('checkbox','composite_image','Bundled image includes its caption',False),setting('text','fallback','Bundled asset','cellulaire-story.webp'),setting('text','image_alt','Image description','The Cellulaire face mist collection'),setting('textarea','overlay','Image caption'),setting('textarea','aside','Side text','More\nthan skincare\na brighter you')])
section('cellulaire-values','Cellulaire values','''
<section class="values wrap inset">{% for block in section.blocks %}<article {{ block.shopify_attributes }}>{% render 'cellulaire-icon', name: block.settings.icon %}<h2>{{ block.settings.heading | escape }}</h2><p>{{ block.settings.description | escape }}</p></article>{% endfor %}</section>
''',[],[dict(type='value',name='Value',settings=[setting('text','icon','Icon','science'),setting('text','heading','Heading','Science'),setting('textarea','description','Description','Backed by research and powered by proven ingredients for visible results.')])])
section('cellulaire-routine','The complete routine','''
{% assign set_product = section.settings.product | default: all_products['signature-set'] %}
<section class="routine wrap inset"><div><p>The Complete Routine</p><h2><span class="desktop-only">{{ section.settings.heading | escape }}</span><span class="mobile-only">The Complete Routine</span></h2><p>Elevate your ritual with our curated collection.</p></div><span class="save-badge">{{ section.settings.badge | escape }}</span><div class="routine-image">{% render 'cellulaire-image', image: set_product.featured_image, fallback: 'cellulaire-routine.webp', alt: 'All four face mists', width: 147, height: 85 %}</div><div class="routine-product"><h3>{{ set_product.title | default: 'The Signature Set' | escape }}</h3><p>All Four Face Mists</p>{% if set_product != blank %}<p>{{ set_product.price | money }} {% if set_product.compare_at_price > set_product.price %}<s>{{ set_product.compare_at_price | money }}</s>{% endif %}</p>{% endif %}{% if set_product != blank and set_product.available and set_product.has_only_default_variant %}{% form 'product', set_product, data-product-form: '' %}<input type="hidden" name="id" value="{{ set_product.selected_or_first_available_variant.id }}"><input type="hidden" name="quantity" value="1"><button class="button" type="submit">Add to bag</button><p data-form-status role="status"></p>{% endform %}{% else %}<a class="button" href="{{ set_product.url | default: routes.all_products_collection_url }}">Shop the set →</a>{% endif %}</div></section>
''',[setting('text','heading','Heading','Better Skin Together'),setting('text','badge','Badge','Save 15%'),setting('product','product','Signature set product')])
section('cellulaire-reviews','Cellulaire testimonials','''
<section class="reviews wrap inset" data-reviews><h2>{{ section.settings.heading | escape }}</h2><div class="review-row"><button class="icon-button" data-review-prev aria-label="Previous testimonial">‹</button><div aria-live="polite">{% for block in section.blocks %}<blockquote {% unless forloop.first %}hidden{% endunless %} {{ block.shopify_attributes }}><p>“{{ block.settings.quote | escape }}”</p>{% if block.settings.author != blank %}<cite>{{ block.settings.author | escape }}</cite>{% endif %}</blockquote>{% endfor %}</div><button class="icon-button" data-review-next aria-label="Next testimonial">›</button></div></section>
''',[setting('text','heading','Heading','Real People. Real Results.')],[dict(type='review',name='Testimonial',settings=[setting('textarea','quote','Quote'),setting('text','author','Author')])])

section('cellulaire-contact','Cellulaire contact','''
<section class="contact-section wrap inset"><aside class="contact-details"><h2>Get in Touch</h2><p>Reach out through any of the channels below.<br>Our team will respond as soon as possible.</p>
  {% if section.settings.email != blank %}<a class="contact-channel" href="mailto:{{ section.settings.email | escape }}">{% render 'cellulaire-icon', name: 'mail' %}<span><strong>Customer Care</strong>{{ section.settings.email | escape }}</span><span class="mobile-only">›</span></a>{% endif %}
  {% if section.settings.phone != blank %}<a class="contact-channel" href="tel:{{ section.settings.phone | remove: ' ' | escape }}">{% render 'cellulaire-icon', name: 'phone' %}<span><strong>Phone Support</strong>{{ section.settings.phone | escape }}</span><span class="mobile-only">›</span></a>{% endif %}
  {% if section.settings.whatsapp != blank %}<a class="contact-channel" href="{{ section.settings.whatsapp }}">{% render 'cellulaire-icon', name: 'whatsapp' %}<span><strong>WhatsApp</strong>Chat with us</span><span class="mobile-only">›</span></a>{% endif %}
  <div class="contact-channel">{% render 'cellulaire-icon', name: 'clock' %}<span><strong>Working Hours</strong>{{ section.settings.hours | escape | newline_to_br }}</span></div>
  <div class="contact-note"><strong>A More Radiant You</strong><p>We're always here to support your skincare journey.</p></div>
</aside><div class="contact-form-column"><h2>Send Us a Message</h2><p>Fill out the form below and we'll get back to you shortly.</p>
{% form 'contact', id: 'ContactForm', class: 'contact-form' %}
  {% if form.posted_successfully? %}<p class="form-success" role="status" tabindex="-1">Thank you. Your message has been sent.</p>{% endif %}
  {% if form.errors %}<div class="form-error" role="alert">{{ form.errors | default_errors }}</div>{% endif %}
  <div class="form-two"><label class="sr-only" for="ContactName">Full Name (required)</label><input id="ContactName" name="contact[name]" autocomplete="name" placeholder="Full Name *" value="{{ form.name | default: customer.name | escape }}" required>
  <label class="sr-only" for="ContactEmail">Email Address (required)</label><input id="ContactEmail" type="email" name="contact[email]" autocomplete="email" placeholder="Email Address *" value="{{ form.email | default: customer.email | escape }}" required {% if form.errors contains 'email' %}aria-invalid="true"{% endif %}></div>
  <label class="sr-only" for="ContactPhone">Phone Number</label><input id="ContactPhone" type="tel" name="contact[phone]" autocomplete="tel" placeholder="Phone Number" value="{{ form.phone | escape }}">
  <label class="sr-only" for="ContactSubject">Subject (required)</label><select id="ContactSubject" name="contact[Subject]" required><option value="" disabled selected>Subject * — Select a topic</option><option>Order Support</option><option>Product Questions</option><option>Wholesale</option><option>Collaborations</option><option>Other</option></select>
  <div class="message-field"><label class="sr-only" for="ContactMessage">Your Message (required)</label><textarea id="ContactMessage" name="contact[body]" placeholder="Your Message *&#10;Tell us how we can help…" rows="6" maxlength="500" data-message required>{{ form.body | escape }}</textarea><span data-counter>0/500</span></div>
  <button type="submit" class="button">Send message <span>→</span></button>
{% endform %}
<div class="inquiry-grid">{% assign topics = 'Order Support,Product Questions,Wholesale,Collaborations' | split: ',' %}{% assign icons = 'truck,bottle,people,heart' | split: ',' %}{% assign descriptions = 'Track your order, shipping or returns.|Find the right formula for your skin.|Partnership and retail inquiries.|Press, creators and brand opportunities.' | split: '|' %}{% assign labels = 'Get help,Ask a question,Learn more,Get in touch' | split: ',' %}{% for topic in topics %}<button data-topic="{{ topic }}" type="button">{% assign icon = icons[forloop.index0] %}{% render 'cellulaire-icon', name: icon %}<strong>{{ topic }}</strong><span class="desktop-only">{{ descriptions[forloop.index0] }}</span><span class="text-link desktop-only">{{ labels[forloop.index0] }} →</span></button>{% endfor %}</div>
</div></section>
''',[setting('text','email','Customer care email','hello@cellulaire.com'),setting('text','phone','Phone number'),setting('url','whatsapp','WhatsApp link'),setting('textarea','hours','Working hours','Mon – Fri, 9AM – 6PM (EST)\nSat – Sun, 10AM – 4PM (EST)')])
section('cellulaire-faq','Cellulaire FAQ','''
<section class="faq-section wrap inset"><div class="section-heading"><div>{% if page.handle == 'faq' %}<h1>{{ section.settings.heading | escape }}</h1>{% else %}<h2>{{ section.settings.heading | escape }}</h2>{% endif %}<p>Quick answers to our most common questions.</p></div>{% unless request.page_type == 'page' and page.handle == 'faq' %}<a class="text-link" href="{{ routes.root_url }}pages/faq">View all FAQs →</a>{% endunless %}</div><div class="faq-grid">{% for block in section.blocks %}<details {{ block.shopify_attributes }}><summary>{{ block.settings.question | escape }}<span class="faq-plus">+</span></summary><div class="rte">{{ block.settings.answer }}</div></details>{% endfor %}</div></section>
''',[setting('text','heading','Heading','Frequently Asked Questions')],[dict(type='question',name='Question',settings=[setting('text','question','Question'),setting('richtext','answer','Answer')])])

section('cellulaire-collection','Cellulaire collection','''
<section class="wrap inset shop-section"><p class="eyebrow">Our signature collection</p><h1>{{ collection.title | escape }}</h1><div class="rte">{{ collection.description }}</div>
{% paginate collection.products by 24 %}<form class="collection-controls" method="get"><label for="SortBy">Sort by</label><select id="SortBy" name="sort_by">{% for option in collection.sort_options %}<option value="{{ option.value }}" {% if option.value == collection.sort_by %}selected{% endif %}>{{ option.name | escape }}</option>{% endfor %}</select><button class="button button-outline" type="submit">Apply</button><span>{{ collection.products_count }} products</span></form>
<div class="product-grid shop-grid">{% for product in collection.products %}{% render 'cellulaire-product-card', product: product, fallback: 'cellulaire-product-night.webp' %}{% else %}<p>No products in this collection yet.</p>{% endfor %}</div>{% if paginate.pages > 1 %}<nav class="pagination" aria-label="Pagination">{{ paginate | default_pagination }}</nav>{% endif %}{% endpaginate %}
</section>
''')
section('cellulaire-product','Cellulaire product','''
<section class="wrap inset product-section"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{{ routes.root_url }}">Home</a> / <a href="{{ routes.all_products_collection_url }}">Face Mists</a> / {{ product.title | escape }}</nav>
<div class="product-layout"><div class="product-gallery">{% assign current_variant = product.selected_or_first_available_variant %}{% assign main_image = current_variant.featured_image | default: product.featured_image %}{% if main_image != blank %}{{ main_image | image_url: width: 1400 | image_tag: widths: '400, 800, 1400', sizes: '(min-width: 750px) 50vw, 100vw', alt: product.title, data-main-image: '', loading: 'eager' }}{% else %}{% capture bundled_photo %}{% render 'cellulaire-product-asset', product: product %}{% endcapture %}{% assign bundled_photo = bundled_photo | strip %}{% if bundled_photo != blank %}{% render 'cellulaire-image', fallback: bundled_photo, alt: product.title, main: true, loading: 'eager' %}{% endif %}{% endif %}<div class="thumbnails">{% for image in product.images %}<button type="button" data-thumbnail="{{ image | image_url: width: 1400 }}" aria-label="View image {{ forloop.index }}" aria-pressed="{% if image == main_image %}true{% else %}false{% endif %}">{{ image | image_url: width: 160 | image_tag: alt: image.alt, loading: 'lazy' }}</button>{% endfor %}</div></div>
<div class="product-information"><p class="eyebrow">{{ product.vendor | escape }}</p><h1>{{ product.title | escape }}</h1><p>{{ product.metafields.custom.short_description | escape }}</p><p class="product-price"><span data-product-price>{{ current_variant.price | money }}</span>{% if current_variant.compare_at_price > current_variant.price %} <s>{{ current_variant.compare_at_price | money }}</s>{% endif %}</p><div class="rte">{{ product.description }}</div>
{% form 'product', product, data-product-form: '' %}<input type="hidden" name="id" value="{{ current_variant.id }}">
{% unless product.has_only_default_variant %}{% for option in product.options_with_values %}<label for="Option-{{ section.id }}-{{ forloop.index }}">{{ option.name | escape }}</label><select id="Option-{{ section.id }}-{{ forloop.index }}" data-option>{% for value in option.values %}<option value="{{ value | escape }}" {% if value.selected %}selected{% endif %}>{{ value | escape }}</option>{% endfor %}</select>{% endfor %}{% endunless %}
<script type="application/json" data-variants>{{ product.variants | json }}</script><label for="Quantity-{{ section.id }}">Quantity</label><input id="Quantity-{{ section.id }}" name="quantity" type="number" value="1" min="1" step="1">
<button class="button" type="submit" {% unless current_variant.available %}disabled{% endunless %}>{% if current_variant.available %}Add to bag{% else %}Sold out{% endif %}</button><p data-form-status role="status"></p>{{ form | payment_terms }}{% endform %}
{% if section.settings.shipping != blank %}<details class="product-disclosure"><summary>Shipping & returns</summary><div class="rte">{{ section.settings.shipping }}</div></details>{% endif %}
{% if product.metafields.custom.ingredients != blank %}<details class="product-disclosure"><summary>Ingredients</summary><div class="rte">{{ product.metafields.custom.ingredients | metafield_tag }}</div></details>{% endif %}
{% if product.metafields.custom.how_to_use != blank %}<details class="product-disclosure"><summary>How to use</summary><div class="rte">{{ product.metafields.custom.how_to_use | metafield_tag }}</div></details>{% endif %}
</div></div><div class="section-heading"><h2>Complete your ritual</h2><a class="text-link" href="{{ routes.all_products_collection_url }}">View all →</a></div><div class="product-grid">{% for related in collections.all.products limit: 5 %}{% unless related.id == product.id %}{% render 'cellulaire-product-card', product: related, fallback: 'cellulaire-product-night.webp' %}{% endunless %}{% endfor %}</div></section>
<script type="application/ld+json">{{ product | structured_data }}</script>
''',[setting('richtext','shipping','Shipping and returns information')])
section('cellulaire-cart','Cellulaire shopping bag','''
<section class="wrap inset cart-section"><h1>Your Bag <span>({{ cart.item_count }})</span></h1>{% if cart.item_count > 0 %}<form action="{{ routes.cart_url }}" method="post" id="CartForm"><div class="cart-layout"><div class="cart-lines">{% for item in cart.items %}<article class="cart-line"><a href="{{ item.url }}">{% capture bundled_photo %}{% render 'cellulaire-product-asset', product: item.product %}{% endcapture %}{% assign bundled_photo = bundled_photo | strip %}{% if item.image != blank or bundled_photo != blank %}{% render 'cellulaire-image', image: item.image, fallback: bundled_photo, alt: item.product.title, width: 120, height: 135 %}{% endif %}</a><div><h2><a href="{{ item.url }}">{{ item.product.title | escape }}</a></h2>{% unless item.product.has_only_default_variant %}<p>{{ item.variant.title | escape }}</p>{% endunless %}{% for property in item.properties %}{% assign first_character = property.first | slice: 0 %}{% if property.last != blank and first_character != '_' %}<p>{{ property.first | escape }}: {{ property.last | escape }}</p>{% endif %}{% endfor %}<p>{{ item.final_price | money }}</p><label for="CartQuantity-{{ forloop.index }}">Quantity</label><input id="CartQuantity-{{ forloop.index }}" type="number" name="updates[]" value="{{ item.quantity }}" min="0" step="1"><a class="text-link" href="{{ routes.cart_change_url }}?id={{ item.key | url_encode }}&quantity=0">Remove</a></div><p>{{ item.final_line_price | money }}</p></article>{% endfor %}<button type="submit" name="update" class="button button-outline">Update bag</button><a class="text-link" href="{{ routes.all_products_collection_url }}">Continue shopping →</a></div><aside class="cart-summary"><h2>Order Summary</h2>{% for discount in cart.cart_level_discount_applications %}<p>{{ discount.title | escape }} <span>−{{ discount.total_allocated_amount | money }}</span></p>{% endfor %}<p>Subtotal <strong>{{ cart.total_price | money }}</strong></p><p>Shipping and taxes calculated at checkout.</p><label for="CartNote">Order note</label><textarea id="CartNote" name="note" rows="3">{{ cart.note | escape }}</textarea><button type="submit" name="checkout" class="button">Checkout →</button></aside></div></form>{% else %}<div class="empty-state"><h2>Your next ritual starts here.</h2><p>Your shopping bag is empty.</p><a class="button" href="{{ routes.all_products_collection_url }}">Discover face mists →</a></div>{% endif %}</section>
''')
section('cellulaire-search','Cellulaire search','''
<section class="wrap inset search-section"><h1>Find Your Ritual</h1><form action="{{ routes.search_url }}" method="get" role="search" class="search-form"><label class="sr-only" for="SearchTerms">Search products and stories</label><input id="SearchTerms" type="search" name="q" value="{{ search.terms | escape }}" placeholder="Search products and stories" required><input type="hidden" name="options[prefix]" value="last"><button class="button" type="submit">Search →</button></form>{% if search.performed %}<p>{{ search.results_count }} results for “{{ search.terms | escape }}”</p>{% paginate search.results by 24 %}<div class="product-grid shop-grid">{% for result in search.results %}{% if result.object_type == 'product' %}{% render 'cellulaire-product-card', product: result, fallback: 'cellulaire-product-night.webp' %}{% else %}<article class="search-result"><p class="eyebrow">{{ result.object_type }}</p><h2><a href="{{ result.url }}">{{ result.title | escape }}</a></h2><p>{{ result.content | strip_html | truncate: 160 }}</p><a class="text-link" href="{{ result.url }}">Read more →</a></article>{% endif %}{% else %}<p>No results found. Try another search.</p>{% endfor %}</div>{% if paginate.pages > 1 %}{{ paginate | default_pagination }}{% endif %}{% endpaginate %}{% endif %}</section>
''')
section('cellulaire-page','Cellulaire page','''
{% if section.settings.show_heading or page.content != blank %}<section class="wrap inset prose-section">{% if section.settings.show_heading %}<h1>{{ page.title | escape }}</h1>{% endif %}<div class="rte">{{ page.content }}</div></section>{% endif %}
''',[setting('checkbox','show_heading','Show page heading',True)])
section('cellulaire-blog','Cellulaire journal','''
<section class="wrap inset journal-section"><p class="eyebrow">Science. Beauty. Confidence.</p><h1>{{ blog.title | escape }}</h1>{% paginate blog.articles by 12 %}<div class="journal-grid">{% for article in blog.articles %}<article>{% if article.image != blank %}<a href="{{ article.url }}">{{ article.image | image_url: width: 900 | image_tag: alt: article.title, loading: 'lazy' }}</a>{% endif %}<p class="eyebrow">{{ article.published_at | date: '%B %d, %Y' }}</p><h2><a href="{{ article.url }}">{{ article.title | escape }}</a></h2><p>{{ article.excerpt_or_content | strip_html | truncate: 180 }}</p><a class="text-link" href="{{ article.url }}">Read story →</a></article>{% else %}<p>Stories from Cellulaire will appear here.</p>{% endfor %}</div>{% if paginate.pages > 1 %}{{ paginate | default_pagination }}{% endif %}{% endpaginate %}</section>
''')
section('cellulaire-article','Cellulaire article','''
<article class="wrap inset prose-section"><a class="text-link" href="{{ blog.url }}">← The Journal</a><p class="eyebrow">{{ article.published_at | date: '%B %d, %Y' }}</p><h1>{{ article.title | escape }}</h1>{% if article.image != blank %}{{ article.image | image_url: width: 1600 | image_tag: alt: article.title, loading: 'eager' }}{% endif %}<div class="rte">{{ article.content }}</div></article>
''')
section('cellulaire-404','Cellulaire not found','''
<section class="wrap inset empty-state"><p class="eyebrow">404</p><h1>A little off the ritual.</h1><p>We couldn't find this page.</p><a href="{{ routes.all_products_collection_url }}" class="button">Discover the collection →</a></section>
''')
section('cellulaire-collections','Cellulaire collections','''
<section class="wrap inset shop-section"><h1>Shop by Collection</h1><div class="journal-grid">{% for collection in collections %}<article><a href="{{ collection.url }}">{% if collection.image != blank %}{{ collection.image | image_url: width: 800 | image_tag: alt: collection.title, loading: 'lazy' }}{% endif %}<h2>{{ collection.title | escape }}</h2></a></article>{% endfor %}</div></section>
''')

def item(id,type,settings={},blocks=None):
    data={'settings':settings}
    if blocks:data.update(blocks={str(i):block for i,block in enumerate(blocks)},block_order=[str(i) for i in range(len(blocks))])
    return (id,type,data)
def block(type,**settings):return dict(type=type,settings=settings)
products=[block('product',handle=name+'-face-mist',title=title+' Face Mist',description=description,fallback='cellulaire-product-'+name+'.webp') for name,title,description in [('night','Night Care','Repair. Renew. Rebalance.'),('hydration','Hydration','Refresh. Hydrate. Plump.'),('sun','Sun Protection','Defend. Soothe. Glow.'),('brightening','Brightening','Even. Brighten. Illuminate.')]]
needs=[block('need',handle=name,heading=title,description=desc,fallback='cellulaire-need-'+name+'.webp',tone=name) for name,title,desc in [('night','Night Care','Repair & renew'),('hydration','Hydration','Refresh & plump'),('sun','Sun Protection','Defend & glow'),('brightening','Brightening','Even & radiate')]]
values=[block('value',icon=icon,heading=title,description=desc) for icon,title,desc in [('science','Science','Backed by research and powered by proven ingredients for visible results.'),('leaf','Precision','Thoughtfully formulated with clean, effective ingredients and exacting standards.'),('diamond','Experience','A refined, sensorial ritual that turns everyday skincare into a luxury experience.')]]
faq=[block('question',question=q,answer=a) for q,a in [('Where is my order?','<p>Use the tracking link in your shipping confirmation email. For help, contact our Customer Care team with your order number.</p>'),('What is your return policy?','<p>Please review the store’s return policy or contact Customer Care before sending your order back.</p>'),('Which Face Mist is right for me?','<p>Explore Night Care, Hydration, Sun Protection and Brightening in our collection, or ask our team for product guidance.</p>'),('How long does shipping take?','<p>Available delivery methods and estimates are shown at checkout. Your shipping confirmation includes tracking details.</p>'),('Do you offer international shipping?','<p>Enter your delivery address at checkout to see available shipping options for your country.</p>'),('Can I become a stockist or partner?','<p>Choose Wholesale or Collaborations in our contact form and tell us about your business.</p>')]]
cta=item('collection_cta','cellulaire-editorial',dict(layout='cta',eyebrow='',heading='Discover the\nComplete Collection',description='Science-backed skincare for real results.',button_label='Shop all products',fallback='cellulaire-story.webp',aside='More\nthan skincare\na brighter you'))
template('index',[
 item('hero','cellulaire-hero',dict(composite_desktop=True,composite_mobile=True,mobile_composite_fallback='cellulaire-hero-mobile.webp')),item('benefits','cellulaire-benefits',blocks=[block('benefit',icon=icon,text=text) for icon,text in [('drop','Science-backed\nformulas'),('leaf','Premium, clean\ningredients'),('diamond','Visible results,\neveryday'),('heart','A ritual\nof self-care')]]),
 item('skin_needs','cellulaire-skin-needs',blocks=needs),item('best_sellers','cellulaire-products',blocks=products),
 item('story','cellulaire-editorial',dict(button_link='/pages/our-story')),item('routine','cellulaire-routine'),
 item('reviews','cellulaire-reviews',blocks=[block('review',quote='My skin feels so refreshed and balanced. These mists are a daily essential!',author='')]),cta])
template('page.our-story',[
 item('hero','cellulaire-hero',dict(composite_desktop=True,composite_fallback='cellulaire-about-banner.webp',composite_mobile=True,mobile_composite_fallback='cellulaire-about-mobile-banner.webp',variant='about',eyebrow='About Cellulaire',heading='Where Science\nMeets Luxury',description='Exceptional skincare begins with exceptional science. We create high-performance, sensorial skincare that delivers visible results — and a more confident you.',button_label='Our story',button_link='#our-story',fallback='cellulaire-about-hero.webp',mobile_fallback='cellulaire-about-mobile.webp')),
 item('our_story','cellulaire-editorial',dict(layout='about-story',anchor='our-story',inset=True,eyebrow='Our Story',small_eyebrow=True,heading='A Higher Standard\nfor Everyday Skincare',description='Cellulaire was born from a simple belief: exceptional skincare begins with exceptional science. Every product is developed through a thoughtful process that combines advanced research, carefully selected ingredients, and uncompromising quality standards. We create skincare that balances performance with elegance — because true luxury is confidence that comes from within.',button_label='Our story',button_link='#our-story',fallback='cellulaire-woman.webp',mobile_fallback='cellulaire-woman-mobile.webp',composite_image=True,image_alt='A moment of self-care',overlay='More\nThan Skincare.\nA Brighter You.',aside='')),
 item('values','cellulaire-values',blocks=values),item('formulas','cellulaire-editorial',dict(layout='formulas',eyebrow='',heading='Elevated Formulas.\nReal Results.',description='From our signature Face Mists to every skincare essential, each formula is designed to deliver effective performance while offering a luxurious, sensorial experience.',button_label='Discover our formulas',button_link='/pages/science',fallback='cellulaire-formulas.webp',mobile_fallback='cellulaire-formulas-mobile.webp',aside='Same\nexceptional\nscience\na brighter you')),
 item('mission','cellulaire-editorial',dict(layout='mission',inset=True,eyebrow='Our Mission',small_eyebrow=True,heading='Skincare That Inspires\nConfidence, Every Day',description='We are committed to creating innovative, high-quality skincare that helps you look and feel your best. Through science, integrity and a passion for excellence, we strive to make luxury skincare a part of everyday life — for everyone.',button_label='',fallback='cellulaire-texture.webp',image_alt='A refined skincare texture',aside='')),
 item('collection','cellulaire-products',dict(eyebrow='Our Signature Collection',heading='The Face Mist Collection',description='Four targeted formulas. One elevated routine.',compact=True),blocks=[products[i] for i in [0,3,2,1]]),cta])
template('page.contact',[
 item('hero','cellulaire-hero',dict(composite_desktop=True,composite_fallback='cellulaire-contact-banner.webp',variant='contact',eyebrow='Contact Us',heading='We’re Here\nfor Your Skin',description='Our team is here to help. Whether you have a question about your order, need product advice, or simply want to learn more about Cellulaire, we’d love to hear from you.',button_label='',fallback='cellulaire-contact-hero.webp',mobile_fallback='cellulaire-contact-mobile.webp')),
 item('contact','cellulaire-contact'),item('faq','cellulaire-faq',blocks=faq),cta])
template('page.faq',[item('faq','cellulaire-faq',blocks=faq),cta])
template('page.science',[item('hero','cellulaire-hero',dict(variant='about',eyebrow='Our Science',heading='Elevated Formulas.\nReal Results.',description='Every formula begins with research, carefully selected ingredients, and an uncompromising commitment to quality.',button_label='Explore face mists',fallback='cellulaire-about-hero.webp',mobile_fallback='cellulaire-about-mobile.webp')),item('values','cellulaire-values',blocks=values),item('content','cellulaire-page',dict(show_heading=False)),cta])
for name,type in [('collection','collection'),('product','product'),('cart','cart'),('search','search'),('page','page'),('blog','blog'),('article','article'),('404','404'),('list-collections','collections')]:template(name,[item('main','cellulaire-'+type)])
