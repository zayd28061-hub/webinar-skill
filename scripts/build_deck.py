#!/usr/bin/env python3
"""Render a webinar deck.json into a self-contained presentation HTML file.

Usage:  python3 build_deck.py deck.json deck.html

Keys in the rendered deck:
  → / space / click   next        ← / backspace   previous
  G  grid overview    S  speaker notes    F  fullscreen
  P  print view (then Cmd-P -> Save as PDF, one slide per page)
  Home / End          first / last slide
"""
import json, sys, html, re, os

DEFAULT_THEME = {
    "bg": "#0C0C0C", "surface": "#161616", "text": "#F2EDE8",
    "muted": "#8C8680", "accent": "#C9A96E", "line": "#262322",
    "display": "'Inter', system-ui, sans-serif",
    "body": "'Inter', system-ui, sans-serif",
    "mono": "'DM Mono', ui-monospace, monospace",
}

def esc(s):
    return html.escape(str(s if s is not None else ""))

def rich(s):
    """Escape, then turn [[word]] into an accent span and *word* into a dim span."""
    out = esc(s)
    out = re.sub(r"\[\[(.+?)\]\]", r'<span class="ac">\1</span>', out)
    out = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r'<span class="dim">\1</span>', out)
    out = out.replace("\n", "<br>")
    return out

# ---------------------------------------------------------------- slide types

def s_cover(d):
    return f"""<div class="pad center">
      {kicker(d)}
      <h1 class="t-cover">{rich(d.get('title',''))}</h1>
      {f'<p class="sub">{rich(d["subtitle"])}</p>' if d.get('subtitle') else ''}
      {f'<p class="presenter">{rich(d["presenter"])}</p>' if d.get('presenter') else ''}
    </div>"""

def s_section(d):
    return f"""<div class="pad center sect">
      {kicker(d)}
      <h2 class="t-section">{rich(d.get('title', d.get('text','')))}</h2>
      {f'<p class="sub">{rich(d["sub"])}</p>' if d.get('sub') else ''}
    </div>"""

def s_statement(d):
    al = d.get("align", "left")
    return f"""<div class="pad {al}">
      {kicker(d)}
      <h2 class="t-stmt">{rich(d.get('text',''))}</h2>
      {f'<p class="sub">{rich(d["sub"])}</p>' if d.get('sub') else ''}
    </div>"""

def s_keyword(d):
    return f"""<div class="pad center">
      {kicker(d)}
      <h2 class="t-key">{rich(d.get('text',''))}</h2>
      {f'<p class="sub">{rich(d["sub"])}</p>' if d.get('sub') else ''}
    </div>"""

def s_question(d):
    return f"""<div class="pad center">
      {kicker(d)}
      <h2 class="t-q">{rich(d.get('text',''))}</h2>
    </div>"""

def s_number(d):
    return f"""<div class="pad center">
      {kicker(d)}
      <div class="t-num">{rich(d.get('value',''))}</div>
      {f'<p class="numlabel">{rich(d["label"])}</p>' if d.get('label') else ''}
      {f'<p class="src">{esc(d["source"])}</p>' if d.get('source') else ''}
    </div>"""

def col(c):
    items = "".join(f"<li>{rich(i)}</li>" for i in c.get("items", []))
    return f"""<div class="col"><div class="collabel">{esc(c.get('label',''))}</div><ul>{items}</ul></div>"""

def s_contrast(d):
    return f"""<div class="pad">
      {kicker(d)}
      {f'<h3 class="t-small">{rich(d["title"])}</h3>' if d.get('title') else ''}
      <div class="cols">{col(d.get('left',{}))}<div class="vr"></div>{col(d.get('right',{}))}</div>
    </div>"""

def s_list(d):
    items = "".join(f"<li>{rich(i)}</li>" for i in d.get("items", []))
    return f"""<div class="pad">
      {kicker(d)}
      {f'<h3 class="t-small">{rich(d["title"])}</h3>' if d.get('title') else ''}
      <ul class="biglist">{items}</ul>
    </div>"""

def s_build(d):
    upto = d.get("upto", len(d.get("items", [])))
    items = "".join(
        f'<li class="{"live" if n == upto else ("done" if n < upto else "pending")}">'
        f'<span class="bn">{n:02d}</span>{rich(i)}</li>'
        for n, i in enumerate(d.get("items", []), 1)
    )
    return f"""<div class="pad">
      {kicker(d)}
      {f'<h3 class="t-small">{rich(d["title"])}</h3>' if d.get('title') else ''}
      <ul class="buildlist">{items}</ul>
    </div>"""

