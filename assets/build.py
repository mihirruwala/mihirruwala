import sys
from PIL import ImageFont
o=sys.argv[1]
SF="/System/Library/Fonts/Supplemental/"
def tw(t,s,it=False): return ImageFont.truetype(SF+("Georgia Italic.ttf" if it else "Georgia.ttf"),s).getlength(t)
SER="'Instrument Serif',Georgia,serif";MONO="'IBM Plex Mono',ui-monospace,Menlo,monospace";SANS="Inter,-apple-system,'Segoe UI',Helvetica,sans-serif"
T={"dark":dict(bg="#101311",p="#171b18",fg="#f0efe7",mu="#92958d",ac="#c9f36a",ln="rgba(240,239,231,0.13)",ln2="rgba(240,239,231,0.05)",ai="#101311"),
   "light":dict(bg="#f0eee5",p="#e7e4d8",fg="#181b18",mu="#5d6159",ac="#6f8a1f",ln="rgba(24,27,24,0.14)",ln2="rgba(24,27,24,0.05)",ai="#f0eee5")}
def svg(w,h,b,c): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" rx="16" fill="{c["bg"]}"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="{c["ln"]}"/>{b}</svg>'
def mono(x,y,t,c,col=None,anc="start",s=11,ls=1.6): return f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{s}" letter-spacing="{ls}" fill="{col or c["mu"]}" text-anchor="{anc}">{t}</text>'
for th,c in T.items():
    # ---------- HEADER
    W,H=840,330; b=""
    b+="".join(f'<line x1="{40+i*63.33:.1f}" y1="72" x2="{40+i*63.33:.1f}" y2="262" stroke="{c["ln2"]}"/>' for i in range(13))
    b+=mono(40,46,"MIHIR RUWALA",c,c["fg"])+mono(800,46,"FRONTEND · iOS · HUMAN–AI TRUST",c,anc="end")
    b+=f'<line x1="40" y1="62" x2="800" y2="62" stroke="{c["ln"]}"/>'+"".join(f'<line x1="{x}" y1="62" x2="{x}" y2="{66 if x%100 else 70}" stroke="{c["ln"]}"/>' for x in range(40,801,20))
    S=70; x2=40+tw("can ",S); wt=tw("trust.",S,True)
    b+=f'<text x="38" y="150" font-family="{SER}" font-size="{S}" fill="{c["fg"]}" letter-spacing="-1">Interfaces people</text>'
    b+=f'<text x="38" y="234" font-family="{SER}" font-size="{S}" fill="{c["fg"]}" letter-spacing="-1">can <tspan font-style="italic" fill="{c["ac"]}">trust.</tspan></text>'
    sx,sy,sw,sh=x2-8,182,wt+10,68
    b+=f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="{c["ac"]}" fill-opacity=".07" stroke="{c["ac"]}" stroke-width="1.25"><animate attributeName="stroke-opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></rect>'
    b+="".join(f'<rect x="{X-3.5}" y="{Y-3.5}" width="7" height="7" fill="{c["bg"]}" stroke="{c["ac"]}" stroke-width="1.25"/>' for X in (sx,sx+sw) for Y in (sy,sy+sh))
    lab=f"{round(sw)} × {sh}"; lw=len(lab)*6.6+16
    b+=f'<rect x="{sx+sw/2-lw/2}" y="{sy+sh+10}" width="{lw}" height="18" rx="4" fill="{c["ac"]}"/>'+mono(sx+sw/2,sy+sh+23,lab,c,c["ai"],"middle",10.5,.4)
    cx,cy=sx+sw+6,sy+sh-14
    b+=f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;64 36;0 0" keyTimes="0;.6;.75;1" dur="5s" calcMode="spline" keySplines="0 0 1 1;.65 0 .35 1;.22 1 .36 1" repeatCount="indefinite"/><path transform="translate({cx} {cy})" d="M0 0 L0 17 L4.6 12.6 L7.6 19.4 L10.4 18.2 L7.4 11.6 L13.4 11.6 Z" fill="{c["fg"]}" stroke="{c["bg"]}" stroke-width="1.2" stroke-linejoin="round"/></g>'
    b+=f'<line x1="40" y1="276" x2="800" y2="276" stroke="{c["ln"]}"/>'+mono(40,302,"2ND-YEAR CSE · VIT VELLORE",c)+mono(800,302,"MIHIRRUWALA.CV ↗",c,c["fg"],"end")
    open(f"{o}/header-{th}.svg","w").write(svg(W,H,b,c))
    # ---------- CARDS
    def card(n,idx,status,live,title,desc,motif,metric,cap,chips):
        W,H=410,330; b=mono(24,36,idx,c)
        pw=len(status)*7.2+(30 if live else 18); px=386-pw
        b+=f'<rect x="{px}" y="22" width="{pw}" height="20" rx="10" fill="none" stroke="{c["ln"]}"/>'
        if live: b+=f'<circle cx="{px+12}" cy="32" r="3" fill="{c["ac"]}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        b+=mono(px+(21 if live else 9),36,status,c,c["fg"],s=10,ls=1.2)
        b+=f'<text x="24" y="84" font-family="{SER}" font-size="34" fill="{c["fg"]}" letter-spacing="-.4">{title}</text><text x="24" y="106" font-family="{SANS}" font-size="12.5" fill="{c["mu"]}">{desc}</text>'
        b+=f'<rect x="24" y="122" width="362" height="92" rx="10" fill="{c["p"]}"/>'+motif
        b+=f'<text x="24" y="262" font-family="{SER}" font-size="38" fill="{c["fg"]}" letter-spacing="-.5">{metric}</text>'+mono(24+tw(metric,38)+12,258,cap,c,s=10.5,ls=.3)
        x=24; b+=f'<line x1="24" y1="280" x2="386" y2="280" stroke="{c["ln"]}"/>'
        for ch in chips:
            w=len(ch)*6.3+16; b+=f'<rect x="{x}" y="294" width="{w}" height="20" rx="5" fill="none" stroke="{c["ln"]}"/>'+mono(x+8,308,ch,c,c["fg"],s=10.5,ls=.2); x+=w+6
        open(f"{o}/{n}-{th}.svg","w").write(svg(W,H,b,c))
    A,F,M,P,L=c["ac"],c["fg"],c["mu"],c["bg"],c["ln"]
    win=lambda x:f'<rect x="{x}" y="138" width="104" height="60" rx="7" fill="{P}" stroke="{L}"/><rect x="{x+12}" y="152" width="58" height="6" rx="3" fill="{L}"/><rect x="{x+12}" y="164" width="40" height="6" rx="3" fill="{L}"/><rect x="{x+12}" y="176" width="70" height="6" rx="3" fill="{L}"/>'
    duo=win(40)+win(266)+f'<line x1="150" y1="168" x2="260" y2="168" stroke="{L}" stroke-dasharray="3 4"/><path d="M199 150 v-4 a6 6 0 0 1 12 0 v4" fill="none" stroke="{M}" stroke-width="1.4"/><rect x="196" y="150" width="18" height="12" rx="2" fill="{M}"/><rect y="163" width="14" height="10" rx="2" fill="{A}"><animate attributeName="x" values="146;250;250;146;146" keyTimes="0;.4;.5;.9;1" dur="3.2s" calcMode="spline" keySplines=".65 0 .35 1;0 0 1 1;.65 0 .35 1;0 0 1 1" repeatCount="indefinite"/></rect>'
    card("duo","01","LIVE",1,"DUO","A private space for two, on web and Chrome.",duo,"E2E","encrypted calls + chat",["Next.js","LiveKit","Supabase","Radix"])
    bp="M64 186 L132 146 L204 182 L268 140 L346 166"
    barca=f'<g stroke="{L}" fill="none"><rect x="40" y="134" width="330" height="68" rx="3"/><line x1="205" y1="134" x2="205" y2="202"/><circle cx="205" cy="168" r="14"/><rect x="40" y="152" width="20" height="32"/><rect x="350" y="152" width="20" height="32"/><path d="{bp}" stroke="{A}" stroke-opacity=".5" stroke-dasharray="2 4"/></g>'+"".join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{F}"/>' for x,y in [(64,186),(132,146),(204,182),(268,140),(346,166)])+"".join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{M}" fill-opacity=".6"/>' for x,y in [(165,160),(236,170),(312,186),(100,166)])+f'<circle r="5" fill="{A}"><animateMotion dur="4s" repeatCount="indefinite" path="{bp}"/></circle>'
    card("barca","02","MTAH 2027",0,"Barça Lab","Who has the ball, every frame, from tracking data.",barca,"0.484","spellF1 · baseline 0.408",["Python","Kalman","HMM","Metrica"])
    hot={(5,1),(6,1),(5,2),(6,2),(7,2),(6,3)}; cells=""
    for r in range(4):
        for col in range(11):
            x,y=40+col*30,134+r*18
            if (col,r) in hot: cells+=f'<rect x="{x}" y="{y}" width="26" height="14" rx="2" fill="{P}" stroke="{L}"><animate attributeName="fill" values="{P};{A};{A};{P}" keyTimes="0;{(x-40)/330:.2f};.9;1" dur="4.5s" repeatCount="indefinite"/></rect>'
            else: cells+=f'<rect x="{x}" y="{y}" width="26" height="14" rx="2" fill="{P}" stroke="{L}"/>'
    dt=cells+f'<rect y="130" width="2" height="76" rx="1" fill="{A}"><animate attributeName="x" values="38;372" dur="4.5s" repeatCount="indefinite"/></rect>'
    card("deeptrace","03","LIVE",1,"DeepTrace","Deepfake and AI-face detection with evidence.",dt,"45/75","fakes caught · 2/88 false flags",["PyTorch","timm","OpenCV"])
    ph=lambda x:f'<rect x="{x}" y="132" width="40" height="72" rx="9" fill="{P}" stroke="{L}"/><rect x="{x+14}" y="137" width="12" height="3" rx="1.5" fill="{L}"/>'
    hop="M80 168 Q130 136 178 168 M232 168 Q282 136 330 168"
    dm=ph(40)+ph(185)+ph(330)+f'<path d="{hop}" stroke="{L}" fill="none" stroke-dasharray="3 4"/><circle r="4.5" fill="{A}"><animateMotion dur="3.6s" repeatCount="indefinite" path="M60 168 L80 168 Q130 136 178 168 L232 168 Q282 136 330 168 L350 168" keyPoints="0;1;1" keyTimes="0;.8;1" calcMode="linear"/></circle><circle cx="350" cy="168" r="6" fill="none" stroke="{A}" opacity="0"><animate attributeName="r" values="6;6;16" keyTimes="0;.8;1" dur="3.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0;1;0" keyTimes="0;.79;.82;1" dur="3.6s" repeatCount="indefinite"/></circle>'
    card("dmesh","04","FIELD-TESTED",0,"D-Mesh","SOS messages that hop phone to phone, no signal.",dm,"337/371","delivered · relay +60 ms",["Swift","Multipeer"])
    # ---------- FOOTER (tokens)
    W,H=840,150; b=mono(40,40,"SYSTEM",c,c["fg"])+mono(800,40,"THE SAME TOKENS AS MY SITE",c,anc="end")+f'<line x1="40" y1="54" x2="800" y2="54" stroke="{c["ln"]}"/>'
    sw=[("ink","#101311"),("ivory","#f0efe7"),("lime","#c9f36a"),("olive","#6f8a1f"),("mute","#92958d")]
    for i,(nm,hx) in enumerate(sw):
        x=40+i*84; b+=f'<rect x="{x}" y="72" width="64" height="40" rx="8" fill="{hx}" stroke="{c["ln"]}"/>'+mono(x,128,nm.upper(),c,c["fg"],s=9.5,ls=1)+mono(x,141,hx.upper(),c,s=9.5,ls=.4)
    b+=f'<line x1="470" y1="72" x2="470" y2="140" stroke="{c["ln"]}"/><text x="494" y="122" font-family="{SER}" font-size="58" fill="{c["fg"]}">Aa</text><text x="560" y="122" font-family="{SER}" font-size="58" font-style="italic" fill="{c["ac"]}">g</text>'
    b+="".join(mono(616,y,k,c,s=9.5,ls=1)+mono(664,y,v,c,c["fg"],s=10,ls=.3) for y,k,v in [(90,"SERIF","Instrument Serif"),(110,"SANS","Inter"),(130,"MONO","IBM Plex Mono")])
    open(f"{o}/tokens-{th}.svg","w").write(svg(W,H,b,c))
