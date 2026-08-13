# -*- coding: utf-8 -*-
"""Grammar drill generator.

Every paradigm below is written out in full and stress-marked, and the multiple-choice
distractors are drawn from *the same paradigm* — so a wrong answer is always a real
Russian form, which is what makes the exercise diagnostic rather than a guessing game.
"""
import json, os, random, sys, zlib
sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import drills_extra as X

PERSONS = ["я", "ты", "он/она́", "мы", "вы", "они́"]

# ---------------------------------------------------------------- verbs
# infinitive, gloss, conjugation class note, 6 present-tense forms
VERBS = [
 ("чита́ть","to read","1st, regular -ать",["чита́ю","чита́ешь","чита́ет","чита́ем","чита́ете","чита́ют"]),
 ("рабо́тать","to work","1st, regular -ать",["рабо́таю","рабо́таешь","рабо́тает","рабо́таем","рабо́таете","рабо́тают"]),
 ("знать","to know","1st, regular -ать",["зна́ю","зна́ешь","зна́ет","зна́ем","зна́ете","зна́ют"]),
 ("де́лать","to do, make","1st, regular -ать",["де́лаю","де́лаешь","де́лает","де́лаем","де́лаете","де́лают"]),
 ("слу́шать","to listen","1st, regular -ать",["слу́шаю","слу́шаешь","слу́шает","слу́шаем","слу́шаете","слу́шают"]),
 ("покупа́ть","to buy","1st, regular -ать",["покупа́ю","покупа́ешь","покупа́ет","покупа́ем","покупа́ете","покупа́ют"]),
 ("понима́ть","to understand","1st, regular -ать",["понима́ю","понима́ешь","понима́ет","понима́ем","понима́ете","понима́ют"]),
 ("писа́ть","to write","1st, с→ш throughout",["пишу́","пи́шешь","пи́шет","пи́шем","пи́шете","пи́шут"]),
 ("иска́ть","to look for","1st, ск→щ throughout",["ищу́","и́щешь","и́щет","и́щем","и́щете","и́щут"]),
 ("сказа́ть","to say (pf.)","1st, з→ж throughout",["скажу́","ска́жешь","ска́жет","ска́жем","ска́жете","ска́жут"]),
 ("жить","to live","1st, stem жив-",["живу́","живёшь","живёт","живём","живёте","живу́т"]),
 ("идти́","to go on foot","1st, stem ид-",["иду́","идёшь","идёт","идём","идёте","иду́т"]),
 ("е́хать","to go by vehicle","1st, stem ед-",["е́ду","е́дешь","е́дет","е́дем","е́дете","е́дут"]),
 ("ждать","to wait","1st, stem жд-",["жду","ждёшь","ждёт","ждём","ждёте","ждут"]),
 ("брать","to take","1st, stem бер-",["беру́","берёшь","берёт","берём","берёте","беру́т"]),
 ("пить","to drink","1st, stem пь-",["пью","пьёшь","пьёт","пьём","пьёте","пьют"]),
 ("петь","to sing","1st, stem по-",["пою́","поёшь","поёт","поём","поёте","пою́т"]),
 ("дава́ть","to give","1st, -ва- drops",["даю́","даёшь","даёт","даём","даёте","даю́т"]),
 ("встава́ть","to get up","1st, -ва- drops",["встаю́","встаёшь","встаёт","встаём","встаёте","встаю́т"]),
 ("сове́товать","to advise","1st, -ова- → -у-",["сове́тую","сове́туешь","сове́тует","сове́туем","сове́туете","сове́туют"]),
 ("говори́ть","to speak","2nd, regular",["говорю́","говори́шь","говори́т","говори́м","говори́те","говоря́т"]),
 ("учи́ть","to learn, teach","2nd, regular",["учу́","у́чишь","у́чит","у́чим","у́чите","у́чат"]),
 ("стро́ить","to build","2nd, regular",["стро́ю","стро́ишь","стро́ит","стро́им","стро́ите","стро́ят"]),
 ("люби́ть","to love","2nd, б→бл in я-form only",["люблю́","лю́бишь","лю́бит","лю́бим","лю́бите","лю́бят"]),
 ("купи́ть","to buy (pf.)","2nd, п→пл in я-form only",["куплю́","ку́пишь","ку́пит","ку́пим","ку́пите","ку́пят"]),
 ("гото́вить","to cook","2nd, в→вл in я-form only",["гото́влю","гото́вишь","гото́вит","гото́вим","гото́вите","гото́вят"]),
 ("ви́деть","to see","2nd, д→ж in я-form only",["ви́жу","ви́дишь","ви́дит","ви́дим","ви́дите","ви́дят"]),
 ("сиде́ть","to sit","2nd, д→ж in я-form only",["сижу́","сиди́шь","сиди́т","сиди́м","сиди́те","сидя́т"]),
 ("ходи́ть","to go (repeatedly)","2nd, д→ж in я-form only",["хожу́","хо́дишь","хо́дит","хо́дим","хо́дите","хо́дят"]),
 ("е́здить","to go by vehicle (repeatedly)","2nd, д→ж in я-form only",["е́зжу","е́здишь","е́здит","е́здим","е́здите","е́здят"]),
 ("смотре́ть","to watch","2nd, stress shifts after я-form",["смотрю́","смо́тришь","смо́трит","смо́трим","смо́трите","смо́трят"]),
 ("спать","to sleep","2nd, п→пл in я-form only",["сплю","спишь","спит","спим","спи́те","спят"]),
 ("хоте́ть","to want","irregular: 1st conj. in sg., 2nd in pl.",["хочу́","хо́чешь","хо́чет","хоти́м","хоти́те","хотя́т"]),
 ("мочь","to be able","irregular, г/ж alternation",["могу́","мо́жешь","мо́жет","мо́жем","мо́жете","мо́гут"]),
 ("есть","to eat","irregular",["ем","ешь","ест","еди́м","еди́те","едя́т"]),
]

