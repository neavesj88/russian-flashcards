# Русский — a single-file Russian study app

One self-contained HTML file: spaced-repetition vocabulary, four practice modes, 470
grammar drills, a sentence builder, and a written grammar reference. No install, no build
step to use it, no accounts, no analytics, no network — open the file and study.

Built for my own use working through a shelf of Russian textbooks, and published because
the grammar drills and the A1 material took long enough to write that someone else may as
well benefit.

![no dependencies](https://img.shields.io/badge/dependencies-none-informational)
![licence MIT](https://img.shields.io/badge/licence-MIT-informational)

## Use it

Download `index.html` (build it first — see below) and open it in any browser. That's it.

On a phone, put the file in a cloud drive or email it to yourself, open it in the browser
and **Add to Home Screen**. Two things make this usable on mobile without installing
anything:

- **A built-in ЙЦУКЕН keyboard.** All 33 Cyrillic letters, space, backspace and clear. On a
  touch screen the app sets `inputmode="none"` so your phone's keyboard doesn't fight it for
  space; the **⌨** key switches to your own keyboard if you have a Russian layout.
- **No language pack required.** Speech is optional. If no Russian voice is installed the
  app says so and tells you where to enable one, rather than going silent.

## Build it

Python 3 only. No package manager, no lockfile, nothing to install.

```bash
git clone https://github.com/neavesj88/russian-flashcards.git
cd russian-flashcards
python src/build.py
```

That writes `index.html`. To check the result:

```bash
python src/verify.py
```

`verify.py` syntax-checks the inline JavaScript with `node --check`, scans for duplicate
element ids, and computes WCAG contrast ratios from the CSS variables in both themes. Node
is optional — everything else runs without it.

## What you get

| Deck | Cards |
|---|---|
| Алфавит — the alphabet | 33 |
| Произношение — pronunciation rules | 22 |
| Core words · A1 (gender, irregular plurals) | 206 |
| Verbs & aspect pairs, with conjugations | 67 |
| Фразы — survival phrases | 88 |
| Предложения — full sentences | 55 |
| Verbs of motion | 21 |
| Numbers, days, months, time | 68 |
| Grammar patterns | 46 |

Plus **470 grammar drills** over 17 topics — pronunciation, conjugation, the six cases,
adjective agreement, plurals, preposition government, aspect, verbs of motion, number
agreement, dative constructions, в/на/о, gender, spelling rules, past tense, `который`, the
instrumental — and **30 sentence-building exercises**.

Every drill paradigm is written out in full and stress-marked in `src/drills.py` and
`src/drills_extra.py`. Distractors are always other real forms of the same word, so a wrong
answer is diagnostic rather than a guess. Wrong answers explain the rule and print the whole
paradigm.

> My own copy also carries 1,270 advanced words and 45 native-speaker recordings. Those are
> derived from books still on sale and are **not** in this repository — see
> [DATA.md](DATA.md). The build skips them cleanly if absent, which is what a fresh clone
> gets.

## Practice modes

- **Cards** — self-graded, for new material.
- **Choice** — four options, distractors drawn from the same deck. Right counts as Good;
  wrong resets the card and requeues it.
- **Type** — produce the Russian. Stress marks, capitals and ё/е are ignored; a one-letter
  slip is flagged as a near-miss rather than marked wrong.
- **Listen** — dictation from the speech voice.

Scheduling is a five-box Leitner system at 1 → 3 → 7 → 21 → 60 days. Keyboard: `1`–`4`
pick, `space` reveals or continues, `Enter` submits, `r` repeats audio.

## Layout

```
index.html          the built app (generated; not committed)
src/build.py        assembles everything into index.html
src/verify.py       syntax, duplicate-id and contrast checks
src/app_template.html   the app — scheduler, modes, drills, builder
src/content.py      A1/A2 words, verbs, phrases, sentences, pronunciation
src/drills.py       drill generator + verb/noun/preposition paradigms
src/drills_extra.py adjective paradigms + authored drill items
src/guide.html      the in-app grammar reference
src/extract_glossary.py   parses a textbook glossary (needs your own copy)
src/qr*.py          reads QR codes off a workbook page (needs your own copy)
```

## Notes

Progress lives in `localStorage`, so it is per-device — use *Progress → Export / Import* to
move it. Some mobile browsers block storage for pages opened straight from a file; the app
detects that and warns rather than silently losing your reviews. Serving over http fixes it:

```bash
python -m http.server 8000
```

## Licence

MIT — see [LICENSE](LICENSE). Covers the code and the study material I wrote, not the
third-party data described in [DATA.md](DATA.md).
