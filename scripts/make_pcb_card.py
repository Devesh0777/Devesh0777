import os

OUTPUT_SVG = "pcb-card.svg"

# Hacker Green PCB Theme
BOARD_COLOR = "#050C07"       # Very dark hacker green background
SILKSCREEN_COLOR = "#00FF66"  # Matrix neon green text/lines
TRACE_COLOR = "#0F2E17"       # Dark green trace paths
GLOW_COLOR = "#39FF14"        # Pulsing bright neon flow
CHIP_BG = "#0A1C0F"           # Dark chip core
PIN_COLOR = "#22C55E"         # Green chip pins

svg_width = 860
svg_height = 240

def draw_chip(x, y, w, h, title, subtitle):
    pins = ""
    pin_spacing = 14
    num_pins_x = int((w - 20) // pin_spacing)
    start_x = x + (w - (num_pins_x * pin_spacing)) / 2 + pin_spacing/2

    for i in range(num_pins_x):
        px = start_x + i * pin_spacing
        pins += f'<rect x="{px-2}" y="{y-6}" width="4" height="8" fill="{PIN_COLOR}" />\n'
        pins += f'<rect x="{px-2}" y="{y+h-2}" width="4" height="8" fill="{PIN_COLOR}" />\n'

    num_pins_y = int((h - 20) // pin_spacing)
    start_y = y + (h - (num_pins_y * pin_spacing)) / 2 + pin_spacing/2
    for i in range(num_pins_y):
        py = start_y + i * pin_spacing
        pins += f'<rect x="{x-6}" y="{py-2}" width="8" height="4" fill="{PIN_COLOR}" />\n'
        pins += f'<rect x="{x+w-2}" y="{py-2}" width="8" height="4" fill="{PIN_COLOR}" />\n'

    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{CHIP_BG}" stroke="{SILKSCREEN_COLOR}" stroke-width="1.5" rx="4" filter="url(#pcb-glow)" />\n'
    
    text_y = y + h/2
    text = f'<text class="silkscreen title" x="{x+w/2}" y="{text_y-4}" text-anchor="middle">{title}</text>\n'
    text += f'<text class="silkscreen subtitle" x="{x+w/2}" y="{text_y+12}" text-anchor="middle">{subtitle}</text>\n'
    
    return pins + body + text

traces = [
    ("M 40,120 L 100,120 L 120,90 L 160,90", 0.0),
    ("M 360,90 L 420,90 L 450,50 L 520,50", 1.0),
    ("M 360,140 L 420,140 L 450,180 L 520,180", 1.2),
    ("M 700,180 L 760,180 L 790,210 L 820,210", 2.2),
    ("M 700,50 L 770,50 L 790,30 L 820,30", 2.0),
    ("M 40,40 L 80,40 L 100,20 L 200,20", 0.5),
    ("M 700,210 L 740,210 L 760,225 L 820,225", 0.8),
    ("M 250,210 L 280,210 L 310,190 L 360,190", 1.5)
]

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
<defs>
    <filter id="pcb-glow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="2.5" result="blur" />
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
</defs>

<style>
    .silkscreen {{
        font-family: 'Courier New', Courier, monospace;
        fill: {SILKSCREEN_COLOR};
        filter: url(#pcb-glow);
    }}
    .title {{
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 1px;
    }}
    .subtitle {{
        font-size: 11px;
        fill: #86EFAC;
    }}
    
    .trace-base {{
        fill: none;
        stroke: {TRACE_COLOR};
        stroke-width: 2.5;
        stroke-linejoin: round;
        stroke-linecap: round;
        opacity: 0.6;
    }}
    
    .trace-flow {{
        fill: none;
        stroke: {GLOW_COLOR};
        stroke-width: 3;
        stroke-linejoin: round;
        stroke-linecap: round;
        stroke-dasharray: 25 1000;
        stroke-dashoffset: 1000;
        animation: flow 3s linear infinite;
        filter: url(#pcb-glow);
    }}
    
    @keyframes flow {{
        0% {{ stroke-dashoffset: 100; }}
        100% {{ stroke-dashoffset: -200; }}
    }}
</style>
<rect width="100%" height="100%" fill="{BOARD_COLOR}" stroke="{SILKSCREEN_COLOR}" stroke-width="2" rx="10" />

<!-- Corner Accents -->
<g stroke="{SILKSCREEN_COLOR}" stroke-width="1.5" opacity="0.8">
    <line x1="12" y1="12" x2="24" y2="12" /><line x1="12" y1="12" x2="12" y2="24" />
    <line x1="{svg_width-12}" y1="12" x2="{svg_width-24}" y2="12" /><line x1="{svg_width-12}" y1="12" x2="{svg_width-12}" y2="24" />
    <line x1="12" y1="{svg_height-12}" x2="24" y2="{svg_height-12}" /><line x1="12" y1="{svg_height-12}" x2="12" y2="{svg_height-24}" />
    <line x1="{svg_width-12}" y1="{svg_height-12}" x2="{svg_width-24}" y2="{svg_height-12}" /><line x1="{svg_width-12}" y1="{svg_height-12}" x2="{svg_width-12}" y2="{svg_height-24}" />
</g>

<!-- Trace bases -->
"""

for d, _ in traces:
    svg_content += f'<path class="trace-base" d="{d}" />\n'

svg_content += "\n<!-- Trace flows -->\n"
for d, delay in traces:
    svg_content += f'<path class="trace-flow" d="{d}" style="animation-delay: {delay}s;" />\n'

svg_content += "\n<!-- Chips -->\n"

# Main MCU Chip
svg_content += draw_chip(160, 60, 200, 110, "DEV-0777 MCU", "Full Stack Core")

# Memory / Backend Chip
svg_content += draw_chip(520, 25, 180, 75, "PYTHON // C++", "Backend Engine")

# Hardware / Frontend Chip
svg_content += draw_chip(520, 140, 180, 75, "HTML // CSS", "Frontend UI")

svg_content += """
<!-- Vias (Holes) -->
<circle cx="40" cy="120" r="4" fill="#050C07" stroke="#00FF66" stroke-width="1.5" />
<circle cx="820" cy="210" r="4" fill="#050C07" stroke="#00FF66" stroke-width="1.5" />
<circle cx="820" cy="30" r="4" fill="#050C07" stroke="#00FF66" stroke-width="1.5" />
<circle cx="200" cy="20" r="3" fill="#050C07" stroke="#00FF66" stroke-width="1.5" />
<circle cx="820" cy="225" r="3" fill="#050C07" stroke="#00FF66" stroke-width="1.5" />

</svg>
"""

with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Updated {OUTPUT_SVG} with Hacker Green PCB Theme")
