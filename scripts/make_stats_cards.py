import os
import shutil

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def generate_stats_card():
    width = 495
    height = 195
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">
  <style>
    .header {{ font: 700 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #22D3EE; }}
    .stat {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #94A3B8; }}
    .stat-bold {{ font: 700 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #F8FAFC; }}
    .icon {{ fill: #A78BFA; }}
    .badge-ring {{ stroke: #22D3EE; stroke-width: 4; fill: none; }}
    .badge-text {{ font: 800 24px 'Segoe UI', Ubuntu, Sans-Serif; fill: #22D3EE; text-anchor: middle; dominant-baseline: central; }}
    .badge-sub {{ font: 600 10px 'Segoe UI', Ubuntu, Sans-Serif; fill: #A78BFA; text-anchor: middle; }}
  </style>
  <rect width="{width}" height="{height}" rx="8" fill="#0A101F" stroke="#1E293B" stroke-width="1.5"/>

  <!-- Title -->
  <text x="25" y="35" class="header">Devesh0777&apos;s GitHub Stats</text>

  <!-- Stat Items -->
  <g transform="translate(25, 55)">
    <!-- Stars -->
    <g transform="translate(0, 0)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16">
        <path fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>
      </svg>
      <text x="25" y="13" class="stat">Total Stars Earned:</text>
      <text x="200" y="13" class="stat-bold">1</text>
    </g>

    <!-- Commits -->
    <g transform="translate(0, 25)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16">
        <path fill-rule="evenodd" d="M10.5 7.75a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zm1.43.75a4.002 4.002 0 01-7.86 0H.75a.75.75 0 110-1.5h3.32a4.002 4.002 0 017.86 0h3.32a.75.75 0 110 1.5h-3.32z"/>
      </svg>
      <text x="25" y="13" class="stat">Total Commits:</text>
      <text x="200" y="13" class="stat-bold">192</text>
    </g>

    <!-- PRs -->
    <g transform="translate(0, 50)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16">
        <path fill-rule="evenodd" d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.256a2.251 2.251 0 11-1.5 0V5a2.5 2.5 0 00-2.5-2.5zm-7.25 9a.75.75 0 100 1.5.75.75 0 000-1.5zm8.5 0a.75.75 0 100 1.5.75.75 0 000-1.5z"/>
      </svg>
      <text x="25" y="13" class="stat">Total PRs:</text>
      <text x="200" y="13" class="stat-bold">18</text>
    </g>

    <!-- Issues -->
    <g transform="translate(0, 75)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16">
        <path fill-rule="evenodd" d="M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm9 3a1 1 0 11-2 0 1 1 0 012 0zm-.25-6.25a.75.75 0 00-1.5 0v3.5a.75.75 0 001.5 0v-3.5z"/>
      </svg>
      <text x="25" y="13" class="stat">Total Issues:</text>
      <text x="200" y="13" class="stat-bold">8</text>
    </g>

    <!-- Contributed to -->
    <g transform="translate(0, 100)">
      <svg class="icon" viewBox="0 0 16 16" width="16" height="16">
        <path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>
      </svg>
      <text x="25" y="13" class="stat">Contributed to:</text>
      <text x="200" y="13" class="stat-bold">5</text>
    </g>
  </g>

  <!-- Rank Badge -->
  <g transform="translate(415, 105)">
    <circle r="40" fill="#0E1626" stroke="#1E293B" stroke-width="2"/>
    <circle r="36" class="badge-ring" stroke-dasharray="190" stroke-dashoffset="30"/>
    <text y="-2" class="badge-text">A+</text>
    <text y="18" class="badge-sub">RANK</text>
  </g>
</svg>'''
    out_path = os.path.join(ROOT_DIR, "github-stats.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated:", out_path)

def generate_langs_card():
    width = 495
    height = 195
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">
  <style>
    .header {{ font: 700 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #22D3EE; }}
    .lang-name {{ font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #F8FAFC; }}
    .lang-pct {{ font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #94A3B8; }}
  </style>
  <rect width="{width}" height="{height}" rx="8" fill="#0A101F" stroke="#1E293B" stroke-width="1.5"/>

  <!-- Title -->
  <text x="25" y="35" class="header">Most Used Languages</text>

  <!-- Multi-Color Progress Bar -->
  <g transform="translate(25, 55)">
    <mask id="bar-mask">
      <rect width="445" height="10" rx="5" fill="#fff"/>
    </mask>
    <g mask="url(#bar-mask)">
      <!-- Python: 45% (200px) -->
      <rect x="0" y="0" width="200" height="10" fill="#3572A5"/>
      <!-- TypeScript: 28% (125px) -->
      <rect x="200" y="0" width="125" height="10" fill="#3178C6"/>
      <!-- JavaScript: 15% (67px) -->
      <rect x="325" y="0" width="67" height="10" fill="#F1E05A"/>
      <!-- C++: 8% (35px) -->
      <rect x="392" y="0" width="35" height="10" fill="#F34B7D"/>
      <!-- HTML/CSS: 4% (18px) -->
      <rect x="427" y="0" width="18" height="10" fill="#E34C26"/>
    </g>
  </g>

  <!-- Language List Grid (2 columns) -->
  <g transform="translate(25, 90)">
    <!-- Column 1 -->
    <g transform="translate(0, 0)">
      <circle cx="6" cy="6" r="5" fill="#3572A5"/>
      <text x="20" y="10" class="lang-name">Python <tspan class="lang-pct">45.0%</tspan></text>
    </g>
    <g transform="translate(0, 30)">
      <circle cx="6" cy="6" r="5" fill="#3178C6"/>
      <text x="20" y="10" class="lang-name">TypeScript <tspan class="lang-pct">28.1%</tspan></text>
    </g>
    <g transform="translate(0, 60)">
      <circle cx="6" cy="6" r="5" fill="#F1E05A"/>
      <text x="20" y="10" class="lang-name">JavaScript <tspan class="lang-pct">15.0%</tspan></text>
    </g>

    <!-- Column 2 -->
    <g transform="translate(220, 0)">
      <circle cx="6" cy="6" r="5" fill="#F34B7D"/>
      <text x="20" y="10" class="lang-name">C++ <tspan class="lang-pct">7.9%</tspan></text>
    </g>
    <g transform="translate(220, 30)">
      <circle cx="6" cy="6" r="5" fill="#E34C26"/>
      <text x="20" y="10" class="lang-name">HTML/CSS <tspan class="lang-pct">4.0%</tspan></text>
    </g>
  </g>
</svg>'''
    out_path = os.path.join(ROOT_DIR, "top-langs.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated:", out_path)

if __name__ == "__main__":
    generate_stats_card()
    generate_langs_card()
    # Copy this script to scripts/make_stats_cards.py
    scripts_dest = os.path.join(ROOT_DIR, "scripts", "make_stats_cards.py")
    shutil.copyfile(__file__, scripts_dest)
    print("Copied script to:", scripts_dest)
