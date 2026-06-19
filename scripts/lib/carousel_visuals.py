"""SVG visuals for Founder Context Problem carousel story."""

from __future__ import annotations

GOLD = "#D4AF37"
WHITE = "#EDEDED"
GREY = "#9CA3AF"


def founder_silhouette() -> str:
    """Head/shoulders silhouette from signal nodes — no human illustration."""
    nodes = [
        (160, 55, 8), (130, 75, 5), (190, 75, 5), (110, 100, 4), (210, 100, 4),
        (145, 110, 5), (175, 110, 5), (160, 130, 6), (125, 145, 4), (195, 145, 4),
        (100, 170, 4), (220, 170, 4), (140, 180, 5), (180, 180, 5), (160, 200, 7),
        (120, 210, 4), (200, 210, 4), (90, 230, 4), (230, 230, 4), (160, 250, 6),
        (130, 260, 4), (190, 260, 4),
    ]
    edges = [
        (160, 55, 160, 130), (130, 75, 160, 110), (190, 75, 160, 110),
        (110, 100, 145, 110), (210, 100, 175, 110), (160, 130, 160, 200),
        (125, 145, 140, 180), (195, 145, 180, 180), (100, 170, 120, 210),
        (220, 170, 200, 210), (160, 200, 160, 250), (130, 260, 160, 250),
        (190, 260, 160, 250), (90, 230, 120, 210), (230, 230, 200, 210),
    ]
    line_svg = "\n".join(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GOLD}" stroke-width="1" opacity="0.4"/>'
        for x1, y1, x2, y2 in edges
    )
    circles = "\n".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD if i % 3 == 0 else WHITE}" opacity="0.85"/>'
        for i, (x, y, r) in enumerate(nodes)
    )
    return f'''<svg viewBox="0 0 320 300" width="100%" xmlns="http://www.w3.org/2000/svg">
  {line_svg}
  {circles}
</svg>'''


def network_splitting() -> str:
    return f'''<svg viewBox="0 0 400 280" width="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- unified top network -->
  <circle cx="200" cy="50" r="6" fill="{GOLD}"/>
  <circle cx="160" cy="70" r="4" fill="{WHITE}"/>
  <circle cx="240" cy="70" r="4" fill="{WHITE}"/>
  <circle cx="180" cy="90" r="4" fill="{WHITE}"/>
  <circle cx="220" cy="90" r="4" fill="{WHITE}"/>
  <line x1="200" y1="50" x2="160" y2="70" stroke="{GOLD}" stroke-width="1" opacity="0.5"/>
  <line x1="200" y1="50" x2="240" y2="70" stroke="{GOLD}" stroke-width="1" opacity="0.5"/>
  <line x1="200" y1="50" x2="180" y2="90" stroke="{GOLD}" stroke-width="1" opacity="0.5"/>
  <line x1="200" y1="50" x2="220" y2="90" stroke="{GOLD}" stroke-width="1" opacity="0.5"/>
  <!-- split arrows -->
  <line x1="120" y1="120" x2="120" y2="150" stroke="{GOLD}" stroke-width="1.5" opacity="0.6"/>
  <line x1="200" y1="120" x2="200" y2="150" stroke="{GOLD}" stroke-width="1.5" opacity="0.6"/>
  <line x1="280" y1="120" x2="280" y2="150" stroke="{GOLD}" stroke-width="1.5" opacity="0.6"/>
  <polygon points="120,150 115,140 125,140" fill="{GOLD}" opacity="0.6"/>
  <polygon points="200,150 195,140 205,140" fill="{GOLD}" opacity="0.6"/>
  <polygon points="280,150 275,140 285,140" fill="{GOLD}" opacity="0.6"/>
  <!-- cluster 1 product -->
  <circle cx="120" cy="190" r="5" fill="{GREY}"/>
  <circle cx="100" cy="210" r="4" fill="{GREY}"/>
  <circle cx="140" cy="215" r="4" fill="{GREY}"/>
  <line x1="120" y1="190" x2="100" y2="210" stroke="{GREY}" stroke-width="1" opacity="0.4"/>
  <line x1="120" y1="190" x2="140" y2="215" stroke="{GREY}" stroke-width="1" opacity="0.4"/>
  <text x="120" y="250" text-anchor="middle" fill="{GREY}" font-size="11" font-family="Inter,sans-serif" letter-spacing="1">PRODUCT</text>
  <!-- cluster 2 sales -->
  <circle cx="200" cy="195" r="5" fill="{GREY}"/>
  <circle cx="185" cy="215" r="4" fill="{GREY}"/>
  <circle cx="220" cy="210" r="4" fill="{GREY}"/>
  <line x1="200" y1="195" x2="185" y2="215" stroke="{GREY}" stroke-width="1" opacity="0.4"/>
  <line x1="200" y1="195" x2="220" y2="210" stroke="{GREY}" stroke-width="1" opacity="0.4"/>
  <text x="200" y="250" text-anchor="middle" fill="{GREY}" font-size="11" font-family="Inter,sans-serif" letter-spacing="1">SALES</text>
  <!-- cluster 3 engineering -->
  <circle cx="280" cy="188" r="5" fill="{GREY}"/>
  <circle cx="265" cy="208" r="4" fill="{GREY}"/>
  <circle cx="300" cy="212" r="4" fill="{GREY}"/>
  <line x1="280" y1="188" x2="265" y2="208" stroke="{GREY}" stroke-width="1" opacity="0.4"/>
  <line x1="280" y1="188" x2="300" y2="212" stroke="{GREY}" stroke-width="1" opacity="0.4"/>
  <text x="280" y="250" text-anchor="middle" fill="{GREY}" font-size="11" font-family="Inter,sans-serif" letter-spacing="1">ENGINEERING</text>
</svg>'''