def s_quote(d):
    return f"""<div class="pad center">
      {kicker(d)}
      <blockquote class="t-quote">{rich(d.get('text',''))}</blockquote>
      {f'<p class="attrib">{esc(d["attrib"])}</p>' if d.get('attrib') else ''}
    </div>"""

def s_proof(d):
    rows = [("started", d.get("start")), ("what happened", d.get("event")), ("how long", d.get("duration"))]
    body = "".join(
        f'<div class="prow"><div class="plabel">{esc(l)}</div><div class="pval">{rich(v)}</div></div>'
        for l, v in rows if v
    )
    img = f'<div class="pimg"><img src="{esc(d["img"])}" alt=""></div>' if d.get("img") else ""
    return f"""<div class="pad">
      {kicker(d)}
      {f'<h3 class="t-mid">{rich(d["headline"])}</h3>' if d.get('headline') else ''}
      <div class="proofwrap"><div class="ptable">{body}</div>{img}</div>
    </div>"""

def s_diagram(d):
    if d.get("svg"):
        inner = d["svg"]
    else:
        nodes = d.get("nodes", [])
        parts = []
        for i, n in enumerate(nodes):
            if i:
                parts.append('<div class="arrow">&rarr;</div>')
            parts.append(f'<div class="node">{rich(n)}</div>')
        inner = f'<div class="flow">{"".join(parts)}</div>'
    return f"""<div class="pad center">
      {kicker(d)}
      {f'<h3 class="t-small">{rich(d["title"])}</h3>' if d.get('title') else ''}
      <div class="diagram">{inner}</div>
    </div>"""

def s_stack(d):
    rows = "".join(
        f'<div class="srow"><div class="sitem">{rich(r.get("item",""))}</div>'
        f'<div class="sval">{esc(r.get("value",""))}</div></div>'
        for r in d.get("rows", [])
    )
    total = f'<div class="srow total"><div class="sitem">{esc(d.get("total_label","Total value"))}</div><div class="sval">{esc(d["total"])}</div></div>' if d.get("total") else ""
    price = f'<div class="stackprice">{rich(d["price"])}</div>' if d.get("price") else ""
    return f"""<div class="pad">
      {kicker(d)}
      {f'<h3 class="t-small">{rich(d["title"])}</h3>' if d.get('title') else ''}
      <div class="stack">{rows}{total}</div>{price}
    </div>"""

def s_price(d):
    return f"""<div class="pad center">
      {kicker(d)}
      <div class="t-price">{rich(d.get('value',''))}</div>
      {f'<p class="sub">{rich(d["terms"])}</p>' if d.get('terms') else ''}
    </div>"""

def s_cta(d):
    return f"""<div class="pad center">
      {kicker(d)}
      <h2 class="t-stmt center-t">{rich(d.get('text',''))}</h2>
      {f'<div class="ctabtn">{rich(d["action"])}</div>' if d.get('action') else ''}
      {f'<p class="url">{esc(d["url"])}</p>' if d.get('url') else ''}
    </div>"""

def s_close(d):
    return f"""<div class="pad center closing">
      {kicker(d)}
      <h2 class="t-mid">{rich(d.get('text',''))}</h2>
      {f'<div class="ctabtn">{rich(d["action"])}</div>' if d.get('action') else ''}
      {f'<p class="url">{esc(d["url"])}</p>' if d.get('url') else ''}
    </div>"""

def s_image(d):
    cap = f'<div class="caption">{rich(d["caption"])}</div>' if d.get("caption") else ""
    return f"""<div class="imgslide"><img src="{esc(d.get('src',''))}" alt="">{cap}</div>"""

def kicker(d):
    return f'<div class="kicker">{esc(d["kicker"])}</div>' if d.get("kicker") else ""

RENDER = {
    "cover": s_cover, "section": s_section, "statement": s_statement, "keyword": s_keyword,
    "number": s_number, "contrast": s_contrast, "list": s_list, "build": s_build,
    "quote": s_quote, "proof": s_proof, "diagram": s_diagram, "stack": s_stack,
    "question": s_question, "image": s_image, "price": s_price, "cta": s_cta, "close": s_close,
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;background:#000;overflow:hidden;font-family:var(--body);
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
#stage{position:fixed;inset:0;display:grid;place-items:center;background:#000}
#deck{width:1600px;height:900px;position:relative;transform-origin:center center}
.slide{position:absolute;inset:0;background:var(--bg);color:var(--text);
  opacity:0;pointer-events:none;transition:opacity .2s ease;overflow:hidden}
.slide.on{opacity:1;pointer-events:auto}
.pad{position:absolute;inset:96px;display:flex;flex-direction:column;justify-content:center}
.pad.center{align-items:center;text-align:center}
.pad.right{align-items:flex-end;text-align:right}
.pad>*{max-width:1200px}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;
  color:var(--muted);margin-bottom:40px}
