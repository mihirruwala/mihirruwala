# Builds the hero (header-dark/light.svg). Fonts are subset and embedded so they render inside GitHub's <img>.
import base64,os
from PIL import ImageFont
F=os.path.join(os.path.dirname(__file__),"fonts")
b64=lambda f:base64.b64encode(open(f"{F}/{f}","rb").read()).decode()
w=lambda t,f,s:ImageFont.truetype(f"{F}/{f}",s).getlength(t)
css=f"@font-face{{font-family:IS;src:url(data:font/ttf;base64,{b64('is.ttf')})}}@font-face{{font-family:ISI;src:url(data:font/ttf;base64,{b64('isi.ttf')})}}@font-face{{font-family:HAND;src:url(data:font/ttf;base64,{b64('cav.ttf')})}}"
SANS="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
T={"dark":dict(bg="#0d1117",fg="#e6edf3",mu="#7d8590",ac="#c9f36a",note="#f2cc60"),
   "light":dict(bg="#ffffff",fg="#1f2328",mu="#656d76",ac="#4d7c0f",note="#b4690e")}
BLUE="#0d99ff"
for th,c in T.items():
    W,H=840,380; S=78; X=26; Y=[128,214,304]
    b=f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>'
    b+=f'<text x="{X+2}" y="40" font-family="{SANS}" font-size="15" fill="{c["fg"]}" font-weight="600">Mihir Ruwala<tspan fill="{c["mu"]}" font-weight="400">  ·  2nd-year CSE, VIT Vellore</tspan></text>'
    b+=f'<g font-family="IS,Georgia,serif" font-size="{S}" fill="{c["fg"]}"><text x="{X}" y="{Y[0]}">I build for the web and iOS,</text><text x="{X}" y="{Y[1]}">and study why people</text></g>'
    b+=f'<text x="{X}" y="{Y[2]}" font-family="ISI,Georgia,serif" font-style="italic" font-size="{S+6}" fill="{c["ac"]}">trust AI.</text>'
    tw=w("trust AI.","isi.ttf",S+6); sx,sy,sw,sh=X-6,Y[2]-62,tw+14,80
    b+=f'<rect x="{sx}" y="{sy}" width="{sw:.1f}" height="{sh}" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    b+="".join(f'<rect x="{x-4:.1f}" y="{y-4}" width="8" height="8" fill="#fff" stroke="{BLUE}" stroke-width="1.5"/>' for x in (sx,sx+sw) for y in (sy,sy+sh))
    lab=f"{round(sw)} × {sh}"; lw=len(lab)*6.6+12
    b+=f'<rect x="{sx+sw/2-lw/2:.1f}" y="{sy+sh+8}" width="{lw:.1f}" height="18" rx="3" fill="{BLUE}"/><text x="{sx+sw/2:.1f}" y="{sy+sh+21}" text-anchor="middle" font-family="{SANS}" font-size="11" font-weight="500" fill="#fff">{lab}</text>'
    # handwritten note + hand-drawn arrow
    nx,ny=W-40-w("AI detector can be trusted?","cav.ttf",28),262
    b+=f'<g transform="rotate(-4 {nx} {ny})" font-family="HAND,cursive" font-size="28" fill="{c["note"]}"><text x="{nx}" y="{ny}">my research:</text><text x="{nx}" y="{ny+30}">who gets to decide if an</text><text x="{nx}" y="{ny+60}">AI detector can be trusted?</text></g>'
    ax=sx+sw+14; ex,ey=ax+4,sy+sh/2-4; c2x,c2y=ax+70,ey-26
    b+=f'<path d="M{nx-8} {ny-14} C {nx-90} {ny-46}, {c2x} {c2y}, {ex} {ey}" fill="none" stroke="{c["note"]}" stroke-width="2.2" stroke-linecap="round"/>'
    # arrowhead follows the curve's end tangent (c2 -> end), so the tip and the line meet
    import math
    th0=math.atan2(c2y-ey,c2x-ex); L=14; A=math.radians(30)
    (p1x,p1y),(p2x,p2y)=[(ex+L*math.cos(th0+s),ey+L*math.sin(th0+s)) for s in (A,-A)]
    b+=f'<path d="M{p1x:.1f} {p1y:.1f} L{ex} {ey} L{p2x:.1f} {p2y:.1f}" fill="none" stroke="{c["note"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
    # multiplayer cursor
    cx,cy=sx+sw-30,sy+sh-14
    b+=f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;220 -150;380 -60;0 0" keyTimes="0;.4;.6;.8;1" dur="8s" calcMode="spline" keySplines="0 0 1 1;.65 0 .35 1;.65 0 .35 1;.22 1 .36 1" repeatCount="indefinite"/><g transform="translate({cx} {cy})"><path d="M0 0 L0 18 L5 13.4 L8.2 20.6 L11.2 19.3 L8 12.3 L14.4 12.3 Z" fill="#ff5ccd" stroke="#fff" stroke-width="1.3" stroke-linejoin="round"/><rect x="13" y="19" width="46" height="20" rx="4" fill="#ff5ccd"/><text x="36" y="33" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="600" fill="#fff">mihir</text></g></g>'
    open(f"{os.path.dirname(__file__)}/header-{th}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>{css}</style>{b}</svg>')
