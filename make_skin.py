#!/usr/bin/env python3
"""Draw the cybersecurity profile skin as a PNG image using Pillow."""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import math

W, H = 1200, 420
IMG = Image.new("RGB", (W, H), (0x01, 0x01, 0x03))
DRAW = ImageDraw.Draw(IMG)

# ---------- Helper fonts ----------
def font(size, bold=True):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()

F_TITLE = font(36, True)
F_SUB   = font(17, True)
F_SMALL = font(13, False)
F_CARD  = font(14, True)
F_CARD_SM = font(12, False)
F_SKILL = font(20, True)
F_SKILL_TXT = font(12, False)
F_FOOT  = font(11, False)

# ---------- Colors ----------
C_BG_DARK   = (0x01, 0x01, 0x03)
C_BG_MID    = (0x0b, 0x0b, 0x1a)
C_BG_LIGHT  = (0x0a, 0x0a, 0x1a)
C_CYAN      = (0x00, 0xff, 0xff)
C_MAGENTA   = (0xff, 0x00, 0xde)
C_YELLOW    = (0xff, 0xff, 0x00)
C_WHITE     = (0xff, 0xff, 0xff)
C_GREEN     = (0x00, 0xff, 0x00)
C_GRAY      = (0xaa, 0xaa, 0xaa)
C_DARK_GRAY = (0x0d, 0x0d, 0x1a)
C_LIGHT_BLUE= (0x88, 0xcc, 0xff)
C_DARK_TEXT = (0x44, 0x44, 0x44)

# ---------- Background gradient ----------
for y in range(H):
    t = y / H
    if t < 0.3:
        r = int(0x01 + (0x0b - 0x01) * (t / 0.3))
        g = int(0x01 + (0x0b - 0x01) * (t / 0.3))
        b = int(0x03 + (0x1a - 0x03) * (t / 0.3))
    elif t < 0.7:
        tt = (t - 0.3) / 0.4
        r = int(0x0b + (0x0a - 0x0b) * tt)
        g = int(0x0b + (0x0a - 0x0b) * tt)
        b = int(0x1a + (0x1a - 0x1a) * tt)
    else:
        tt = (t - 0.7) / 0.3
        r = int(0x0a + (0x01 - 0x0a) * tt)
        g = int(0x0a + (0x01 - 0x0a) * tt)
        b = int(0x1a + (0x03 - 0x1a) * tt)
    DRAW.line([(0, y), (W, y)], fill=(r, g, b))

# ---------- Circuit grid pattern ----------
grid = 40
for x in range(0, W, grid):
    DRAW.line([(x, 0), (x, H)], fill=(0x00, 0xff, 0xff, 8), width=1)
for y in range(0, H, grid):
    DRAW.line([(0, y), (W, y)], fill=(0x00, 0xff, 0xff, 8), width=1)

# ---------- Frame ----------
FRAME_X, FRAME_Y = 30, 30
FRAME_W, FRAME_H = 1140, 360
# Neon border (drawn as thick rect with gradient effect)
for i in range(3):
    offset = i * 2
    color = (
        int(C_CYAN[0] * (1 - i * 0.25)),
        int(C_CYAN[1] * (1 - i * 0.25)),
        int(C_CYAN[2] * (1 - i * 0.25)),
    )
    DRAW.rounded_rectangle(
        [FRAME_X - offset, FRAME_Y - offset, FRAME_X + FRAME_W + offset, FRAME_Y + FRAME_H + offset],
        radius=20 + offset,
        outline=color,
        width=2,
    )
# Inner white thin rect
DRAW.rounded_rectangle(
    [FRAME_X, FRAME_Y, FRAME_X + FRAME_W, FRAME_Y + FRAME_H],
    radius=20,
    outline=(0xff, 0xff, 0xff, 15),
    width=1,
)