h1,h2,h3{font-family:var(--display);font-weight:700;letter-spacing:-.04em;line-height:.98}
.t-cover{font-size:132px;letter-spacing:-.045em}
.t-section{font-size:104px}
.t-stmt{font-size:76px;letter-spacing:-.035em;line-height:1.04}
.t-key{font-size:184px;letter-spacing:-.05em;line-height:.9}
.t-q{font-size:88px;letter-spacing:-.035em;line-height:1.05;font-weight:300}
.t-mid{font-size:56px;letter-spacing:-.03em}
.t-small{font-size:36px;letter-spacing:-.02em;margin-bottom:56px;font-weight:700}
.t-num{font-family:var(--display);font-weight:700;font-size:248px;letter-spacing:-.055em;line-height:.85}
.t-price{font-family:var(--display);font-weight:700;font-size:176px;letter-spacing:-.05em;line-height:.9}
.t-quote{font-family:var(--display);font-weight:300;font-size:56px;line-height:1.25;letter-spacing:-.02em;max-width:1120px}
.ac{color:var(--accent)}
.dim{color:var(--muted)}
.sub{font-size:29px;font-weight:300;color:var(--muted);margin-top:36px;line-height:1.45;max-width:880px}
.presenter{font-family:var(--mono);font-size:13px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--muted);margin-top:72px}
.numlabel{font-size:27px;font-weight:300;color:var(--text);margin-top:40px;max-width:820px;line-height:1.4}
.src{font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-top:28px}
.attrib{font-family:var(--mono);font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-top:48px}
.sect{background:var(--surface)}
.center-t{text-align:center}
.cols{display:flex;gap:0;align-items:stretch;width:100%}
.col{flex:1;padding-right:64px}
.cols .col:last-child{padding-right:0;padding-left:64px}
.vr{width:1px;background:var(--line)}
.collabel{font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;
  color:var(--muted);margin-bottom:40px}
.col ul{list-style:none}
.col li{font-size:36px;font-weight:300;line-height:1.3;margin-bottom:32px;letter-spacing:-.01em}
.biglist{list-style:none}
.biglist li{font-size:44px;font-weight:300;line-height:1.25;margin-bottom:40px;letter-spacing:-.015em}
.buildlist{list-style:none;width:100%}
.buildlist li{font-size:34px;font-weight:300;line-height:1.3;margin-bottom:26px;display:flex;
  gap:32px;align-items:baseline;transition:color .2s ease,opacity .2s ease}
.buildlist li.pending{opacity:0}
.buildlist li.done{color:var(--muted)}
.buildlist li.live{color:var(--text)}
.bn{font-family:var(--mono);font-size:13px;letter-spacing:.14em;color:var(--muted);min-width:36px}
.buildlist li.live .bn{color:var(--accent)}
.proofwrap{display:flex;gap:80px;align-items:center}
.ptable{flex:1}
.prow{display:flex;gap:40px;padding:28px 0;border-top:1px solid var(--line);align-items:baseline}
.prow:last-child{border-bottom:1px solid var(--line)}
.plabel{font-family:var(--mono);font-size:12px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--muted);min-width:220px}
.pval{font-size:34px;font-weight:300;line-height:1.3;letter-spacing:-.01em}
.pimg img{max-width:420px;max-height:560px;border-radius:6px;display:block}
.diagram{width:100%;display:flex;justify-content:center}
.flow{display:flex;align-items:center;gap:28px;flex-wrap:wrap;justify-content:center}
.node{border:1px solid var(--line);background:var(--surface);border-radius:6px;padding:28px 34px;
  font-size:24px;font-weight:300;letter-spacing:-.01em;max-width:280px;line-height:1.3}
.arrow{color:var(--muted);font-size:30px}
.stack{width:100%;max-width:1100px}
.srow{display:flex;justify-content:space-between;gap:48px;padding:22px 0;
  border-bottom:1px solid var(--line);align-items:baseline}
.sitem{font-size:28px;font-weight:300;letter-spacing:-.01em}
.sval{font-family:var(--mono);font-size:19px;color:var(--muted);white-space:nowrap}
.srow.total{border-bottom:none;border-top:1px solid var(--accent);margin-top:12px;padding-top:26px}
.srow.total .sitem{font-weight:700;font-size:30px}
.srow.total .sval{color:var(--accent);font-size:26px}
.stackprice{font-family:var(--display);font-weight:700;font-size:92px;letter-spacing:-.045em;margin-top:48px}
.ctabtn{margin-top:56px;display:inline-block;background:var(--accent);color:var(--bg);
  font-family:var(--display);font-weight:700;font-size:30px;letter-spacing:-.02em;padding:22px 52px;border-radius:5px}