# ---------------------------------------------------------------- nouns
CASES = ["Nominative","Genitive","Dative","Accusative","Instrumental","Prepositional"]
# lemma, gloss, gender/type, 6 singular forms
NOUNS = [
 ("кни́га","book","f. -а",["кни́га","кни́ги","кни́ге","кни́гу","кни́гой","кни́ге"]),
 ("маши́на","car","f. -а",["маши́на","маши́ны","маши́не","маши́ну","маши́ной","маши́не"]),
 ("сестра́","sister","f. -а, end-stressed",["сестра́","сестры́","сестре́","сестру́","сестро́й","сестре́"]),
 ("Москва́","Moscow","f. -а, end-stressed",["Москва́","Москвы́","Москве́","Москву́","Москво́й","Москве́"]),
 ("у́лица","street","f. -а after ц → -ей",["у́лица","у́лицы","у́лице","у́лицу","у́лицей","у́лице"]),
 ("Росси́я","Russia","f. -ия → -ии",["Росси́я","Росси́и","Росси́и","Росси́ю","Росси́ей","Росси́и"]),
 ("тетра́дь","notebook","f. -ь",["тетра́дь","тетра́ди","тетра́ди","тетра́дь","тетра́дью","тетра́ди"]),
 ("пло́щадь","square","f. -ь",["пло́щадь","пло́щади","пло́щади","пло́щадь","пло́щадью","пло́щади"]),
 ("студе́нт","student","m. animate",["студе́нт","студе́нта","студе́нту","студе́нта","студе́нтом","студе́нте"]),
 ("брат","brother","m. animate",["брат","бра́та","бра́ту","бра́та","бра́том","бра́те"]),
 ("го́род","city","m. inanimate",["го́род","го́рода","го́роду","го́род","го́родом","го́роде"]),
 ("музе́й","museum","m. -й",["музе́й","музе́я","музе́ю","музе́й","музе́ем","музе́е"]),
 ("слова́рь","dictionary","m. -ь, end-stressed",["слова́рь","словаря́","словарю́","слова́рь","словарём","словаре́"]),
 ("преподава́тель","teacher","m. -ь animate",["преподава́тель","преподава́теля","преподава́телю","преподава́теля","преподава́телем","преподава́теле"]),
 ("письмо́","letter","n. -о, end-stressed",["письмо́","письма́","письму́","письмо́","письмо́м","письме́"]),
 ("окно́","window","n. -о, end-stressed",["окно́","окна́","окну́","окно́","окно́м","окне́"]),
 ("сло́во","word","n. -о",["сло́во","сло́ва","сло́ву","сло́во","сло́вом","сло́ве"]),
 ("общежи́тие","dormitory","n. -ие → -ии",["общежи́тие","общежи́тия","общежи́тию","общежи́тие","общежи́тием","общежи́тии"]),
]

