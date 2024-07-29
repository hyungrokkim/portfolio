s### suppose that * is not necessarily symmetric, while () is symmetric
### we want x*(yz) = y(x*z) = z(x*y)
### the dimension is:
### (1) things like x*(yz): 3
### (2) things like (xy)*z: 3
### (3) things like (x*y)z = z(x*y): 6
### so 12-dimensional in totals
### The identities are:
###   x*(yz) = y(x*z) = z(x*y)  ⑵
###   (xy)*z = x*(yz) + y*(xz)  ⑶
### So, the number of relations are 3×2=6 for ⑵ and 3 for ⑶
### and the dual should be 3-diimiensional.
###
### We need to represent this space. It is natural to do it as a pair (for (*)) and frozenset (for the commutative product).
from itertools import permutations

# Names of the basis vectors
gens = {lambda x, y, z: (x, frozenset({y,z})),
        lambda x, y, z: (frozenset({x,y}), z),
        lambda x, y, z: frozenset({(x,y),z}),
       }
basis_names = {g(*p) for p in permutations("xyz") for g in gens}

# Mapping from basis vector name to numerical index (0–11)
ss_inv = dict(enumerate(basis_names))
# Mapping from numerical index (0–11) to basis vector name
ss = {v: k for k, v in ss_inv.items()}

def ident1(gen, x, y, z):
    "associativity between * and ()"
    return gen(ss[(frozenset({x,y}),z)]) - gen(ss[frozenset({x,(y,z)})])

def ident2(gen, x, y, z):
    "distributivity"
    return gen(ss[(x,frozenset({y,z}))]) \
        - gen(ss[frozenset({(x,y),z})]) - gen(ss[frozenset({x,(y,z)})])

def perm_apply(f, gen, args):
    "generate all permutations of variables of a given identity"
    return [f(gen, *perm) for perm in permutations(args)]

def print_vector(v, s_inv):
    "stringify a polynomial"
    def gen():
        for (index, coeff) in enumerate(v):
            if not coeff:
                continue
            yield "+" if coeff > 0 else "-"
            if abs(coeff) != 1:
                yield str(abs(coeff))
            yield print_term(s_inv[index])
    return "".join(gen()).lstrip("+")

def print_term(t, outer_bracket=False):
    "stringify a monomial without coefficients"
    return t if isinstance(t, str) else \
        ("({})" if outer_bracket else "{}").format(
            ('*' * isinstance(t,tuple)).join(print_term(i, True) for i in t)
        )

L = IntegralLattice(matrix.identity(12))

relations = L.span(perm_apply(ident1, L.gen, "xyz") + perm_apply(ident2, L.gen, "xyz"))
for v in L.orthogonal_complement(relations).basis_matrix():
    print(print_vector(v,ss_inv))

## RESULT:
##  x*(yz)(z*x)y+(xy)*z(y*x)z+(x*z)yz*(xy)(yz)*x+(y*z)x
##  (xz)*y+(z*x)y+(x*y)z(xy)*z+(y*x)z(x*z)y+2z*(xy)+(yz)*x+(z*y)x(y*z)x
##  y*(xz)+(z*x)y+(y*x)z+z*(xy)+(yz)*x

####

## verifying the associativity property
"""
s = dict(zip("x(yz) y(zx) z(xy) z(yx) y(xz) x(zy) (xy)z (yz)x (zx)y (zy)x (yx)z (xz)y".split(), itertools.count()))
s_inv = {v: k for k, v in s.items()}

def associator(L, t):
    (x,y,z) = t
    return L.gen(s[f"{x}({y}{z})"]) - L.gen(s[f"({x}{y}){z}"])

def associator_perm(L, vars):
    return [associator(L, perm) for perm in itertools.permutations(vars)]

def print_vector(v):
    s = ""
    for (index, value) in enumerate(v):
        if value == 1:
            s += f"+{s_inv[index]}"
        elif value == -1:
            s += f"-{s_inv[index]}"            
        elif value > 0:
            s += f"+{value}{s_inv[index]}"
        elif value < 0:
            s += f"{value}{s_inv[index]}"
    return s

L = IntegralLattice(matrix.identity(12))

associator_subspace = L.span(associator_perm(L,"xyz"))
print([print_vector(v) for v in L.orthogonal_complement(associator_subspace).basis_matrix()])
"""


