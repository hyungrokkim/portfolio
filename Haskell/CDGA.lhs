> {-# LANGUAGE FlexibleInstances #-}
> module CDGA where

> import Control.Monad
> import Control.Arrow ((&&&))
> import Data.List
> import Data.Ord
> import Data.Monoid
> import Data.Map (Map, mapWithKey, unionWith)
> import qualified Data.Map as Map
> import qualified Data.Set as Set (toList, unions)
> import Kernel (Matrix, nullVectors)

Class for things with integer degrees.

> class Degreed a where
>   deg :: a -> Integer

A list, thought of as products of terms.

> instance Degreed a => Degreed [a] where
>   deg = sum . map deg

Terms with coeffs

> instance (Degreed a, Num t) => Degreed (t, a) where
>   deg = deg . snd

Canonicalize a term
Bool = False for coeff 1, True for coeff -1.

> canonicalize :: (Eq t, Num t, Ord a, Degreed a) => Map [a] t -> Map [a] t
> canonicalize p = Map.filter (/=0) $ Map.unionsWith (+) [f t $ canonicalize1 $ x | (x,t) <- Map.toList p] where
>   f :: Num b => b -> Maybe (Bool, [a]) -> Map [a] b
>   f t Nothing = Map.empty
>   f t (Just (False, l)) = Map.singleton l t
>   f t (Just (True, l)) = Map.singleton l (-t)

> canonicalize1 :: (Degreed a, Ord a) => [a] -> Maybe (Bool, [a])
> canonicalize1 l =
>   let evens = sort . filter (even . deg) $ l
>       odds = isort . filter (odd . deg) $ l
>   in do
>       (p, l) <- odds
>       return (p, l ++ evens)

Take the derivative of a term.

=== Derivation; product rule ===

> class Degreed a => Derivable a where
>   deriv :: (Num t, Eq t) => a -> Map [a] t

> derivPoly :: (Num t, Eq t, Ord a, Derivable a) => Map [a] t-> Map [a] t
> derivPoly = derivGen deriv

> derivGen :: (Num t, Eq t, Ord a, Degreed a) => (a -> Map [a] t) -> Map [a] t -> Map [a] t
> derivGen d a = sum [fmap (*t) $ deriv1 d x | (x, t) <- Map.toList a]

Function for deriving monomials

> deriv1 :: (Num t, Eq t, Ord a, Degreed a) => (a -> Map [a] t) -> [a] -> Map [a] t
> deriv1 _ [] = 0
> deriv1 dmap (x:xs) = Map.fromList [(y ++ xs, t) | (y,t) <- Map.toList $ dmap x] + ((if even (deg x) then id else negate) $ Map.fromList [(x:ys, t) | (ys,t) <- Map.toList $ deriv1 dmap xs])

Utility for constructing a monomial

> singleTerm a = Map.singleton [a] 1

=== Finding closed elements ===
Given a list of monomials, find a basis for the kernel of the derivation map. (TODO: generalize to non-monomials if/when necessary.)

> closed :: (Fractional t, Eq t, Ord a, Derivable a) => [[a]] -> [Map [a] t]
> closed js = map (canonicalize . Map.fromList . zip js) $ nulls
>   where
>     nulls = nullVectors . toMatrix js $ canonicalize . derivPoly . flip Map.singleton 1

> toMatrix :: (Num t, Ord b) => [a] -> (a -> Map b t) -> Matrix t
> toMatrix js m = ([[Map.findWithDefault 0 i (m j)  | j <- js] | i <- Set.toList is], length js) where
>   is = Set.unions . map (Map.keysSet . m) $ js

Convenience function for getting all values of an enumerated type

> values_ :: (Bounded a, Enum a) => a -> [a]
> values_ = const [minBound..]

=== L∞-algbras ===
Here we implement the coversion from a semifree DGA to an L∞-algebra.

The formula is: if the L∞-basis is t_a, with the dual basis t^a,

  dt^a = - \sum_n (1/n!) \sum_{b₁, …, b_n} t^a([t_b₁, t_b₂, ..., t_b_n]) t^b₁ t^b₂ … t^b_n

Concretely,

  1. Canonicalize the input order, and remember the sign s = ±1.
  2. For each basis element, compute the differential, and look up the canonicalized ordered input.
  3. Assemble the result of (2) into a Map.
  4. Multiply all coefficients by -s.

> bracket :: (Num t, Eq t, Ord t, Ord a, Bounded a, Enum a, Derivable a) => [a] -> Map a t
> bracket xs_noncanon = case canonicalize1 xs_noncanon of 
>   Nothing -> Map.empty
>   Just (s, xs) -> fmap (if s then id else negate) . Map.mapMaybe (Map.lookup xs . deriv) . Map.fromList . map (id &&& id) . values_ . head $ xs

=== Utilities ===
Given a list of Ints, find the combinations that sum to k
Assumes that all entries are nonnegative

> sumCombination :: (Ord b, Num b) => b -> (a -> b) -> [a] -> [[a]]
> sumCombination k _ _ | k < 0 = undefined
> sumCombination 0 _ [] = [[]]
> sumCombination k _ [] = []
> sumCombination k f (x:xs)
>   | f x <= k = [x:ys | ys <- sumCombination (k - f x) f xs] ++ sumCombination k f xs
>   | otherwise = sumCombination k f xs

Sorting, but keeps track of parity
Bool = False if even, True if odd parity.

> isort :: Ord a => [a] -> Maybe (Bool, [a])
> isort [] = Just (False, [])
> isort xs = let
>  (i, m) = minimumBy (comparing snd) . zip [0..] $ xs
>  uniq = [x | x <- xs, x == m] == [m]
>  ne = isort [x | x <- xs, x /= m]
>  in do
>      guard uniq
>      (p, l) <- ne
>      return (p /= odd i, m : l)

Above, /= is the xor operation for bools

Implement a monoid algebra.

> instance (Monoid a, Ord a, Num t, Eq t) => Num (Map a t) where
>   a + b = Map.filter (/= 0) $ unionWith (+) a b
>   negate = fmap negate
>   a * b =  Map.filter (/= 0) $ Map.fromListWith (+) [(k <> k2, v * v2) | (k,v) <- Map.toList a, (k2,v2) <- Map.toList b]
>   abs = undefined
>   signum = undefined
>   fromInteger 0 = Map.empty
>   fromInteger n = Map.singleton mempty (fromInteger n)

> showPoly :: (Show a, Show t, Eq t, Num t) => Map [a] t -> String
> showPoly m | Map.null m = "0"
> showPoly m = intercalate " + " . map (\(k, v) -> (if v == 1 then "" else show v ++ " ") ++ (if null k then "1" else concatMap show k)) . Map.toList $ m
> monomial a = Map.singleton a 1

