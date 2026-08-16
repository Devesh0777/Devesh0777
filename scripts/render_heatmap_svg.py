import json
import os
import math

OUTPUT_SVG = "contrib-heatmap.svg"

# Grid size: 45 cols x 15 rows matching the exact pixel Batman Beyond / Red Bat emblem image
# Dark background: #121212
# Red pixel color: #E50914 (or #E63946 / #DC2626)

def generate_batman_grid():
    rows = 15
    cols = 45
    
    # Initialize dark grid
    DARK_BG = "#121212"
    RED_BAT = "#E50914"

    grid = [[DARK_BG for _ in range(cols)] for _ in range(rows)]

    # Exact pixel coordinate mapping of the red Batman emblem from the provided image:
    # Midline is col 22.
    red_pixels = [
        # Tips of wings (top)
        (11, 0), (33, 0),
        (12, 1), (13, 1), (31, 1), (32, 1),
        (13, 2), (14, 2), (15, 2), (29, 2), (30, 2), (31, 2),
        (13, 3), (14, 3), (15, 3), (16, 3), (28, 3), (29, 3), (30, 3), (31, 3),
        (13, 4), (14, 4), (15, 4), (16, 4), (17, 4), (27, 4), (28, 4), (29, 4), (30, 4), (31, 4),
        
        # Bat ears & upper wing curves
        (21, 4), (23, 4), # Ears
        (14, 5), (15, 5), (16, 5), (17, 5), (21, 5), (22, 5), (23, 5), (27, 5), (28, 5), (29, 5), (30, 5),
        (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (21, 6), (22, 6), (23, 6), (26, 6), (27, 6), (28, 6), (29, 6), (30, 6),
        (14, 7), (15, 7), (16, 7), (17, 7), (18, 7), (19, 7), (20, 7), (21, 7), (22, 7), (23, 7), (24, 7), (25, 7), (26, 7), (27, 7), (28, 7), (29, 7), (30, 7),
        
        # Wing body expansion
        (15, 8), (16, 8), (17, 8), (18, 8), (19, 8), (20, 8), (21, 8), (22, 8), (23, 8), (24, 8), (25, 8), (26, 8), (27, 8), (28, 8), (29, 8),
        (17, 9), (18, 9), (19, 9), (20, 9), (21, 9), (22, 9), (23, 9), (24, 9), (25, 9), (26, 9), (27, 9),
        
        # Lower V shape body
        (19, 10), (20, 10), (21, 10), (22, 10), (23, 10), (24, 10), (25, 10),
        (20, 11), (21, 11), (22, 11), (23, 11), (24, 11),
        (21, 12), (22, 12), (23, 12),
        (22, 13), # Tail
        (22, 14)  # Tail tip
    ]

    for c, r in red_pixels:
        if 0 <= r < rows and 0 <= c < cols:
            grid[r][c] = RED_BAT

    return grid

def generate_svg():
    grid = generate_batman_grid()
    rows = len(grid)
    cols = len(grid[0])

    box_size = 15
    box_spacing = 3
    padding = 24

    svg_width = cols * (box_size + box_spacing) + (padding * 2)
    svg_height = rows * (box_size + box_spacing) + (padding * 2)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
    <defs>
        <!-- Neon Glow Filter -->
        <filter id="bat-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="2.5" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>

    <style>
        .pixel {{
            transition: transform 0.2s ease, opacity 0.3s ease;
        }}
        .pixel:hover {{
            transform: scale(1.3);
            filter: brightness(1.5);
        }}
        .bg-rect {{
            fill: #0A0A0C;
            rx: 12px;
        }}
        .snake-head {{
            fill: #FF2E93;
            filter: url(#bat-glow);
        }}
    </style>

    <!-- Background Base -->
    <rect width="100%" height="100%" class="bg-rect" />

    <g transform="translate({padding}, {padding})">
'''

    # Generate Rectangles for each Pixel in Grid
    for r in range(rows):
        for c in range(cols):
            color = grid[r][c]
            x = c * (box_size + box_spacing)
            y = r * (box_size + box_spacing)
            
            # Subtle glow filter on red pixels
            glow_attr = ' filter="url(#bat-glow)"' if color == "#E50914" else ""

            svg_content += f'      <rect class="pixel" x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}"{glow_attr} />\n'

    # Add Animated Snake Path slithering through the Batman grid!
    snake_points = []
    for c in range(0, cols, 3):
        x1 = c * (box_size + box_spacing) + box_size / 2
        x2 = (c + 1) * (box_size + box_spacing) + box_size / 2
        snake_points.append(f"{x1},{box_size / 2}")
        snake_points.append(f"{x1},{(rows-1) * (box_size + box_spacing) + box_size / 2}")
        snake_points.append(f"{x2},{(rows-1) * (box_size + box_spacing) + box_size / 2}")
        snake_points.append(f"{x2},{box_size / 2}")

    snake_path_d = "M " + " L ".join(snake_points)

    svg_content += f'''
    <!-- Animated Cyber Snake Slithering across Batman Grid -->
    <g class="snake">
      <rect width="12" height="12" rx="3" fill="#800020">
        <animateMotion path="{snake_path_d}" dur="16s" repeatCount="indefinite" begin="-0.6s" />
      </rect>
      <rect width="12" height="12" rx="3" fill="#B91C1C">
        <animateMotion path="{snake_path_d}" dur="16s" repeatCount="indefinite" begin="-0.4s" />
      </rect>
      <rect width="12" height="12" rx="3" fill="#EF4444">
        <animateMotion path="{snake_path_d}" dur="16s" repeatCount="indefinite" begin="-0.2s" />
      </rect>
      <!-- Snake Head -->
      <rect width="13" height="13" rx="3" class="snake-head" stroke="#FFFFFF" stroke-width="1.5">
        <animateMotion path="{snake_path_d}" dur="16s" repeatCount="indefinite" begin="0s" />
      </rect>
    </g>
    '''

    svg_content += """    </g>
</svg>"""

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated {OUTPUT_SVG} with Batman pixel emblem matrix ({cols}x{rows})!")

if __name__ == "__main__":
    generate_svg()
