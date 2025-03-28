import Data.List

main :: IO ()
main =
  print (filter selector2 generator2)

digits :: Int -> [Int]
digits 0 = [0]
digits n = reverse (rdigits n)
  where
    rdigits 0 = []
    rdigits n = mod n 10 : rdigits (div n 10)

generator2 :: [(Int, Int, Int, Int, Int, Int, Int, Int)]
  -- select an x, where x must be <23 because otherwise there wont be enough other numbers
  -- get all the 'unique squares' greater than x
  -- get all the subsequences of length 7 of these
  -- get all permutations of these subsequences
generator2 =
  [(a, b, c, x, d, e, f, g) | x <- filter (< 23) uniqueSquares, ys <- validSubsequences (filter (> x) uniqueSquares), [a, b, c, d, e, f, g] <- permutations ys]

validSubsequences :: [Int] -> [[Int]]
validSubsequences xs = [ys | ys <- subsequences xs, length ys == 7]

uniqueSquares :: [Int]
-- a unique square is a number that squares to a number with three unique digits
uniqueSquares =
  [x | x <- [13 .. 31], unique_digits (x * x)]
  where
    unique_digits n =
      length (nub (digits n)) == length (digits n)

selector2 :: (Int, Int, Int, Int, Int, Int, Int, Int) -> Bool
selector2 (a, b, c, d, e, f, g, h) =
  and ([valid p q | p <- name_num_pairs, q <- name_num_pairs, p /= q])
  where
    name_num_pairs = zip ["alan", "cary", "james", "lucy", "nick", "ricky", "steve", "victor"] [a, b, c, d, e, f, g, h]

    valid :: (String, Int) -> (String, Int) -> Bool
    valid (a, x) (b, y) =
      if hasCommonLetters a b then
          hasCommonSquareDigits x y
        else
          not (hasCommonSquareDigits x y)

hasCommonSquareDigits :: Int -> Int -> Bool
hasCommonSquareDigits a b =
  not (null (intersect (digits (a * a)) (digits (b * b))))

hasCommonLetters :: String -> String -> Bool
hasCommonLetters a b =
  not (null (intersect a b))
