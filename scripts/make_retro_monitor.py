import os

def create_retro_monitor_svg(output_path="pcb-card.svg"):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" width="800" height="480">
<defs>
    <!-- CRT Glow Filter -->
    <filter id="crt-glow" x="-10%" y="-10%" width="120%" height="120%">
        <feGaussianBlur stdDeviation="2" result="blur" />
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
    
    <!-- Monitor Outer Shadow -->
    <filter id="drop-shadow" x="-10%" y="-10%" width="120%" height="120%">
        <feDropShadow dx="0" dy="12" stdDeviation="15" flood-color="#000000" flood-opacity="0.6"/>
    </filter>

    <!-- Scanline Pattern -->
    <pattern id="scanlines" width="100" height="4" patternUnits="userSpaceOnUse">
        <line x1="0" y1="0" x2="100" y2="0" stroke="#000000" stroke-width="1.2" opacity="0.35"/>
    </pattern>

    <!-- CRT Bezel Gradient -->
    <linearGradient id="bezel-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1E293B"/>
        <stop offset="50%" stop-color="#0F172A"/>
        <stop offset="100%" stop-color="#020617"/>
    </linearGradient>

    <!-- CRT Screen Reflection -->
    <linearGradient id="screen-glare" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.08"/>
        <stop offset="30%" stop-color="#FFFFFF" stop-opacity="0.03"/>
        <stop offset="100%" stop-color="#000000" stop-opacity="0.4"/>
    </linearGradient>
</defs>

