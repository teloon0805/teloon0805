"""Original, self-contained SVG artwork for E7ian's profile."""
import html
import math
from pathlib import Path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
FONT_DIR = Path('C:/Windows/Fonts')
FONTS = [TTFont(FONT_DIR/'bahnschrift.ttf'), TTFont(FONT_DIR/'msyh.ttc',fontNumber=0), TTFont(FONT_DIR/'consola.ttf')]

class Art:
    def __init__(self,w,h,title,description):
        self.w,self.h,self.title,self.description=w,h,title,description
        self.parts=[]
        self.glyphs={}
    def add(self,value):
        self.parts.append(value)
    def text(self,value,x,y,size,color='#eaf7fb',face=0,tracking=0):
        font=FONTS[face]; cmap=font.getBestCmap(); glyphset=font.getGlyphSet(); scale=size/font['head'].unitsPerEm
        uses=[]
        for character in value:
            name=cmap.get(ord(character),'.notdef'); key=f'f{face}-{font.getGlyphID(name)}'
            if key not in self.glyphs:
                pen=SVGPathPen(glyphset); glyphset[name].draw(pen); self.glyphs[key]=pen.getCommands()
            uses.append(f'<use href="#{key}" transform="translate({x:.3f} {y:.3f}) scale({scale:.6f} {-scale:.6f})"/>')
            x+=glyphset[name].width*scale+tracking
        self.add(f'<g fill="{color}" aria-label="{html.escape(value,quote=True)}">'+''.join(uses)+'</g>')
    def save(self,name):
        defs=''.join(f'<path id="{k}" d="{v}"/>' for k,v in self.glyphs.items())
        source=f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(self.title)}</title><desc id="desc">{html.escape(self.description)}</desc><defs>{defs}</defs>'+''.join(self.parts)+'</svg>\n'
        (OUT/name).write_text(source,encoding='utf-8')

def terrain(u,v,x,y,w,h):
    ridge=math.sin(u*7.2+v*2)*.23+math.sin(u*14-v*4)*.10+math.exp(-((u-.62)**2/.025+(v-.42)**2/.2))*.8
    return x+u*w+(v-.5)*w*.12,y+v*h-ridge*h*.52

def poly(points):
    return ' '.join(f'{x:.2f},{y:.2f}' for x,y in points)

def mesh(a,x,y,w,h,rows=17,cols=29):
    for i in range(rows):
        v=i/(rows-1); points=[terrain(j/70,v,x,y,w,h) for j in range(71)]
        a.add(f'<polyline points="{poly(points)}" fill="none" stroke="#41cebf" stroke-width="{.7+v*.55:.2f}" opacity="{.14+v*.35:.2f}"/>')
    for j in range(cols):
        points=[terrain(j/(cols-1),i/35,x,y,w,h) for i in range(36)]
        a.add(f'<polyline points="{poly(points)}" fill="none" stroke="#54adcf" stroke-width=".75" opacity=".24"/>')