# preposition, case index, gloss
PREPS = [
 ("без",1,"without"),("для",1,"for"),("до",1,"until, as far as"),("из",1,"out of"),
 ("от",1,"away from"),("о́коло",1,"near"),("по́сле",1,"after"),("у",1,"at, by (to have)"),
 ("кро́ме",1,"except"),("напро́тив",1,"opposite"),
 ("к",2,"towards"),("по",2,"along, around"),
 ("че́рез",3,"across, in (time)"),
 ("с",4,"with (together with)"),("над",4,"above"),("под",4,"under"),
 ("ме́жду",4,"between"),("пе́ред",4,"in front of"),("ря́дом с",4,"next to"),
 ("о",5,"about"),("при",5,"in the presence of, under"),
]

def gen(seed=11):
    rng = random.Random(seed)
    items = []
    def add(cat, q, correct, distractors, why, hint=""):
        opts = [correct] + [d for d in distractors if d != correct]
        # dedupe, keep order, cap at 4
        seen, uniq = set(), []
        for o in opts:
            if o not in seen:
                seen.add(o); uniq.append(o)
        uniq = uniq[:4]
        if len(uniq) < 3:
            return
        rng.shuffle(uniq)
        items.append({"cat": cat, "q": q, "opts": uniq, "a": uniq.index(correct),
                      "why": why, "hint": hint})

    # --- verb conjugation -------------------------------------------------
    for inf, gloss, note, forms in VERBS:
        for pi in (0, 2, 5):
            add("conj",
                f"{inf} — {PERSONS[pi]} …",
                forms[pi],
                [f for i, f in enumerate(forms) if i != pi],
                f"{inf} ({gloss}) — {note}. Full: " + ", ".join(forms) + ".",
                hint=gloss)

    # --- noun case forms --------------------------------------------------
    for lemma, gloss, typ, forms in NOUNS:
        for ci in (1, 2, 3, 4, 5):
            add("case",
                f"{lemma} → {CASES[ci]}",
                forms[ci],
                [f for i, f in enumerate(forms) if i != ci],
                f"{lemma} ({gloss}) is {typ}. {CASES[ci]}: {forms[ci]}.",
                hint=gloss)

    # --- which case does this preposition take? --------------------------
    for prep, ci, gloss in PREPS:
        add("prep",
            f"Which case follows «{prep}»?",
            CASES[ci],
            [c for i, c in enumerate(CASES) if i != ci and i != 0],
            f"«{prep}» ({gloss}) governs the {CASES[ci].lower()}.",
            hint=gloss)

    # --- preposition + real noun form ------------------------------------
    for prep, ci, gloss in PREPS:
        lemma, ngloss, typ, forms = rng.choice(NOUNS)
        add("prep",
            f"{prep} … ({lemma})",
            forms[ci],
            [f for i, f in enumerate(forms) if i != ci],
            f"«{prep}» takes the {CASES[ci].lower()} → {forms[ci]}.",
            hint=f"{gloss} + {ngloss}")

    # --- adjective agreement, generated from full paradigms ---------------
    X.gen_adj(add)
    return items

