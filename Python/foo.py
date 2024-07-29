#!/usr/bin/python3
import fileinput

"""
64-bit.
-> 7*9  (ASCII)   0.9 B 0b[7]b[7]b[7]b[7]b[7]b[7]b[7]b[7]b[7]
   8*7  (Latin-1) 1.1 B 11000110b[8]b[8]b[8]b[8]b[8]b[8]b[8]
   10*6 (~1%)     1.3 B 1111b[10]b[10]b[10]b[10]b[10]b[10]
   12*5 (~3%)     1.6 B 1110b[12]b[12]b[12]b[12]b[12]
   15*4 (25%)     2   B 1101b[15]b[15]b[15]
   21*3 (100%)    2.7 B 10????b[16]0????b[16]0????b[16]
                        110000b[16]10000b[16]10000b[16]
   21*2           4   B 1                    EOFCHAR
   21*1           8   B 1          EOFCHAR   EOFCHAR

We can also have additional compression
   21+13*3        2   B 1?????b[16]101b[13]b[13]b[13]
   21+10*4        1.6 B 1?????b[16]11b[10]b[10]b[10]b[10]
   21+7*5         1.3 B 1?????b[16]1000100b[7]b[7]b[7]b[7]b[7]
   21+6*6         1.1 B 1?????b[16]100011b[6]b[6]b[6]b[6]b[6]b[6]
   21+5*7         1   B 1?????b[16]1000101b[5]b[5]b[5]b[5]b[5]b[5]b[5]
   21+4*8         0.9 B 1?????b[16]1001000000b[4]b[4]b[4]b[4]b[4]b[4]b[4]b[4]

8 bytes vs 1+1+3=5 bytes. 

CJK range:
  U+0000 - 00FF (Latin-1)
  U+1100 - 11FF (hangul jamo)
  U+2000 - 20FF (gen. punct., sup/sub, currency)
  U+3000 - 30FF (kana, CJK symbols/punct)
  U+4E00 - 9FFF (CJK unified ideographs)
  U+AC00 - D7FF (hangul syllables)
  U+FF00 - FFFF (halfwidth/fullwidth)

7*8=56.
64-56=8.
10FFFF
00000(....)
01111(....)
10000(....)

~2^17 chars in use

UTF-8:
   1 byte (ASCII)
   2 byte (2^11)
   3 byte (2^16)
   4 byte (2^21)
"""

def cjkvalue(c):
    gaps = [0x1100-0x0100, 0x2000 - 0x1200, 0x3000 - 0x2100, 0x4E00 - 0x3100, 0xAC00 - 0xA000, 0xFF00 - 0xD800]
    offset = 0 if c in range(0x0000, 0x0100) else \
             1 if c in range(0x1100, 0x1200) else \
             2 if c in range(0x2000, 0x2100) else \
             3 if c in range(0x3000, 0x3100) else \
             4 if c in range(0x4E00, 0xA000) else \
             5 if c in range(0xAC00, 0xD800) else \
             5 if c in range(0xFF00, 0x10000) else None
    return c - sum(gaps[0:offset])

def incjkrange(c):
    return c in range(0x0000, 0x0100) or \
           c in range(0x1100, 0x1200) or \
           c in range(0x2000, 0x2100) or \
           c in range(0x3000, 0x3100) or \
           c in range(0x4E00, 0xA000) or \
           c in range(0xAC00, 0xD800) or \
           c in range(0xFF00, 0x10000)
"""
  U+0000 - 00FF (Latin-1)
  U+1100 - 11FF (hangul jamo)
  U+2000 - 20FF (gen. punct., sup/sub, currency)
  U+3000 - 30FF (kana, CJK symbols/punct)
  U+4E00 - 9FFF (CJK unified ideographs)
  U+AC00 - D7FF (hangul syllables)
  U+FF00 - FFFF (halfwidth/fullwidth)
"""
def cond_general(s, f):
    "Checks if f(s[i])…f(s[i+chars-1]) inclusive all belong to range_."
    return all(map(f, s))

def cond(s, chars, maxsize):
    "Checks if s[i]…s[i+chars-1] inclusive all belong to 0…2^maxsize-1 inclusive."
    r = range(0,2**maxsize).__contains__
    return chars <= len(s) and all(map(r, map(ord, s[0:chars])))