def hero(animated):
    a=Art(1280,480,'E7ian · 田承龙','深海科技主题。曲阜师范大学软件工程本科，已保研至西安电子科技大学电子工程学院，2027年9月入学。右侧为原创海底地形与声呐扫描示意。')
    style='@keyframes sweep{to{transform:rotate(360deg)}}@keyframes pulse{0%,100%{opacity:.18}50%{opacity:.95}}.scan{animation:sweep 22s linear infinite}.echo{animation:pulse 5s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.scan,.echo{animation:none}}' if animated else ''
    a.add('''<defs>
    <radialGradient id="ocean" cx="83%" cy="0%" r="100%"><stop stop-color="#123e52"/><stop offset=".55" stop-color="#071e2d"/><stop offset="1" stop-color="#03111d"/></radialGradient>
    <linearGradient id="beam" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#72ffe8" stop-opacity=".27"/><stop offset="1" stop-color="#72ffe8" stop-opacity="0"/></linearGradient>
    <clipPath id="ocean-clip"><rect x="640" y="0" width="640" height="412"/></clipPath>
    <style>.scan{transform-origin:1000px 177px}.echo{opacity:.8}'''+style+'''</style></defs>
    <rect width="1280" height="480" rx="14" fill="url(#ocean)"/>
    <g clip-path="url(#ocean-clip)">
    <path d="M1090 0 670 415 1200 415Z" fill="url(#beam)" opacity=".20"/>
    <path d="M1180 0 980 412 1280 412Z" fill="url(#beam)" opacity=".17"/>
    <g fill="none" stroke="#6db8c9" stroke-width=".8" opacity=".17"><circle cx="1000" cy="177" r="48"/><circle cx="1000" cy="177" r="90"/><circle cx="1000" cy="177" r="132"/><path d="M845 177H1155M1000 22V332" stroke-dasharray="3 8"/></g>
    <g class="scan"><path d="M1000 177 1047 54A132 132 0 0 1 1132 177Z" fill="url(#beam)"/><path d="M1000 177H1132" stroke="#56e5d4" opacity=".6"/></g></g>''')
    mesh(a,710,240,560,167)
    for x,y,r in [(1041,115,3),(946,210,3),(1095,235,2)]:
        a.add(f'<g class="echo"><circle cx="{x}" cy="{y}" r="{r}" fill="#8ffff0"/><circle cx="{x}" cy="{y}" r="{r+7}" stroke="#56e5d4" fill="none" opacity=".3"/></g>')
    a.add('<path d="M56 55H78" stroke="#56e5d4" stroke-width="3"/><circle cx="1217" cy="55" r="3" fill="#56e5d4"/>')
    a.text('E7IAN / PERSONAL LOGBOOK',90,60,12,'#91b5c6',2,.8)
    a.text('E7ian',50,189,116,tracking=-2)
    a.text('田承龙',56,232,24,'#56e5d4',1)
    a.add('<path d="M150 213V235" stroke="#345666"/>')
    a.text('从海底地形，到视觉感知',170,231,20,'#b6d0da',1)
    a.text('水下视觉 · 遥感多模态 · 对抗鲁棒性',56,289,21,'#d5e9ee',1)
    a.text('西安电子科技大学 · 电子工程学院',56,339,19,'#a6c6d3',1)
    a.text('推免硕士 / 电子科学与技术 / 2027.09 入学',56,369,15,'#91b5c6',1)
    a.text('PERCEPTION',1115,61,10,'#71a4b7',2,1)
    a.text('BATHYMETRY',1090,392,10,'#83b8c1',2,1)
    a.add('<path d="M56 414H1224" stroke="#224451"/><path d="M56 414H144" stroke="#56e5d4" stroke-width="2"/>')
    a.text('曲阜师范大学 · 软件工程本科',56,447,14,'#91b5c6',1)
    a.text('KEEP EXPLORING THE UNKNOWN',975,447,11,'#91b5c6',2)
    a.save('hero.svg' if animated else 'hero-static.svg')

def focus():
    a=Art(1280,225,'研究主线','水下视觉与目标识别、遥感多模态大模型、对抗攻击与模型鲁棒性。')
    a.add('<rect width="1280" height="225" rx="12" fill="#061b28"/><path d="M427 28V197M853 28V197" stroke="#23404e"/>')
    items=[('01 / UNDERWATER','水下视觉与目标识别','UNDERWATER PERCEPTION','在复杂水下环境中理解目标'),('02 / REMOTE SENSING','遥感多模态大模型','MULTIMODAL FOUNDATION MODELS','关注遥感场景中的多源信息融合'),('03 / ROBUSTNESS','对抗攻击与模型鲁棒性','ADVERSARIAL ROBUSTNESS','从航拍图像与对抗补丁问题出发')]
    for i,(tag,title,en,note) in enumerate(items):
        x=i*427+32
        a.text(tag,x,43,12,'#56e5d4',2)
        a.text(title,x,94,24,face=1)
        a.text(en,x,125,11.5,'#91b5c6',2)
        a.text(note,x,180,16,'#a9c6d2',1)
        a.add(f'<path d="M{x} 202H{x+40}" stroke="#56e5d4" opacity=".6"/>')
    a.save('research.svg')