def signal_noise_highlight() -> str:
    import random
    random.seed(42)
    dots = []
    for _ in range(80):
        x, y = random.randint(40, 360), random.randint(40, 220)
        r = random.choice([2, 2, 3])
        dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}" opacity="0.15"/>')
    return f'''<svg viewBox="0 0 400 260" width="100%" xmlns="http://www.w3.org/2000/svg">
  {"".join(dots)}
  <circle cx="200" cy="180" r="10" fill="{GOLD}"/>
  <circle cx="200" cy="180" r="22" fill="none" stroke="{GOLD}" stroke-width="1" opacity="0.4"/>
  <circle cx="200" cy="180" r="36" fill="none" stroke="{GOLD}" stroke-width="0.5" opacity="0.25"/>
  <circle cx="200" cy="180" r="50" fill="none" stroke="{GOLD}" stroke-width="0.5" opacity="0.15"/>
  <text x="60" y="240" fill="{GREY}" font-size="10" font-family="Inter,sans-serif" letter-spacing="2">NOISE</text>
  <text x="185" y="240" fill="{GOLD}" font-size="10" font-family="Inter,sans-serif" letter-spacing="2">SIGNAL</text>
</svg>'''


def question_mark_nodes() -> str:
    return f'''<svg viewBox="0 0 200 280" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <circle cx="120" cy="40" r="5" fill="{GOLD}"/>
  <circle cx="80" cy="70" r="4" fill="{WHITE}"/>
  <circle cx="150" cy="65" r="4" fill="{WHITE}"/>
  <circle cx="60" cy="110" r="4" fill="{WHITE}"/>
  <circle cx="130" cy="100" r="5" fill="{GOLD}"/>
  <circle cx="170" cy="130" r="4" fill="{WHITE}"/>
  <circle cx="90" cy="150" r="4" fill="{WHITE}"/>
  <circle cx="140" cy="170" r="5" fill="{GOLD}"/>
  <circle cx="110" cy="210" r="6" fill="{GOLD}"/>
  <line x1="120" y1="40" x2="80" y2="70" stroke="{GOLD}" stroke-width="1" opacity="0.5"/>
  <line x1="120" y1="40" x2="150" y2="65" stroke="{GOLD}" stroke-width="1" opacity="0.5"/>
  <line x1="80" y1="70" x2="60" y2="110" stroke="{GOLD}" stroke-width="1" opacity="0.4"/>
  <line x1="150" y1="65" x2="130" y2="100" stroke="{GOLD}" stroke-width="1" opacity="0.4"/>
  <line x1="130" y1="100" x2="170" y2="130" stroke="{GOLD}" stroke-width="1" opacity="0.4"/>
  <line x1="60" y1="110" x2="90" y2="150" stroke="{GOLD}" stroke-width="1" opacity="0.3"/>
  <line x1="130" y1="100" x2="90" y2="150" stroke="{GOLD}" stroke-width="1" opacity="0.3"/>
  <line x1="90" y1="150" x2="140" y2="170" stroke="{GOLD}" stroke-width="1" opacity="0.4"/>
  <line x1="140" y1="170" x2="110" y2="210" stroke="{GOLD}" stroke-width="1" opacity="0.5"/>
</svg>'''


def hook_signal_glow() -> str:
    return f'''<svg viewBox="0 0 120 120" width="120" height="120" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="60" r="8" fill="{GOLD}"/>
  <circle cx="60" cy="60" r="20" fill="none" stroke="{GOLD}" stroke-width="1" opacity="0.35"/>
  <circle cx="60" cy="60" r="35" fill="none" stroke="{GOLD}" stroke-width="0.5" opacity="0.2"/>
  <circle cx="60" cy="60" r="50" fill="none" stroke="{GOLD}" stroke-width="0.5" opacity="0.12"/>
</svg>'''


def execution_arrow() -> str:
    return f'''<svg viewBox="0 0 280 80" width="100%" height="80" xmlns="http://www.w3.org/2000/svg">
  <line x1="20" y1="40" x2="220" y2="40" stroke="{GOLD}" stroke-width="2"/>
  <polygon points="220,40 200,28 200,52" fill="{GOLD}"/>
</svg>'''


def signal_network(active: bool = False) -> str:
    gold = GOLD if active else GREY
    return f'''<svg viewBox="0 0 320 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <circle cx="160" cy="160" r="8" fill="{gold}" opacity="0.9"/>
  <circle cx="160" cy="160" r="24" fill="none" stroke="{gold}" stroke-width="1" opacity="0.3"/>
  <line x1="160" y1="160" x2="80" y2="80" stroke="{gold}" stroke-width="1.5" opacity="0.5"/>
  <line x1="160" y1="160" x2="240" y2="80" stroke="{gold}" stroke-width="1.5" opacity="0.5"/>
  <circle cx="80" cy="80" r="6" fill="{gold}"/>
  <circle cx="240" cy="80" r="6" fill="{gold}"/>
</svg>'''


def fragmented_nodes() -> str:
    return network_splitting()


def unified_network() -> str:
    return signal_network(active=True)
