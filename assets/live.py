# Rebuilds the live cards (activity heatmap + latest writing). Run daily by .github/workflows/live.yml
import sys,re,urllib.request,datetime as D,xml.etree.ElementTree as E,html
o=sys.argv[1] if len(sys.argv)>1 else "assets"; U="mihirruwala"
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
SEED=[("The Distance Was Never the Point","29 Jul 2026"),("Take the Risk of Grief","06 Jun 2026"),("Introduction","30 Oct 2025")]
x=get(f"https://medium.com/feed/@{U}")
posts=[(html.unescape(t),d[5:16]) for t,d in re.findall(r"<item>.*?<title><!\[CDATA\[(.*?)\]\]></title>.*?<pubDate>(.*?)</pubDate>",x,re.S)][:3] or SEED
posts=[(t,D.datetime.strptime(d,"%d %b %Y")) for t,d in posts]
today=D.date.today().strftime("%d %b %Y").upper()
for th,c in T.items():
    # activity
    W,H=840,250; b=mono(40,46,"ACTIVITY",c,c["fg"])+mono(800,46,"LAST 52 WEEKS",c,anc="end")+f'<line x1="40" y1="62" x2="800" y2="62" stroke="{c["ln"]}"/>'
    first=D.date.fromisoformat(days[0][0]); off=(first.weekday()+1)%7; cs,g=11,3.3; x0,y0=48,96; lastm=None
    op=["", ".28", ".52", ".78", "1"]
    for k,(d,l) in enumerate(days):
        n=k+off; col,row=n//7,n%7; x,y=x0+col*(cs+g),y0+row*(cs+g); dd=D.date.fromisoformat(d)
        if dd.day<=7 and row==0 and dd.month!=lastm: b+=mono(x,y0-10,dd.strftime("%b").upper(),c,s=9,ls=1); lastm=dd.month
        b+=f'<rect x="{x}" y="{y:.1f}" width="{cs}" height="{cs}" rx="2.5" fill="{c["e"] if l==0 else c["ac"]}"{"" if l==0 else f" fill-opacity=\"{op[l]}\""}/>'
    b+=f'<rect x="{x-2.5}" y="{y-2.5:.1f}" width="{cs+5}" height="{cs+5}" rx="4" fill="none" stroke="{c["fg"]}" stroke-width="1"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></rect>'
    sx=40
    for big,lab in [(total,"contributions"),(str(activeD),"active days"),(str(best),"longest streak"),(str(streak),"current streak")]:
        b+=f'<text x="{sx}" y="222" font-family="{SER}" font-size="30" fill="{c["fg"]}">{big}</text>'+mono(sx+len(big)*15+10,218,lab.upper(),c,s=9.5,ls=1); sx+=200
    open(f"{o}/activity-{th}.svg","w").write(svg(W,H,b,c))
    # writing
    W,H=840,116+len(posts)*52; b=mono(40,46,"WRITING",c,c["fg"])+mono(800,46,"LATEST ON MEDIUM",c,anc="end")+f'<line x1="40" y1="62" x2="800" y2="62" stroke="{c["ln"]}"/>'
    for j,(t,dt) in enumerate(posts):
        y=100+j*52; b+=mono(40,y,dt.strftime("%d %b %Y").upper(),c,s=10,ls=1)+f'<text x="170" y="{y+2}" font-family="{SER}" font-size="24" fill="{c["fg"] if j else c["ac"]}"{" font-style=\"italic\"" if j==0 else ""}>{html.escape(t)}</text>'+mono(800,y,"↗",c,c["fg"],"end",s=13)
        b+=f'<line x1="40" y1="{y+20}" x2="800" y2="{y+20}" stroke="{c["ln"]}"/>'
    b+=mono(40,H-24,f"REBUILT DAILY BY GITHUB ACTIONS · {today}",c,s=9,ls=1)
    open(f"{o}/writing-{th}.svg","w").write(svg(W,H,b,c))
print(total,activeD,best,streak,len(days),[p[0] for p in posts])