# ------------------------------------------------------- hand-written items
# Aspect, motion and agreement need real sentence context, so these are authored
# rather than generated. The motion set follows the pattern of the exercises in
# «Тесты по РКИ», Тест 1, А16–А18.
AUTHORED = [
 ("aspect","Вчера́ я весь ве́чер … кни́гу.","чита́л",["прочита́л","чита́ю","прочита́ю"],
  "«весь ве́чер» (all evening) describes a process with no endpoint → imperfective чита́ть.","duration → imperfective"),
 ("aspect","Вчера́ я наконе́ц … э́ту кни́гу.","прочита́л",["чита́л","чита́ю","бу́ду чита́ть"],
  "«наконе́ц» (finally) marks a completed result → perfective прочита́ть.","result → perfective"),
 ("aspect","Ка́ждый день он … пи́сьма.","пи́шет",["напи́шет","написа́л","напиши́"],
  "«ка́ждый день» (every day) is repetition → imperfective писа́ть.","repetition → imperfective"),
 ("aspect","За́втра я … э́то письмо́ и отпра́влю его́.","напишу́",["бу́ду писа́ть","пишу́","писа́л"],
  "One completed future action with a result → perfective. The perfective present form IS the future.","future result → perfective"),
 ("aspect","За́втра я … весь день.","бу́ду рабо́тать",["порабо́таю","рабо́таю","рабо́тал"],
  "Imperfective future is compound: бу́ду + infinitive. «весь день» = process.","process → бу́ду + infinitive"),
 ("aspect","Он на́чал … по-ру́сски.","говори́ть",["сказа́ть","поговори́ть","ска́жет"],
  "After нача́ть / ко́нчить / продолжа́ть the infinitive is always imperfective.","after начать → imperfective"),
 ("aspect","Не … э́ту дверь!","открыва́йте",["откро́йте","откры́ть","откры́л"],
  "Negative commands take the imperfective imperative.","negative command → imperfective"),
 ("aspect","— Ты … мне помо́чь? — Да, коне́чно.","мо́жешь",["мог","смо́жет","мочь"],
  "Present tense, 2nd person singular of мочь.","мочь, ты-form"),

 ("motion","Ма́льчик … на велосипе́де.","е́дет",["идёт","иду́т","хо́дит"],
  "На велосипе́де = by vehicle → е́хать, not идти́. 3rd person singular: е́дет.","by bicycle"),
 ("motion","И́горь … пешко́м.","идёт",["е́дет","е́дут","е́здит"],
  "Пешко́м = on foot → идти́.","on foot"),
 ("motion","Ба́бушка … в дере́вню на по́езде.","е́дет",["идёт","хо́дит","е́здит"],
  "На по́езде = by train → е́хать.","by train"),
 ("motion","Мы … в университе́т на метро́.","е́дем",["идём","е́дет","хо́дим"],
  "By metro → е́хать; мы-form is е́дем.","by metro, we"),
 ("motion","Де́ти … в парк.","иду́т",["идём","идёте","идёт"],
  "Де́ти is 3rd person plural → иду́т.","they, on foot"),
 ("motion","Я … в Москву́ за́втра.","е́ду",["е́дем","е́дут","иду́"],
  "To another city → е́хать; я-form is е́ду.","I, by vehicle"),
 ("motion","Ка́ждое у́тро я … в университе́т.","хожу́",["иду́","е́ду","ходи́л"],
  "«Ка́ждое у́тро» = a repeated, there-and-back trip → multidirectional ходи́ть.","repeated → ходить"),
 ("motion","Смотри́, вон он … сюда́!","идёт",["хо́дит","е́здит","пойдёт"],
  "One direction, happening right now → unidirectional идти́.","right now → идти"),
 ("motion","Он … в ко́мнату и сел.","вошёл",["пришёл","ушёл","вы́шел"],
  "Into an enclosed space → в- + идти́ = войти́.","entered"),
 ("motion","Она́ … из до́ма в 8 часо́в.","вы́шла",["вошла́","подошла́","перешла́"],
  "Out of → вы- + идти́ = вы́йти.","exited"),
 ("motion","По́езд … в Москву́ в 10 часо́в.","прихо́дит",["ухо́дит","вхо́дит","отхо́дит"],
  "Arrives → при-. (Ухо́дит would mean it departs.)","arrives"),

 ("num","У меня́ есть два …","бра́та",["брат","бра́тья","бра́тьев"],
  "After 2, 3, 4 the noun goes into the genitive SINGULAR: два бра́та.","2,3,4 + gen. sg."),
 ("num","В гру́ппе пять …","студе́нтов",["студе́нт","студе́нта","студе́нты"],
  "After 5 and above the noun goes into the genitive PLURAL: пять студе́нтов.","5+ → gen. pl."),
 ("num","Я купи́л три …","кни́ги",["кни́га","книг","кни́гу"],
  "3 + genitive singular of кни́га = кни́ги.","3 + gen. sg."),
 ("num","Здесь два́дцать оди́н …","студе́нт",["студе́нта","студе́нтов","студе́нты"],
  "Numbers ending in 1 (except 11) take the nominative singular: два́дцать оди́н студе́нт.","…1 → nom. sg."),
 ("num","Ему́ два́дцать пять …","лет",["год","го́да","года́м"],
  "5–20 and anything ending 5–0 take genitive plural; the suppletive form of год here is лет.","25 лет"),

 ("have","У … есть маши́на.","меня́",["я","мне","мной"],
  "«У меня́ есть» — у takes the genitive; the genitive of я is меня́.","I have"),
 ("have","У … есть вопро́с?","вас",["вы","вам","ва́ми"],
  "у + genitive; the genitive of вы is вас.","do you have"),
 ("have","У меня́ нет …","вре́мени",["вре́мя","вре́менем","вре́мени"],
  "«нет» is followed by the genitive. Вре́мя is a neuter -мя noun: genitive вре́мени.","there is no…"),
 ("have","У бра́та нет …","маши́ны",["маши́на","маши́ну","маши́ной"],
  "After нет the thing that is absent goes into the genitive.","absence → genitive"),

 ("dat","Мне … э́тот фильм.","нра́вится",["нра́влюсь","нра́вятся","нра́вился"],
  "In нра́виться the thing liked is the SUBJECT and the person goes in the dative. Фильм is singular → нра́вится.","I like this film"),
 ("dat","… на́до отдохну́ть.","Тебе́",["Ты","Тебя́","Тобо́й"],
  "На́до / ну́жно / мо́жно take the dative for the person.","you must"),
 ("dat","Ско́лько … лет?","тебе́",["ты","тебя́","тобо́й"],
  "Age is expressed with the dative: Мне два́дцать лет.","how old are you"),
 ("dat","Я звоню́ … ка́ждый день.","дру́гу",["друг","дру́га","дру́гом"],
  "Звони́ть takes the dative — you ring TO someone.","I call my friend"),

 ("vwhere","Я живу́ … Москве́.","в",["на","из","к"],
  "Location inside a city → в + prepositional.","location"),
 ("vwhere","Я иду́ … рабо́ту.","на",["в","из","у"],
  "Рабо́та is one of the nouns that takes на, and direction requires the accusative: на рабо́ту.","direction"),
 ("vwhere","Кни́га лежи́т … столе́.","на",["в","к","о"],
  "On a surface → на + prepositional.","on the table"),
 ("vwhere","Мы говори́м … фи́льме.","о",["в","на","с"],
  "«About» a topic → о + prepositional.","about the film"),
 ("vwhere","Он идёт в …","теа́тр",["теа́тре","теа́тра","теа́тром"],
  "Direction after в takes the accusative: в теа́тр. «в теа́тре» (prepositional) would mean he IS at the theatre.","into the theatre"),

 ("gender","Како́го ро́да «тетра́дь»?","feminine",["masculine","neuter","it varies"],
  "Nouns ending in -ь can be either, but тетра́дь is feminine — hence тетра́дью, о тетра́ди.","-ь noun"),
 ("gender","Како́го ро́да «слова́рь»?","masculine",["feminine","neuter","it varies"],
  "Слова́рь is masculine: словаря́, словарём.","-ь noun"),
 ("gender","Како́го ро́да «и́мя»?","neuter",["masculine","feminine","it varies"],
  "Nouns in -мя (и́мя, вре́мя) are neuter and decline irregularly.","-мя noun"),

 ("spell","Кни́га → plural?","кни́ги",["кни́гы","кни́га","книг"],
  "The 7-letter rule: after г к х ж ч ш щ write и, never ы.","spelling rule"),
 ("spell","Хоро́ший → genitive masculine?","хоро́шего",["хоро́шого","хоро́шый","хоро́шым"],
  "The 5-letter rule: after ж ч ш щ ц write о only under stress, otherwise е.","spelling rule"),

 ("past","Анна вчера́ … в кино́.","ходи́ла",["ходи́л","ходи́ло","ходи́ли"],
  "The past tense agrees with GENDER, not person. Анна is feminine → -ла.","she went"),
 ("past","Мы вчера́ … до́ма.","бы́ли",["был","была́","бы́ло"],
  "Plural past → -ли.","we were"),
 ("past","Э́то … интере́сно.","бы́ло",["был","была́","бы́ли"],
  "Э́то is neuter → -ло.","it was"),

 ("which","Я чита́ю кни́гу, … я купи́л вчера́.","кото́рую",["кото́рый","кото́рая","кото́рым"],
  "Кото́рый takes its GENDER from кни́га (f.) but its CASE from its own clause — here a direct object → accusative кото́рую.","relative clause"),
 ("which","Э́то мой друг, … живёт в Москве́.","кото́рый",["кото́рого","кото́рому","кото́рым"],
  "Masculine, and the subject of its own clause → nominative кото́рый.","relative clause"),

 ("instr","Он рабо́тает …","инжене́ром",["инжене́р","инжене́ра","инжене́ру"],
  "«To work as» takes the instrumental.","works as"),
 ("instr","Я пишу́ …","ру́чкой",["ру́чка","ру́чку","ру́чке"],
  "The instrument you do something with → instrumental.","with a pen"),
 ("instr","Я иду́ в кино́ … дру́гом.","с",["о","у","к"],
  "Accompaniment → с + instrumental.","with a friend"),
 ("instr","Он интересу́ется …","му́зыкой",["му́зыка","му́зыку","му́зыке"],
  "Интересова́ться / занима́ться / увлека́ться all take the instrumental.","interested in music"),
]

