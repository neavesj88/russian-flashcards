# -*- coding: utf-8 -*-
"""Extract QR matrices from the rasterised workbook pages.

The codes sit in a narrow left margin, axis-aligned and isolated on white, so the
dark bounding box IS the code's bounding box (a QR always has black modules in all
three finder corners). The module size is measured from the top-left finder, which
is exactly 7 modules wide.
"""
import fitz, sys
sys.stdout.reconfigure(encoding="utf-8")

DARK = bytes(1 if i < 140 else 0 for i in range(256))
# The codes sit at x≈44.7–86pt (confirmed against the vector-drawn ones). Keep the
# band tight so neighbouring page furniture does not widen the dark bounding box.
BAND = fitz.Rect(36, 20, 94, 830)
DPI  = 400

def bands(pg, dpi=DPI):
    pix = pg.get_pixmap(clip=BAND, colorspace=fitz.csGRAY, dpi=dpi)
    W, H = pix.width, pix.height
    B = pix.samples.translate(DARK)
    rows = [y for y in range(H) if B[y*W:(y+1)*W].count(1)]
    if not rows: return []
    out, start, prev = [], rows[0], rows[0]
    for y in rows[1:]:
        if y - prev > 4:
            out.append((start, prev)); start = y
        prev = y
    out.append((start, prev))
    return [(y0, y1, B, W, H) for y0, y1 in out]

def matrices(pg, dpi=DPI):
    res = []
    for y0, y1, B, W, H in bands(pg, dpi):
        h = y1 - y0 + 1
        if h < 40: continue
        xs = [x for x in range(W)
              if any(B[y*W + x] for y in range(y0, y1+1))]
        if not xs: continue
        x0, x1 = xs[0], xs[-1]
        w = x1 - x0 + 1
        if abs(w - h) > 0.10 * max(w, h): continue          # must be square
        # module size from the top-left finder, which is exactly 7 modules wide.
        # Take the longest leading dark run over the first few rows, so a ragged
        # top edge from anti-aliasing cannot throw the measurement off.
        run = 0
        for yy in range(y0, min(y0 + 5, y1 + 1)):
            k = 0
            while x0 + k <= x1 and B[yy*W + x0 + k]: k += 1
            run = max(run, k)
        if run < 5: continue
        mod = run / 7.0
        n = int(round(w / mod))
        if n < 21 or n > 45 or (n - 17) % 4: continue
        mod = w / n                                          # refine
        M = [[False]*n for _ in range(n)]
        for r in range(n):
            yy = int(y0 + (r + 0.5) * mod)
            if yy >= H: yy = H - 1
            for c in range(n):
                xx = int(x0 + (c + 0.5) * mod)
                if xx >= W: xx = W - 1
                M[r][c] = bool(B[yy*W + xx])
        res.append((M, n, y0))
    return res