<style>
    .bg { fill: #0B0F19; }
    .bezel { fill: url(#bezel-grad); stroke: #334155; stroke-width: 3; }
    .screen-border { fill: #030712; stroke: #1E293B; stroke-width: 4; }
    .crt-bg { fill: #050B14; }

    /* Text Fonts */
    .hud-text { font-family: 'Courier New', monospace; font-size: 13px; font-weight: bold; fill: #22D3EE; letter-spacing: 1.5px; }
    .hud-val { font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; fill: #10B981; }
    .insert-coin { font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; fill: #F43F5E; animation: blink 1.2s infinite; }

    /* Game Elements */
    .player-ship { fill: #22D3EE; stroke: #38BDF8; stroke-width: 1.5; filter: url(#crt-glow); }
    .alien-1 { fill: #A78BFA; filter: url(#crt-glow); }
    .alien-2 { fill: #F43F5E; filter: url(#crt-glow); }
    .alien-3 { fill: #F59E0B; filter: url(#crt-glow); }
    .laser { fill: #34D399; filter: url(#crt-glow); }

    /* Animations */
    @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }

    /* Player Ship Left-Right Oscillation */
    @keyframes ship-move {
        0%, 100% { transform: translateX(0px); }
        25% { transform: translateX(110px); }
        50% { transform: translateX(40px); }
        75% { transform: translateX(-90px); }
    }

    /* Laser Shot 1 */
    @keyframes laser1-anim {
        0% { transform: translateY(0); opacity: 0; }
        10% { opacity: 1; }
        80% { transform: translateY(-210px); opacity: 1; }
        85%, 100% { transform: translateY(-210px); opacity: 0; }
    }

    /* Laser Shot 2 */
    @keyframes laser2-anim {
        0%, 35% { transform: translateY(0); opacity: 0; }
        40% { opacity: 1; }
        90% { transform: translateY(-210px); opacity: 1; }
        95%, 100% { transform: translateY(-210px); opacity: 0; }
    }

    /* Alien Grid Sway */
    @keyframes alien-sway {
        0%, 100% { transform: translateX(0px); }
        50% { transform: translateX(25px); }
    }

    /* Hit Explosion Flash */
    @keyframes hit-flash {
        0%, 75%, 85%, 100% { opacity: 0; transform: scale(0.5); }
        78%, 82% { opacity: 1; transform: scale(1.4); }
    }

    /* CRT Scanline Scroll */
    @keyframes scanline-scroll {
        0% { transform: translateY(0); }
        100% { transform: translateY(4px); }
    }

    .ship-group { animation: ship-move 6s ease-in-out infinite; }
    .laser-1 { animation: laser1-anim 2.4s linear infinite; }
    .laser-2 { animation: laser2-anim 2.4s linear infinite; }
    .alien-grid { animation: alien-sway 4s ease-in-out infinite; }
    .explosion-1 { animation: hit-flash 2.4s ease-out infinite; }
    .scanline-overlay { animation: scanline-scroll 0.2s linear infinite; }
</style>

<!-- Main Canvas Background -->
<rect width="800" height="480" class="bg" rx="16"/>

<!-- CRT Monitor Body / Stand -->
<g filter="url(#drop-shadow)">
    <!-- Monitor Stand Base -->
    <path d="M280 430 L520 430 L500 455 L300 455 Z" fill="#0F172A" stroke="#334155" stroke-width="2"/>
    <rect x="360" y="405" width="80" height="30" fill="#1E293B" rx="4"/>
    
    <!-- Monitor Outer Cabinet Bezel -->
    <rect x="70" y="25" width="660" height="385" rx="28" class="bezel"/>
    
    <!-- Inner Screen Border -->
    <rect x="95" y="45" width="610" height="340" rx="18" class="screen-border"/>

    <!-- CRT Display Screen -->
    <rect x="105" y="55" width="590" height="320" rx="12" class="crt-bg"/>

    <!-- Game HUD Header -->
    <g transform="translate(125, 80)">
        <text x="0" y="0" class="hud-text">SCORE: <tspan class="hud-val">08420</tspan></text>
        <text x="210" y="0" class="hud-text">HI-SCORE: <tspan class="hud-val">99990</tspan></text>
        <text x="440" y="0" class="hud-text">PLAYER: <tspan class="hud-val">DEVESH</tspan></text>
        <line x1="0" y1="12" x2="550" y2="12" stroke="#1E293B" stroke-width="1.5"/>
    </g>

    <!-- Alien Invaders Grid -->
    <g class="alien-grid" transform="translate(160, 125)">
        <!-- Row 1 (Top Aliens - Gold) -->
        <g class="alien-3">
            <rect x="20" y="0" width="22" height="14" rx="3"/>
            <rect x="80" y="0" width="22" height="14" rx="3"/>
            <rect x="140" y="0" width="22" height="14" rx="3"/>
            <rect x="200" y="0" width="22" height="14" rx="3"/>
            <rect x="260" y="0" width="22" height="14" rx="3"/>
            <rect x="320" y="0" width="22" height="14" rx="3"/>
            <rect x="380" y="0" width="22" height="14" rx="3"/>
            <rect x="440" y="0" width="22" height="14" rx="3"/>
        </g>

        <!-- Row 2 (Middle Aliens - Purple) -->
        <g class="alien-1" transform="translate(0, 32)">
            <rect x="20" y="0" width="24" height="15" rx="3"/>
            <rect x="80" y="0" width="24" height="15" rx="3"/>
            <rect x="140" y="0" width="24" height="15" rx="3"/>
            <rect x="200" y="0" width="24" height="15" rx="3"/>
            <rect x="260" y="0" width="24" height="15" rx="3"/>
            <rect x="320" y="0" width="24" height="15" rx="3"/>
            <rect x="380" y="0" width="24" height="15" rx="3"/>
            <rect x="440" y="0" width="24" height="15" rx="3"/>
        </g>

        <!-- Row 3 (Lower Aliens - Red) -->
        <g class="alien-2" transform="translate(0, 64)">
            <rect x="20" y="0" width="24" height="15" rx="3"/>
            <rect x="80" y="0" width="24" height="15" rx="3"/>
            <rect x="140" y="0" width="24" height="15" rx="3"/>
            <rect x="200" y="0" width="24" height="15" rx="3"/>
            <rect x="260" y="0" width="24" height="15" rx="3"/>
            <rect x="320" y="0" width="24" height="15" rx="3"/>
            <rect x="380" y="0" width="24" height="15" rx="3"/>
            <rect x="440" y="0" width="24" height="15" rx="3"/>
        </g>

        <!-- Explosion Hit Effect on Alien -->
        <g class="explosion-1" transform="translate(200, 32)">
            <circle cx="12" cy="7" r="16" fill="#F59E0B" opacity="0.8"/>
            <circle cx="12" cy="7" r="10" fill="#EF4444"/>
            <circle cx="12" cy="7" r="5" fill="#FFFFFF"/>
        </g>
    </g>

    <!-- Animated Player Spaceship + Fired Lasers -->
    <g transform="translate(400, 325)">
        <g class="ship-group">
            <!-- Laser Shots -->
            <rect x="-2" y="-15" width="4" height="14" class="laser laser-1"/>
            <rect x="-2" y="-15" width="4" height="14" class="laser laser-2"/>

            <!-- Player Cannon / Ship -->
            <path d="M0 -14 L8 0 L16 8 L-16 8 L-8 0 Z" class="player-ship"/>
            <rect x="-3" y="-18" width="6" height="6" fill="#67E8F9"/>
        </g>
    </g>

    <!-- Footer HUD: Press Start -->
    <g transform="translate(400, 355)">
        <text x="0" y="0" text-anchor="middle" class="insert-coin">★ 1P READY - PRESS START ★</text>
    </g>

    <!-- CRT Scanline Grid Overlay -->
    <rect x="105" y="55" width="590" height="320" fill="url(#scanlines)" pointer-events="none" class="scanline-overlay"/>

    <!-- Screen Glass Curved Glare Overlay -->
    <rect x="105" y="55" width="590" height="320" rx="12" fill="url(#screen-glare)" pointer-events="none"/>

    <!-- Monitor Control Panel & Badges -->
    <g transform="translate(105, 372)">
        <!-- Brand Badge -->
        <rect x="250" y="6" width="90" height="16" fill="#0F172A" rx="3" stroke="#334155"/>
        <text x="295" y="18" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="#94A3B8">CRT-80s OS</text>

        <!-- Power Button & Status LED -->
        <circle cx="560" cy="14" r="5" fill="#10B981" filter="url(#crt-glow)"/>
        <circle cx="560" cy="14" r="2" fill="#A7F3D0"/>
        <rect x="530" y="9" width="16" height="10" rx="2" fill="#334155"/>
    </g>
</g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Created {output_path} — {round(len(svg)/1024, 1)} KB")

if __name__ == "__main__":
    create_retro_monitor_svg()
