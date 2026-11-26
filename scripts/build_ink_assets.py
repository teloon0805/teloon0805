"""Ink, paper, calligraphy and slow layered movement for E7ian's profile."""
import base64
import html
import math
import random
from pathlib import Path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
FONT_DIR=Path('C:/Windows/Fonts')
FONTS=[TTFont(FONT_DIR/'BOD_BI.TTF'),TTFont(FONT_DIR/'STXINGKA.TTF'),TTFont(FONT_DIR/'simkai.ttf'),TTFont(FONT_DIR/'consola.ttf'),TTFont(FONT_DIR/'BOD_R.TTF'),TTFont(FONT_DIR/'FZSTK.TTF')]
PAINT='data:image/jpeg;base64,'+base64.b64encode((OUT/'ink-landscape.jpg').read_bytes()).decode()
INK='#e4e7e6'
MUTED='#adb5b6'
RED='#737d81'

class Art:
    def __init__(self,w,h,title,description):
        self.w,self.h,self.title,self.description=w,h,title,description
        self.parts=[];self.glyphs={}
    def add(self,s):self.parts.append(s)
    def width(self,value,size,face=2,tracking=0):
        font=FONTS[face];cmap=font.getBestCmap();gs=font.getGlyphSet();scale=size/font['head'].unitsPerEm
        return sum(gs[cmap.get(ord(c),'.notdef')].width*scale+tracking for c in value)-tracking
    def text(self,value,x,y,size,color=INK,face=2,tracking=0,center=False,cls=''):
        if center:x-=self.width(value,size,face,tracking)/2
        font=FONTS[face];cmap=font.getBestCmap();gs=font.getGlyphSet();scale=size/font['head'].unitsPerEm
        uses=[]
        for c in value:
            name=cmap.get(ord(c),'.notdef');key=f'f{face}-{font.getGlyphID(name)}'
            if name=='.notdef':raise ValueError(f'Missing glyph {c!r} in font {face}')
            if key not in self.glyphs:
                pen=SVGPathPen(gs);gs[name].draw(pen);self.glyphs[key]=pen.getCommands()
            uses.append(f'<use href="#{key}" transform="translate({x:.3f} {y:.3f}) scale({scale:.6f} {-scale:.6f})"/>')
            x+=gs[name].width*scale+tracking
        self.add(f'<g class="{cls}" fill="{color}" aria-label="{html.escape(value,quote=True)}">'+''.join(uses)+'</g>')
    def save(self,name):
        glyphs=''.join(f'<path id="{k}" d="{v}"/>' for k,v in self.glyphs.items())
        source=f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(self.title)}</title><desc id="desc">{html.escape(self.description)}</desc><defs>{glyphs}</defs>'+''.join(self.parts)+'</svg>\n'
        (OUT/name).write_text(source,encoding='utf-8',newline='\n')

def paper(a,opacity=1,fit='xMidYMid slice'):
    a.add(f'<rect width="{a.w}" height="{a.h}" fill="#101619"/><image href="{PAINT}" width="{a.w}" height="{a.h}" preserveAspectRatio="{fit}" opacity="{opacity}"/>')

def ink_defs(a,animated=True):
    motion='''
    @keyframes turn{to{transform:rotate(360deg)}}
    @keyframes reverse-turn{to{transform:rotate(-360deg)}}
    @keyframes mist-drift{0%,100%{transform:translate(-18px,1px);opacity:.28}50%{transform:translate(24px,-5px);opacity:.54}}
    @keyframes mist-drift-back{0%,100%{transform:translate(12px,2px);opacity:.22}50%{transform:translate(-22px,7px);opacity:.43}}
    @keyframes water-flow{to{stroke-dashoffset:-180}}
    @keyframes ink-arrive{from{opacity:.48;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}}
    .orbit{animation:turn 40s linear infinite}.outer-orbit{animation:reverse-turn 82s linear infinite}
    .mist-a{animation:mist-drift 17s ease-in-out infinite}.mist-b{animation:mist-drift-back 23s ease-in-out infinite}
    .water{animation:water-flow 26s linear infinite}.title-ink{animation:ink-arrive 2.8s ease-out both}
    @media(prefers-reduced-motion:reduce){.orbit,.outer-orbit,.mist-a,.mist-b,.water,.title-ink{animation:none!important}}
    ''' if animated else ''
    a.add('''<defs>
    <filter id="dry-ink" x="-15%" y="-15%" width="130%" height="130%"><feTurbulence type="fractalNoise" baseFrequency=".045 .08" numOctaves="3" seed="17" result="grain"/><feDisplacementMap in="SourceGraphic" in2="grain" scale="3.5" xChannelSelector="R" yChannelSelector="G"/></filter>
    <filter id="soft-mist" x="-15%" y="-60%" width="130%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
    <linearGradient id="veil"><stop stop-color="#0c1114" stop-opacity=".24"/><stop offset=".52" stop-color="#0c1114" stop-opacity=".08"/><stop offset="1" stop-color="#0c1114" stop-opacity="0"/></linearGradient>
    <linearGradient id="mist-tone"><stop stop-color="#c8cfd1" stop-opacity="0"/><stop offset=".4" stop-color="#eff3f4"/><stop offset="1" stop-color="#d0d8da" stop-opacity="0"/></linearGradient>
    <style>.mist-a{opacity:.38}.mist-b{opacity:.28}'''+motion+'''</style></defs>''')

