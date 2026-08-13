# -*- coding: utf-8 -*-
"""Reconstruct QR module matrices from the vector rectangles in the workbook PDF.

Clusters the tiny rectangles spatially first, then derives the module size per
cluster — different codes on the same page can be drawn at different scales.
"""
import fitz, sys, collections
sys.stdout.reconfigure(encoding="utf-8")

PDF = r"C:\Users\binja\Documents\Russian\Рабочая тетрадь_200047_Юлия Капур (QR Unlocked).pdf"

def _clusters(rects, cell):
    buckets = collections.defaultdict(list)
    for r in rects:
        buckets[(int(r.x0 // cell), int(r.y0 // cell))].append(r)
    seen, groups = set(), []
    for key in list(buckets):
        if key in seen: continue
        stack, grp = [key], []
        seen.add(key)
        while stack:
            k = stack.pop()
            grp += buckets.get(k, [])
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nk = (k[0]+dx, k[1]+dy)
                    if nk in buckets and nk not in seen:
                        seen.add(nk); stack.append(nk)
        if len(grp) >= 80:
            groups.append(grp)
    return groups

def page_qr_matrices(pg):
    rects = [d['rect'] for d in pg.get_drawings()
             if len([i for i in d['items'] if i[0] == 're']) == 1
             and 0.4 < d['rect'].width < 8
             and abs(d['rect'].width - d['rect'].height) < 0.4]
    if len(rects) < 80:
        return []
    out = []
    for grp in _clusters(rects, 6.0):
        # module size for THIS cluster
        mod = collections.Counter(round(r.width, 2) for r in grp).most_common(1)[0][0]
        g = [r for r in grp if abs(r.width - mod) < 0.25]
        if len(g) < 80: continue
        x0 = min(r.x0 for r in g); y0 = min(r.y0 for r in g)
        x1 = max(r.x1 for r in g); y1 = max(r.y1 for r in g)
        n = int(round((x1-x0)/mod)); m = int(round((y1-y0)/mod))
        if n != m or n < 21 or n > 45 or (n-17) % 4:
            continue
        M = [[False]*n for _ in range(n)]
        for r in g:
            c = int(round((r.x0-x0)/mod)); rr = int(round((r.y0-y0)/mod))
            if 0 <= rr < n and 0 <= c < n: M[rr][c] = True
        out.append((M, n, len(g), (round(x0,1), round(y0,1))))
    out.sort(key=lambda t: t[3][1])
    return out

def looks_like_qr(M):
    n = len(M)
    def finder(r0, c0):
        for i in range(7):
            for j in range(7):
                ring = (i in (0,6) or j in (0,6))
                white = (i in (1,5) or j in (1,5)) and not ring
                want = (ring or (2 <= i <= 4 and 2 <= j <= 4)) and not white
                if M[r0+i][c0+j] != want: return False
        return True
    return finder(0,0) and finder(0,n-7) and finder(n-7,0)
