"""Extract + repair the Russian-English glossary from Kagan/Kudyma/Miller,
'Russian: From Intermediate to Advanced' (Routledge 2015), pp.419-448.

The PDF text layer is an OCR of italic serif type, so Latin letters were widely
misread as Cyrillic homoglyphs (m->т, n->п, b->Ь, bl->Ы...). Stress marks on the
Russian side survived as UPPERCASE vowels. Many entries carry Russian sub-senses
inside the English field, so the field is cleaned run-by-run, not wholesale.
"""
import re, sys, json
sys.stdout.reconfigure(encoding="utf-8")

import os
BASE = os.path.dirname(os.path.abspath(__file__))
# pdftotext -layout dump of 'Russian: From Intermediate to Advanced'
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "d1_layout.txt")
START, END = 25897, 27397          # glossary line range in that dump

lines = open(SRC, encoding="utf-8").read().split("\n")[START - 1:END]
DROP = re.compile(r"^\s*$|РУССКО-АНГЛИЙСКИЙ СЛОВАРЬ|^\s*1?\d{3}\s*$"
                  r"|The English equivalents are given|textbook\. For other meanings")
lines = [l.strip() for l in lines if not DROP.search(l)]
# Cyrillic З is routinely OCR'd for the chapter digit 3
lines = [re.sub(r"(?<=\s)З(?=\s*[-–])", "3", l) for l in lines]

SEP = re.compile(r"\s+(?:(?P<ch>\d+(?:\s*,\s*\d+)*)\s*[-–]\s*|[-–]\s+)")
DEF_RU = re.compile(r"[бвджзйклмнфцчшщъэюяёБГДЖЗЙЛПФЦЧШЩЪЫЭЮЯ]")
RU_TOK = re.compile(r"[А-Яа-яЁё\u0301().,?!/«»\-\d+]+$")
LABELS = {"f", "f.", "m.", "m", "impf", "pfv.", "pl.", "sing.", "т.", "р/.", "/"}

# --- stitch wrapped continuation lines --------------------------------------
raw = []
for s in lines:
    if SEP.search(s) and re.match(r"^[А-ЯЁа-яёf/]", s):
        raw.append(s)
    elif raw:
        raw[-1] += " " + s
    else:
        raw.append(s)

# --- split lines that hold two entries --------------------------------------
def depth_ok(line, pos):
    seg = line[:pos]
    return seg.count("(") <= seg.count(")")

def find_head(line, lo, hi):
    best, seen = None, False
    for t in reversed(list(re.finditer(r"\S+", line[lo:hi]))):
        w = t.group()
        if RU_TOK.match(w) or w in LABELS:
            if DEF_RU.search(w):
                seen = True
            best = lo + t.start()
        else:
            break
    return best if seen else None

def split_entries(line):
    seps = [m for m in SEP.finditer(line) if depth_ok(line, m.start())]
    if len(seps) < 2:
        return [line]
    out, start = [], 0
    for prev, cur in zip(seps, seps[1:]):
        hs = find_head(line, prev.end(), cur.start())
        if hs is None:
            continue
        if line[:hs].rstrip().endswith((";", ",", ":")):   # sub-sense, not a new entry
            continue
        out.append(line[start:hs].strip())
        start = hs
    out.append(line[start:].strip())
    return [o for o in out if o]

entries = [e for l in raw for e in split_entries(l)]

