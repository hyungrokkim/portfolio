> module Kernel where
> import Data.List (find, elemIndex)
> import Data.Maybe (maybeToList, fromMaybe)
> import Control.Monad (guard)

Replaces the element at the given index.

> replace :: Int -> a -> [a] -> [a]
> replace n e l = a ++ e : b
>   where (a, _ : b) = splitAt n l

A matrix data type. We need to store the number of columns for the degenerate case of n×0 matrices.

> type Matrix a = ([[a]], Int) -- ncols
> nrows :: Matrix a -> Int
> nrows (m, _) = length m
> ncols (_, j) = j
> getCol i (m, _) = map (!! pred i) m

> rref :: (Fractional t, Eq t) => Matrix t -> Matrix t
> rref mm = (f m 0 [0 .. rows - 1], cols)
>   where
>         (m, cols) = mm
>         rows = nrows mm
>         f m _    []              = m
>         f m lead (r : rs)
>             | indices == Nothing = m
>             | otherwise          = f m' (lead' + 1) rs
>           where indices = find p l
>                 p (col, row) = m !! row !! col /= 0
>                 l = [(col, row) |
>                     col <- [lead .. cols - 1],
>                     row <- [r .. rows - 1]]
>                 Just (lead', i) = indices
>                 newRow = map (/ m !! i !! lead') $ m !! i
>                 m' = zipWith g [0..] $
>                     replace r newRow $
>                     replace i (m !! r) m
>                 g n row
>                     | n == r    = row
>                     | otherwise = zipWith h newRow row
>                   where h = subtract . (* row !! lead')

Construct a basis for the kernel from the reduced row echelon form

e.g.
  [0  1  2  0]
  [0  0  3  1]
has dimension 2 kernel

e. g. 

[1 0]
[0 1]
has dim 0 kernel

rank: # of 1s
coimage: # of null rows
kernel: # of columns that do not map to the rows

> echelonCols (m, ncols) = concat . map (maybeToList . elemIndex 1) $ m
> colToRow (m, cols) j = find (\r -> elemIndex 1 r == Just j) m
> nullVector (m, cols) j = let
>    f j jj
>      | jj == j = 1
>      | otherwise = negate $ (fromMaybe (repeat 0) $ colToRow (m, cols) jj) !! j
>   in do
>     guard $ not (j `elem` echelonCols (m, cols))
>     return $ map (f j) [0..cols-1]

> nullVectors (m, cols) = concat . map (maybeToList . nullVector (rref (m, cols))) $ [0..cols-1]


