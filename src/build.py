# -*- coding: utf-8 -*-
"""Assemble the single-file study app from the extracted glossary, the hand-authored
A1/A2 content, and the generated grammar drills."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
OUT = os.path.join(BASE, os.pardir, "index.html")

import content as C
import drills as D

def optional(name):
    """Load a JSON data file if it is present, else return None.

    glossary.json and audio.json are derived from copyrighted textbooks and are NOT in the
    repository (see DATA.md). The build has to produce a working app without them, so a
    fresh clone gets the original decks and drills and simply omits the rest.
    """
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)

gloss = optional("glossary.json") or []

decks = []
def deck(did, name, sub, cards, on=False, prefix=None):
    p = prefix or did
    decks.append({"id": did, "name": name, "sub": sub, "on": on,
                  "cards": [dict(c, id=f"{p}-{i}") for i, c in enumerate(cards)]})

def W(ru, en, n=None, say=None):
    c = {"ru": ru, "en": en}
    if n:   c["n"] = n
    if say: c["say"] = say
    return c

# ---------------------------------------------------------------- alphabet
ALPHABET = [
 ("А а","ah","like a in father","а"),("Б б","beh","b as in boy","бэ"),
 ("В в","veh","v as in van","вэ"),("Г г","geh","g as in go","гэ"),
 ("Д д","deh","d as in do","дэ"),("Е е","yeh","ye as in yes","е"),
 ("Ё ё","yoh","yo as in yonder — always stressed","ё"),
 ("Ж ж","zheh","s as in measure; always hard","жэ"),
 ("З з","zeh","z as in zoo","зэ"),("И и","ee","ee as in see","и"),
 ("Й й","и краткое","y as in boy","й"),("К к","kah","k as in kit","ка"),
 ("Л л","ell","dark l, as in full","эль"),("М м","em","m as in map","эм"),
 ("Н н","en","n as in net","эн"),
 ("О о","oh","o as in more when stressed; like a when not","о"),
 ("П п","peh","p as in pet","пэ"),("Р р","err","rolled r","эр"),
 ("С с","ess","s as in sun","эс"),("Т т","teh","t as in top","тэ"),
 ("У у","oo","oo as in boot","у"),("Ф ф","eff","f as in fun","эф"),
 ("Х х","khah","ch as in Scottish loch","ха"),("Ц ц","tseh","ts as in cats","цэ"),
 ("Ч ч","cheh","ch as in chip; always soft","че"),
 ("Ш ш","shah","sh as in shut; always hard","ша"),
 ("Щ щ","shchah","a longer, softer sh","ща"),
 ("ъ","твёрдый знак","hard sign — a silent separator","твёрдый знак"),
 ("ы","ы","blunt i, tongue pulled back","ы"),
 ("ь","мягкий знак","soft sign — softens the letter before it","мягкий знак"),
 ("Э э","eh","e as in end","э"),("Ю ю","yoo","yu as in universe","ю"),
 ("Я я","yah","ya as in yard","я"),
]
deck("alphabet", "Алфави́т — the alphabet", "33 letters: name and sound",
     [W(l, f"{nm} — {snd}", say=say) for l, nm, snd, say in ALPHABET], on=True)

deck("pron", "Произноше́ние — pronunciation", "the rules that make Russian sound Russian",
     [W(rule, expl) for rule, expl in C.PRON], on=True)

deck("a1core", "Core words · A1",
     f"{len(C.CORE)} highest-frequency words, with gender and irregular forms",
     [W(ru, en, n or None) for ru, en, n in C.CORE], on=True)

deck("a1verbs", "Verbs & aspect pairs · A1–A2",
     f"{len(C.VERBS)} verbs with the conjugation forms you cannot guess",
     [W(ru, en, n) for ru, en, n in C.VERBS], on=True)

deck("phrases", "Фра́зы — things to actually say",
     f"{len(C.PHRASES)} survival phrases and everyday expressions",
     [W(ru, en) for ru, en in C.PHRASES], on=True)

deck("sentences", "Предложе́ния — sentences",
     f"{len(C.SENTENCES)} full sentences; also the dictation corpus",
     [W(ru, en) for ru, en in C.SENTENCES])

# ---------------------------------------------------------------- motion
MOTION = [
 ("идти́ / ходи́ть","to go on foot — one direction now / repeatedly, there and back"),
 ("е́хать / е́здить","to go by vehicle — one direction now / repeatedly"),
 ("лете́ть / лета́ть","to fly — one direction now / repeatedly"),
 ("плыть / пла́вать","to swim, sail — one direction now / repeatedly"),
 ("бежа́ть / бе́гать","to run — one direction now / repeatedly"),
 ("нести́ / носи́ть","to carry (on foot)"),("везти́ / вози́ть","to transport (by vehicle)"),
 ("вести́ / води́ть","to lead, take (someone)"),
 ("пойти́","to set off on foot (perfective)"),("пое́хать","to set off by vehicle (perfective)"),
 ("прийти́ / приезжа́ть","to arrive — при-"),("уйти́ / уезжа́ть","to leave, go away — у-"),
 ("войти́","to enter — в-"),("вы́йти","to go out — вы- (always stressed)"),
 ("подойти́","to approach — под- (+ к + dative)"),("отойти́","to move away — от-"),
 ("перейти́","to cross — пере- (+ че́рез + acc.)"),("дойти́","to reach — до- (+ до + gen.)"),
 ("зайти́","to drop in on the way — за-"),("пройти́","to go past, through — про-"),
 ("обойти́","to go around — об-"),
]
deck("motion", "Verbs of motion", "unidirectional vs multidirectional, and the prefixes",
     [W(r, e) for r, e in MOTION])

# ---------------------------------------------------------------- numbers
NUM = [
 ("оди́н, одна́, одно́","1 — agrees with its noun"),("два, две","2 — две with feminines"),
 ("три","3"),("четы́ре","4"),("пять","5"),("шесть","6"),("семь","7"),("во́семь","8"),
 ("де́вять","9"),("де́сять","10"),("оди́ннадцать","11"),("двена́дцать","12"),
 ("трина́дцать","13"),("четы́рнадцать","14"),("пятна́дцать","15"),("шестна́дцать","16"),
 ("семна́дцать","17"),("восемна́дцать","18"),("девятна́дцать","19"),("два́дцать","20"),
 ("три́дцать","30"),("со́рок","40"),("пятьдеся́т","50"),("шестьдеся́т","60"),
 ("се́мьдесят","70"),("во́семьдесят","80"),("девяно́сто","90"),("сто","100"),
 ("ты́сяча","1 000"),("миллио́н","1 000 000"),
 ("пе́рвый","first"),("второ́й","second"),("тре́тий","third — declines irregularly"),
 ("четвёртый","fourth"),("пя́тый","fifth"),
 ("понеде́льник","Monday — в понеде́льник"),("вто́рник","Tuesday"),("среда́","Wednesday — в сре́ду"),
 ("четве́рг","Thursday"),("пя́тница","Friday"),("суббо́та","Saturday"),("воскресе́нье","Sunday"),
 ("янва́рь","January — в январе́"),("февра́ль","February"),("март","March"),("апре́ль","April"),
 ("май","May"),("ию́нь","June"),("ию́ль","July"),("а́вгуст","August"),("сентя́брь","September"),
 ("октя́брь","October"),("ноя́брь","November"),("дека́брь","December"),
 ("зимо́й","in winter"),("весно́й","in spring"),("ле́том","in summer"),("о́сенью","in autumn"),
 ("у́тром","in the morning"),("днём","in the afternoon"),("ве́чером","in the evening"),
 ("но́чью","at night"),
 ("1, 21, 31 + noun","nominative SINGULAR: два́дцать оди́н год"),
 ("2, 3, 4 + noun","genitive SINGULAR: два часа́, три кни́ги"),
 ("5–20 + noun","genitive PLURAL: пять часо́в, оди́ннадцать книг"),
 ("11–14","always genitive plural, even though 1–4 are not"),
 ("Кото́рый час?","What time is it? — Сейча́с два часа́."),
 ("Ско́лько вам лет?","How old are you? — dative + год / го́да / лет"),
]
deck("numbers", "Numbers, days, months, time", "counting, dates and the agreement rules",
     [W(r, e) for r, e in NUM])

# ---------------------------------------------------------------- grammar
GRAM = [
 ("Имени́тельный (1) — Nominative","кто? что? — the subject, and the dictionary form"),
 ("Роди́тельный (2) — Genitive","кого? чего? — possession, absence, quantity; after без, для, до, из, от, о́коло, по́сле, у"),
 ("Да́тельный (3) — Dative","кому? чему? — the indirect object; after к, по; with на́до, нра́виться, age"),
 ("Вини́тельный (4) — Accusative","кого? что? — the direct object; direction after в/на; duration"),
 ("Твори́тельный (5) — Instrumental","кем? чем? — the means; after с, над, под, ме́жду, за, пе́ред"),
 ("Предло́жный (6) — Prepositional","о ком? о чём? где? — only ever after a preposition"),
 ("Noun endings — Genitive sg.","m. -а/-я · f. -ы/-и · n. -а/-я · f. in -ь → -и"),
 ("Noun endings — Dative sg.","m. -у/-ю · f. -е (-ии after -ия) · n. -у/-ю"),
 ("Noun endings — Accusative sg.","m. inanimate = nom., animate = gen. · f. -у/-ю · n. = nom."),
 ("Noun endings — Instrumental sg.","m. -ом/-ем · f. -ой/-ей · n. -ом/-ем · f. in -ь → -ью"),
 ("Noun endings — Prepositional sg.","-е for most · -ии for nouns in -ия/-ие · f. in -ь → -и"),
 ("Noun endings — plural","Nom -ы/-и (n. -а/-я) · Dat -ам/-ям · Instr -ами/-ями · Prep -ах/-ях"),
 ("Genitive plural","m. -ов/-ев/-ей · f. and n. usually a zero ending: книг, слов"),
 ("Adjective — Nominative","-ый/-о́й (m.) · -ая (f.) · -ое (n.) · -ые (pl.)"),
 ("Adjective — Genitive","-ого (m./n.) · -ой (f.) · -ых (pl.) — -ого is said [-ово]"),
 ("Adjective — Dative","-ому (m./n.) · -ой (f.) · -ым (pl.)"),
 ("Adjective — Accusative","f. -ую; m./n./pl. copy the nominative or the genitive by animacy"),
 ("Adjective — Instrumental","-ым (m./n.) · -ой (f.) · -ыми (pl.)"),
 ("Adjective — Prepositional","-ом (m./n.) · -ой (f.) · -ых (pl.)"),
 ("1st conjugation","-ю/-у, -ешь, -ет, -ем, -ете, -ют/-ут — чита́ю, чита́ешь…"),
 ("2nd conjugation","-ю/-у, -ишь, -ит, -им, -ите, -ят/-ат — говорю́, говори́шь…"),
 ("Which conjugation?","the ты-form tells you: -ешь/-ёшь = 1st, -ишь = 2nd"),
 ("Past tense","drop -ть, add -л / -ла / -ло / -ли — agrees with GENDER, not person"),
 ("Future — imperfective","бу́ду/бу́дешь/бу́дет… + infinitive: я бу́ду чита́ть"),
 ("Future — perfective","the perfective present-tense form IS the future: я прочита́ю"),
 ("Imperfective aspect","process, repetition, or the plain fact of the action"),
 ("Perfective aspect","a single completed action with a result — and no present tense"),
 ("Imperative","-и(те) / -й(те) / -ь(те): чита́йте, скажи́те, гото́вь"),
 ("Negative imperative","almost always imperfective: не открыва́йте"),
 ("У меня́ есть…","'I have' — у + genitive of the owner, the thing in the nominative"),
 ("У меня́ нет…","absence takes the genitive: у меня́ нет вре́мени"),
 ("Personal pronouns — Gen/Acc","меня́, тебя́, его́, её, нас, вас, их"),
 ("Personal pronouns — Dative","мне, тебе́, ему́, ей, нам, вам, им"),
 ("Personal pronouns — Instrumental","мной, тобо́й, им, ей, на́ми, ва́ми, и́ми"),
 ("Personal pronouns — Prepositional","обо мне́, о тебе́, о нём, о ней, о нас, о вас, о них"),
 ("The н- rule","after a preposition, он/она́/они́ add н-: у него́, к ней, с ни́ми"),
 ("кото́рый","GENDER from the noun it describes, CASE from its own clause"),
 ("что́бы","+ infinitive if the subject is the same, + past tense if it changes"),
 ("Comparative","-ее: но́вый → нове́е · or бо́лее + adjective · 'than' = чем, or the genitive"),
 ("Superlative","са́мый + adjective: са́мый большо́й"),
 ("Verbs in -ова-/-ева-","the suffix becomes -у- in the present: сове́товать → сове́тую"),
 ("Animacy","for animate masculines the accusative copies the genitive"),
 ("Spelling rule 7","after г к х ж ч ш щ write И, never Ы"),
 ("Spelling rule 5","after ж ч ш щ ц write О only under stress, otherwise Е"),
 ("Spelling rule — я/ю","after ж ч ш щ write А and У, never Я or Ю"),
 ("Double negative","required: я никогда́ ничего́ не говорю́"),
]
deck("grammar", "Grammar patterns", "cases, endings, aspect, conjugation, pronouns",
     [W(r, e) for r, e in GRAM])

# ---------------------------------------------------------------- B2 themes
THEMES = {
 1:("Образова́ние и 21 век","Education and the 21st century"),
 2:("Рабо́та и жизнь","Work and life"),
 3:("Свобо́дное вре́мя","Leisure and lifestyle"),
 4:("Семья́","Family and relationships"),
 5:("Го́род и дере́вня","City, suburb and countryside"),
 6:("Молодёжь и о́бщество","Youth and society"),
 7:("Здоро́вье","Health and habits"),
 8:("Поли́тика и о́бщество","Politics and society"),
 9:("Эконо́мика","Economy and money"),
 10:("Глоба́льные пробле́мы","Russia and global issues"),
}
# Only built when the local glossary is present; skipped entirely otherwise.
for ch, (nm, sub) in THEMES.items():
    cs = [c for c in gloss if ch in c["ch"]]
    if not cs:
        continue
    cards = [{k: v for k, v in (("ru", c["ru"]), ("en", c["en"]), ("g", c.get("g"))) if v}
             for c in cs]
    deck(f"b2-{ch}", f"{ch}. {nm}", f"{sub} · B2 · {len(cards)} words", cards, prefix=f"b{ch}")

misc = [c for c in gloss if not c["ch"]]
if misc:
    deck("b2-misc", "Idioms & set phrases", "expressions with no chapter number · B2",
         [{"ru": c["ru"], "en": c["en"]} for c in misc], prefix="bm")

# ---------------------------------------------------------------- assemble
drill_items = D.build()
word_order = [{"id": f"wo-{i}", "ru": s, "en": e, "why": w}
              for i, (s, e, w) in enumerate(C.WORDORDER)]
# Workbook audio: decoded from the QR codes in «Россия — моя любовь: Рабочая тетрадь».
audio = optional("audio.json") or []

total = sum(len(d["cards"]) for d in decks)
print(f"decks {len(decks)} · vocabulary cards {total} · drills {len(drill_items)} "
      f"· word-order {len(word_order)} · workbook audio {len(audio)}")
if not gloss:
    print("  note: glossary.json absent — the 10 B2 theme decks were skipped (see DATA.md)")
if not audio:
    print("  note: audio.json absent — the Audio tab is hidden (see DATA.md)")
for d in decks:
    print(f"  {d['id']:<10} {len(d['cards']):>4}  {'on ' if d['on'] else '   '}{d['name']}")

J = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
html = (open(os.path.join(BASE, "app_template.html"), encoding="utf-8").read()
        .replace("__DATA__", J({"decks": decks}))
        .replace("__DRILLS__", J(drill_items))
        .replace("__DCATS__", J(D.CATS))
        .replace("__WORDORDER__", J(word_order))
        .replace("__AUDIO__", J(audio))
        .replace("__GUIDE__", open(os.path.join(BASE, "guide.html"), encoding="utf-8").read())
        .replace("__TOTAL__", str(total)))
open(OUT, "w", encoding="utf-8").write(html)
print(f"wrote {os.path.abspath(OUT)} ({len(html)/1024:.0f} KB)")
