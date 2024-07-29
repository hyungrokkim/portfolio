#!/bin/env python3
import csv
from collections import defaultdict
import unicodedata

table = [{},{},{}]
with open('yale.txt') as f:
    for l in f:
        (en, ko) = l.split()
        table[3-len(en)][en] = ko

consonants = set("ㄱㄲㄴㄷㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ")

def choseong_to_jongseong(c):
    def cho_to_jong(c):
        if c <= 0x1101:
            return 0
        if c == 0x1102:
            return 1
        if c == 0x1103:
            return 3
        if c == 0x1105:
            return 2
        if c <= 0x110C:
            return 9
        else:
            return 8
    return chr(ord(c) + cho_to_jong(ord(c)) + 168)


def unyale(s):
    for t in table:
        for (en, ko) in t.items():
            s = s.replace(en,ko)
    if s[0] not in consonants:
        s = 'ㅇ' + s
    s = unicodedata.normalize('NFKC',s)
    if len(s) == 2:
        s = s[0] + choseong_to_jongseong(s[1])
        s = unicodedata.normalize('NFKC',s)
    assert len(s) == 1
    return s

kHangul = defaultdict(set)
with open("Unihan_Readings.txt") as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if len(row) < 3:
            continue
        c = chr(int(row[0][2:],base=16))
        if row[1] == 'kHangul':
            kHangul[c] |= set(row[2].split())
        elif row[1] == 'kKorean':
            kHangul[c] |= set(map(unyale,row[2].split()))

hangulToHanja = defaultdict(set)
for c, hs in kHangul.items():
    for h in hs:
        hangulToHanja[h].add(c)


