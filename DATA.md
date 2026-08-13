# Where the content comes from

This repository holds a study app and the material I wrote for it. It deliberately does
**not** hold two data files that my local copy uses, because they are derived from
commercial products I do not own the rights to redistribute.

## What is in the repository

All of it is original work, written for this project, and covered by the MIT licence:

| Source | What it is |
|---|---|
| `src/content.py` | ~206 core words with gender and irregular forms, 67 verbs with conjugations, 88 phrases, 55 sentences, 22 pronunciation cards, 30 word-order exercises |
| `src/drills.py`, `src/drills_extra.py` | 470 grammar drill items across 17 topics, generated from full stress-marked paradigms written out in these files |
| `src/guide.html` | The grammar reference and study plan |
| `src/app_template.html` | The app itself — scheduler, four practice modes, drills, builder |
| `src/build.py` | Assembles everything into a single `index.html` |

The word list was chosen using a frequency count of elementary textbooks, and the verb list
follows the lesson sequence of a published syllabus. Neither a frequency ranking nor a list
of which verbs a course teaches is itself copyrightable; the definitions, example sentences,
paradigms and explanations here are all written from scratch.

## What is not in the repository, and why

**`src/glossary.json`** — 1,270 Russian–English pairs extracted from the glossary printed at
the back of Kagan, Kudyma & Miller, *Russian: From Intermediate to Advanced* (Routledge,
2015), pp. 419–448. A selected, ordered, translated word list of that size is a protected
compilation. Publishing it would be redistributing a chunk of a book that is still on sale.

**`src/audio.json`** — 45 URLs to audio files hosted by the МГУ Russian language centre,
recovered by decoding the QR codes printed in *Россия — моя любовь: Рабочая тетрадь*. Those
codes are in the workbook because you bought the workbook. Publishing the links hands out
free access to something the publisher sells.

`index.html` is gitignored for the same reason: the built file embeds both.

## Building without them

`python src/build.py` works with either file absent. It prints a note, skips the ten B2
theme decks, and removes the Audio tab. What you get is the full A1–A2 course, all 470
grammar drills and the sentence builder — a complete app, just without the advanced
vocabulary and the workbook recordings.

## Regenerating them, if you own the books

`src/extract_glossary.py` parses the Routledge glossary out of a `pdftotext -layout` dump.
`src/qrgrid.py`, `src/qrraster.py` and `src/qrdecode.py` locate and decode the workbook's QR
codes — they are drawn images with no embedded links, so they have to be read off the page.
Both scripts need your own copy of the book as input; neither is much use without one.
