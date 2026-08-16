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

def build_hacker_profile_svg():
    img_path = "photo1.png"

    if not os.path.exists(img_path):
        img  = Image.new('L', (340, 340), color=128)
        mask = Image.new('L', (340, 340), 255)
    else:
        raw = Image.open(img_path)
        if raw.mode == 'RGBA':
            r, g, b, a = raw.split()
            img  = raw.convert('L')
            mask = a
        else:
            img  = raw.convert('L')
            mask = Image.new('L', img.size, 255)

    W, H = 320, 320
    img  = ImageOps.fit(img,  (W, H), Image.Resampling.LANCZOS)
    mask = ImageOps.fit(mask, (W, H), Image.Resampling.LANCZOS)

    img = ImageOps.autocontrast(img, cutoff=2)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    img = ImageOps.invert(img)

    img_arr  = np.array(img,  dtype=float)
    mask_arr = np.array(mask, dtype=float)

    all_dots = floyd_steinberg_dither(img_arr)
    dots = [(x, y) for x, y in all_dots if mask_arr[y, x] > 128]
    dots = random.sample(dots, min(len(dots), 3500))

    # Phase animation for dither portrait
    NP = 6
    css_phases = ""
    for i in range(NP):
        delay = round(i * 0.8, 1)
        dur   = round(1.5 + (i % 3) * 0.5, 1)
        css_phases += f".p{i}{{animation:tw {dur}s {delay}s infinite;}}"

    # Hacker Green Palette
    # Primary Green: #39FF14 / #00FF66 / #22C55E
    # Dark BG: #050C07 / #08120B

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 620" width="860" height="620">
<defs>
    <!-- Hacker Green Glow Filter -->
    <filter id="green-glow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="2.5" result="blur" />
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>

    <!-- Scanline Pattern -->
    <pattern id="hacker-scanlines" width="100" height="4" patternUnits="userSpaceOnUse">
        <line x1="0" y1="0" x2="100" y2="0" stroke="#00FF66" stroke-width="1" opacity="0.12"/>
    </pattern>
</defs>

