> {-# LANGUAGE FlexibleContexts #-}
> import CDGA (Degreed, Derivable, deriv, canonicalize, showPoly, sumCombination, deg, singleTerm, derivPoly, closed, values_)
> import Kernel (Matrix, nullVectors)
> import Data.Foldable (for_)
> import Data.Ratio (Rational)
> import qualified Data.Map as Map
> import Data.Map (Map, singleton)
> import qualified Data.Set as Set (toList, unions)
> import Weil (Weil, invariant_)

== 6D case ==

> data Generators6D = B₁ | B₂ | B₃ | C₁ | C₂ | C₃ deriving (Eq, Ord, Show, Bounded, Enum)
> instance Degreed Generators6D where
>   deg B₁ = 2
>   deg B₂ = 2
>   deg B₃ = 2
>   deg C₁ = 3
>   deg C₂ = 3
>   deg C₃ = 3
> instance Derivable Generators6D where
>   deriv C₁ = singleton [B₁, B₁] (-1)
>   deriv C₂ = singleton [B₂, B₂] (-1)
>   deriv C₃ = singleton [B₃, B₃] (-1)
>   deriv _ = 0

   c1 = Symbol "C₁" 3 $ (singleton [b1, b2, b3] (-1))
   c2 = Symbol "C₂" 3 $ (singleton [b1, b2, b3] (-1))
   c3 = Symbol "C₃" 3 $ (singleton [b1, b2, b3] (-1))

== 4D case, SU(2)×U(1) ==

 generators4D :: [(Symbol, Polynomial Rational)]
 generators4D = [
    (a0, 0),
    (a1, singleton [a2, a3] (-1)),
    (a2, singleton [a3, a1] (-1)),
    (a3, singleton [a1, a2] (-1)),
    (Symbol "B₀" 2, singleton [a1, a2, a3] (-1)),
    (b1, singleton [a0, a2, a3] 1 + singleton [a2, b3] (-1) + singleton [a3, b2] 1),
    (b2, singleton [a0, a3, a1] 1 + singleton [a3, b1] (-1) + singleton [a1, b3] 1),
    (b3, singleton [a0, a1, a2] 1 + singleton [a1, b2] (-1) + singleton [a2, b1] 1)
  ] where
   a0 = Symbol "A₀" 1 
   a1 = Symbol "A₁" 1
   a2 = Symbol "A₂" 1
   a3 = Symbol "A₃" 1
   b1 = Symbol "B₁" 2
   b2 = Symbol "B₂" 2
   b3 = Symbol "B₃" 2

== Main printing routine ==

We suffix with _ functions that take a dummy argument purely for type deduction.

> main = main_invariants

> main_gaugeTransform = values_ (undefined :: Generators6D)

Search through all values, whose higher bracket equals it. (Because of degree restrictions, only a finite number of such things exist.)

  where
    c :: Generators6D
    g :: [a]
    g = values_ (undefined :: Generators6D)
    candidates :: [[a]]
    candidates = sumCombination (deg c + 1) deg g
    coeff :: [a] -> Rational
    coeff cand = Map.findWithDefault 0 c (bracket cand)
    print 

> main_cohomology = for_ [0 .. 15] $ showKernel_ (undefined :: Generators6D)

> main_invariants = for_ [0 .. 15] (\n -> do
>   putStrLn $ "Degree " ++ show n
>   sequence_ . map (putStrLn . showPoly) $ (invariant_ (undefined :: Generators6D) n :: [Map [Weil Generators6D] Rational])
>  )

> showKernel_ :: (Show a, Bounded a, Enum a, Ord a, Derivable a) => a -> Integer -> IO ()
> showKernel_ a n = do
>   putStrLn $ "Degree " ++ show n
>   sequence_ . map (putStrLn . showPoly) . closed . sumCombination n deg . values_ $ a

== Stupider version, where we don't do Gaussian elimination ==

> foo :: Degreed a => Integer -> [a] -> [Map [a] Rational]
> foo n = map (`singleton` (1 :: Rational)) . sumCombination n deg

> showDeg :: (Show a, Ord a, Derivable a) => [a] -> Integer -> IO ()
> showDeg g n = do
>   putStrLn ("Degree " ++ show n)
>   sequence_ $ map (putStrLn . showPoly . canonicalize) . filter (Map.null . canonicalize . derivPoly) $ foo n g

== Sanity check ==

Test whether exterior derivative is nilpotent as required:

> integrity_ :: (Bounded a, Enum a, Ord a, Derivable a) => a -> Bool
> integrity_ = and . map (Map.null . canonicalize . derivPoly . derivPoly . singleTerm) . values_

e.g. integrity_ B₁; True is the sane value.