def seal(a,x,y,label='承龙',size=32):
    a.add(f'<g transform="translate({x} {y})" filter="url(#dry-ink)"><path d="M1 1 {size-1} 0 {size} {size+7} 0 {size+8}Z" fill="#737d81" opacity=".86"/><path d="M3 3H{size-3}V{size+4}H3Z" fill="none" stroke="#d3d9db" stroke-width=".7" opacity=".65"/></g>')
    if len(label)==2:
        a.text(label[0],x+size/2,y+17,16,'#f1f4f4',5,center=True)
        a.text(label[1],x+size/2,y+33,16,'#f1f4f4',5,center=True)
    else:a.text(label,x+size/2,y+size*.72,size*.65,'#f1f4f4',5,center=True)

def orbit(a,cx,cy,r=98):
    a.add(f'<g transform="translate({cx} {cy})">')
    # A brushed, off-register ring and finely spaced marks frame the ink form.
    rng=random.Random(8)
    for k in range(5):
        radius=r+42+k*2.2
        points=[]
        for j in range(139):
            t=(j/138*math.tau)+.07*k
            rr=radius+math.sin(t*5+k)*1.1+math.sin(t*13)*.5
            points.append((math.cos(t)*rr,math.sin(t)*rr))
        a.add('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+'" stroke="#b7bfc1" stroke-width=".5" fill="none" opacity=".24"/>')
    a.add('<g class="outer-orbit">')
    for j in range(8):
        angle=j*45+22.5
        a.add(f'<g transform="rotate({angle})" opacity=".56" stroke="#c7ced0" stroke-width="2">')
        for k in range(3):
            y=-r-29-k*5
            if (j>>k)&1:a.add(f'<path d="M-11 {y}H11"/>')
            else:a.add(f'<path d="M-11 {y}H-3M3 {y}H11"/>')
        a.add('</g>')
    a.add('</g>')
    a.add(f'<g class="outer-orbit"><path d="M{-r-24} -11 A{r+25} {r+25} 0 0 1 61 {-r-10}" fill="none" stroke="#b9c2c4" stroke-width="4.5" stroke-linecap="round" opacity=".26" filter="url(#dry-ink)"/>')
    for j in range(28):
        t=rng.uniform(0,math.tau);rr=rng.uniform(r+18,r+35);s=rng.uniform(.5,1.9)
        a.add(f'<ellipse cx="{math.cos(t)*rr:.2f}" cy="{math.sin(t)*rr:.2f}" rx="{s:.2f}" ry="{s*.5:.2f}" fill="#c4cbcd" opacity="{rng.uniform(.12,.34):.2f}"/>')
    a.add('</g><g class="orbit" filter="url(#dry-ink)">')
    a.add(f'<circle r="{r}" fill="#d6dbdc" fill-opacity=".8" stroke="#abb8bd" stroke-width=".7"/>')
    a.add(f'<path d="M0 {-r} A{r} {r} 0 0 1 0 {r} A{r/2} {r/2} 0 0 1 0 0 A{r/2} {r/2} 0 0 0 0 {-r}Z" fill="#192226" opacity=".96"/>')
    a.add(f'<circle cy="{-r/2}" r="{r*.125}" fill="#192226"/><circle cy="{r/2}" r="{r*.125}" fill="#d6dbdc"/>')
    a.add(f'<path d="M{-r*.69} {-r*.68} A{r*.98} {r*.98} 0 0 0 {-r*.92} {r*.31}" stroke="#abb5b9" stroke-width="2" fill="none" opacity=".35"/>')
    a.add('</g></g>')

def clouds(a,cx,cy,scale=1):
    a.add(f'<g transform="translate({cx} {cy}) scale({scale})" pointer-events="none"><g filter="url(#soft-mist)"><path class="mist-a" d="M-260 35C-210-3-139 54-80 29S36 4 107 34 217 59 273 14L273 62H-260Z" fill="url(#mist-tone)"/><path class="mist-b" d="M-265 74C-194 53-145 101-62 66S73 57 130 78 215 87 274 55L274 96H-265Z" fill="url(#mist-tone)"/></g></g>')

def water(a,x,y,width):
    a.add(f'<g transform="translate({x} {y})" fill="none" stroke="#b7c2c5" stroke-linecap="round">')
    for j in range(5):
        points=[(i/40*width,math.sin(i/40*math.pi*3+j*.58)*2.1+j*7) for i in range(41)]
        a.add(f'<polyline class="water" points="'+ ' '.join(f'{px:.2f},{py:.2f}' for px,py in points)+f'" stroke-width="{.7-j*.07}" opacity="{.22-j*.026}" stroke-dasharray="21 16 46 11 70 16"/>')
    a.add('</g>')

def hero(animated=True,mobile=False):
    w,h=(760,790) if mobile else (1440,600)
    a=Art(w,h,'田承龙 · E7ian','水墨山水与缓慢流动的云水。学历：本科曲阜师范大学软件工程，硕士西安电子科技大学电子科学与技术。双弧墨色为装饰构图。')
    paper(a);ink_defs(a,animated)
    a.add(f'<rect width="{w*.61}" height="{h}" fill="url(#veil)"/>')
    if mobile:
        a.text('E7ian',48,182,146,face=0,cls='title-ink')
        a.text('田承龙',59,259,61,face=1,cls='title-ink');seal(a,272,215,size=30)
        a.text('水下视觉 · 遥感多模态 · 模型鲁棒性',60,316,23,face=2)
        orbit(a,510,466,79);clouds(a,485,480,.85);water(a,45,592,645)
        a.text('本科  曲阜师范大学 · 软件工程',60,680,24,face=2)
        a.text('硕士  西安电子科技大学 · 电子科学与技术',60,724,23,face=2)
        a.text('RESEARCH  /  CREATION  /  LIFE',60,762,12,MUTED,4,1.4)
    else:
        a.text('E7ian',69,206,168,face=0,cls='title-ink')
        a.text('田承龙',85,292,66,face=1,cls='title-ink');seal(a,314,248,size=33)
        a.text('水下视觉 · 遥感多模态 · 模型鲁棒性',87,355,25,face=2)
        a.text('本科  曲阜师范大学 · 软件工程',87,429,24,face=2)
        a.text('硕士  西安电子科技大学 · 电子科学与技术',87,474,24,face=2)
        a.text('RESEARCH  /  CREATION  /  LIFE',89,537,12,MUTED,4,1.6)
        orbit(a,1060,262,107);clouds(a,1040,300,1.13);water(a,765,493,550)
        a.text('观',1339,108,32,'#b9c1c3',1,center=True)
        a.text('微',1339,146,32,'#b9c1c3',1,center=True)
        a.text('知',1339,196,32,'#b9c1c3',1,center=True)
        a.text('远',1339,234,32,'#b9c1c3',1,center=True)
    name='hero-mobile' if mobile else 'hero'
    a.save(name+('' if animated else '-static')+'.svg')

def research(mobile=False):
    a=Art(760,750,'研究主线','居中的行书研究标题：水下视觉与目标识别、遥感多模态大模型、对抗攻击与模型鲁棒性。') if mobile else Art(1440,315,'研究主线','居中的行书研究标题与水墨山水底景。')
    paper(a,.3);ink_defs(a,False)
    a.add(f'<rect width="{a.w}" height="{a.h}" fill="#101619" opacity=".48"/>')
    topics=[('识','水下视觉与目标识别','UNDERWATER PERCEPTION','在复杂水下环境中理解目标'),('融','遥感多模态大模型','MULTIMODAL FOUNDATION MODELS','关注多源信息的融合与理解'),('辨','对抗攻击与模型鲁棒性','ADVERSARIAL ROBUSTNESS','从航拍图像与对抗补丁问题出发')]
    for i,(mark,title,en,note) in enumerate(topics):
        cx,top=(380,i*250) if mobile else (240+i*480,0)
        seal(a,cx-13,top+28 if mobile else 35,mark,26)
        a.text(title,cx,top+116 if mobile else 142,39 if mobile else 40,face=1,center=True)
        a.text(en,cx,top+157 if mobile else 184,15 if mobile else 14,MUTED,4,1,center=True)
        a.text(note,cx,top+207 if mobile else 238,24 if mobile else 21,MUTED,2,center=True)
        if mobile and i<2:a.add(f'<path d="M118 {top+246}Q380 {top+249} 642 {top+246}" stroke="#a8b1b4" opacity=".24" fill="none"/>')
        elif not mobile and i<2:a.add(f'<path d="M{cx+240} 90Q{cx+237} 158 {cx+240} 225" stroke="#a8b1b4" opacity=".3" fill="none"/>')
    water(a,80,a.h-22,a.w-160)
    a.save('research-mobile.svg' if mobile else 'research.svg')

def terrain(u,v,x,y,w,h):
    ridge=math.sin(u*7.2+v*2)*.23+math.sin(u*14-v*4)*.10+math.exp(-((u-.62)**2/.025+(v-.42)**2/.2))*.8
    return x+u*w+(v-.5)*w*.12,y+v*h-ridge*h*.52

def poly(points):return ' '.join(f'{x:.2f},{y:.2f}' for x,y in points)

def mesh(a,x,y,w,h,rows=15,cols=28):
    for i in range(rows):
        v=i/(rows-1);p=[terrain(j/70,v,x,y,w,h) for j in range(71)]
        a.add(f'<polyline points="{poly(p)}" fill="none" stroke="#b6c2c6" stroke-width=".9" opacity="{.14+v*.26:.2f}"/>')
    for j in range(cols):
        p=[terrain(j/(cols-1),i/35,x,y,w,h) for i in range(36)]
        a.add(f'<polyline points="{poly(p)}" fill="none" stroke="#a3adb1" stroke-width=".75" opacity=".24"/>')

def multibeam(mobile=False):
    a=Art(760,650,'多波束测深论文案例','示意地形与测线。论文匿名真实海底案例中的几何覆盖率98.81%，漏测率1.19%，总测线长度449.33公里。') if mobile else Art(1440,370,'多波束测深论文案例','左侧为原创方法示意，右侧是论文匿名海底案例的几何覆盖指标。')
    paper(a,.23);ink_defs(a,False)
    a.add(f'<rect width="{a.w}" height="{a.h}" fill="#101619" opacity=".5"/>')
    if mobile:
        a.text('多波束测深测线规划',380,69,40,face=1,center=True)
        a.text('覆盖感知 · 自适应分区 · 测线布设',380,113,23,MUTED,2,center=True)
        x,y,w,h=45,180,655,145
    else:
        a.text('复杂海底地形的多波束测线规划',45,70,36,face=1)
        a.text('覆盖感知 · 自适应分区 · 测线布设',47,109,20,MUTED,2)
        x,y,w,h=50,167,645,125
    mesh(a,x,y,w,h)
    for j in range(7):
        u=.10+.12*j;p=[terrain(u+.012*math.sin(v*8),v,x,y,w,h) for v in [i/30 for i in range(31)]]
        a.add(f'<polyline points="{poly(p)}" fill="none" stroke="{["#d8e0e2","#b7c0c4","#84979e"][j//3]}" stroke-width="2.1" opacity=".9"/>')
    if mobile:
        for cx,value,label in [(206,'98.81%','几何覆盖率'),(555,'1.19%','漏测率')]:
            a.text(value,cx,463,62,face=0,center=True);a.text(label,cx,511,28,MUTED,2,center=True)
        a.text('449.33 km',215,581,38,face=0,center=True);a.text('总测线长度',551,576,24,MUTED,2,center=True)
        a.text('论文匿名海底案例；上方为原创方法示意',380,625,19,MUTED,2,center=True)
    else:
        a.add('<path d="M760 53Q757 170 760 297" fill="none" stroke="#a7b3b7" opacity=".32"/>')
        for cx,value,label in [(929,'98.81%','几何覆盖率'),(1240,'1.19%','漏测率')]:
            a.text(value,cx,160,62,face=0,center=True);a.text(label,cx,204,24,MUTED,2,center=True)
        a.text('449.33 km',929,281,40,face=0,center=True);a.text('总测线长度',1240,273,24,MUTED,2,center=True)
        a.text('论文匿名海底案例 · 几何覆盖口径；左侧为原创方法示意',48,345,17,MUTED,2)
    a.save('multibeam-mobile.svg' if mobile else 'multibeam-overview.svg')

def small_assets():
    a=Art(283,38,'邮件联系','13774949997@163.com')
    a.add('<rect x=".5" y=".5" width="282" height="37" rx="2" fill="#171f23" stroke="#657176"/><path d="M15 12H33V26H15ZM15 13 24 20 33 13" fill="none" stroke="#d2dadd" stroke-width="1.3"/>')
    a.text('13774949997@163.com',45,25,16,INK,3);a.save('contact.svg')
    a=Art(1440,115,'田承龙 · E7ian','水墨画卷落款。')
    paper(a,.3);ink_defs(a,False)
    a.text('田承龙',62,77,42,face=1);a.text('E7ian',228,77,36,face=0);seal(a,358,39,size=26)
    water(a,650,58,700);a.save('footer.svg')

def main():
    OUT.mkdir(exist_ok=True)
    for mobile in [False,True]:
        for animated in [True,False]:hero(animated,mobile)
        research(mobile);multibeam(mobile)
    small_assets()
    for path in sorted(OUT.glob('*.svg')):print(f'{path.name}: {path.stat().st_size:,} bytes')

if __name__=='__main__':main()
