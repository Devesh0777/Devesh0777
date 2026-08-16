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

    # Portrait size inside frame (300x280)
    W, H = 280, 280
    if not os.path.exists(img_path):
        img = Image.new('L', (W, H), color=128)
        mask = Image.new('L', (W, H), 255)
    else:
        raw = Image.open(img_path)
        if raw.mode == 'RGBA':
            r, g, b, a = raw.split()
            img = raw.convert('L')
            mask = a
        else:
            img = raw.convert('L')
            mask = Image.new('L', img.size, 255)

    img = ImageOps.fit(img, (W, H), Image.Resampling.LANCZOS)
    mask = ImageOps.fit(mask, (W, H), Image.Resampling.LANCZOS)

    img = ImageOps.autocontrast(img, cutoff=2)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    img = ImageOps.invert(img)

    img_arr = np.array(img, dtype=float)
    mask_arr = np.array(mask, dtype=float)

    all_dots = floyd_steinberg_dither(img_arr)
    dots = [(x, y) for x, y in all_dots if mask_arr[y, x] > 128]

    # Generate full dither bitmap path for authentic retro CRT look (no particle sampling)
    portrait_dither_path = " ".join([f"M{x},{y}h1.5v1.5h-1.5z" for x, y in dots])

    # Terminal Typewriter Text Animation Setup (Aligned inside container box width 365px)
    info_fields = [
        ("NAME", "DEVESH KHALKAR"),
        ("INCEPT DATE", "03/05/2008"),
        ("FUNCTION", "FULL STACK DEVELOPER"),
        ("MENTAL STATE", "OPERATIONAL // OPTIMAL"),
        ("LAST KNOWN LOCATION", "INDIA"),
        ("THREAT ASSESSMENT", "★ ★ ★ ★ ★ (MAX)"),
        ("SPECIAL SKILLS", "PYTHON · C++ · HTML · GIT")
    ]

    char_duration = 0.05  # seconds per character
    line_pause = 0.2
    
    css_typewriter = ""
    clip_defs = ""
    cumulative_delay = 0.3

    field_elements = []
    
    for idx, (lbl, val) in enumerate(info_fields):
        y_pos = idx * 22
        
        field_elements.append(f"""
        <g transform="translate(0, {y_pos})">
            <!-- Label -->
            <text x="0" y="14" class="lbl-purple">{lbl}</text>
            <!-- Direct Value Text (Guaranteed GitHub Markdown Render) -->
            <text x="150" y="14" class="val-purple">{val}</text>
        </g>
        """)

    final_cur_delay = 0.5

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 760" width="860" height="760">
<defs>
    {clip_defs}
    <!-- Purple Intense CRT Glow Filter -->
    <filter id="purple-glow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3.5" result="blur1" />
        <feGaussianBlur stdDeviation="1.5" result="blur2" />
        <feMerge>
            <feMergeNode in="blur1"/>
            <feMergeNode in="blur2"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>

    <!-- Retro CRT Grain / Film Noise Filter -->
    <filter id="crt-grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" result="noise" />
        <feColorMatrix type="matrix" values="1 0 0 0 0  0 0.8 0 0 0  0 0 1 0 0  0 0 0 0.18 0" in="noise" result="coloredNoise" />
        <feComposite operator="in" in2="SourceGraphic" />
    </filter>

    <!-- CRT Scanline Pattern -->
    <pattern id="purple-scanlines" width="100" height="4" patternUnits="userSpaceOnUse">
        <line x1="0" y1="0" x2="100" y2="0" stroke="#B18CFF" stroke-width="1.2" opacity="0.15"/>
    </pattern>

    <!-- 3D Solid Earth Shading Gradients -->
    <radialGradient id="earth-sphere-grad" cx="35%" cy="30%" r="65%">
        <stop offset="0%" stop-color="#3D1D75"/>
        <stop offset="60%" stop-color="#1A0B36"/>
        <stop offset="100%" stop-color="#070312"/>
    </radialGradient>
    <radialGradient id="earth-atmosphere-grad" cx="40%" cy="35%" r="60%">
        <stop offset="70%" stop-color="#A77BFF" stop-opacity="0"/>
        <stop offset="95%" stop-color="#D4BEFF" stop-opacity="0.5"/>
        <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.8"/>
    </radialGradient>
</defs>

