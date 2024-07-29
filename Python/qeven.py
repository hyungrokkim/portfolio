### Python3 + SymPy code to check whether 
### adjustability forbids exotic codim-2 branes.
### 
### Results:
###   * for 𝑛=1, there are no constraints.
###   * for 𝑛≥2, there are constraints. However, Q-fluxes corresponding to the generators (A-transform, B-transform, β-transform, factorised duality, diag(1,−1))  are not constrained.

from random import random, choice, choices, randrange, sample
from numpy.random import randint
from sympy import zeros, eye, diag, Matrix

### Main functions: check for the evenness condition 

def check(g: Matrix, m1: int, m2: int):
    """
    Check evenness condition for a codim-2 brane.
    We use the cover ℝ→𝕊¹ where 𝕊¹ is the angle around the brane.
    Then the cocycle is
    :   𝑔(𝑥,𝑦)=𝑔₀ˣ⁻ʸ
    where 𝑔₀∈GO(𝑛,𝑛;ℤ). Then, for any integers 𝑚₁,𝑚₂,
    it must be that
    :   𝑔₀^{𝑚₁+𝑚₂} 𝜂 𝜎_L(𝑔₀^𝑚₁,𝑔₀^𝑚₂)
    has to be a 2𝑛‐component vector of even integers.
    Returns True if the evenness condition is satisfied, False if it fails.
    """
    n = g.shape[0] // 2
    return check3(g**(m1+m2),g**m1,g**m2)

def check3(g1,g2,g3):
    """
    Check evenness condition for general 𝒯𝒟‐bundle:
    :   𝑔₁ 𝜂 𝜎_L(𝑔₂,𝑔₃)
    has to be a 2𝑛‐component vector of even integers.
    Returns True if the evenness condition is satisfied, False if it fails.
    """
    n = g1.shape[0] // 2
    return ((g1 @ eta(n) @ σL(g2,g3).diagonal().T) % 2) == zeros(2*n,1)


def test():
    for i in range(0,50):
        print(check(random_GO_element(2, threshold=8),1,1))

### === Functions for randomly generating an element of GO(𝑛,𝑛;ℤ) ===

def random_GO_element(n: int, threshold = 0.9):
    """
    Return a randomly generated element of GO(𝑛,𝑛;ℤ), as defined in hep-th/0409073.
    The argument `threshold` is how hard it should try to generate an element; can be any positive float.
    """
    g = random_GO_generator(n)
    if random() > threshold:
        return g
    else:
        return g @ random_GO_element(n, threshold*0.9)

def random_o_element(n:int, maxint=100):
    """
    Return a randomly generated antisymmetric 𝑛×𝑛 integer matrix.
    Its components are bounded by `maxint`.
    """
    g = Matrix(randint(maxint, size=(n,n)))
    return g - g.T

def random_GO_generator(n: int):
    """
    Return a randomly selected generator of GO(𝑛,𝑛;ℤ).
    This will be either
        * A-transformation
        * B-transformation
        * β-transformation
        * factorised duality
        * diag(1,…,1,−1,…,−1)
    For the first four, see 1811.11203 §2.3.
    """
    s = choice([f.__name__ for f in [krflip, Atransform, factorduality, ll_abelian, ur_abelian]])
    match s:
        case krflip.__name__:
            return krflip(n)
        case Atransform.__name__:
            return Atransform(random_GL_element(n))
        case factorduality.__name__:
            return factorduality(n, randrange(n), randrange(2))
        case ll_abelian.__name__:
            return ll_abelian(random_o_element(n))
        case ur_abelian.__name__:
            return ur_abelian(random_o_element(n))
        case _:
            assert False

def ll_abelian(g: Matrix):
    """Generate matrices of the form [[1,0],[g,1]] where g is n×n"""
    (n,y) = g.shape
    assert n == y
    assert g.T == -g 
    return block([[eye(n), zeros(n,n)],[g, eye(n)]])

def ur_abelian(g: Matrix):
    """Generate matrices of the form [[1,g],[0,1]] where g is n×n"""
    (n,y) = g.shape
    assert n == y
    assert g.T == -g
    return block([[eye(n), g],[zeros(n,n), eye(n)]])

def factorduality(n: int, i: int, s: bool):
    """Factorised duality [[1-E_i],[(-)^s*E_i],[(-)^s*E_i,1-E_i] where E_i=diag(0,…,1,…,0), with sign flip if True"""
    assert 0 <= i < n
    e = zeros(n,n)
    e[i,i] = 1
    i = eye(n)
    return block([[i-e,(-1)**s*e],[(-1)**s*e,i-e]])

def Atransform(g):
    """Generate A-transformations, see 1811.11203 (2.43)"""
    (n,y) = g.shape
    assert n == y
    assert g.det() in {1, -1}
    ginv = g**(-1)
    assert g @ ginv == eye(n), f"{g=}\n{ginv=}\ng@ginv={g@ginv}\nginv@g={ginv@g}"
    assert ginv @ g == eye(n), f"{g=}, {ginv=}"
    z = zeros(n,n)
    return block([[ginv,z],[z,g.T]])

def krflip(n: int):
    """
    Return 2n×2n matrix [[1,0],[0,-1]].
    This corresponds to a flip of the Kalb–Ramond field.
    This lies in GO(𝑛,𝑛) but not in O(𝑛,𝑛).
    """
    i = eye(n)
    z = zeros(n,n)
    return block([[i,z],[z,-i]])

def check_GL_element(g):
    """Return true iff g is an 𝑛×𝑛 matrix in GL(𝑛;ℤ)"""
    (n,y) = g.shape
    assert n == y
    return g.det() in {1, -1}

