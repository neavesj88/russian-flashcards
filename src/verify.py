# -*- coding: utf-8 -*-
"""Build-output checks that need no browser.

Extracts the inline script so node can syntax-check it, and scans the built page for
duplicate element ids — the defect class that previously left 🔊 buttons dead.
Run: python src/verify.py
"""
import collections, io, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(BASE, os.pardir, "index.html")
html = io.open(PAGE, encoding="utf-8").read()

print(f"index.html: {len(html.encode('utf-8')):,} bytes, {html.count(chr(10))+1:,} lines")

# --- JavaScript syntax ------------------------------------------------------
script = re.search(r"<script>(.*)</script>", html, re.S).group(1)
tmp = os.path.join(BASE, "_syntax_check.js")
io.open(tmp, "w", encoding="utf-8").write(script)
try:
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    print(f"node --check: {'PASS' if r.returncode == 0 else 'FAIL'}"
          f"{'' if r.returncode == 0 else chr(10) + r.stderr[:600]}")
finally:
    os.remove(tmp)

# --- duplicate ids ----------------------------------------------------------
# Scan the markup with the script stripped out, or every id inside a JS string literal
# counts twice and every result is a false positive.
markup = re.sub(r"<script>.*</script>", "", html, flags=re.S)
static = re.findall(r'\sid="([A-Za-z][\w-]*)"', markup)
dupes = [k for k, v in collections.Counter(static).items() if v > 1]
print("duplicate ids in static markup:", dupes or "none")

emitted = re.findall(r"""id=\\?["']([A-Za-z][\w-]*)\\?["']""", script)
multi = [k for k, v in collections.Counter(emitted).items() if v > 1]
print("ids emitted from more than one place in JS:", multi or "none")

# --- contrast ---------------------------------------------------------------
# Computed from the CSS variables rather than eyeballed, so a colour tweak that breaks
# WCAG AA fails here instead of shipping.
def _lum(hexval):
    h = hexval.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    def chan(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return .2126 * chan(r) + .7152 * chan(g) + .0722 * chan(b)

def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)

roots = re.findall(r":root\{(.*?)\}", html, re.S)
themes = [dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})", blk)) for blk in roots[:2]]
# (label, foreground, background, minimum) — minimum is 3.0 only for large/bold text
PAIRS = [("body on page", "--ink", "--bg", 4.5),
         ("muted small on card", "--muted", "--panel", 4.5),
         ("muted on page", "--muted", "--bg", 4.5),
         ("muted on selected deck", "--muted", "--accent-soft", 4.5),
         ("label on filled accent button", "--on-accent", "--accent", 4.5),
         ("correct option", "--good", "--good-soft", 4.5),
         ("wrong option", "--bad", "--bad-soft", 4.5),
         ("verdict ok on panel", "--good", "--bg", 4.5),
         ("speak button label", "--accent", "--panel", 4.5)]
fails = 0
for name, V in zip(("light", "dark"), themes):
    for label, fg, bg, need in PAIRS:
        r = contrast(V[fg], V[bg])
        if r < need:
            fails += 1
            print(f"  CONTRAST FAIL [{name}] {label}: {r:.2f}:1 (need {need})")
print(f"contrast: {'all pairs pass AA' if not fails else str(fails) + ' failure(s)'}")

# --- accessibility spot checks ---------------------------------------------
print("lang=\"ru\" occurrences:", html.count('lang="ru"'))
print("<noscript> present:", "<noscript>" in html)
print("aria-label on the speak button:", 'aria-label="Play the Russian"' in html)
print("outline:none anywhere (would kill focus rings):", "outline:none" in html)