<style>
    .bg {{ fill: #050C07; stroke: #00FF66; stroke-width: 2; }}
    .frame-border {{ fill: none; stroke: #00FF66; stroke-width: 1.5; opacity: 0.85; filter: url(#green-glow); }}
    .frame-sub {{ fill: none; stroke: #00FF66; stroke-width: 1; opacity: 0.4; }}

    /* Text Typography */
    .hdr-title {{ font-family: 'Courier New', monospace; font-size: 15px; font-weight: bold; fill: #00FF66; letter-spacing: 3px; filter: url(#green-glow); }}
    .lbl-green {{ font-family: 'Courier New', monospace; font-size: 13px; font-weight: bold; fill: #39FF14; letter-spacing: 1.5px; }}
    .val-green {{ font-family: 'Courier New', monospace; font-size: 13px; font-weight: bold; fill: #86EFAC; }}
    .val-accent {{ font-family: 'Courier New', monospace; font-size: 13px; font-weight: bold; fill: #00FF66; filter: url(#green-glow); }}

    .dot {{ fill: #00FF66; shape-rendering: crispEdges; filter: url(#green-glow); }}
    .cur {{ fill: #00FF66; animation: blink 1s infinite; filter: url(#green-glow); }}

    @keyframes tw {{ 0%,100% {{ opacity: .2; }} 50% {{ opacity: 1; }} }}
    @keyframes blink {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
    @keyframes wave {{ 0% {{ stroke-dashoffset: 0; }} 100% {{ stroke-dashoffset: -120; }} }}

    .sine-wave {{
        fill: none;
        stroke: #00FF66;
        stroke-width: 1.8;
        filter: url(#green-glow);
        stroke-dasharray: 8 4;
        animation: wave 4s linear infinite;
    }}
    {css_phases}
</style>

<!-- Main Outer Cyber Frame -->
<rect width="860" height="620" class="bg" rx="10" />

<!-- Outer Corner Crosshairs -->
<g stroke="#00FF66" stroke-width="1.5" opacity="0.8">
    <line x1="20" y1="20" x2="35" y2="20" /><line x1="20" y1="20" x2="20" y2="35" />
    <line x1="840" y1="20" x2="825" y2="20" /><line x1="840" y1="20" x2="840" y2="35" />
    <line x1="20" y1="600" x2="35" y2="600" /><line x1="20" y1="600" x2="20" y2="585" />
    <line x1="840" y1="600" x2="825" y2="600" /><line x1="840" y1="600" x2="840" y2="585" />
</g>

<!-- Top Header Bar -->
<g transform="translate(35, 30)">
    <text x="0" y="20" class="hdr-title">SUBJECT: DEVESH.0777</text>
    <text x="790" y="20" class="hdr-title" text-anchor="end">[SYS.SEC // LEVEL 5]</text>
    <line x1="0" y1="32" x2="790" y2="32" class="frame-border" />
</g>

<!-- Top Left: Photo Portrait Container -->
<g transform="translate(35, 80)">
    <rect width="360" height="340" fill="#040905" stroke="#00FF66" stroke-width="1.5" rx="4" />
    <!-- Target Reticle Overlay -->
    <circle cx="180" cy="170" r="140" fill="none" stroke="#00FF66" stroke-width="1" opacity="0.25" stroke-dasharray="6 6" />
    <line x1="180" y1="20" x2="180" y2="320" stroke="#00FF66" stroke-width="1" opacity="0.15" />
    <line x1="20" y1="170" x2="340" y2="170" stroke="#00FF66" stroke-width="1" opacity="0.15" />
    
    <!-- Dither Portrait Dots -->
    <g transform="translate(20, 10)">
"""

    phase_dots = {i: [] for i in range(NP)}
    for x, y in dots:
        p = random.randint(0, NP - 1)
        phase_dots[p].append((x, y))

    for i in range(NP):
        d_path = " ".join([f"M{x},{y}h2v2h-2z" for x, y in phase_dots[i]])
        svg += f'<path d="{d_path}" class="dot p{i}"/>\n'

    svg += """    </g>
</g>

<!-- Top Right: Motherboard Circuit Diagram -->
<g transform="translate(420, 80)">
    <rect width="405" height="340" fill="#040905" stroke="#00FF66" stroke-width="1.5" rx="4" />
    
    <!-- CPU Chip Core -->
    <rect x="130" y="70" width="145" height="130" fill="#0A1C0F" stroke="#00FF66" stroke-width="2" rx="6" filter="url(#green-glow)"/>
    <text x="202" y="130" class="hdr-title" text-anchor="middle">DEV-CORE</text>
    <text x="202" y="152" class="lbl-green" text-anchor="middle" font-size="10">x64 // 4.8 GHz</text>

    <!-- Circuit Traces -->
    <path d="M 40,40 L 130,70 M 40,80 L 130,100 M 40,140 L 130,130 M 40,260 L 130,180" stroke="#00FF66" stroke-width="2" opacity="0.7" fill="none" />
    <path d="M 275,100 L 360,60 M 275,130 L 360,140 M 275,170 L 360,240" stroke="#00FF66" stroke-width="2" opacity="0.7" fill="none" />
    <circle cx="40" cy="40" r="3" fill="#00FF66" />
    <circle cx="40" cy="80" r="3" fill="#00FF66" />
    <circle cx="40" cy="140" r="3" fill="#00FF66" />
    <circle cx="360" cy="60" r="3" fill="#00FF66" />
    <circle cx="360" cy="140" r="3" fill="#00FF66" />

    <!-- RAM Slots -->
    <rect x="50" y="270" width="300" height="40" fill="#08140B" stroke="#00FF66" stroke-width="1" />
    <text x="200" y="295" class="lbl-green" text-anchor="middle">SYSTEM MEMORY // 64GB DDR5 OK</text>
</g>

<!-- Bottom Left: Fingerprint Scan & Walker Signal -->
<g transform="translate(35, 435)">
    <!-- Fingerprint Box -->
    <g transform="translate(0, 0)">
        <rect width="170" height="155" fill="#040905" stroke="#00FF66" stroke-width="1.5" rx="4" />
        <path d="M 50,40 Q 85,20 120,40 Q 135,70 120,110 Q 85,135 50,110 Q 35,70 50,40 Z" fill="none" stroke="#00FF66" stroke-width="2" opacity="0.8" />
        <path d="M 65,55 Q 85,40 105,55 Q 115,75 105,95 Q 85,110 65,95 Q 55,75 65,55 Z" fill="none" stroke="#00FF66" stroke-width="1.5" opacity="0.6" />
        <circle cx="85" cy="75" r="10" fill="#00FF66" opacity="0.3" />
        <text x="85" y="142" class="lbl-green" text-anchor="middle" font-size="10">BIO.PRINT: VERIFIED</text>
    </g>

    <!-- Signal Wave Box -->
    <g transform="translate(185, 0)">
        <rect width="175" height="155" fill="#040905" stroke="#00FF66" stroke-width="1.5" rx="4" />
        <!-- Oscilloscope Waveform -->
        <path d="M 10,75 Q 35,15 60,75 T 110,75 T 160,75" class="sine-wave" />
        <path d="M 10,75 Q 35,135 60,75 T 110,75 T 160,75" class="sine-wave" style="animation-delay: -2s;" />
        <text x="87" y="142" class="lbl-green" text-anchor="middle" font-size="10">NEURAL SIGNAL: ACTIVE</text>
    </g>
</g>

<!-- Bottom Right: Detailed Hacker Info Sheet -->
<g transform="translate(420, 435)">
    <rect width="405" height="155" fill="#040905" stroke="#00FF66" stroke-width="1.5" rx="4" />
    
    <g transform="translate(20, 25)">
        <text x="0" y="0"><tspan class="lbl-green">HANDLE        </tspan><tspan class="val-accent"> DEVESH KHALKAR</tspan></text>
        <text x="0" y="24"><tspan class="lbl-green">PRIMARY ROLE  </tspan><tspan class="val-green"> FULL STACK DEVELOPER</tspan></text>
        <text x="0" y="48"><tspan class="lbl-green">CORE STACK    </tspan><tspan class="val-green"> PYTHON · C++ · HTML · CSS · GIT</tspan></text>
        <text x="0" y="72"><tspan class="lbl-green">STATUS        </tspan><tspan class="val-accent"> SYSTEM OPERATIONAL // BUILDING</tspan></text>
        <text x="0" y="96"><tspan class="lbl-green">THREAT LEVEL  </tspan><tspan class="val-accent"> ★ ★ ★ ★ ★ (MAX)</tspan></text>
        <rect x="330" y="82" width="10" height="18" class="cur" />
    </g>
</g>

<!-- CRT Scanline Grid Overlay -->
<rect width="860" height="620" rx="10" fill="url(#hacker-scanlines)" pointer-events="none" />

</svg>"""

    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Created hacker green dark.svg —", round(len(svg)/1024), "KB")

if __name__ == "__main__":
    build_hacker_profile_svg()