def hero_mobile(animated):
    a=Art(720,690,'E7ian · 田承龙','移动版深海科技头图。已保研至西安电子科技大学，2027年9月入学。原创海底地形与声呐扫描示意。')
    style='@keyframes sweep{to{transform:rotate(360deg)}}.scan{animation:sweep 22s linear infinite}@media(prefers-reduced-motion:reduce){.scan{animation:none}}' if animated else ''
    a.add('<defs><radialGradient id="sea" cx="90%" cy="70%" r="85%"><stop stop-color="#124351"/><stop offset="1" stop-color="#03111d"/></radialGradient><style>.scan{transform-origin:560px 480px}'+style+'</style><clipPath id="mesh-clip"><rect x="0" y="360" width="720" height="245"/></clipPath></defs><rect width="720" height="690" rx="14" fill="url(#sea)"/>')
    a.add('<path d="M40 49H61" stroke="#56e5d4" stroke-width="3"/>')
    a.text('E7IAN / PERSONAL LOGBOOK',75,54,13,'#91b5c6',2,.7)
    a.text('E7ian',33,192,132,tracking=-2)
    a.text('田承龙',40,248,31,'#56e5d4',1)
    a.text('从海底地形，到视觉感知',40,300,24,'#c3dce6',1)
    a.text('水下视觉 · 遥感多模态 · 对抗鲁棒性',40,352,24,'#d5e9ee',1)
    a.add('<g clip-path="url(#mesh-clip)"><g fill="none" stroke="#6db8c9" opacity=".2"><circle cx="560" cy="480" r="60"/><circle cx="560" cy="480" r="108"/></g><g class="scan"><path d="M560 480H668" stroke="#56e5d4" opacity=".7"/><path d="M560 480 636 404A108 108 0 0 1 668 480Z" fill="#56e5d4" opacity=".07"/></g>')
    mesh(a,20,430,700,145,13,26)
    a.add('</g><path d="M40 589H680" stroke="#23404e"/>')
    a.text('西安电子科技大学 · 电子工程学院',40,630,22,'#b6d0da',1)
    a.text('推免硕士 / 电子科学与技术 / 2027.09 入学',40,663,18,'#91b5c6',1)
    a.save('hero-mobile.svg' if animated else 'hero-mobile-static.svg')

def focus_mobile():
    a=Art(720,600,'研究主线','水下视觉与目标识别、遥感多模态大模型、对抗攻击与模型鲁棒性。')
    a.add('<rect width="720" height="600" rx="12" fill="#061b28"/><path d="M40 200H680M40 400H680" stroke="#23404e"/>')
    items=[('01 / UNDERWATER','水下视觉与目标识别','UNDERWATER PERCEPTION'),('02 / REMOTE SENSING','遥感多模态大模型','MULTIMODAL FOUNDATION MODELS'),('03 / ROBUSTNESS','对抗攻击与模型鲁棒性','ADVERSARIAL ROBUSTNESS')]
    for i,(tag,title,en) in enumerate(items):
        y=i*200
        a.text(tag,40,y+48,18,'#56e5d4',2)
        a.text(title,40,y+108,34,face=1)
        a.text(en,40,y+151,18,'#91b5c6',2)
    a.save('research-mobile.svg')

