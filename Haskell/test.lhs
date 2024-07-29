\documentclass{article}
\usepackage{amsmath}
%include polycode.fmt
%format minimum a = "\min" a
%format filter (a) b = "\operatorname*{filter}_{" a "}\limits" b
%format div a b = a "\setminus" b
%format `div` = "\setminus"
\title{Sorting Algorithms in Haskell}
\author{Hyungrok Kim}
\begin{document}
\maketitle
\section{Selection Sort}
Selection sort is the simplest sorting algorithm: extract the
least element, extract the next least, etc. It runs in
\(\Theta(n^2)\) time.
\begin{code}
ssort :: Ord a => [a] -> [a]
ssort [] = []
ssort x  = m : (filter (/= m) x) where m = minimum x
\end{code}

\section{Insertion sort}
Insertion sort is another primitive sorting algorithm. With
insertion sort, each element is inserted into the correct place
in order, thus the name. It runs in \(\Theta(n^2)\) time.
\begin{code}
insert :: a -> [a] -> [a]
insert x [] = [x]
insert x (y:ys)
  | x <  y  = x : y : ys
  | x >= y  = y : (insert x ys)

isort :: Ord a => [a] -> [a]
isort []     = []
isort (x:xs) = insert x (isort xs)
\end{code}

\section{Quick sort}
Quick sort is a divide-and-conquer algorithm: each array is pivoted by an
element (the first one in this implementation) and the two subarrays are
sorted recursively. On average, it is \(\Theta(n\log n)\), though the
worst-case is \(\Theta(n^2)\).
\begin{code}
qsort :: Ord a => [a] -> [a]
qsort []    = []
qsort(x:xs) = qsort (filter (< x) xs) ++ [x] ++ qsort (filter (>= x) xs)
\end{code}

\section{Merge sort}
Merge sort is another divide-and-conquer algorithm: divide,
sort recursively, and merge the sorted subarrays. It is always \(\Theta(n\log n)\).
\begin{code}
merge :: Ord a => [a] -> [a] -> [a]
merge x [] = x
merge [] x = x
merge (x:xs) (y:ys)
  | x <  y = x : merge xs (y:ys)
  | x >= y = y : merge (x:xs) ys

msort :: Ord a => [a] -> [a]
msort []  = []
msort [x] = [x]
msort x   = merge (msort a) (msort b)
            where (a, b) = splitAt (length x `div` 2) x
\end{code}
\end{document}