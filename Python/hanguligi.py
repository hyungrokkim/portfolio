import re
from functools import reduce
from unicodedata import normalize, name
from itertools import chain
import fileinput

vokaloj = sorted([
    ("a", "ᅡ"),
    ("e", "ᅥ"),
    ("i", "ᅵ"),
    ("o", "ᅩ"),
    ("u", "ᅮ"),
    ("j", "ᆞ"),
    ("ŭ", "ᅳ"),
    ("jaj", "ᅤ"),
    ("jej", "ᅨ"),
    ("joj", "ᆈ"),
    ("juj", "ᆔ"),
    ("jaŭ", "ᆤ"),
    ("jeŭ", "ᅾ"),
    ("juŭ", "ᆓ"),
    ("ja", "ᅣ"),
    ("je", "ᅧ"),
    ("jo", "ᅭ"),
    ("ju", "ᅲ"),
    ("aŭ", "ᅷ"),
    ("eŭ", "ᅻ"),
    ("iŭ", "ᆛ"),
    ("oŭ", "ᆃ"),
    ("aj", "ᅢ"),
    ("ej", "ᅦ"),
    ("oj", "ᅬ"),
    ("uj", "ᅱ"),
    ("ŭa", "ᅷ"),
    ("ŭe", "ᅯ"),
    ("ŭej", "ᅰ"),
], key=lambda p: len(p[0]), reverse=True)

konsonantoj = [
    ("g", "ᄀ", "ᆨ"),
    ("n", "ᄂ", "ᆫ"),
    ("d", "ᄃ", "ᆮ"),
    ("l", "ᄅ", "ᆯ"),
    ("r", "ᄛ", "ퟝ"),
    ("m", "ᄆ", "ᆷ"),
    ("b", "ᄇ", "ᆸ"),
    ("v", "ᄫ", "ᇦ"),
    ("s", "ᄉ", "ᆺ"),
    ("ŝ", "ᄾ", None),
    ("z", "ᅀ", "ᇫ"),
    ("ĝ", "ᄌ", "ᆽ"),
    ("ĵ", "ᅐ", None),
    ("c", "ᄎ", "ᆾ"),
    ("ĉ", "ᅕ", None),
    ("k", "ᄏ", "ᆿ"),
    ("t", "ᄐ", "ᇀ"),
    ("p", "ᄑ", "ᇁ"),
    ("f", "ᅗ", "ᇴ"),
    ("ĥ", "ᅙ", "ᇹ"),
    ("h", "ᄒ", "ᇂ"),
]

def decompose(c):
    choseong = {
        name(c)[16:]: c
        for c in map(chr, range(ord("ᄀ"), ord("ᄒ")+1))
        if "-" not in name(c)
    }
    jongseong = {
        name(c)[16:]: c
        for c in map(chr, range(ord("ᆨ"), ord("ᇂ")+1))
        if "-" not in name(c)
    }
    n = unicodedata.name(c)
    if n.startsWith("HANGUL JONGSEONG "):
        return "".join(
            jongseong[s]
            for s in n[17:].split("-")
        )
    elif n.startsWith("HANGUL CHOSEONG "):
        return "".join(
            choseong[s]
            for s in n[16:].split("-")
        )
    raise ValueError(c)

choseong = list(map(chr, list(range(0x1100, 0x1160)) + list(range(0xa960, 0xa97d))))
jungseong = list(map(chr, list(range(0x1160, 0x11a8)) + list(range(0xd7b0, 0xd7c7))))
jongseong = list(map(chr, list(range(0x11a8, 0x1200)) + list(range(0xd7cb, 0xd7fc))))

choseong_table = { ord(k): ord(v) for (k,v,_) in konsonantoj }
jongseong_table = { ord(k): ord(v or v2) for (k,v2,v) in konsonantoj}

vowel_regex = "[{}]".format("".join(b for (_,b) in vokaloj))

def make_table(d):
    return { ord(k): ord(v) for (k,v) in d.items() }

def hangul(s):
    if s != s.strip().lower(): return hangul(s.strip().lower())
    s2 = reduce(
        lambda s, p: s.replace(p[0], p[1]),
        vokaloj,
        s)
    def iterator(s):
        remaining = s
        while remaining:
            m = re.fullmatch("(?s)([^a-pr-vzĉĝĥĵŝŭ]*)([a-pr-vzĉĝĥĵŝŭ]+)(.*)", remaining)
            if not m:
                yield remaining
                return
            yield m.group(1)
            yield process_consonant(m.group(2),
                word_initial=not re.match(vowel_regex, m.group(1)[::-1]),
                word_final=not re.match(vowel_regex, m.group(3)),
            )
            #print("MATCH", m.group(1)[-1] if m.group(1) else "", "|", m.group(3)[0])
            remaining = m.group(3)
    def add_ieung(i):
        necesas = True
        for c in i:
            if necesas and name(c,"").startswith("HANGUL JUNGSEONG"):
                yield 'ᄋ'
            yield c
            necesas = not name(c,"").startswith("HANGUL CHOSEONG")
    
    def add_filler(i):
        necesas = False
        for c in i:
            if necesas and not name(c,"").startswith("HANGUL JUNGSEONG"):
                yield "\u1160"
            yield c
            necesas = name(c,"").startswith("HANGUL CHOSEONG")
        if necesas:
            yield "\u1160"

    return normalize("NFC", "".join(
        add_ieung("".join(
            iterator(s2)
        ))
    ))