def build():
    items = gen()
    for cat, q, correct, distr, why, hint in AUTHORED + X.EXTRA:
        opts = [correct] + list(distr)
        seen, uniq = set(), []
        for o in opts:
            if o not in seen:
                seen.add(o); uniq.append(o)
        uniq = uniq[:4]
        # zlib.crc32, not hash(): str hashing is salted per process, which would
        # reshuffle the options on every build
        rng = random.Random(zlib.crc32(q.encode("utf-8")))
        rng.shuffle(uniq)
        items.append({"cat": cat, "q": q, "opts": uniq, "a": uniq.index(correct),
                      "why": why, "hint": hint})
    for i, it in enumerate(items):
        it["id"] = f"dr-{i}"
    return items

CATS = {
 "pron":("Pronunciation","reduction, devoicing, and the words said unlike their spelling"),
 "conj":("Verb conjugation","present tense, both conjugations"),
 "case":("Noun cases","singular forms of 18 common nouns"),
 "adj":("Adjective agreement","hard, soft and end-stressed endings"),
 "plural":("Plurals","regular endings and the irregulars worth knowing"),
 "prep":("Prepositions & case","which case each preposition governs"),
 "aspect":("Aspect","imperfective vs perfective in context"),
 "motion":("Verbs of motion","идти/ехать/ходить/ездить and the prefixes"),
 "num":("Numbers & agreement","what case a number puts the noun in"),
 "have":("У меня есть / нет","possession and absence"),
 "dat":("Dative constructions","нравиться, надо, age, звонить"),
 "vwhere":("В / НА / О","location vs direction"),
 "gender":("Gender","the tricky -ь and -мя nouns"),
 "spell":("Spelling rules","the 7-letter and 5-letter rules"),
 "past":("Past tense","agreement by gender and number"),
 "which":("который","relative clauses"),
 "instr":("Instrumental","working as, doing with, being interested in"),
}

if __name__ == "__main__":
    # Run directly to see the drill inventory. build.py imports build() and never reads a
    # file, so nothing is written here — dumping a JSON copy would only go stale.
    items = build()
    from collections import Counter
    c = Counter(i["cat"] for i in items)
    print("drill items:", len(items))
    for k, (nm, sub) in CATS.items():
        print(f"  {k:<8} {c[k]:>4}  {nm}")
