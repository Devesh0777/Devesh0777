import json
import os
import math

OUTPUT_SVG = "stats-graph.svg"

# Purple Cyber Sci-Fi Theme:
BG_COLOR = "#0B0813"
BORDER_COLOR = "#A77BFF"
TEXT_GREEN = "#D4BEFF"
TEXT_DIM = "#A77BFF"
GLOW_COLOR = "#B18CFF"
GRID_COLOR = "#22133E"

def generate_graph_svg():
    width = 860
    height = 240
    padding = 20

    # Data points for 12 months activity / commits graph
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    activity_values = [42, 68, 85, 54, 110, 95, 130, 160, 145, 180, 210, 240]

    # Map graph values to Y coordinates
    min_val, max_val = 0, 260
    graph_x_start = 70
    graph_x_end = 810
    graph_y_top = 60
    graph_y_bottom = 190

    dx = (graph_x_end - graph_x_start) / (len(months) - 1)
    points = []
    for i, val in enumerate(activity_values):
        cx = graph_x_start + i * dx
        cy = graph_y_bottom - ((val - min_val) / (max_val - min_val)) * (graph_y_bottom - graph_y_top)
        points.append((cx, cy))

    path_d = "M " + " L ".join([f"{x:.1f},{y:.1f}" for x, y in points])
    area_d = path_d + f" L {graph_x_end},{graph_y_bottom} L {graph_x_start},{graph_y_bottom} Z"

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <defs>
        <filter id="hacker-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <linearGradient id="area-grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#00FF66" stop-opacity="0.35"/>
            <stop offset="100%" stop-color="#00FF66" stop-opacity="0.0"/>
        </linearGradient>
    </defs>

    <style>
        .bg {{ fill: {BG_COLOR}; stroke: {BORDER_COLOR}; stroke-width: 2; }}
        .header-title {{ font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; fill: {TEXT_GREEN}; letter-spacing: 2px; filter: url(#hacker-glow); }}
        .axis-text {{ font-family: 'Courier New', monospace; font-size: 11px; font-weight: bold; fill: {TEXT_DIM}; }}
        .graph-line {{ fill: none; stroke: {TEXT_GREEN}; stroke-width: 2.5; filter: url(#hacker-glow); }}
        .graph-point {{ fill: {BG_COLOR}; stroke: {TEXT_GREEN}; stroke-width: 2; filter: url(#hacker-glow); transition: transform 0.2s; }}
        .grid-line {{ stroke: {GRID_COLOR}; stroke-width: 1; stroke-dasharray: 4 4; }}
    </style>

    <!-- Outer Frame -->
    <rect width="{width}" height="{height}" class="bg" rx="10" />

    <!-- Corner Accents -->
    <g stroke="{BORDER_COLOR}" stroke-width="1.5" opacity="0.8">
        <line x1="12" y1="12" x2="24" y2="12" /><line x1="12" y1="12" x2="12" y2="24" />
        <line x1="{width-12}" y1="12" x2="{width-24}" y2="12" /><line x1="{width-12}" y1="12" x2="{width-12}" y2="24" />
        <line x1="12" y1="{height-12}" x2="24" y2="{height-12}" /><line x1="12" y1="{height-12}" x2="12" y2="{height-24}" />
        <line x1="{width-12}" y1="{height-12}" x2="{width-24}" y2="{height-12}" /><line x1="{width-12}" y1="{height-12}" x2="{width-12}" y2="{height-24}" />
    </g>

    <!-- Header Bar -->
    <text x="25" y="32" class="header-title">[SYSTEM.ANALYTICS // ANNUAL COMMIT &amp; CODE ACTIVITY GRAPH]</text>
    <line x1="25" y1="42" x2="{width-25}" y2="42" stroke="{BORDER_COLOR}" stroke-width="1" opacity="0.4" />

    <!-- Grid Horizontal Lines -->
    <line x1="{graph_x_start}" y1="{graph_y_top}" x2="{graph_x_end}" y2="{graph_y_top}" class="grid-line" />
    <line x1="{graph_x_start}" y1="{(graph_y_top + graph_y_bottom)/2}" x2="{graph_x_end}" y2="{(graph_y_top + graph_y_bottom)/2}" class="grid-line" />
    <line x1="{graph_x_start}" y1="{graph_y_bottom}" x2="{graph_x_end}" y2="{graph_y_bottom}" stroke="{BORDER_COLOR}" stroke-width="1.5" opacity="0.6" />

    <!-- Y Axis Labels -->
    <text x="55" y="{graph_y_top + 4}" class="axis-text" text-anchor="end">250</text>
    <text x="55" y="{(graph_y_top + graph_y_bottom)/2 + 4}" class="axis-text" text-anchor="end">125</text>
    <text x="55" y="{graph_y_bottom + 4}" class="axis-text" text-anchor="end">0</text>

    <!-- Area Fill & Main Line -->
    <path d="{area_d}" fill="url(#area-grad)" />
    <path d="{path_d}" class="graph-line" />

    <!-- Data Points & X Axis Labels -->
'''

    for i, (cx, cy) in enumerate(points):
        month = months[i]
        svg_content += f'    <text x="{cx:.1f}" y="{graph_y_bottom + 20}" class="axis-text" text-anchor="middle">{month}</text>\n'
        svg_content += f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" class="graph-point" />\n'

    svg_content += """</svg>"""

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {OUTPUT_SVG}")

if __name__ == "__main__":
    generate_graph_svg()
