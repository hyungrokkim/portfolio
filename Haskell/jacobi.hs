import Data.List

-- R i j = r^i_j
-- S i j = r^ij
-- T i j = r_ij
-- E i = e^i
-- F i = e_i
data Term = R Int Int | S Int Int | T Int Int | E Int | F Int | D0 | D2 Int Int | D4 Int | Sum [Term] | Mult Double Term deriving (Show, Eq, Ord)

zero = Sum []
minus a = Mult (-1) a
δ i j = if i == j then 1 else 0

ε' :: [Int] -> Int
ε' [1] = 1
ε' l = let
    n = length l
    in
    case elemIndex n l of
        Just i -> (if even (n-1-i) then 1 else -1) * ε' (let (as, bs) = splitAt i l in as ++ tail bs)
        Nothing -> 0
ε i j k l m = fromIntegral $ ε' [i,j,k,l,m]

bracket (a `Mult` b) c = a `Mult` bracket b c
bracket a (b `Mult` c) = b `Mult` bracket a c
bracket (Sum []) _ = zero
bracket _ (Sum []) = zero
bracket (Sum [a,b]) c = Sum [bracket a c, bracket b c]
bracket a (Sum [b, c]) = Sum [bracket a b, bracket a c]
bracket (R i j) (R k l) = Sum[(δ j k) `Mult` R i l, minus ((δ i l) `Mult` R k j)]
bracket (R i j) (S k l) = Sum [(δ k j) `Mult` S i l, (δ l j) `Mult` S k i]
bracket (S k l) (R i j) = minus ((R i j) `bracket` (S k l))
bracket (S _ _) (S _ _) = zero

bracket (R i j) (T k l) = minus $ Sum [(δ i k) `Mult` T j l, (δ i l) `Mult` T k j]
bracket (T k l) (R i j) = minus $ bracket (R i j) (T k l)
bracket (T _ _) (T _ _) = zero
bracket (S i j) (T k l) = Sum [
    (δ i k) `Mult` R j l,
    minus ((δ i l) `Mult` R j k),
    minus ((δ j k) `Mult` R i l),
    (δ j l) `Mult` R i k]
bracket (T k l) (S i j) = minus $ bracket (S i j) (T k l)

bracket (R i j) (E k) = (δ k j) `Mult` E i
bracket (E k) (R i j) = minus $ bracket (R i j) (E k)
bracket (T i j) (E k) = Sum [δ k i `Mult` F j,
    minus $ δ k j `Mult` F i]
bracket (E k) (T i j) = minus $ bracket (T i j) (E k)
bracket (S _ _) (E _) = zero
bracket (E _) (S _ _) = zero

bracket (R i j) (F k) = minus $ (δ i k) `Mult` F j
bracket (F k) (R i j) = minus $ bracket (R i j) (F k)
bracket (S i j) (F k) = Sum [δ j k `Mult` E i,
    minus $ δ i k `Mult` E j]
bracket (F k) (S i j) = minus $ bracket (S i j) (F k)
bracket (T _ _) (F _) = zero
bracket (F _) (T _ _) = zero

bracket (E _) (E _) = zero
bracket (E _) (F _) = zero
bracket (F _) (E _) = zero
bracket (F _) (F _) = zero

-- {r^i_j, d}
bracket (R i j) D0 = (0.5 * δ i j) `Mult` D0
bracket (R i j) (D2 k l) = Sum [
    minus $ δ i k `Mult` D2 j l,
    minus $ δ i l `Mult` D2 k j,
        (0.5 * δ i j) `Mult` D2 k l]
bracket (R i j) (D4 k) = Sum [
    δ j k `Mult` D4 i,
    (-0.5 * δ i j) `Mult` D4 k]
bracket D0 (R i j) = minus $ bracket (R i j) D0
bracket (D2 k l) (R i j) = minus $ bracket (R i j) (D2 k l)
bracket (D4 k) (R i j) = minus $ bracket (R i j) (D4 k)

-- {d,d}
bracket (D2 i j) (D2 k l) = minus $ Sum [ε i j k l m `Mult` E m | m <- [1..5]]
bracket (D2 i j) (D4 k) = Sum [δ i k `Mult` F j, minus $ δ j k `Mult` F i]
bracket (D4 k) (D2 i j) = bracket (D2 i j) (D4 k)
bracket D0 (D4 i) = E i
bracket (D4 i) D0 = bracket D0 (D4 i)
bracket (D4 _) (D4 _) = zero
bracket D0 D0 = zero
bracket D0 (D2 _ _) = zero
bracket (D2 _ _) D0 = zero

-- {d, r^ij} and {d, r_ij}
bracket (T i j) D0 = D2 i j
bracket D0 (T i j) = minus $ bracket (T i j) D0
bracket (S _ _) D0 = zero
bracket D0 (S _ _) = zero