choseongs=sorted("""
    g gg n d dd l m b bb s ss ĝ ĝĝ c k
    t p h ng nn nd nb dg ln ll lh r mb bg bn
    bd bs bsg bsd bsb bss bsĝ bĝ bc bt bp v sg sn sd
    sl sm sb sbg sss sĝ sc sk st sp sh ŝ ŝŝ
    z
    ĵ ĵĵ ĉ pb f hh ĥ gd ns nĝ nh dl
    dm db ds dĝ lg lgg ld ldd lm lb lbb lv ls lĝ lk
    md ms bst bk bh ssb ĝĝh tt ph hs ĥĥ
""".split(), key=len, reverse=True)

jongseongs=sorted("""
    g gg gs n nĝ nh d l
    lg lm lb ls lt lp lh m b bs s ss ĝ c k
    t p h gl gsg ng nd ns nz nt dg dl lgs ln ld ldh
    ll lmg lms lbs lbh lv lss lz lk lĥ mg ml mb ms mss mz
    mc mh bl bp bh v sg sd dl sb z
    pb f hn gl gm hb ĥ gn gb gc gk gh nn
    nl nc dd ddb db
    ds dsg dĝ dc dt lgg lgh llk lmh lbd lbp r mn mnn
    mm mbs mĝ bd blp bm bb bsd bĝ bc sd sv ssg ssd sz zĝ
    sc st sh zb zv ĝb ĝbb gg ps pt
""".split(), key=len, reverse=True)


def process_consonant(s, word_initial=False, word_final=False):
    regex = (r"""
        (?x)
        () ((?:{choseong})*)
    """
        if word_initial
        else r"""
        (?x)
        ((?:{jongseong})?) ((?:{choseong})*)
        """ if word_final
        else
        r"""
        (?x)
        ((?:{jongseong})?) ((?:{choseong}))
    """
    ).format(
        choseong="|".join(choseongs),
        jongseong="|".join(jongseongs),
    )
    m = re.fullmatch(regex, s)
    if not m and not word_initial and not word_final:
        m = re.fullmatch(
        r"(?x) ((?:{jongseong})?) ((?:{choseong})*)".format(
            choseong="|".join(choseongs),
            jongseong="|".join(jongseongs),
        ), s)
        assert m
    if not m:
        print("ERROR!", s, regex, word_initial, word_final)
    (j, c) = m.group(1, 2)
    #print((j,c), "{word_initial} {word_final}".format(
    #    word_initial=word_initial,
    #    word_final=word_final
    #))
    return "".join(chain(map(
        lambda s: alpha_to_jamo(s,key='jongseong'), regex_matches("|".join(jongseongs), j)),
        map(lambda s: alpha_to_jamo(s,key='choseong'), regex_matches("|".join(choseongs), c))))

def regex_matches(regex, s):
    def temp(regex, s):
        if not s:
            return
        m = re.fullmatch("(" + regex + ")*", s)
        assert m
        assert m.group(1)
        yield m.group(1)
        yield from temp(regex, s[:-len(m.group(1))])
    return reversed(list(temp(regex, s)))

def alpha_to_jamo(s, key='choseong'):
    if key=='choseong' and s=='ŝŝ': return "ᄿ"
    if key=='choseong' and s=='ĵĵ': return "ᅑ"
    name_components = dict(
        g='kiyeok',
        n='nieun', 
        d='tikeut',
        l='rieul',
        r='kapyeounrieul',
        m='mieum',
        b='pieup',
        v='kapyeounpieup',
        s='sios',
        ŝ='ceongchieumsios',
        z='pansios',
        ĝ='cieuc',
        ĵ='ceongchieumcieuc',
        c='chieuch',
        ĉ='ceongchieumchieuch',
        k='khieukh',
        t='thieuth',
        p='phieuph',
        f='kapyeounphieuph',
        h='hieuh',
        ĥ='yeorinhieuh',
    )
    
    uname = "HANGUL " + key.upper() + " " + (
        "SSANG{}".format(name_components[s[0]])
        if len(s) == 2 and s[0] == s[1]
        else "{}-SSANG{}".format(name_components[s[0]], name_components[s[1]])
        if len(s) == 3 and s[1] == s[2]
        else "SSANG{}-{}".format(name_components[s[0]], name_components[s[2]])
        if len(s) == 3 and s[0] == s[1]
        else "-".join(name_components[c] for c in s)
    ).upper()
    for i in list(range(0x1100, 0x1160)) + list(range(0xa960, 0xa97d)) \
                       + list(range(0x11a8, 0x1200)) + list(range(0xd7cb, 0xd7fc)):
       if name(chr(i), "") == uname:
            return chr(i)

if __name__ == "__main__":
    for l in fileinput.input():
        print(hangul(l))
