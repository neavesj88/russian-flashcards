# -*- coding: utf-8 -*-
"""A minimal QR decoder for clean, axis-aligned matrices (versions 1-6, no
Reed-Solomon correction needed since the source is vector-perfect).

Correctness is checked by re-encoding the decoded payload with the `qrcode`
library and comparing matrices bit for bit.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

ALIGN = {1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30], 6: [6, 34]}
EC_BITS = {1: 'L', 0: 'M', 3: 'Q', 2: 'H'}
# version -> ec -> list of (total_codewords, data_codewords) per block
BLOCKS = {
 1: {'L': [(26,19)], 'M': [(26,16)], 'Q': [(26,13)], 'H': [(26,9)]},
 2: {'L': [(44,34)], 'M': [(44,28)], 'Q': [(44,22)], 'H': [(44,16)]},
 3: {'L': [(70,55)], 'M': [(70,44)], 'Q': [(35,17)]*2, 'H': [(35,13)]*2},
 4: {'L': [(100,80)], 'M': [(50,32)]*2, 'Q': [(50,24)]*2, 'H': [(25,9)]*4},
 5: {'L': [(134,108)], 'M': [(67,43)]*2,
     'Q': [(33,15)]*2 + [(34,16)]*2, 'H': [(33,11)]*2 + [(34,12)]*2},
 6: {'L': [(86,68)]*2, 'M': [(43,27)]*4, 'Q': [(43,19)]*4, 'H': [(43,15)]*4},
}
MASKS = [
 lambda r,c: (r+c) % 2 == 0,
 lambda r,c: r % 2 == 0,
 lambda r,c: c % 3 == 0,
 lambda r,c: (r+c) % 3 == 0,
 lambda r,c: (r//2 + c//3) % 2 == 0,
 lambda r,c: (r*c) % 2 + (r*c) % 3 == 0,
 lambda r,c: ((r*c) % 2 + (r*c) % 3) % 2 == 0,
 lambda r,c: ((r+c) % 2 + (r*c) % 3) % 2 == 0,
]

def bch_correct_format(v):
    """Find the format value whose BCH encoding is closest to v."""
    best, bd = None, 99
    for f in range(32):
        d = f << 10
        for i in range(4, -1, -1):
            if d & (1 << (i+10)):
                d ^= 0x537 << i
        code = ((f << 10) | d) ^ 0x5412
        dist = bin(code ^ v).count('1')
        if dist < bd:
            bd, best = dist, code
    return best, bd

def read_format(M):
    n = len(M)
    b = []
    for c in range(6): b.append(M[8][c])
    b += [M[8][7], M[8][8], M[7][8]]
    for r in range(5, -1, -1): b.append(M[r][8])
    v = 0
    for x in b: v = (v << 1) | (1 if x else 0)
    code, dist = bch_correct_format(v)
    raw = code ^ 0x5412
    return EC_BITS[(raw >> 13) & 3], (raw >> 10) & 7, dist

def reserved_map(n, version):
    R = [[False]*n for _ in range(n)]
    def block(r0, r1, c0, c1):
        for r in range(r0, r1+1):
            for c in range(c0, c1+1):
                if 0 <= r < n and 0 <= c < n: R[r][c] = True
    block(0, 8, 0, 8)          # top-left finder + format
    block(0, 8, n-8, n-1)      # top-right finder + format
    block(n-8, n-1, 0, 8)      # bottom-left finder + format + dark module
    for i in range(n): R[6][i] = True; R[i][6] = True   # timing
    coords = ALIGN[version]
    for i, ar in enumerate(coords):
        for j, ac in enumerate(coords):
            if (i, j) in ((0, 0), (0, len(coords)-1), (len(coords)-1, 0)):
                continue
            block(ar-2, ar+2, ac-2, ac+2)
    return R

def read_codewords(M, version, mask):
    n = len(M)
    R = reserved_map(n, version)
    f = MASKS[mask]
    bits = []
    col = n - 1
    up = True
    while col > 0:
        if col == 6: col -= 1
        for i in range(n):
            r = (n-1-i) if up else i
            for c in (col, col-1):
                if not R[r][c]:
                    bit = M[r][c]
                    if f(r, c): bit = not bit          # unmask
                    bits.append(1 if bit else 0)
        col -= 2
        up = not up
    cw = []
    for i in range(0, len(bits) - 7, 8):
        v = 0
        for j in range(8): v = (v << 1) | bits[i+j]
        cw.append(v)
    return cw

def deinterleave(cw, spec):
    data_lens = [d for _, d in spec]
    blocks = [[] for _ in spec]
    i = 0
    for k in range(max(data_lens)):
        for b, dl in enumerate(data_lens):
            if k < dl:
                if i < len(cw): blocks[b].append(cw[i]); i += 1
    return b''.join(bytes(x) for x in blocks)

def parse_payload(data, version):
    bits = []
    for byte in data:
        for i in range(7, -1, -1): bits.append((byte >> i) & 1)
    pos = 0
    def take(k):
        nonlocal pos
        v = 0
        for _ in range(k):
            v = (v << 1) | (bits[pos] if pos < len(bits) else 0); pos += 1
        return v
    out = []
    while pos + 4 <= len(bits):
        mode = take(4)
        if mode == 0: break
        if mode == 4:                        # byte mode
            ln = take(8 if version < 10 else 16)
            raw = bytes(take(8) for _ in range(ln))
            for enc in ('utf-8', 'cp1251', 'latin-1'):
                try: out.append(raw.decode(enc)); break
                except UnicodeDecodeError: continue
        elif mode == 2:                      # alphanumeric
            AN = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
            ln = take(9 if version < 10 else 11)
            s = ''
            while ln >= 2:
                v = take(11); s += AN[v // 45] + AN[v % 45]; ln -= 2
            if ln: s += AN[take(6)]
            out.append(s)
        elif mode == 1:                      # numeric
            ln = take(10 if version < 10 else 12)
            s = ''
            while ln >= 3:
                s += str(take(10)).zfill(3); ln -= 3
            if ln == 2: s += str(take(7)).zfill(2)
            elif ln == 1: s += str(take(4))
            out.append(s)
        else:
            break
    return ''.join(out)

def decode(M):
    n = len(M)
    version = (n - 17) // 4
    if version not in BLOCKS:
        return None, f'unsupported version {version}'
    ec, mask, dist = read_format(M)
    cw = read_codewords(M, version, mask)
    spec = BLOCKS[version][ec]
    total = sum(t for t, _ in spec)
    if len(cw) < total:
        return None, f'expected {total} codewords, read {len(cw)}'
    data = deinterleave(cw[:total], spec)
    text = parse_payload(data, version)
    return text, f'v{version} {ec} mask{mask} fmt_dist={dist}'

def verify(text, M, ec, mask):
    """Re-encode and compare — proves the decode was right."""
    try:
        import qrcode
        from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
    except Exception as e:
        return None, 'qrcode unavailable: %s' % e
    lv = {'L': ERROR_CORRECT_L, 'M': ERROR_CORRECT_M, 'Q': ERROR_CORRECT_Q, 'H': ERROR_CORRECT_H}[ec]
    n = len(M)
    try:
        q = qrcode.QRCode(version=(n-17)//4, error_correction=lv, box_size=1, border=0,
                          mask_pattern=mask)
        q.add_data(text)
        q.make(fit=False)
        got = q.get_matrix()
    except Exception as e:
        return False, 're-encode failed: %s' % type(e).__name__
    if len(got) != n:
        return False, 'size mismatch %d vs %d' % (len(got), n)
    diff = sum(1 for r in range(n) for c in range(n) if bool(got[r][c]) != bool(M[r][c]))
    return diff == 0, '%d differing modules' % diff