def cond_relative(s, chars, maxsize):
    "Checks if s[i+1]-s[i]…s[i+chars-1]-s[i] inclusive all belong to -2^(maxsize-1)-1…2^(maxsize-1)-1 or space inclusive."
    r = lambda c: abs(ord(c)-ord(s[0])) < 2**(maxsize-1) or c == ' '    
    return chars <= len(s) and all(map(r, s[1:chars]))

def value(s, maxsize, transform=ord):
    return sum(transform(c)<<maxsize*i for (i,c) in enumerate(reversed(s)))

def value_relative(s, magic, maxsize):
    new_s = [ord(c) % 2**maxsize if c != ' ' else 1<<maxsize-1 for c in s[1:]]
    return (1<<63) + (ord(s[0])<<42) + (magic << maxsize*(len(s)-1)) + value(new_s, maxsize, transform=lambda i:i)

def encode(s):
    EOFCHAR = 0b10001*2**(21-5)
    while True:
        if not s:
            return
        elif cond(s, chars=9, maxsize=7):
            yield value(s[:9], maxsize=7)
            s = s[9:]
            print("9")
        elif cond_relative(s, chars=9, maxsize=4):
            yield value_relative(s[:9], magic=0b1001000000, maxsize=4)
            s = s[9:]
            print("9r")
        elif cond_relative(s, chars=8, maxsize=5):
            yield value_relative(s[:8], magic=0b1000101, maxsize=5)
            s = s[8:]
            print("8r")
        elif cond(s, chars=7, maxsize=8):
            yield (0b11000110<<7*8) + value(s[:7], maxsize=8)
            s = s[7:]
            print("7")
        elif cond_relative(s, chars=7, maxsize=6):
            yield value_relative(s[:6], magic=0b100011, maxsize=6)
            s = s[7:]
            print("7r")
        elif cond(s, chars=6, maxsize=10):
            yield (0b1111<<60) + value(s[:6], maxsize=10)
            s = s[6:]
            print("6")
        elif cond_relative(s, chars=6, maxsize=7):
            yield value_relative(s[:6], magic=0b1000100, maxsize=7)
            s = s[6:]
            print("6r")
        elif cond(s, chars=5, maxsize=12):
            yield (0b1110<<60) + value(s[:5], maxsize=12)
            s = s[5:]
            print("5")
        elif cond_relative(s, chars=5, maxsize=10):
            yield value_relative(s[:5], magic=0b11, maxsize=10)
            s = s[5:]
            print("5r")
        elif 4 <= len(s) and all(incjkrange(ord(s[k])) for k in range(0, 4)):
            yield (0b1101<<60) + value(s[:4], maxsize=15, transform=lambda c: cjkvalue(ord(c)))
            s = s[4:]
            print("4")
        elif cond_relative(s, chars=4, maxsize=13):
            yield value_relative(s[:4], magic=0b101, maxsize=13)
            s = s[4:]
            print("4r")
        elif cond(s, chars=3, maxsize=21):
            yield 2**63 + value(s[:3], maxsize=21)
            s = s[3:]
            print("3")
        elif 2 == len(s):
            yield 2**63 + (ord(s[0])<<21*2)+ (ord(s[1])<<21) + EOFCHAR
            s = s[2:]
        else:
            assert 1 == len(s)
            yield 2**63 + (ord(s[0])<<21*2) + (EOFCHAR<<21) + EOFCHAR
            s = s[1:]

def display(s):
    return (list(map(hex, encode(s))), 8*len(list(encode(s)))/len(list(s)))

def ratio(s):
    return (8*len(list(encode(s)))/len(s))

def utf8ratio(s):
    return (len(s.encode('utf-8'))/len(s))

def utf16ratio(s):
    return (len(s.encode('utf-16'))/len(s))

if __name__ == "__main__":
    s = "\n".join(fileinput.input())
    print("WTF-64: {:2.2f} byte/char".format(ratio(s)))
    print("UTF-8: {:2.2f} byte/char".format(utf8ratio(s)))
    print("UTF-16: {:2.2f} byte/char".format(utf16ratio(s)))