# --- cleaners ---------------------------------------------------------------
CYR2LAT = str.maketrans({
    "а": "a", "е": "e", "о": "o", "с": "c", "р": "p", "у": "y", "х": "x",
    "п": "n", "т": "m", "и": "u", "г": "r", "ѕ": "s", "ј": "j", "і": "i",
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O",
    "Р": "P", "С": "C", "Т": "T", "У": "Y", "Х": "X", "Ј": "J", "І": "I",
    "Ь": "b", "ь": "b", "З": "3",
})
EN_FIXES = [
    (r"\bJl(u)\b", r"fl\1"), (r"bllity\b", "bility"),
    (r"\bhabl(t|ts)\b", r"habi\1"), (r"\bblrd(s?)\b", r"bird\1"),
    (r"\bamblvalent\b", "ambivalent"), (r"\bublquitous\b", "ubiquitous"),
    (r"\binhabltants\b", "inhabitants"), (r"\bexhiblt\b", "exhibit"),
    # NB: no \b before '/', there is no word boundary between a space and a slash
    (r"\bon/y\b", "only"), (r"/oca/", "local"), (r"/ocal\b", "local"),
    (r"/aw(s?)\b", r"law\1"), (r"/ay\b", "lay"), (r"/oan\b", "loan"),
    (r"/ife\b", "life"), (r"/imit", "limit"), (r"/iterally\b", "literally"),
    (r"/eisure\b", "leisure"), (r"/ike\b", "like"), (r"/ine\b", "line"),
    # 'i' misread as 'l' in italic
    (r"plumblng", "plumbing"), (r"unamblguous", "unambiguous"),
    (r"deblt", "debit"), (r"combln", "combin"), (r"prohibltion", "prohibition"),
    (r"inhabltants", "inhabitants"),
    # dropped spaces after short function words
    (r"Presidentjfor", "President / for"),
    (r"\boffuel\b", "of fuel"), (r"\boffact\b", "of fact"),
    (r"\bof(?!f)(?!ten\b)(?=[a-z]{2,})", "of "), (r"\bof(?=[A-Z])", "of "),
    (r"(?<=[a-z]),(?=[a-z])", ", "), (r"(?<=[a-z]);(?=[a-z])", "; "),
    (r"\bmonkjnun\b", "monk/nun"), (r"\bfightfor\b", "fight for"),
    (r"\boffairness\b", "of fairness"), (r"\bBecome\b", "become"),
    (r"\bcourtjto\b", "court / to"), (r"\bupsetfor\b", "upset for"),
    (r"\bafterfinishing\b", "after finishing"), (r"\btoform\b", "to form"),
    (r"\bwayfor\b", "way for"), (r"\babouta\b", "about a"),
    (r"\bandfuture\b", "and future"), (r"\bofgovernment\b", "of government"),
    (r"\bofthe\b", "of the"), (r"\bofa\b", "of a"), (r"\bofmind\b", "of mind"),
    (r"\bina\b", "in a"), (r"\boften\b(?= stone)", "of ten"),
]
def clean_en(s):
    s = s.replace("Ы", "bl").replace("ы", "bl").translate(CYR2LAT)
    s = s.replace("}", ")").replace("{", "(")
    for bad, good in EN_FIXES:
        s = re.sub(bad, good, s)
    return re.sub(r"\s+", " ", s)

ST = "\u0301"
VOW = "аеиоуыэюяёАЕИОУЫЭЮЯЁ"
UP2LOW = {"А": "а", "Е": "е", "И": "и", "О": "о", "У": "у",
          "Ы": "ы", "Э": "э", "Ю": "ю", "Я": "я"}

def clean_ru(s, first_of_section=False):
    s = re.sub(r"l([" + VOW + r"])l", r"\1", s)
    s = s.replace("ьi", "ы" + ST)
    for bad, good in [("siпg.", "sing."), ("оп/у", "only"), ("р/.", "pl."),
                      ("рl.", "pl."), ("iтpf", "impf"), ("рfv.", "pfv."),
                      ("апd", "and"), ("gеп.", "gen.")]:
        s = s.replace(bad, good)
    out = []
    for i, ch in enumerate(s):
        if ch in UP2LOW and i > 0 and (s[i - 1].isalpha() or s[i - 1] == ST):
            out.append(UP2LOW[ch] + ST)
        else:
            out.append(ch)
    s = "".join(out)
    if first_of_section and s[:1].isupper():
        s = s[0].lower() + s[1:]
    return re.sub(r"\s+", " ", s).strip()

# --- mixed-script field cleaning -------------------------------------------
HOMO = set("аеосрухптигьыАВЕКМНОРСТУХЗЬЫ")
LATIN = re.compile(r"[A-Za-z]")
CYR = re.compile(r"[А-Яа-яЁё]")

def tok_class(w):
    if LATIN.search(w):
        return "EN"
    cy = [c for c in w if CYR.match(c)]
    if not cy:
        return "AMB"
    return "RU" if any(c not in HOMO for c in cy) else "AMB"