<style>
    .bg {{ fill: #0B0813; stroke: #A77BFF; stroke-width: 2; }}
    .frame-border {{ fill: none; stroke: #A77BFF; stroke-width: 1.5; opacity: 0.85; filter: url(#purple-glow); }}
    .frame-sub {{ fill: none; stroke: #8A52FF; stroke-width: 1; opacity: 0.4; }}

    /* Typography - Pixel Perfect Alignment */
    .hdr-title {{ font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; font-weight: bold; fill: #D4BEFF; letter-spacing: 2px; filter: url(#purple-glow); }}
    .lbl-purple {{ font-family: 'Consolas', 'Courier New', monospace; font-size: 11px; font-weight: bold; fill: #A77BFF; letter-spacing: 1px; }}
    .val-purple {{ font-family: 'Consolas', 'Courier New', monospace; font-size: 11px; font-weight: bold; fill: #E5D9FF; letter-spacing: 0.5px; filter: url(#purple-glow); }}

    .dither-dot {{ fill: #D4BEFF; shape-rendering: crispEdges; filter: url(#purple-glow); }}
    
    @keyframes rotate-globe {{
        0% {{ transform: translateX(0px); }}
        100% {{ transform: translateX(-180px); }}
    }}
    .rotating-earth {{
        animation: rotate-globe 10s linear infinite;
    }}

    .term-cursor {{
        fill: #A77BFF;
        filter: url(#purple-glow);
    }}


    @keyframes blink {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
    
    @keyframes wave-move {{ 
        0% {{ transform: translateX(0); }} 
        100% {{ transform: translateX(-120px); }} 
    }}
    @keyframes wave-move-reverse {{ 
        0% {{ transform: translateX(0); }} 
        100% {{ transform: translateX(120px); }} 
    }}

    .moving-sine-1 {{
        animation: wave-move 3s linear infinite;
    }}
    .moving-sine-2 {{
        animation: wave-move-reverse 4.5s linear infinite;
    }}

    {css_typewriter}

    .final-blinker {{
        animation: blink 0.8s infinite;
        animation-delay: {final_cur_delay:.2f}s;
        opacity: 0;
    }}
</style>



<!-- Main Outer Cyber Frame -->
<rect width="860" height="760" class="bg" rx="10" />

<!-- Outer Corner Crosshairs -->
<g stroke="#A77BFF" stroke-width="1.5" opacity="0.8">
    <line x1="20" y1="20" x2="35" y2="20" /><line x1="20" y1="20" x2="20" y2="35" />
    <line x1="840" y1="20" x2="825" y2="20" /><line x1="840" y1="20" x2="840" y2="35" />
    <line x1="20" y1="740" x2="35" y2="740" /><line x1="20" y1="740" x2="20" y2="725" />
    <line x1="840" y1="740" x2="825" y2="740" /><line x1="840" y1="740" x2="840" y2="725" />
</g>

<!-- Top Header Bar -->
<g transform="translate(35, 30)">
    <text x="0" y="20" class="hdr-title">SUBJECT A-34 // DEVESH.0777</text>
    <!-- Battery / Status Indicator -->
    <g transform="translate(740, 6)" stroke="#A77BFF" fill="none" stroke-width="1.5">
        <rect x="0" y="0" width="30" height="16" rx="2" />
        <rect x="30" y="4" width="3" height="8" fill="#A77BFF" />
        <rect x="4" y="4" width="6" height="8" fill="#A77BFF" />
        <rect x="12" y="4" width="6" height="8" fill="#A77BFF" />
        <rect x="20" y="4" width="6" height="8" fill="#A77BFF" />
    </g>
    <line x1="0" y1="35" x2="790" y2="35" class="frame-border" />
</g>

<!-- Top Left: Photo Portrait Container with Authentic 1:1 Floyd-Steinberg Dither Bitmap -->
<g transform="translate(35, 85)">
    <rect width="360" height="340" fill="#07040E" stroke="#A77BFF" stroke-width="1.5" rx="4" />
    
    <!-- Indicator Rings -->
    <circle cx="280" cy="25" r="5" fill="none" stroke="#A77BFF" stroke-width="1.2" />
    <circle cx="300" cy="25" r="5" fill="none" stroke="#A77BFF" stroke-width="1.2" />
    <circle cx="320" cy="25" r="5" fill="none" stroke="#A77BFF" stroke-width="1.2" />

    <!-- Pure Dither Bitmap Path -->
    <g transform="translate(40, 30)">
        <path d="{portrait_dither_path}" class="dither-dot"/>
    </g>
</g>

<!-- Top Right: Reference Motherboard Circuit Diagram -->
<g transform="translate(420, 85)">
    <rect width="405" height="340" fill="#07040E" stroke="#A77BFF" stroke-width="1.5" rx="4" />
    
    <!-- CPU Chip with Laptop Icon -->
    <rect x="135" y="70" width="140" height="120" fill="#130A24" stroke="#A77BFF" stroke-width="2" rx="4" filter="url(#purple-glow)"/>
    
    <g transform="translate(180, 105)" stroke="#D4BEFF" stroke-width="2" fill="none" filter="url(#purple-glow)">
        <rect x="-20" y="-20" width="40" height="26" rx="2" />
        <line x1="-14" y1="-14" x2="4" y2="-14" stroke-width="1.5" />
        <line x1="-14" y1="-8" x2="10" y2="-8" stroke-width="1.5" />
        <line x1="-14" y1="-2" x2="-2" y2="-2" stroke-width="1.5" />
        <path d="M -28,10 L 28,10 L 22,17 L -22,17 Z" fill="#A77BFF" opacity="0.6"/>
        <line x1="-28" y1="10" x2="28" y2="10" />
    </g>

    <!-- PCB Traces -->
    <path d="M 275,85 H 340 V 45 H 375" stroke="#A77BFF" stroke-width="2" fill="none" />
    <path d="M 275,100 H 350 V 60 H 375" stroke="#A77BFF" stroke-width="2" fill="none" />
    <path d="M 275,115 H 360 V 75 H 375" stroke="#A77BFF" stroke-width="2" fill="none" />
    
    <path d="M 275,145 H 330 V 220 L 350,240 H 375" stroke="#A77BFF" stroke-width="2" fill="none" />
    <path d="M 275,160 H 320 V 230 L 340,250 H 375" stroke="#A77BFF" stroke-width="2" fill="none" opacity="0.7"/>
    <path d="M 275,175 H 310 V 240 L 330,260 H 375" stroke="#A77BFF" stroke-width="2" fill="none" opacity="0.7"/>

    <circle cx="375" cy="45" r="3" fill="#A77BFF" filter="url(#purple-glow)"/>
    <circle cx="375" cy="60" r="3" fill="#A77BFF" filter="url(#purple-glow)"/>
    <circle cx="375" cy="75" r="3" fill="#A77BFF" filter="url(#purple-glow)"/>
    <circle cx="375" cy="240" r="3" fill="#A77BFF" filter="url(#purple-glow)"/>
    <circle cx="375" cy="250" r="3" fill="#A77BFF" filter="url(#purple-glow)"/>

    <path d="M 30,85 H 135" stroke="#A77BFF" stroke-width="2" fill="none" />
    <path d="M 30,100 H 135" stroke="#A77BFF" stroke-width="2" fill="none" />
    <path d="M 30,115 H 135" stroke="#A77BFF" stroke-width="2" fill="none" />
    <path d="M 30,130 H 135" stroke="#A77BFF" stroke-width="2" fill="none" opacity="0.6"/>
    <path d="M 30,145 H 135" stroke="#A77BFF" stroke-width="2" fill="none" opacity="0.6"/>

    <path d="M 135,175 V 230 H 40 V 280 H 360" stroke="#A77BFF" stroke-width="1.5" stroke-dasharray="4 2" fill="none" opacity="0.6" />
    <path d="M 160,190 V 245 H 60 V 290 H 360" stroke="#A77BFF" stroke-width="1.5" stroke-dasharray="4 2" fill="none" opacity="0.6" />

    <rect x="330" y="110" width="16" height="28" fill="#1B0E33" stroke="#A77BFF" stroke-width="1.5"/>
    <rect x="352" y="110" width="16" height="28" fill="#1B0E33" stroke="#A77BFF" stroke-width="1.5"/>
    <rect x="330" y="145" width="16" height="28" fill="#1B0E33" stroke="#A77BFF" stroke-width="1.5"/>
    <rect x="352" y="145" width="16" height="28" fill="#1B0E33" stroke="#A77BFF" stroke-width="1.5"/>

    <rect x="160" y="25" width="90" height="25" fill="#130A24" stroke="#A77BFF" stroke-width="1.5" />
    <circle cx="175" cy="37" r="2.5" fill="#A77BFF" />
    <circle cx="190" cy="37" r="2.5" fill="#A77BFF" />
    <circle cx="205" cy="37" r="2.5" fill="#A77BFF" />
    <circle cx="220" cy="37" r="2.5" fill="#A77BFF" />
</g>

<!-- Bottom Left: Fingerprint Scanner Box -->
<g transform="translate(35, 445)">
    <rect width="170" height="140" fill="#07040E" stroke="#A77BFF" stroke-width="1.5" rx="4" />
    <path d="M 12,22 V 12 H 22 M 148,12 H 158 V 22 M 12,118 V 128 H 22 M 148,128 H 158 V 118" stroke="#A77BFF" stroke-width="1.5" fill="none" opacity="0.7"/>

    <g transform="translate(85, 70)" stroke="#A77BFF" stroke-width="1.5" fill="none" opacity="0.85" filter="url(#purple-glow)">
        <ellipse rx="42" ry="52" stroke-dasharray="140 10 30 5" />
        <ellipse rx="34" ry="42" stroke-dasharray="90 8 40 8" />
        <ellipse rx="26" ry="32" stroke-dasharray="70 5 25 5" />
        <ellipse rx="18" ry="22" stroke-dasharray="40 5 15 5" />
        <ellipse rx="10" ry="12" />
        <circle cx="0" cy="0" r="3" fill="#A77BFF" />
    </g>
</g>

<!-- Bottom Left Sci-Fi Box: Pixel Art 8-Bit Rotating Earth Globe -->
<g transform="translate(35, 595)">
    <rect width="170" height="130" fill="#07040E" stroke="#A77BFF" stroke-width="1.5" rx="4" />
    <path d="M 8,16 V 8 H 16 M 154,8 H 162 V 16 M 8,114 V 122 H 16 M 154,122 H 162 V 114" stroke="#A77BFF" stroke-width="1.2" fill="none" opacity="0.7"/>

    <!-- Retro Pixel Art Earth Globe -->
    <g transform="translate(85, 65)">
        <defs>
            <clipPath id="pixel-earth-clip">
                <circle cx="0" cy="0" r="44" />
            </clipPath>
        </defs>

        <!-- Base Ocean Sphere Background -->
        <circle cx="0" cy="0" r="44" fill="#150B2D" stroke="#A77BFF" stroke-width="1.8" filter="url(#purple-glow)"/>

        <!-- Rotating Pixel Art Landmasses & Swirl Clouds -->
        <g clip-path="url(#pixel-earth-clip)">
            <!-- Ocean Depth Shading Pixels -->
            <rect x="-44" y="15" width="88" height="30" fill="#0A041A" opacity="0.6"/>
            
            <g class="rotating-earth" shape-rendering="crispEdges">
                <!-- Pixel Landmasses Pass 1 -->
                <g fill="#A77BFF" opacity="0.9">
                    <!-- Eurasia / Asia Block -->
                    <rect x="-40" y="-32" width="28" height="12" />
                    <rect x="-24" y="-20" width="36" height="16" />
                    <rect x="0" y="-36" width="32" height="16" />
                    <rect x="20" y="-24" width="24" height="12" />
                    
                    <!-- Africa Block -->
                    <rect x="-32" y="-4" width="20" height="24" />
                    <rect x="-24" y="20" width="12" height="12" />

                    <!-- North America Block -->
                    <rect x="-135" y="-32" width="28" height="16" />
                    <rect x="-120" y="-16" width="20" height="12" />
                    
                    <!-- South America Block -->
                    <rect x="-112" y="0" width="16" height="24" />
                    <rect x="-108" y="24" width="8" height="12" />

                    <!-- Australia Block -->
                    <rect x="32" y="8" width="16" height="12" />

                    <!-- Continents Loop Copy (Offset by 180px) -->
                    <rect x="140" y="-32" width="28" height="12" />
                    <rect x="156" y="-20" width="36" height="16" />
                    <rect x="180" y="-36" width="32" height="16" />
                    <rect x="45" y="-32" width="28" height="16" />
                    <rect x="60" y="-16" width="20" height="12" />
                    <rect x="68" y="0" width="16" height="24" />
                </g>

                <!-- Pixel Shading Highlights (Greenish/Lighter Purple accents) -->
                <g fill="#E5D9FF" opacity="0.8">
                    <rect x="-20" y="-28" width="12" height="6" />
                    <rect x="4" y="-20" width="16" height="6" />
                    <rect x="-28" y="0" width="8" height="8" />
                    <rect x="-115" y="-26" width="10" height="6" />
                    <rect x="65" y="-26" width="10" height="6" />
                </g>

                <!-- Swirl Pixel Cloud Trails (Matching Reference Image) -->
                <g fill="#FFFFFF" opacity="0.75">
                    <rect x="-30" y="-10" width="24" height="4" />
                    <rect x="-10" y="-6" width="16" height="4" />
                    <rect x="-18" y="-2" width="8" height="4" />
                    <rect x="10" y="10" width="20" height="4" />
                    <rect x="150" y="-10" width="24" height="4" />
                    <rect x="170" y="-6" width="16" height="4" />
                </g>
            </g>
        </g>

        <!-- Spherical Pixel Atmosphere Edge Shading -->
        <circle cx="0" cy="0" r="44" fill="url(#earth-atmosphere-grad)" />

        <!-- Orbital Equatorial Scan Line -->
        <ellipse cx="0" cy="0" rx="52" ry="12" fill="none" stroke="#D4BEFF" stroke-width="1.2" stroke-dasharray="6 3" transform="rotate(-15)" filter="url(#purple-glow)"/>
    </g>

    <!-- Sci-Fi Animated Scanning Laser Beam -->
    <g transform="translate(10, 0)">
        <rect x="0" y="20" width="150" height="2" fill="#FFFFFF" opacity="0.85" filter="url(#purple-glow)">
            <animate attributeName="y" values="15; 110; 15" dur="2.2s" repeatCount="indefinite" />
        </rect>
    </g>
</g>

<!-- Bottom Right: Hacker Info & Moving Wave Graph Box -->
<g transform="translate(420, 445)">
    <rect width="405" height="285" fill="#07040E" stroke="#A77BFF" stroke-width="1.5" rx="4" />
    
    <!-- User Information Section with Fixed Box Alignment -->
    <g transform="translate(20, 16)">
"""

    for elem in field_elements:
        svg += elem

    svg += f"""
    </g>

    <!-- Bottom Continuous Moving Wave Graph -->
    <g transform="translate(20, 180)">
        <rect width="365" height="75" fill="url(#graph-grid)" stroke="#A77BFF" stroke-width="1" rx="2" />
        
        <line x1="0" y1="37.5" x2="365" y2="37.5" stroke="#A77BFF" stroke-width="1" opacity="0.4" stroke-dasharray="4 4" />
        <line x1="182.5" y1="0" x2="182.5" y2="75" stroke="#A77BFF" stroke-width="1" opacity="0.4" stroke-dasharray="4 4" />

        <g clip-path="url(#graph-clip)">
            <clipPath id="graph-clip">
                <rect width="365" height="85" />
            </clipPath>
            
            <g class="moving-sine-1">
                <path d="M -120,42.5 Q -90,5 -60,42.5 T 0,42.5 T 60,42.5 T 120,42.5 T 180,42.5 T 240,42.5 T 300,42.5 T 360,42.5 T 420,42.5 T 480,42.5" 
                      fill="none" stroke="#D4BEFF" stroke-width="2" filter="url(#purple-glow)" />
                <path d="M -120,42.5 Q -90,80 -60,42.5 T 0,42.5 T 60,42.5 T 120,42.5 T 180,42.5 T 240,42.5 T 300,42.5 T 360,42.5 T 420,42.5 T 480,42.5" 
                      fill="none" stroke="#8A52FF" stroke-width="1.5" opacity="0.7" />
            </g>

            <g class="moving-sine-2">
                <path d="M -120,42.5 Q -90,75 -60,42.5 T 0,42.5 T 60,42.5 T 120,42.5 T 180,42.5 T 240,42.5 T 300,42.5 T 360,42.5 T 420,42.5 T 480,42.5" 
                      fill="none" stroke="#FFFFFF" stroke-width="1.8" filter="url(#purple-glow)" stroke-dasharray="6 3" />
            </g>
        </g>

        <text x="5" y="98" class="lbl-purple" font-size="8" opacity="0.8">FREQ: 440Hz // AMP: 0.85 // WAVE: HARMONIC SINE // SYNC: OK</text>
    </g>
</g>

<!-- CRT Scanline Grid Overlay -->
<rect width="860" height="760" rx="10" fill="url(#purple-scanlines)" pointer-events="none" />

<!-- Retro Film Grain / CRT Noise Overlay -->
<rect width="860" height="760" rx="10" filter="url(#crt-grain)" opacity="0.25" pointer-events="none" />

</svg>"""

    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Updated retro CRT dark.svg —", round(len(svg)/1024), "KB")

if __name__ == "__main__":
    build_hacker_profile_svg()
