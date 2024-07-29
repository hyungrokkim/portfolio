from re import sub
from functools import reduce

"""
Ekzemploj:

Aaron -> Aarono
Abaddon -> Abadono
Abelard -> Abelardo
Abishag -> Abiŝag
Abner -> Abnero
Abraham -> Abrahamo
Abruzzo -> Abruzo
Abshalom -> Abŝalomo
Abu Dhabi -> Abudabio
Abuja -> Abuĝo
Waringhien → Varigjeno
"""

esperantigi = lambda s: reduce(lambda s, p: sub(*p, s), [
        (r"ch", r"ĉ"),
        (r"sc?h", r"ŝ"),
        ("j", "ĵ"),
        (r"([^ae])e$", r"\1"),
        ("x", "ks"),
        ("qu", "kv"),
        (r"q", r"k"),
        (r"kh", r"ĥ"),
        (r"ph", r"f"),
        (r"g([ie])", r"ĝ\1"),
        (r"gy", r"ĝi"),
        (r"([bdg])h", r"\1"),
        (r"c([^ei])", r"k\1"),
        (r"c$", r"k"),
        (r"t[sz]", r"c"),
        # Handle y
        (r"y([aeou])", r"j\1"),
        (r"y", r"i"),
        # Handle diphthongs
        (r"([ae])[wu]", r"\1ŭ"),
        (r"([aeou])i", r"\1j"),
        (r"ee", r"i"),
        (r"oo", r"u"),
        (r"w", r"v"),
        *((s*2, s) for s in "bdfglmnprstzaeiou"),
    ], s.lower().strip()).capitalize() + "o"
