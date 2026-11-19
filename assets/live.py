# Rebuilds the live cards (activity heatmap + latest writing). Run daily by .github/workflows/live.yml
import sys,re,urllib.request,datetime as D,xml.etree.ElementTree as E,html
o=sys.argv[1] if len(sys.argv)>1 else "assets"; U="mihirruwala"; M="ruwalamihir"
import subprocess
def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=30).read().decode()
    except Exception: return subprocess.run(["curl","-sL","-A","Mozilla/5.0",u],capture_output=True,text=True,timeout=60).stdout
SER="'Instrument Serif',Georgia,serif";MONO="'IBM Plex Mono',ui-monospace,Menlo,monospace"
T={"dark":dict(bg="#101311",p="#171b18",fg="#f0efe7",mu="#92958d",ac="#c9f36a",ln="rgba(240,239,231,0.13)",ai="#101311",glow=".10",grain=".07",e="rgba(240,239,231,0.06)"),
   "light":dict(bg="#f0eee5",p="#e7e4d8",fg="#181b18",mu="#5d6159",ac="#6f8a1f",ln="rgba(24,27,24,0.14)",ai="#f0eee5",glow=".14",grain=".09",e="rgba(24,27,24,0.07)")}
def svg(w,h,b,c): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><radialGradient id="g" cx="1" cy="0" r="1"><stop offset="0" stop-color="{c["ac"]}" stop-opacity="{c["glow"]}"/><stop offset=".6" stop-color="{c["ac"]}" stop-opacity="0"/></radialGradient><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 {c["grain"]} 0"/></filter><clipPath id="k"><rect width="{w}" height="{h}" rx="16"/></clipPath></defs><rect width="{w}" height="{h}" rx="16" fill="{c["bg"]}"/><g clip-path="url(#k)"><rect width="{w}" height="{h}" fill="url(#g)"/><rect width="{w}" height="{h}" filter="url(#n)"/></g><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="{c["ln"]}"/>{b}</svg>'
def mono(x,y,t,c,col=None,anc="start",s=11,ls=1.6): return f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{s}" letter-spacing="{ls}" fill="{col or c["mu"]}" text-anchor="{anc}">{html.escape(t)}</text>'
# --- data
h=get(f"https://github.com/users/{U}/contributions")
days=sorted((d,int(l)) for d,l in re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*data-level="(\d)"',h)+[(d,int(l)) for l,d in re.findall(r'data-level="(\d)"[^>]*data-date="(\d{4}-\d\d-\d\d)"',h)])
days=sorted(dict(days).items())
m=re.search(r'([\d,]+)\s+contributions?\s+in the last year',h); total=m.group(1) if m else "—"
act=[l>0 for _,l in days]; streak=best=cur=0
for a in act: cur=cur+1 if a else 0; best=max(best,cur)
i=len(act)-1
if i>=0 and not act[i]: i-=1
while i>=0 and act[i]: streak+=1; i-=1
activeD=sum(act)
# Medium sometimes serves an empty feed to scripts; fall back to the last known posts
SEED=[("The Distance Was Never the Point","29 Jul 2026",f"https://medium.com/@{M}"),("Take the Risk of Grief","06 Jun 2026",f"https://medium.com/@{M}"),("Introduction","30 Oct 2025",f"https://medium.com/@{M}")]
x=get(f"https://medium.com/feed/@{M}")
posts=[(html.unescape(t),d[5:16],l.split("?")[0]) for t,l,d in re.findall(r"<item>.*?<title><!\[CDATA\[(.*?)\]\]></title>.*?<link>(.*?)</link>.*?<pubDate>(.*?)</pubDate>",x,re.S)][:3] or SEED
posts=[(t,D.datetime.strptime(d,"%d %b %Y"),l) for t,d,l in posts]
today=D.date.today()
P={"dark":dict(bg="#0d1117",e="#161b22",lv=["","#0e4429","#006d32","#26a641","#39d353"],ln="rgba(255,255,255,0.55)",tx="#7d8590",fg="#e6edf3",kit="#58a6ff",opp="#f85149",skin="#f2cc8f"),
   "light":dict(bg="#ffffff",e="#ebedf0",lv=["","#9be9a8","#40c463","#30a14e","#216e39"],ln="rgba(31,35,40,0.45)",tx="#57606a",fg="#1f2328",kit="#0969da",opp="#cf222e",skin="#d4a373")}
SPR=["..HHH..","..HHH..","...H...",".SSSSS.","S.SSS.S","..SSS..","..L.L.."]
LEGA=[".L...L.",".L...L."]; LEGB=["..L.L..","...L..."]
def sprite(c,col,ps=1.6):
    def px(rows,y0,cls=""):
        o=""
        for r,row in enumerate(rows):
            for k,ch in enumerate(row):
                if ch!=".": o+=f'<rect x="{k*ps:.1f}" y="{(y0+r)*ps:.1f}" width="{ps}" height="{ps}" fill="{c["skin"] if ch=="H" else col}"/>'
        return o
    return px(SPR,0)+f'<g>{px(LEGA,7)}<animate attributeName="opacity" values="1;0" dur=".3s" calcMode="discrete" repeatCount="indefinite"/></g><g opacity="0">{px(LEGB,7)}<animate attributeName="opacity" values="0;1" dur=".3s" calcMode="discrete" repeatCount="indefinite"/></g>'
import random
SANS="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
for th,c in P.items():
    W,H=840,262; cs,g=11,3; x0,y0=56,104
    first=D.date.fromisoformat(days[0][0]); off=(first.weekday()+1)%7
    ncol=(len(days)+off+6)//7; gx1=x0+ncol*(cs+g)-g
    PX0,PX1,PT,PB=x0-14,gx1+14,y0-16,y0+7*(cs+g)-g+16; mid=(PT+PB)/2; hx=(PX0+PX1)/2
    b=f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>'
    # crowd
    rnd=random.Random(7); cols=["#f85149","#58a6ff","#e3b341","#f0f6fc","#a371f7","#3fb950","#ff7b72","#79c0ff"]
    for r in range(3):
        for k in range(int((PX1-PX0)/5.2)):
            x=PX0+k*5.2+(r%2)*2.6; y=58+r*8
            fl=rnd.random()<.03
            b+=f'<circle cx="{x:.1f}" cy="{y}" r="2" fill="{rnd.choice(cols)}" fill-opacity="{.55 if r else .8}"/>'
            if fl: b+=f'<circle cx="{x:.1f}" cy="{y}" r="2.6" fill="#fff" opacity="0"><animate attributeName="opacity" values="0;0;1;0" keyTimes="0;.9;.93;1" dur="{rnd.uniform(1.5,5):.1f}s" begin="{rnd.uniform(0,4):.1f}s" repeatCount="indefinite"/></circle>'
    b+=f'<rect x="{PX0-8}" y="80" width="{PX1-PX0+16}" height="4" fill="#30363d"/>'
    # grass stripes
    sw=(PX1-PX0)/14
    b+=f'<rect x="{PX0-8}" y="{PT-8}" width="{PX1-PX0+16}" height="{PB-PT+16}" fill="#2c6e31"/>'+"".join(f'<rect x="{PX0+i*sw:.1f}" y="{PT-8}" width="{sw:.1f}" height="{PB-PT+16}" fill="#337a37"/>' for i in range(0,14,2))
    for k,(d,l) in enumerate(days):
        n=k+off; col,row=n//7,n%7; x,y=x0+col*(cs+g),y0+row*(cs+g)
        b+=f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" rx="2" fill="{"#000" if l==0 else "#eaffd0"}" fill-opacity="{[.13,.4,.6,.8,1][l]}"/>'
    # markings
    L='stroke="#fff" stroke-opacity=".85" stroke-width="1.4" fill="none"'
    b+=f'<rect x="{PX0}" y="{PT}" width="{PX1-PX0}" height="{PB-PT}" {L}/><line x1="{hx}" y1="{PT}" x2="{hx}" y2="{PB}" {L}/><circle cx="{hx}" cy="{mid}" r="30" {L}/><circle cx="{hx}" cy="{mid}" r="2" fill="#fff"/>'
    for sgn,ex in [(1,PX0),(-1,PX1)]:
        b+=f'<path d="M{ex} {mid-44} h{sgn*66} v88 h{-sgn*66} M{ex} {mid-20} h{sgn*24} v40 h{-sgn*24}" {L}/><circle cx="{ex+sgn*46}" cy="{mid}" r="1.8" fill="#fff"/><path d="M{ex+sgn*66} {mid-18} a24 24 0 0 {1 if sgn>0 else 0} 0 36" {L}/>'
        b+=f'<path d="M{ex} {PT+8} a8 8 0 0 {1 if sgn<0 else 0} {sgn*8} -8 M{ex} {PB-8} a8 8 0 0 {0 if sgn<0 else 1} {sgn*8} 8" {L}/>'
    # goals with nets
    def goal(ex,sgn,shake):
        gx=ex-14 if sgn<0 else ex
        net="".join(f'<line x1="{gx+i*3.5}" y1="{mid-18}" x2="{gx+i*3.5}" y2="{mid+18}" stroke="#fff" stroke-opacity=".35"/>' for i in range(5))+"".join(f'<line x1="{gx}" y1="{mid-18+j*4}" x2="{gx+14}" y2="{mid-18+j*4}" stroke="#fff" stroke-opacity=".35"/>' for j in range(10))
        an=f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;3 0;-1 1;2 -1;0 0;0 0" keyTimes="0;.86;.88;.9;.92;.94;1" dur="{{dur}}s" repeatCount="indefinite"/>' if shake else ""
        return f'<g>{an}{net}<path d="M{ex} {mid-18} h{sgn*14} v36 h{-sgn*14}" stroke="#fff" stroke-width="2.4" fill="none"/></g>'
    pts=[(x0+((k+off)//7)*(cs+g)+cs/2,y0+((k+off)%7)*(cs+g)+cs/2) for k,(d,l) in enumerate(days) if l]
    route=[(PX0+30,mid)]+pts+[(PX1+7,mid)]
    path="M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in route); dur=round(max(10,len(route)*0.7),1)
    b+=goal(PX0,-1,False)+goal(PX1,1,True).replace("{dur}",str(dur))
    b+=f'<path d="{path}" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="1" stroke-dasharray="2 3"/>'
    kit,opp=c["kit"],c["opp"]
    # keepers
    b+=f'<g><animateTransform attributeName="transform" type="translate" values="{PX0+4} {mid-18};{PX0+4} {mid+4};{PX0+4} {mid-18}" dur="2.6s" repeatCount="indefinite"/>{sprite(c,"#e3b341")}</g>'
    b+=f'<g><animateTransform attributeName="transform" type="translate" values="{PX1-16} {mid-20};{PX1-16} {mid+6};{PX1-16} {mid-20}" dur="1.9s" repeatCount="indefinite"/>{sprite(c,"#a371f7")}</g>'
    for dx,sp in [(0.3,3.1),(0.55,2.3),(0.78,2.7)]:
        x=PX0+(PX1-PX0)*dx
        b+=f'<g><animateTransform attributeName="transform" type="translate" values="{x:.0f} {PT+2};{x:.0f} {PB-16};{x:.0f} {PT+2}" dur="{sp}s" repeatCount="indefinite"/>{sprite(c,opp)}</g>'
    mv=lambda beg:f'<animateMotion dur="{dur}s" begin="{beg}s" repeatCount="indefinite" path="{path}" keyPoints="0;1;1" keyTimes="0;.86;1" calcMode="linear"/>'
    for beg,dy in [(-0.6,-26),(-1.1,22)]:
        b+=f'<g>{mv(beg)}<g transform="translate(-14 {dy})">{sprite(c,kit)}</g></g>'
    b+=f'<g>{mv(0)}<g transform="translate(-14 -14)">{sprite(c,kit)}</g><circle r="3.8" fill="#fff" stroke="#111" stroke-width="1"/><circle r="1.4" fill="#111"/></g>'
    # GOAL flash
    b+=f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.86;.875;.98;1" dur="{dur}s" repeatCount="indefinite"/><rect x="{hx-90}" y="{mid-24}" width="180" height="48" rx="6" fill="#111" fill-opacity=".8"/><text x="{hx}" y="{mid+12}" text-anchor="middle" font-family="{SANS}" font-weight="900" font-style="italic" font-size="34" fill="#fff" letter-spacing="1">GOAL!</text></g>'
    # scoreboard
    sb=f'<g font-family="{SANS}" font-weight="700" font-size="13"><rect x="{PX0-8}" y="14" width="196" height="28" rx="5" fill="#161b22" stroke="#30363d"/><rect x="{PX0-8}" y="14" width="6" height="28" rx="2" fill="{kit}"/><text x="{PX0+8}" y="33" fill="#f0f6fc">MIHIR</text>'
    sb+=f'<text x="{PX0+90}" y="33" text-anchor="middle" fill="#f0f6fc">0 – 0<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.875;.876;1" dur="{dur}s" repeatCount="indefinite"/></text><text x="{PX0+90}" y="33" text-anchor="middle" fill="#e3b341" opacity="0">1 – 0<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;.875;.876;1" dur="{dur}s" repeatCount="indefinite"/></text>'
    sb+=f'<text x="{PX0+130}" y="33" fill="#f0f6fc">BUGS</text><rect x="{PX0+182}" y="14" width="6" height="28" rx="2" fill="{opp}"/></g>'
    b+=sb+f'<text x="{PX1+8}" y="33" text-anchor="end" font-family="{SANS}" font-size="13" fill="{c["tx"]}"><tspan fill="#f85149">●</tspan> LIVE · {total} contributions this year</text>'
    b+=f'<text x="{PX0-8}" y="{H-12}" font-family="{SANS}" font-size="12" fill="{c["tx"]}">Every square is a day; the bright ones are days I shipped something. The ball visits them in order, then scores. Redrawn daily.</text>'
    open(f"{o}/pitch-{th}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{b}</svg>')
# writing list straight into README (real text, not an image)
md="\n".join(f"- [{t}]({l}) · {dt.strftime('%b %Y')}" for t,dt,l in posts)
R=open("README.md").read()
if "<!--writing-->" in R:
    a=R.index("<!--writing-->")+len("<!--writing-->"); b2=R.index("<!--/writing-->")
    open("README.md","w").write(R[:a]+"\n"+md+"\n"+R[b2:])
print(total,[p[2] for p in posts])