.url{font-family:var(--mono);font-size:17px;letter-spacing:.06em;color:var(--muted);margin-top:34px}
.closing{background:var(--surface)}
.imgslide{position:absolute;inset:0}
.imgslide img{width:100%;height:100%;object-fit:cover}
.caption{position:absolute;left:96px;bottom:96px;right:96px;font-size:30px;font-weight:300;
  text-shadow:0 2px 24px rgba(0,0,0,.85);line-height:1.35}
#hud{position:absolute;right:40px;bottom:32px;font-family:var(--mono);font-size:11px;
  letter-spacing:.18em;text-transform:uppercase;color:var(--muted);opacity:.5;z-index:40;
  display:flex;gap:22px;pointer-events:none}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:38vh;overflow:auto;background:#0a0a0a;
  border-top:1px solid #222;padding:26px 36px;color:#ddd;font-size:16px;line-height:1.6;
  display:none;z-index:60;font-family:var(--body)}
#notes.on{display:block}
#notes .nlabel{font-family:var(--mono);font-size:10px;letter-spacing:.24em;text-transform:uppercase;
  color:#666;margin-bottom:12px}
#notes .nnext{margin-top:20px;padding-top:16px;border-top:1px solid #1d1d1d;color:#777;font-size:14px}
#grid{position:fixed;inset:0;background:#070707;overflow:auto;padding:40px;display:none;z-index:70}
#grid.on{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;align-content:start}
.gcell{aspect-ratio:16/9;background:var(--bg);border:1px solid #1c1c1c;border-radius:4px;
  padding:14px;overflow:hidden;cursor:pointer;position:relative}
.gcell:hover{border-color:var(--accent)}
.gcell .gt{font-family:var(--display);font-weight:700;font-size:13px;line-height:1.2;color:var(--text);
  letter-spacing:-.02em;max-height:72px;overflow:hidden}
