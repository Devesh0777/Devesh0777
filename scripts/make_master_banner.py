import os
import random
import numpy as np
from PIL import Image, ImageOps, ImageFilter

def floyd_steinberg_dither(img_array):
    h, w = img_array.shape
    dithered = np.copy(img_array)
    dots = []
    for y in range(h):
        for x in range(w):
            old = dithered[y, x]
            new = 255 if old > 128 else 0
            dithered[y, x] = new
            err = old - new
            if new == 0:
                dots.append((x, y))
            if x + 1 < w:
                dithered[y, x+1] = min(max(dithered[y, x+1] + err * 7/16, 0), 255)
            if y + 1 < h:
                if x > 0:
                    dithered[y+1, x-1] = min(max(dithered[y+1, x-1] + err * 3/16, 0), 255)
                dithered[y+1, x] = min(max(dithered[y+1, x] + err * 5/16, 0), 255)
                if x + 1 < w:
                    dithered[y+1, x+1] = min(max(dithered[y+1, x+1] + err * 1/16, 0), 255)
    return dots

def build_banner():
    img_path = "photo1.png"

    if not os.path.exists(img_path):
        img  = Image.new('L', (380, 480), color=128)
        mask = Image.new('L', (380, 480), 255)
    else:
        raw = Image.open(img_path)
        if raw.mode == 'RGBA':
            r, g, b, a = raw.split()
            img  = raw.convert('L')
            mask = a
        else:
            img  = raw.convert('L')
            mask = Image.new('L', img.size, 255)

    W, H = 380, 480
    img  = ImageOps.fit(img,  (W, H), Image.Resampling.LANCZOS)
    mask = ImageOps.fit(mask, (W, H), Image.Resampling.LANCZOS)

    img = ImageOps.autocontrast(img, cutoff=2)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    img = ImageOps.invert(img)

    img_arr  = np.array(img,  dtype=float)
    mask_arr = np.array(mask, dtype=float)

    all_dots = floyd_steinberg_dither(img_arr)
    dots = [(x, y) for x, y in all_dots if mask_arr[y, x] > 128]
    dots = random.sample(dots, min(len(dots), 4000))

    # Build compact SVG using CSS keyframe classes only (no SMIL)
    NP = 8  # number of animation phases
    css_phases = ""
    for i in range(NP):
        delay = round(i * 1.0, 1)
        dur   = round(1.8 + (i % 3) * 0.7, 1)
        css_phases += f".p{i}{{animation:tw {dur}s {delay}s infinite;}}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 540" width="860" height="540">
<style>
.bg{{fill:#0D1117}}.dot{{fill:#A78BFA;shape-rendering:crispEdges}}
.lbl{{fill:#22D3EE;font-family:monospace;font-size:12px;letter-spacing:2px}}
.key{{fill:#10B981;font-family:monospace;font-size:17px}}
.val{{fill:#C4B5FD;font-family:monospace;font-size:17px;font-weight:bold}}
.div{{fill:none;stroke:#22D3EE;stroke-width:1;opacity:0.4}}
.cur{{fill:#22D3EE;animation:blink 1.1s infinite}}
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
{css_phases}
</style>
<rect width="860" height="540" class="bg" rx="10"/>
<line x1="415" y1="16" x2="415" y2="524" class="div"/>
<text x="435" y="58" class="lbl">SYSTEM.INFO</text>
<line x1="435" y1="65" x2="840" y2="65" stroke="#22D3EE" stroke-width="1" opacity="0.25"/>
<text x="435" y="105"><tspan class="key">Subject  </tspan><tspan class="val"> Devesh</tspan></text>
<text x="435" y="145"><tspan class="key">Role     </tspan><tspan class="val"> Full Stack Developer</tspan></text>
<text x="435" y="185"><tspan class="key">Location </tspan><tspan class="val"> India</tspan></text>
<text x="435" y="225"><tspan class="key">Education</tspan><tspan class="val"> Information Tech</tspan></text>
<text x="435" y="265"><tspan class="key">Status   </tspan><tspan class="val"> Building &amp; Learning</tspan></text>
<text x="435" y="305"><tspan class="key">ToolChain</tspan><tspan class="val"> Git · HTML · CSS</tspan></text>
<text x="435" y="345"><tspan class="key">Core.Lang</tspan><tspan class="val"> Python · C++</tspan></text>
<rect x="435" y="368" width="10" height="18" class="cur"/>
<g transform="translate(18,30)">
"""

    for x, y in dots:
        p = random.randint(0, NP - 1)
        svg += f'<rect x="{x}" y="{y}" width="2" height="2" class="dot p{p}"/>\n'

    svg += "</g>\n</svg>"

    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Created dark.svg —", round(len(svg)/1024), "KB")

if __name__ == "__main__":
    build_banner()