def multibeam():
    a=Art(1280,360,'覆盖感知自适应分区与多波束测线规划','原创方法示意。论文匿名真实海底案例中的几何覆盖率98.81%，漏测率1.19%，测线总长449.33公里。图形不是实际海域或模型预测。')
    a.add('<defs><linearGradient id="mb-bg" x2="1" y2=".4"><stop stop-color="#092332"/><stop offset="1" stop-color="#041420"/></linearGradient><clipPath id="terrain-clip"><rect x="30" y="136" width="646" height="178"/></clipPath></defs><rect width="1280" height="360" rx="12" fill="url(#mb-bg)"/><path d="M708 50V300" stroke="#23404e"/>')
    a.text('SELECTED WORK / 01',40,42,12,'#56e5d4',2,.8)
    a.text('复杂海底地形的多波束测线规划',40,88,28,face=1)
    a.text('覆盖感知 · 自适应分区 · 测线布设',40,119,15,'#91b5c6',1)
    a.add('<g clip-path="url(#terrain-clip)">')
    mesh(a,48,169,590,130,14,28)
    for j in range(7):
        u=.10+.12*j;points=[terrain(u+.012*math.sin(v*8),v,48,169,590,130) for v in [i/30 for i in range(31)]]
        color=['#8bf4dc','#5ebae7','#b5dbba'][j//3]
        a.add(f'<polyline points="{poly(points)}" fill="none" stroke="{color}" stroke-width="2.1" opacity=".9"/>')
    a.add('</g>')
    a.text('98.81',751,155,54,'#7df0d8');a.text('%',916,155,24,'#7df0d8')
    a.text('几何覆盖率',754,190,17,'#b6d0da',1)
    a.text('1.19',1002,155,54,'#a5d1ee');a.text('%',1134,155,24,'#a5d1ee')
    a.text('漏测率',1005,190,17,'#b6d0da',1)
    a.text('449.33',752,264,36);a.text('km',922,264,18,'#91b5c6',2)
    a.text('总测线长度',1005,260,17,'#b6d0da',1)
    a.add('<path d="M40 313H1240" stroke="#23404e"/>')
    a.text('论文匿名海底案例 · 几何覆盖口径；左侧为原创方法示意',40,339,13,'#91b5c6',1)
    a.save('multibeam-overview.svg')

def contact():
    a=Art(283,38,'邮件联系','13774949997@163.com')
    a.add('<rect x=".5" y=".5" width="282" height="37" rx="6" fill="#092633" stroke="#2c5b66"/><path d="M16 12H34V26H16ZM16 13 25 20 34 13" fill="none" stroke="#7df0d8" stroke-width="1.5"/>')
    a.text('13774949997@163.com',46,25,16,'#d6efef',2);a.save('contact.svg')

def multibeam_mobile():
    a=Art(720,650,'多波束测深论文案例','原创示意地形。论文匿名海底案例几何覆盖率98.81%，漏测率1.19%，测线总长449.33公里。')
    a.add('<defs><clipPath id="terrain-clip"><rect x="0" y="145" width="720" height="220"/></clipPath></defs><rect width="720" height="650" rx="12" fill="#061b28"/>')
    a.text('SELECTED WORK / 01',40,47,16,'#56e5d4',2,.6)
    a.text('多波束测深测线规划',40,110,36,face=1)
    a.text('覆盖感知 · 自适应分区 · 测线布设',40,153,22,'#91b5c6',1)
    a.add('<g clip-path="url(#terrain-clip)">')
    mesh(a,35,206,650,150,13,28)
    for j in range(7):
        u=.10+.12*j;points=[terrain(u+.012*math.sin(v*8),v,35,206,650,150) for v in [i/30 for i in range(31)]]
        a.add(f'<polyline points="{poly(points)}" fill="none" stroke="#83e5d3" stroke-width="2.2"/>')
    a.add('</g><path d="M40 393H680" stroke="#23404e"/>')
    a.text('98.81%',40,477,65,'#7df0d8');a.text('1.19%',405,477,65,'#a5d1ee')
    a.text('几何覆盖率',43,519,24,'#b6d0da',1);a.text('漏测率',409,519,24,'#b6d0da',1)
    a.text('449.33 km',40,579,36);a.text('总测线长度',400,578,23,'#b6d0da',1)
    a.text('论文匿名海底案例；上方为原创方法示意',40,624,18,'#91b5c6',1)
    a.save('multibeam-mobile.svg')

def footer():
    a=Art(1280,85,'保持好奇，继续下潜。','E7ian · teloon0805')
    a.add('<rect width="1280" height="85" rx="10" fill="#041420"/>')
    points=[(x,44+math.sin(x/14)*14*math.exp(-((x-790)/110)**2)) for x in range(560,950,2)]
    a.add(f'<polyline points="{poly(points)}" fill="none" stroke="#56e5d4" opacity=".45"/>')
    a.text('保持好奇，继续下潜。',40,53,22,'#c3e2e9',1)
    a.text('E7ian / teloon0805',1020,50,14,'#91b5c6',2);a.save('footer.svg')

if __name__=='__main__':
    hero(True);hero(False);hero_mobile(True);hero_mobile(False);focus();focus_mobile();multibeam();multibeam_mobile();contact();footer()
    for path in sorted(OUT.glob('*.svg')): print(f'{path.name}: {path.stat().st_size:,} bytes')