bracket (S i j) (D2 k l) = Sum [((δ i k) * (δ j l)) `Mult` D0, (-(δ i l) * (δ j k)) `Mult` D0]
bracket (D2 k l) (S i j) = minus $ bracket (S i j) (D2 k l)
bracket (T i j) (D2 k l) = Sum [fromIntegral (ε i j k l m) `Mult` D4 m | m <- [1..5]]  
bracket (D2 k l) (T i j) = minus $ bracket (T i j) (D2 k l)

bracket (S i j) (D4 k) = Sum [(0.5*fromIntegral (ε i j k l m)) `Mult` D2 l m | l <- [1..5], m <- [1..5]] 
bracket (D4 k) (S i j) = minus $ bracket (S i j) (D4 k)
bracket (T _ _) (D4 _) = zero
bracket (D4 _) (T _ _) = zero

-- {d,e^i} = {d,e_i} = 0
bracket D0 (E _) = zero
bracket (E _) D0 = zero
bracket D0 (F _) = zero
bracket (F _) D0 = zero
bracket (D2 _ _) (E _) = zero
bracket (E _) (D2 _ _) = zero
bracket (D2 _ _) (F _) = zero
bracket (F _) (D2 _ _) = zero
bracket (D4 _) (E _) = zero
bracket (E _) (D4 _) = zero
bracket (D4 _) (F _) = zero
bracket (F _) (D4 _) = zero

bracket' a b = rsimplify $ bracket (rsimplify a) (rsimplify b)

jacobi x y z = Sum [(x `bracket'` y) `bracket'` z, (y `bracket'` z) `bracket'` x, (z `bracket'` x) `bracket'` y]
jacobi' x y z = rsimplify $ jacobi (rsimplify x) (rsimplify y) (rsimplify z)

bffjacobi x y z = Sum [(x `bracket'` y) `bracket'` z, (y `bracket'` z) `bracket'` x, (-1) `Mult` ((z `bracket'` x) `bracket'` y)]
bffjacobi' x y z = rsimplify $ bffjacobi (rsimplify x) (rsimplify y) (rsimplify z)

simplify (S i j)
  | i < j = S i j
  | i == j = zero
  | i > j = minus (S j i)
simplify (T i j)
  | i < j = T i j
  | i == j = zero
  | i > j = minus (T j i)
simplify (D2 i j)
  | i < j = D2 i j
  | i == j = zero
  | i > j = minus (D2 j i)
simplify (Mult 0 a) = zero
simplify (Mult 1 a) = simplify a
simplify (Mult a (Sum [])) = zero
simplify (Mult a (Sum l)) = Sum $ map (Mult a) l
simplify (Mult a (Mult b c)) = Mult (a*b) c
simplify (Mult a b) = Mult a (simplify b)
simplify (Sum []) = zero
simplify (Sum [a]) = a
simplify (Sum (x:y:l)) | x == y = Sum $ (Mult 2 (simplify x)):(map simplify l)
simplify (Sum [Mult c a,Mult d b]) | a == b = Mult (c+d) (simplify a)
simplify (Sum (x:Mult a y:l)) | x == y = Sum $ (Mult (a+1) x):(map simplify l)
simplify (Sum (Mult a x:Mult b y:l)) | x == y = Sum $ (Mult (a+b) x):(map simplify l)
simplify (Sum [a, Mult (-1) b]) | a == b = zero
simplify (Sum [a,b,Mult (-1) c, Mult (-1) d]) | a == c && b == d = zero
simplify (Sum [a,b,c, Mult (-1) d, Mult (-1) e, Mult (-1) f]) | a == d && b == e && c == f = zero
simplify (Sum l) = let
    f :: Term -> [Term]
    f (Sum x) = x
    f x = [x]
    in
    Sum $ filter (/= zero) (sort . (map simplify) . concat . (map f) $ l)
simplify a = a

rsimplify a = let a' = simplify a in if a == a' then a else rsimplify a'

b = [R i j | i <- [1..5], j <- [1..5]] ++ [S i j | i <- [1..5], j <- [i+1..5]] ++ [T i j | i <- [1..5], j <- [i+1..5]] ++ [E i | i <- [1..5]] ++ [F i | i <- [1..5]]
f = [D0] ++ [D2 i j | i <- [1..5], j <- [i+1..5]] ++ [D4 i | i <- [1..5]]

check = concat ([ if jacobi' x y z == zero then [] else [(x,y,z)] | x <- b, y <- b, z <- b ++ f]
                    ++ [ if bffjacobi' x y z == zero then [] else [(x,y,z)] | x <- b, y <- f, z <- f])
