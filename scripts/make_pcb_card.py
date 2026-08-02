import os

OUTPUT_SVG = "pcb-card.svg"

# Colors
BOARD_COLOR = "#003300"  # Classic PCB dark green
SILKSCREEN_COLOR = "#ccffcc" # Pale green
TRACE_COLOR = "#006600"  # Trace green
GLOW_COLOR = "#39d353"   # Bright green for the animated flow
CHIP_BG = "#001a00"      # Very dark green for chips
PIN_COLOR = "#66cc66"    # Greenish pins

svg_width = 490
svg_height = 225

def draw_chip(x, y, w, h, title, subtitle):
    # Draw pins (top and bottom)
    pins = ""
    pin_spacing = 10
    num_pins_x = (w - 10) // pin_spacing
    start_x = x + (w - (num_pins_x * pin_spacing)) / 2 + pin_spacing/2

    for i in range(num_pins_x):
        px = start_x + i * pin_spacing
        # Top pins
        pins += f'<rect x="{px-1.5}" y="{y-4}" width="3" height="8" fill="{PIN_COLOR}" />\n'
        # Bottom pins
        pins += f'<rect x="{px-1.5}" y="{y+h-4}" width="3" height="8" fill="{PIN_COLOR}" />\n'

    # Draw pins (left and right) if height allows
    num_pins_y = (h - 10) // pin_spacing
    start_y = y + (h - (num_pins_y * pin_spacing)) / 2 + pin_spacing/2
    for i in range(num_pins_y):
        py = start_y + i * pin_spacing
        # Left pins
        pins += f'<rect x="{x-4}" y="{py-1.5}" width="8" height="3" fill="{PIN_COLOR}" />\n'
        # Right pins
        pins += f'<rect x="{x+w-4}" y="{py-1.5}" width="8" height="3" fill="{PIN_COLOR}" />\n'

    # Draw body
    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{CHIP_BG}" stroke="{SILKSCREEN_COLOR}" stroke-width="1" rx="2" />\n'
    
    # Text
    text_y = y + h/2
    text = f'<text class="silkscreen title" x="{x+w/2}" y="{text_y-2}" text-anchor="middle">{title}</text>\n'
    text += f'<text class="silkscreen subtitle" x="{x+w/2}" y="{text_y+10}" text-anchor="middle">{subtitle}</text>\n'
    
    return pins + body + text

# Paths for traces
# Each trace is a tuple: (path_d_string, delay)
traces = [
    # Trace from left to MCU
    ("M 20,112 L 50,112 L 60,95 L 90,95", 0.0),
    # MCU to Memory
    ("M 190,95 L 220,95 L 240,65 L 290,65", 1.0),
    # MCU to FPGA
    ("M 190,125 L 220,125 L 240,155 L 290,155", 1.2),
    # FPGA to Edge
    ("M 390,155 L 420,155 L 440,185 L 470,185", 2.2),
    # Memory to Edge
    ("M 390,65 L 440,65 L 450,45 L 470,45", 2.0),
    # Random decoration traces
    ("M 20,40 L 40,40 L 50,30 L 100,30", 0.5),
    ("M 400,200 L 420,200 L 430,210 L 470,210", 0.8),
    ("M 150,200 L 170,200 L 190,180 L 220,180", 1.5)
]

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
<style>
    .silkscreen {{
        font-family: 'Courier New', Courier, monospace;
        fill: {SILKSCREEN_COLOR};
    }}
    .title {{
        font-size: 12px;
        font-weight: bold;
    }}
    .subtitle {{
        font-size: 9px;
    }}
    
    .trace-base {{
        fill: none;
        stroke: {TRACE_COLOR};
        stroke-width: 2;
        stroke-linejoin: round;
        stroke-linecap: round;
        opacity: 0.4;
    }}
    
    .trace-flow {{
        fill: none;
        stroke: {GLOW_COLOR};
        stroke-width: 2.5;
        stroke-linejoin: round;
        stroke-linecap: round;
        stroke-dasharray: 20 1000;
        stroke-dashoffset: 1000;
        animation: flow 3s linear infinite;
    }}
    
    @keyframes flow {{
        0% {{ stroke-dashoffset: 100; }}
        100% {{ stroke-dashoffset: -200; }}
    }}
</style>
<rect width="100%" height="100%" fill="{BOARD_COLOR}" rx="8" />

<!-- Trace bases -->
"""

for d, _ in traces:
    svg_content += f'<path class="trace-base" d="{d}" />\n'

svg_content += "\n<!-- Trace flows -->\n"
for d, delay in traces:
    svg_content += f'<path class="trace-flow" d="{d}" style="animation-delay: {delay}s;" />\n'

svg_content += "\n<!-- Chips -->\n"
# Center Y is ~112

# MCU Chip
svg_content += draw_chip(90, 75, 100, 75, "DEV-0777", "Full Stack")

# Software / Memory Chip
svg_content += draw_chip(290, 40, 100, 50, "PYTHON-C++", "Backend & Core")

# Hardware / Frontend Chip
svg_content += draw_chip(290, 130, 100, 50, "HTML-CSS", "Frontend & UI")

svg_content += """
<!-- Vias (Holes) -->
<circle cx="20" cy="112" r="3" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5" />
<circle cx="470" cy="185" r="3" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5" />
<circle cx="470" cy="45" r="3" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5" />
<circle cx="100" cy="30" r="2" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5" />
<circle cx="400" cy="200" r="2" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5" />
<circle cx="150" cy="200" r="2" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5" />

</svg>
"""

with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Created {OUTPUT_SVG}")
