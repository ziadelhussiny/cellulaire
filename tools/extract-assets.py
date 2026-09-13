"""Extract reference imagery without generating substitute photographs."""
from pathlib import Path
import json
from PIL import Image
root = Path(__file__).resolve().parents[1]
source = root / 'tmp/reference/original'
assets = root / 'assets'
manifest = []
def crop(name, page, box):
    image = Image.open(source / page).convert('RGB').crop(box)
    image.save(assets / ('cellulaire-' + name + '.webp'), 'WEBP', quality=95)
    manifest.append({'asset': 'cellulaire-' + name + '.webp', 'source':page, 'box':box, 'size':image.size})
crop('hero', 'mockup-1.png', (593,75,1042,333))
crop('hero-mobile', 'mockup-1.png', (1097,99,1408,367))
crop('about-hero', 'mockup-2.png', (578,69,1014,308))
crop('about-mobile', 'mockup-2.png', (1075,345,1406,552))
crop('contact-hero', 'mockup-3.png', (654,76,1057,312))
crop('contact-mobile', 'mockup-3.png', (1115,95,1406,277))
crop('story', 'mockup-1.png', (598,837,885,1019))
crop('formulas', 'mockup-2.png', (594,641,879,806))
crop('woman', 'mockup-2.png', (349,315,639,493))
crop('woman-mobile', 'mockup-2.png', (1095,560,1386,675))
crop('woman-wide', 'mockup-1.png', (1097,797,1245,883))
crop('texture', 'mockup-2.png', (634,815,985,941))
crop('routine', 'mockup-1.png', (1108,920,1255,1005))
for name, x1, x2 in [('night',488,615),('hydration',622,748),('sun',755,882),('brightening',889,1016)]:
    crop('need-'+name, 'mockup-1.png', (x1,403,x2,498))
for name, x1, x2 in [('night',354,512),('hydration',520,677),('sun',686,841),('brightening',849,1005)]:
    crop('product-'+name, 'mockup-1.png', (x1,601,x2,735))
for i in [4,5,6,7,8,9,11,13]:
    crop('brand-'+str(i), 'brand-'+str(i)+'.jpeg', (0,0,1920,1080))
# Use the complete large logo from the branding slide, with the background
# converted to alpha while retaining the original letterforms.
logo = Image.open(source/'mockup-1.png').convert('RGB').crop((39,83,278,134))
gray = logo.convert('L')
alpha = gray.point(lambda v: max(0,min(255,(200-v)*2)))
result=Image.new('RGBA',logo.size,(0,0,0,0)); result.putalpha(alpha)
result.save(assets/'cellulaire-logo.png')
(root/'docs/asset-provenance.json').write_text(json.dumps(manifest,indent=2))