# ---------- Corner brackets ----------
bracket_color = C_CYAN
bracket_len = 110
bracket_w = 3
corners = [
    (FRAME_X + 30, FRAME_Y + 30, "tl"),
    (FRAME_X + FRAME_W - 30, FRAME_Y + 30, "tr"),
    (FRAME_X + 30, FRAME_Y + FRAME_H - 30, "bl"),
    (FRAME_X + FRAME_W - 30, FRAME_Y + FRAME_H - 30, "br"),
]
for cx, cy, pos in corners:
    if pos == "tl":
        DRAW.line([(cx, cy), (cx + bracket_len, cy)], fill=bracket_color, width=bracket_w)
        DRAW.line([(cx, cy), (cx, cy + bracket_len)], fill=bracket_color, width=bracket_w)
    elif pos == "tr":
        DRAW.line([(cx, cy), (cx - bracket_len, cy)], fill=bracket_color, width=bracket_w)
        DRAW.line([(cx, cy), (cx, cy + bracket_len)], fill=bracket_color, width=bracket_w)
    elif pos == "bl":
        DRAW.line([(cx, cy), (cx + bracket_len, cy)], fill=bracket_color, width=bracket_w)
        DRAW.line([(cx, cy), (cx, cy - bracket_len)], fill=bracket_color, width=bracket_w)
    elif pos == "br":
        DRAW.line([(cx, cy), (cx - bracket_len, cy)], fill=bracket_color, width=bracket_w)
        DRAW.line([(cx, cy), (cx, cy - bracket_len)], fill=bracket_color, width=bracket_w)

# ---------- Central Shield ----------
shield_cx, shield_cy = 600, 170
shield_scale = 1.0

def shield_path_points():
    # Shield shape points relative to center
    pts = [
        (0, -70),   # top
        (-35, -70), # top left curve start
        (-60, -50), # curve
        (-70, -20), # side
        (-70, 60),  # lower side
        (-60, 110), # curve to bottom
        (-40, 130), # bottom left
        (0, 150),   # bottom point
        (40, 130),  # bottom right
        (60, 110),  # curve
        (70, 60),   # right side
        (70, -20),  # right side top
        (60, -50),  # curve
        (35, -70),  # top right curve end
    ]
    return [(shield_cx + x * shield_scale, shield_cy + y * shield_scale) for x, y in pts]

# Shield outer (filled dark)
outer_pts = shield_path_points()
DRAW.polygon(outer_pts, fill=(0x1a, 0x1a, 0x2e))
DRAW.polygon(outer_pts, outline=C_CYAN, width=3)

# Shield inner
inner_pts = [(x, y + 12) for x, y in shield_path_points()]
inner_pts = [(shield_cx + (x - shield_cx) * 0.85, shield_cy + (y - shield_cy) * 0.85) for x, y in inner_pts]
DRAW.polygon(inner_pts, outline=(0xff, 0xff, 0xff), width=2)

