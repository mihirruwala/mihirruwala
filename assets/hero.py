# Builds the hero (header-dark/light.svg) as native iOS UI: SF Pro large title, iOS text selection with the
# edit menu, and the handwritten note as a Markup annotation. SF Pro can't be embedded (licence), so the title
# uses the system font stack (SF on Apple devices); only the Markup hand (Caveat) is embedded.
import base64,math,os
from PIL import ImageFont
D=os.path.dirname(__file__); F=f"{D}/fonts"
b64=lambda f:base64.b64encode(open(f"{F}/{f}","rb").read()).decode()
def sf(s,wt="Bold"):
    f=ImageFont.truetype("/System/Library/Fonts/SFNS.ttf",s); f.set_variation_by_name(wt); return f
cav=lambda s:ImageFont.truetype(f"{F}/cav.ttf",s)
css=f"@font-face{{font-family:HAND;src:url(data:font/ttf;base64,{b64('cav.ttf')})}}"
SF="-apple-system,'SF Pro Display',BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
SFT="-apple-system,'SF Pro Text',BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
# iOS system colours (dark / light variants); backgrounds stay GitHub's so the card sits flush on the profile.
T={"dark":dict(bg="#0d1117",label="#ffffff",sec="#98989f",blue="#0a84ff",hi=.32,menu="#2c2c2e",mtx="#ffffff",div="#48484a",note="#ffd60a",ptr="#ffffff"),
   "light":dict(bg="#ffffff",label="#000000",sec="#6c6c70",blue="#007aff",hi=.2,menu="#f2f2f7",mtx="#000000",div="#c6c6c8",note="#c26a00",ptr="#000000")}
W,H=840,380; X=26; S=58; Y=[118,188,258]; TR=-0.6  # large-title tracking, px
for th,c in T.items():
    b=f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>'
    b+=f'<text x="{X}" y="44" font-family="{SFT}" font-size="15" font-weight="600" fill="{c["label"]}">Mihir Ruwala<tspan fill="{c["sec"]}" font-weight="400">  ·  2nd-year CSE, VIT Vellore</tspan></text>'
    b+=f'<g font-family="{SF}" font-size="{S}" font-weight="700" letter-spacing="{TR}" fill="{c["label"]}"><text x="{X}" y="{Y[0]}">I build for the web and iOS,</text><text x="{X}" y="{Y[1]}">and study why people</text>'
    # selected run: highlight sits behind the glyphs, like UITextView
    sel="trust AI."; tw=sf(S).getlength(sel)+TR*len(sel)
    sx,sy,sw,sh=X-3,Y[2]-S*.78,tw+10,S*1.0
    b+=f'</g><rect x="{sx:.1f}" y="{sy:.1f}" width="{sw:.1f}" height="{sh:.1f}" fill="{c["blue"]}" fill-opacity="{c["hi"]}"/>'
    b+=f'<text x="{X}" y="{Y[2]}" font-family="{SF}" font-size="{S}" font-weight="700" letter-spacing="{TR}" fill="{c["label"]}">{sel}</text>'
    # lollipop handles: knob on top of the start, under the end
    for hx,ky in ((sx,sy-5),(sx+sw,sy+sh+5)):
        b+=f'<rect x="{hx-1:.1f}" y="{sy:.1f}" width="2" height="{sh:.1f}" fill="{c["blue"]}"/><circle cx="{hx:.1f}" cy="{ky:.1f}" r="5.5" fill="{c["blue"]}"/>'
    # edit menu (iOS 16+), below the selection since the title fills the space above
    items=["Copy","Look Up","Translate","Share"]; fs=sf(15,"Regular"); pad=14
    iw=[fs.getlength(t)+2*pad for t in items]; mw=sum(iw)+34; mh=38
    mx=max(X-2,sx+sw/2-mw/2); my=sy+sh+20
    b+=f'<defs><filter id="sh" x="-20%" y="-40%" width="140%" height="200%"><feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000" flood-opacity="{.45 if th=="dark" else .16}"/></filter></defs>'
    tipx=sx+sw/2
    b+=f'<g filter="url(#sh)"><rect x="{mx:.1f}" y="{my:.1f}" width="{mw:.1f}" height="{mh}" rx="9" fill="{c["menu"]}"/><path d="M{tipx-8:.1f} {my+.5:.1f} L{tipx:.1f} {my-7:.1f} L{tipx+8:.1f} {my+.5:.1f} Z" fill="{c["menu"]}"/></g>'
    x=mx
    for i,(t,wi) in enumerate(zip(items,iw)):
        if i==1: b+=f'<rect x="{x+3:.1f}" y="{my+3}" width="{wi-6:.1f}" height="{mh-6}" rx="6" fill="{c["mtx"]}" fill-opacity=".1"/>'
        b+=f'<text x="{x+wi/2:.1f}" y="{my+24.5:.1f}" text-anchor="middle" font-family="{SFT}" font-size="15" fill="{c["mtx"]}">{t}</text>'
        x+=wi; b+=f'<rect x="{x:.1f}" y="{my+9}" width="1" height="{mh-18}" fill="{c["div"]}"/>'
    b+=f'<path d="M{x+13:.1f} {my+13} L{x+19:.1f} {my+19} L{x+13:.1f} {my+25}" fill="none" stroke="{c["mtx"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    # Markup: handwritten note + pen arrow, arrowhead along the curve's end tangent
    lines=["my research:","who gets to decide if an","AI detector can be trusted?"]
    nx,ny=W-36-cav(28).getlength(lines[2]),262
    b+=f'<g transform="rotate(-4 {nx:.1f} {ny})" font-family="HAND,cursive" font-size="28" fill="{c["note"]}">'+"".join(f'<text x="{nx:.1f}" y="{ny+30*i}">{t}</text>' for i,t in enumerate(lines))+'</g>'
    ex,ey=sx+sw+18,sy+sh/2-2; c2x,c2y=ex+66,ey-24
    b+=f'<path d="M{nx-8:.1f} {ny-14} C {nx-90:.1f} {ny-46}, {c2x:.1f} {c2y:.1f}, {ex:.1f} {ey:.1f}" fill="none" stroke="{c["note"]}" stroke-width="2.4" stroke-linecap="round"/>'
    a=math.atan2(c2y-ey,c2x-ex); L=14; A=math.radians(30)
    (p1x,p1y),(p2x,p2y)=[(ex+L*math.cos(a+s),ey+L*math.sin(a+s)) for s in (A,-A)]
    b+=f'<path d="M{p1x:.1f} {p1y:.1f} L{ex:.1f} {ey:.1f} L{p2x:.1f} {p2y:.1f}" fill="none" stroke="{c["note"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    open(f"{D}/header-{th}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>{css}</style>{b}</svg>')
