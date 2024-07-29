from itertools import product
A4 = WeylCharacterRing("A4",style="coroots")
z=A4(1,0,0,0)
ddz=e=A4(0,0,0,1)
r=A4(0,1,0,0)
N=20
okays = set()
for (p,q,n) in filter(lambda x: (x[0]+x[1]) % 2 and x[0]+x[1]>1, product(range(0,11), range(0,6), range(0,N))):
    if (p,q) in okays:
        continue
    s1=set((r.exterior_power(p)*e.exterior_power(q)).monomials())
    s2=set((z.symmetric_power(n-((1+q-p)//2 if 1+q-p<0 else 0))*ddz.symmetric_power(n+((1+q-p)//2 if 1+q-p>0 else 0))).monomials())
    if s1 & s2:
        print(f"(p,q,n)={(p,q,n)}", s1 & s2)
        okays.add((p,q))
"""
Suppose we want to rule out ρᵢ(𝚛_{⋀²𝐿},…,𝚛_{⋀²𝐿},𝚎_{𝐿*},…,𝚎_{𝐿*}), where we have 𝑝 arguments 𝚛_{⋀²𝐿} and 𝑞 arguments 𝚎_{𝐿*} (with 𝑖=𝑝+𝑞 odd).

On the one hand, it should be inside (⋀²𝐿)^{∧𝑝}⊗(𝐿*)^{∧𝑞}.

On the other hand, it is of degree 1−(𝑝+𝑞)+2𝑞=1+𝑞−𝑝. So:

 * For 1+𝑞−𝑝>0, it should be inside ⨁_{𝑛=0}^∞ 𝐿*^{⊙(𝑛+½(1+𝑞−𝑝))}
   ⊗ 𝐿^{⊙𝑛}, since it should be of the ansatz 𝑧ⁿ(∂/∂𝑧)^{𝑛+½(1+𝑞−𝑝)}.
 * For 1+𝑞−𝑝<0, it should be inside ⨁_{𝑛=0}^∞ 𝐿*^{⊙𝑛} ⊗
   𝐿^{⊙(𝑛−½(1+𝑞−𝑝))}, since it should be of the ansatz
   𝑧^{𝑛−½(1+𝑞−𝑝)}(∂/∂𝑧)ⁿ.

So, to check: For 𝑛,𝑝,𝑞∈{1,…100}, with 𝑝+𝑞 odd, compute whether there exists an irrep that is a submodule of both (⋀²𝐿)^{∧𝑝}⊗(𝐿*)^{∧𝑞} AND also (𝐿*^{⊙(𝑛+½(1+𝑞−𝑝))} ⊗ 𝐿^{⊙𝑛} OR 𝐿*^{⊙𝑛} ⊗ 𝐿^{⊙(𝑛−½(1+𝑞−𝑝))}), depending on the sign of 1+𝑞−𝑝.
"""

# output:
# (p,q,n)=(3, 0, 1) {A4(2,0,0,1)}
# (p,q,n)=(4, 3, 1) {A4(1,0,0,1)}