# Digital Lock
lock_cx, lock_cy = shield_cx, shield_cy + 25
lock_w, lock_h = 28, 26
# Lock body
DRAW.rounded_rectangle(
    [lock_cx - lock_w//2, lock_cy - lock_h//2, lock_cx + lock_w//2, lock_cy + lock_h//2],
    radius=6,
    fill=C_CYAN,
)
# Shackle
DRAW.arc(
    [lock_cx - 18, lock_cy - 40, lock_cx + 18, lock_cy - 4],
    start=180, end=0,
    fill=C_WHITE,
    width=3,
)
# Keyhole
DRAW.ellipse([lock_cx - 4, lock_cy + 2, lock_cx + 4, lock_cy + 10], fill=C_BG_DARK)

# Core glow circle
glow_r = 34
for i in range(glow_r, 0, -3):
    alpha = int(100 * (1 - i / glow_r))
    color = (0, 255, 255, alpha)
    # Pillow doesn't support alpha in ellipse directly on RGB, so skip multi-layer glow
    break
DRAW.ellipse([shield_cx - glow_r, shield_cy - 40 - glow_r, shield_cx + glow_r, shield_cy - 40 + glow_r], outline=(0x00, 0xff, 0xff, 60), width=1)

# ---------- Header ----------
title = "RKN-702"
tw = DRAW.textlength(title, font=F_TITLE)
DRAW.text(((W - tw) / 2, 50), title, font=F_TITLE, fill=C_WHITE)

subtitle = "CYBERSECURITY RESEARCHER & PENETRATION TESTER"
tw = DRAW.textlength(subtitle, font=F_SUB)
DRAW.text(((W - tw) / 2, 92), subtitle, font=F_SUB, fill=C_CYAN)

subtitle2 = "WEB SECURITY  •  BUG BOUNTY HUNTER  •  DAMMAM, SAUDI ARABIA"
tw = DRAW.textlength(subtitle2, font=F_SMALL)
DRAW.text(((W - tw) / 2, 116), subtitle2, font=F_SMALL, fill=(0xaa, 0xaa, 0xaa))

# ---------- Status Bar ----------
status_x, status_y = 80, 160
status_w, status_h = 340, 50
DRAW.rounded_rectangle([status_x, status_y, status_x + status_w, status_y + status_h], radius=10, fill=C_DARK_GRAY, outline=C_CYAN, width=1)
# Green dot
DRAW.ellipse([status_x + 20, status_y + 12, status_x + 34, status_y + 26], fill=C_GREEN)
# Text
DRAW.text([status_x + 42, status_y + 14], "SYSTEM SECURE", font=F_CARD, fill=C_GREEN)
DRAW.text([status_x + 195, status_y + 14], "LIVE MONITORING", font=F_CARD, fill=C_YELLOW)

# ---------- Bug Bounty Platforms ----------
sect_x, sect_y = 80, 220
DRAW.text([sect_x, sect_y], "BUG BOUNTY PLATFORMS", font=F_SKILL, fill=C_WHITE)

cards = [
    ("bugbounty.sa", "/profile/rkn_702", C_CYAN),
    ("HackenProof", "/hackers/rkn702", (0x00, 0xd9, 0xff)),
    ("Intigriti", "/researcher/rkn_702", (0xff, 0x6b, 0x00)),
    ("Bugcrowd", "/h/rkn_702", (0xef, 0x47, 0x6f)),
]
card_w, card_h = 240, 70
card_gap = 20
card_start_y = sect_y + 25

for i, (name, url, color) in enumerate(cards):
    cx = sect_x + i * (card_w + card_gap)
    cy = card_start_y
    DRAW.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=10, fill=C_DARK_GRAY, outline=color, width=1)
    DRAW.text([cx + 18, cy + 10], name, font=F_CARD, fill=color)
    DRAW.text([cx + 18, cy + 34], url, font=F_CARD_SM, fill=(0xcc, 0xcc, 0xcc))

# ---------- Skills Section ----------
skills_x, skills_y = 80, 350
DRAW.text([skills_x, skills_y], "WEB SECURITY SKILLS", font=F_SKILL, fill=C_WHITE)
skills_text = "OWASP Top 10  •  XSS  •  SQL Injection  •  IDOR  •  SSRF  •  CSRF  •  Race Conditions  •  API Security  •  Burp Suite  •  Recon"
DRAW.text([skills_x, skills_y + 22], skills_text, font=F_SKILL_TXT, fill=C_LIGHT_BLUE)

# ---------- Decorative Binary Code ----------
bin_texts = ["01001000", "01101001", "01100101", "01110011", "01010011", "01100101", "01100011", "01110101"]
bin_x, bin_y = 900, 300
for i, t in enumerate(bin_texts):
    DRAW.text([bin_x, bin_y + i * 15], t, font=F_SMALL, fill=(0x00, 0xff, 0xff, 30))

# ---------- Connection Dots ----------
dots = [(100, 300), (140, 290), (180, 305), (1100, 300), (1060, 290), (1020, 305)]
for dx, dy in dots:
    DRAW.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(0x00, 0xff, 0xff, 100))
# Lines
DRAW.line([100, 300, 140, 290], fill=(0x00, 0xff, 0xff, 40), width=1)
DRAW.line([140, 290, 180, 305], fill=(0x00, 0xff, 0xff, 40), width=1)
DRAW.line([1100, 300, 1060, 290], fill=(0x00, 0xff, 0xff, 40), width=1)
DRAW.line([1060, 290, 1020, 305], fill=(0x00, 0xff, 0xff, 40), width=1)

# ---------- Footer ----------
footer = "ETHICAL HACKING  •  RESPONSIBLE DISCLOSURE  •  SECURE THE WEB"
tw = DRAW.textlength(footer, font=F_FOOT)
DRAW.text(((W - tw) / 2, 408), footer, font=F_FOOT, fill=(0x44, 0x44, 0x44))

# ---------- Save ----------
IMG.save("skins/custom-security.png", "PNG")
print("PNG saved: skins/custom-security.png")
print(f"Size: {IMG.size}")