.gcell .gk{font-family:var(--mono);font-size:8px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--muted);margin-bottom:8px}
.gcell .gn{position:absolute;right:10px;bottom:8px;font-family:var(--mono);font-size:9px;color:#444}
.gcell.cur{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
@media print{
  html,body{overflow:visible;background:#fff;height:auto}
  #stage{position:static;display:block}
  #deck{width:auto;height:auto;transform:none!important}
  .slide{position:relative;opacity:1!important;pointer-events:auto;width:1600px;height:900px;
    page-break-after:always;break-after:page;display:block}
  #hud,#notes,#grid{display:none!important}
  @page{size:1600px 900px;margin:0}
}
"""

JS = """
var N=SLIDES.length, i=0, notesOn=false;
var stage=document.getElementById('stage'), deck=document.getElementById('deck');
function fit(){var s=Math.min(window.innerWidth/1600, window.innerHeight/900);
  deck.style.transform='scale('+s+')';}
window.addEventListener('resize',fit); fit();
function show(n){
  if(n<0)n=0; if(n>N-1)n=N-1; i=n;
  for(var k=0;k<N;k++){document.getElementById('s'+k).classList.toggle('on',k===i);}
  document.getElementById('hud-n').textContent=(i+1)+' / '+N;
  document.getElementById('hud-a').textContent=SLIDES[i].act||'';
  document.getElementById('nbody').innerHTML=SLIDES[i].note||'<i style="color:#555">no note</i>';
  var nx=SLIDES[i+1];
  document.getElementById('nnext').textContent= nx ? ('NEXT  ·  '+(nx.label||'')) : 'END';
  var cur=document.querySelector('.gcell.cur'); if(cur)cur.classList.remove('cur');
  var gc=document.getElementById('g'+i); if(gc)gc.classList.add('cur');
  try{location.hash=i+1;}catch(e){}
}
function next(){show(i+1)} function prev(){show(i-1)}
document.addEventListener('keydown',function(e){
  var g=document.getElementById('grid');
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();next()}
  else if(e.key==='ArrowLeft'||e.key==='Backspace'||e.key==='PageUp'){e.preventDefault();prev()}
  else if(e.key==='Home'){show(0)} else if(e.key==='End'){show(N-1)}
  else if(e.key==='s'||e.key==='S'){notesOn=!notesOn;document.getElementById('notes').classList.toggle('on',notesOn)}
  else if(e.key==='g'||e.key==='G'){g.classList.toggle('on')}
  else if(e.key==='f'||e.key==='F'){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}
  else if(e.key==='p'||e.key==='P'){window.print()}
  else if(e.key==='Escape'){g.classList.remove('on')}
});
stage.addEventListener('click',function(e){ if(e.clientX < window.innerWidth*0.22) prev(); else next(); });
document.getElementById('grid').addEventListener('click',function(e){
  var c=e.target.closest('.gcell'); if(!c)return;
  show(parseInt(c.dataset.i,10)); document.getElementById('grid').classList.remove('on');
});
var h=parseInt((location.hash||'').replace('#',''),10);
show(isNaN(h)?0:h-1);
"""

def plain(d):
    for k in ("text", "title", "value", "headline"):
        if d.get(k):
            return re.sub(r"\[\[|\]\]", "", str(d[k]))
    return d.get("type", "")

def build(spec, out_path):
    meta = spec.get("meta", {})
    theme = dict(DEFAULT_THEME)
    theme.update(meta.get("theme", {}))
    slides = spec.get("slides", [])

    body, index = [], []
    for n, d in enumerate(slides):
        t = d.get("type", "statement")
        fn = RENDER.get(t, s_statement)
        body.append(f'<section class="slide" id="s{n}" data-type="{esc(t)}">{fn(d)}</section>')
        index.append({
            "act": d.get("act", ""),
            "note": rich(d.get("note", "")) if d.get("note") else "",
            "label": plain(d)[:70],
        })
        cells_txt = plain(d)
        index[-1]["cell"] = cells_txt

    cells = "".join(
        f'<div class="gcell" id="g{n}" data-i="{n}"><div class="gk">{esc(s.get("act",""))}</div>'
        f'<div class="gt">{esc(plain(s)[:90])}</div><div class="gn">{n+1}</div></div>'
        for n, s in enumerate(slides)
    )

    font_link = meta.get("font_link",
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;800&"
        "family=DM+Mono:wght@300;400&display=swap")

    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(meta.get('title','Webinar'))}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{esc(font_link)}" rel="stylesheet">
<style>
:root{{--bg:{theme['bg']};--surface:{theme['surface']};--text:{theme['text']};
--muted:{theme['muted']};--accent:{theme['accent']};--line:{theme['line']};
--display:{theme['display']};--body:{theme['body']};--mono:{theme['mono']};}}
{CSS}
</style></head><body>
<div id="stage"><div id="deck">{''.join(body)}
<div id="hud"><span id="hud-a"></span><span id="hud-n"></span></div>
</div></div>
<div id="notes"><div class="nlabel">Speaker notes &nbsp;·&nbsp; press S to hide</div>
<div id="nbody"></div><div class="nnext" id="nnext"></div></div>
<div id="grid">{cells}</div>
<script>var SLIDES={json.dumps(index)};
{JS}
</script></body></html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    return len(slides)

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".html"
    with open(src, encoding="utf-8") as f:
        spec = json.load(f)
    n = build(spec, out)

    # quality check
    warn = []
    prev_type, run = None, 0
    DENSE = ("quote", "stack", "proof", "contrast", "list", "build", "cover")
    for idx, d in enumerate(spec.get("slides", []), 1):
        head = " ".join(str(d.get(k, "")) for k in ("text", "title", "headline") if d.get(k))
        sub = " ".join(str(d.get(k, "")) for k in ("sub", "subtitle", "label", "terms") if d.get(k))
        hw = len(re.sub(r"\[\[|\]\]", "", head).split())
        sw = len(re.sub(r"\[\[|\]\]", "", sub).split())
        if d.get("type") not in DENSE and hw > 14:
            warn.append(f"  slide {idx}: headline is {hw} words (max 14) — {head[:64]}")
        if sw > 14:
            warn.append(f"  slide {idx}: sub is {sw} words (max 14) — {sub[:64]}")
        if (head + " " + sub).count("[[") > 1:
            warn.append(f"  slide {idx}: more than one accent word")
        if not d.get("note"):
            warn.append(f"  slide {idx}: no speaker note")
        run = run + 1 if d.get("type") == prev_type else 1
        prev_type = d.get("type")
        if run == 7 and prev_type not in ("build",):
            warn.append(f"  slide {idx}: 7 consecutive '{prev_type}' slides — vary the rhythm")
    print(f"built {out} — {n} slides")
    if warn:
        print(f"\n{len(warn)} quality warnings:")
        print("\n".join(warn[:40]))
    else:
        print("quality check: clean")

if __name__ == "__main__":
    main()