def check_GO_element(g):
    """Return true iff g is an 2𝑛×2𝑛 matrix in GO(n,n;ℤ)"""
    (x,y)=g.shape
    assert x == y and not x % 2
    n = x//2
    c1 = g.T @ eta(n) @ g == eta(n)
    c2 = g.T @ eta(n) @ g == -eta(n)
    return c1 ^ c2

### == Functions for generating random GL(𝑛;ℤ) elements ==

def random_GL_element(n:int, threshold=0.9):
    """
    Return a randomly generated 𝑛×𝑛 invertible integer matrix.
    The argument `threshold` is how hard it should try to generate an element; can be any positive float.
    """
    g = random_GL_generator(n)
    if random() > threshold:
        return g
    else:
        return g @ random_GL_element(n, threshold*0.9)

def random_GL_generator(n):
    """
    Return a randomly selected generator of GL(𝑛;ℤ).
    """
    match choice([f.__name__ for f in [random_upper_triangular, random_lower_triangular, perm_matrix, signed_diagonal]]):
        case random_upper_triangular.__name__:
            return random_upper_triangular(n)
        case random_lower_triangular.__name__:
            return random_lower_triangular(n)
        case signed_diagonal.__name__:
            return signed_diagonal(n)
        case perm_matrix.__name__:
            return perm_matrix(n)

def random_upper_triangular(n, maxint=100):
    """
    Return a randomly generated 𝑛×𝑛 upper integer triangular matrix whose diagonals are all 1.
    Each entry is from 0 to maxint−1.
    """
    return Matrix(randint(maxint, size=(n,n))).upper_triangular(1) + eye(n)

def random_lower_triangular(n, maxint=100):
    """
    Return a randomly generated 𝑛×𝑛 lower integer triangular matrix whose diagonals are all 1.
    Each entry is from 0 to maxint−1.
    """
    return Matrix(randint(maxint, size=(n,n))).lower_triangular(-1) + eye(n)

def signed_diagonal(n):
    """
    Return a randomly generated 𝑛×𝑛 diagonal matrix whose diagonal entries are ±1.
    """
    return diag(*choices([-1,1], k=n))

def perm_matrix(n):
    """
    Return a randomly generated 𝑛×𝑛 permutation matrix that permutes a single pair of indices.
    """
    m = eye(n)
    if n > 1:
        i, j = sample(range(n), k=2)
        m[i,i] = m[j,j] = 0
        m[i,j] = m[j,i] = 1
    return m


def sanity_test():
    """Check that random GL and GO generators work as intended."""
    for i in range(0,50):
        assert check_GL_element(random_GL_generator(7))

    for i in range(0,50):
        assert check_GO_element(random_GO_generator(7))

### === Utility functions ===
def block(l):
    """Construct a 2×2 block matrix, similar to numpy.block (which SymPy lacks)"""
    ((a,b),(c,d))=l
    return a.row_join(b).col_join(c.row_join(d))

def decompose(m: Matrix):
    """Decompose a 2n×2n matrix [[A,B],[C,D]] into four n×n matrices (A,B,C,D)"""
    (x,y)=m.shape
    assert x == y and not x % 2
    return (m[:x//2,:x//2], m[:x//2,x//2:], m[x//2:,:x//2], m[x//2:,x//2:])

def eta(n: int):
    """2n×2n matrix [[0,1],[1,0]], the (n,n)-signature integer metric"""
    return block([[zeros(n,n), eye(n)],[eye(n), zeros(n,n)]])

def J(n):
    """2n×2n matrix J=[[0,0],[1,0]] that appears in the 2-group TD_n in Nikolaus--Waldorf 1804.00677"""
    return block([[zeros(n,n), zeros(n,n)],[eye(n), zeros(n,n)]])

def sign(m):
    """The homomorphism GO(𝑛,𝑛;ℤ)→{±1}"""
    # return ±1
    (x,y)=m.shape
    assert x == y and not x % 2
    n = x//2
    c1 = m.T @ eta(n) @ m == eta(n)
    c2 = m.T @ eta(n) @ m == -eta(n)
    assert c1 ^ c2
    return 1 if c1 else -1

def σL(g1: Matrix, g2: Matrix):
    """
    Function 𝜎_L(𝑔₁,𝑔₂) that appears in the GO action on TDₙ: notes023CS (3.22).
    Takes: two elements of GO(𝑛,𝑛;ℤ)
    Returns:  symmetric 2n×2n integer matrix
    """
    return g2.T @ ρL(g1) @ g2 + sign(g2) * ρL(g2) - ρL(g1 @ g2);

def ρL(g):
    """
    The lower triangular matrix 𝜌_L(𝑔) such that
    : 𝜌(𝑔)=𝜌_L(𝑔)−𝜌_Lᵀ(𝑔)
    where 𝜌(𝑔) is a 2𝑛×2𝑛 antisymmetric integer matrix.
    Cf. notes023CS (3.18).
    Takes: antisymmetric 2𝑛×2𝑛 integer matrix
    Returns: lower triangular 2𝑛×2𝑛 integer matrix
    """
    return ρ(g).lower_triangular()

def ρ(g):
    """
    Cf. notes023CS (3.18).
    Takes: element of GO(𝑛,𝑛;ℤ)
    Returns: antisymmetric 2𝑛×2𝑛 integer matrix
    """
    (x,y)=g.shape
    assert x == y and not x % 2
    n = x//2
    return g.T @ J(n) @ g - sign(g) * J(n)