def clean_mixed(s):
    toks = s.split(" ")
    cls = [tok_class(t) for t in toks]
    # ambiguous tokens join the nearest decided neighbour, preferring the right
    for i, c in enumerate(cls):
        if c != "AMB":
            continue
        nxt = next((j for j in range(i + 1, len(cls)) if cls[j] != "AMB"), None)
        prv = next((j for j in range(i - 1, -1, -1) if cls[j] != "AMB"), None)
        if nxt is not None and prv is not None:
            cls[i] = cls[nxt] if (nxt - i) <= (i - prv) else cls[prv]
        elif nxt is not None:
            cls[i] = cls[nxt]
        elif prv is not None:
            cls[i] = cls[prv]
        else:
            cls[i] = "EN"
    parts, buf, cur = [], [], cls[0]
    for t, c in zip(toks, cls):
        if c != cur:
            parts.append((cur, " ".join(buf))); buf, cur = [], c
        buf.append(t)
    parts.append((cur, " ".join(buf)))
    out = " ".join((clean_en(txt) if c == "EN" else clean_ru(txt)) for c, txt in parts)
    out = re.sub(r"\s+(\d+(?:,\s*\d+)*)\s*[-–]\s*", " — ", out)   # inner chapter refs
    out = re.sub(r"\s+[-–]\s+", " — ", out)                       # inner sub-sense dash
    return re.sub(r"\s+", " ", out).strip(" ;,")

# Source-side OCR errors on the Russian headword (и misread as о, н as п).
# Each was confirmed against the English gloss and the chapter's theme.
RU_TYPOS = {
    "нотка": "ни́тка",                              # ch3, glossed 'thread'
    "отлов": "отли́в",                              # ch10, glossed 'low tide'
    "палочные (деньги)": "нали́чные (деньги)",      # ch9, glossed 'cash'
    "мотов (преступления)": "моти́в (преступления)",# ch6, glossed 'motive'
    "ободный": "оби́дный",                          # ch9, glossed 'offensive, hurtful'
}

def split_gender(head):
    g = ""
    m = re.match(r"^(f|m\.|т\.)\s+(.*)$", head)
    if m:
        g, head = ("f." if m.group(1) == "f" else "m."), m.group(2)
    head, n = re.subn(r"\s*\bf\b\.?\s*$", "", head)
    if n: g = "f."
    head, n = re.subn(r"(?<=ь)\s*/(?=\s|$)", "", head)
    if n: g = "f."
    head, n = re.subn(r"(?<=ь)f\s*$", "", head)
    if n: g = "f."
    head = re.sub(r"\s*\bm\.\s*$", "", head)
    return head.strip(), g

# --- parse ------------------------------------------------------------------
cards, bad = [], []
prev_letter = None
for e in entries:
    e = re.sub(r"\s+", " ", e).strip()
    e = re.sub(r"\s*Выражения\s*$", "", e)          # trailing section heading
    m = SEP.search(e)
    if not m or m.start() == 0:
        bad.append(e); continue
    head_raw, en_raw = e[:m.start()].strip(), e[m.end():].strip()
    head_raw, gender = split_gender(head_raw)
    first = head_raw[:1].isupper() and head_raw[:1].upper() != prev_letter
    if head_raw[:1].isupper():
        prev_letter = head_raw[:1].upper()
    ru, en = clean_ru(head_raw, first), clean_mixed(en_raw)
    ru = RU_TYPOS.get(ru, ru)
    chs = sorted({int(x) for x in re.findall(r"\d+", m.group("ch") or "")})
    if not ru or not en or not CYR.search(ru):
        bad.append(e); continue
    c = {"ru": ru, "en": en, "ch": chs}
    if gender: c["g"] = gender
    cards.append(c)

print(f"entries={len(entries)} parsed={len(cards)} unparsed={len(bad)}")
odd = [c for c in cards if CYR.search(c["en"])]
print(f"entries whose translation contains Russian (sub-senses) = {len(odd)}")
for c in odd[:30]:
    print(f"   {c['ru']}  ||  {c['en']}")
print(f"no-chapter={sum(1 for c in cards if not c['ch'])}")
from collections import Counter
print("per-chapter:", sorted(Counter(ch for c in cards for ch in c["ch"]).items()))
json.dump(cards, open(os.path.join(BASE, "glossary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
