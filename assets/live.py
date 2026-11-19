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
for th,c in P.items():
    W,H=840,232; cs,g=11,3; x0,y0=50,96
    b=f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/><text x="24" y="44" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="22" font-weight="700" fill="{c["fg"]}">⚽ Contributions</text>'
    b+=f'<text x="816" y="44" text-anchor="end" font-family="Georgia,serif" font-size="13" fill="{c["tx"]}">{total} this year, every one of them a pass</text>'
    first=D.date.fromisoformat(days[0][0]); off=(first.weekday()+1)%7; lastm=None; pts=[]
    for k,(d,l) in enumerate(days):
        n=k+off; col,row=n//7,n%7; x,y=x0+col*(cs+g),y0+row*(cs+g); dd=D.date.fromisoformat(d)
        if dd.day<=7 and row==0 and dd.month!=lastm: b+=f'<text x="{x}" y="{y0-10}" font-family="Georgia,serif" font-size="12" fill="{c["tx"]}">{dd.strftime("%b")}</text>'; lastm=dd.month
        b+=f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" rx="2" fill="{c["lv"][l] if l else c["e"]}"/>'
        if l: pts.append((x+cs/2,y+cs/2))
    gx1=x0+(col+1)*(cs+g); mid=y0+3.5*(cs+g)-g/2; top,bot=y0-4,y0+7*(cs+g)+1; hx=(x0-4+gx1)/2
    L=c["ln"]
    b+=f'<g fill="none" stroke="{L}" stroke-width="1.2"><rect x="{x0-4}" y="{top}" width="{gx1-x0+2}" height="{bot-top}"/><line x1="{hx}" y1="{top}" x2="{hx}" y2="{bot}"/><circle cx="{hx}" cy="{mid}" r="26"/><rect x="{x0-4}" y="{mid-34}" width="56" height="68"/><rect x="{gx1-58}" y="{mid-34}" width="56" height="68"/><path d="M{x0+52} {mid-16} a20 20 0 0 1 0 32 M{gx1-58} {mid-16} a20 20 0 0 0 0 32"/></g>'
    b+=f'<g stroke="{c["fg"]}" stroke-width="1.5" fill="none"><path d="M{x0-4} {mid-18} h-10 v36 h10"/><path d="M{gx1-2} {mid-18} h10 v36 h-10"/></g>'
    route=[(x0+4,mid)]+pts+[(gx1+6,mid)]
    path="M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in route)
    b+=f'<path d="{path}" fill="none" stroke="{c["fg"]}" stroke-opacity=".28" stroke-width="1" stroke-dasharray="2 3"/>'
    for k,(dx,sp) in enumerate([(0.30,3.1),(0.55,2.3),(0.78,2.7)]):
        x=x0+(gx1-x0)*dx
        b+=f'<g><animateTransform attributeName="transform" type="translate" values="{x:.0f} {y0};{x:.0f} {bot-16};{x:.0f} {y0}" dur="{sp}s" repeatCount="indefinite"/>{sprite(c,c["opp"])}</g>'
    dur=max(10,len(route)*0.7)
    mv=f'<animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}" keyPoints="0;1;1" keyTimes="0;.86;1" calcMode="linear"/>'
    b+=f'<g>{mv}<g transform="translate(-14 -14)">{sprite(c,c["kit"])}</g><circle r="3.6" fill="#fff" stroke="#1f2328" stroke-width="1"/><circle r="1.3" fill="#1f2328"/></g>'
    b+=f'<text x="{gx1-70}" y="{top-8}" font-family="Georgia,serif" font-style="italic" font-size="20" font-weight="700" fill="{c["fg"]}" opacity="0">GOAL!<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.86;.88;.98;1" dur="{dur}s" repeatCount="indefinite"/></text>'
    b+=f'<text x="24" y="{H-12}" font-family="Georgia,serif" font-size="12" fill="{c["tx"]}">Every green square is a day I shipped something. The ball visits them in order. Redrawn daily.</text>'
    open(f"{o}/pitch-{th}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{b}</svg>')
# writing list straight into README (real text, not an image)
md="\n".join(f"- [{t}]({l}) · {dt.strftime('%b %Y')}" for t,dt,l in posts)
R=open("README.md").read()
if "<!--writing-->" in R:
    a=R.index("<!--writing-->")+len("<!--writing-->"); b2=R.index("<!--/writing-->")
    open("README.md","w").write(R[:a]+"\n"+md+"\n"+R[b2:])
print(total,len(pts),[p[2] for p in posts])
