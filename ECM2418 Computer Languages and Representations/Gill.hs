import Data.List

main :: IO ()
main
 = print (filter selector1 generator1)

number :: [Int] -> Int
number []
 = 0
number ys
 = number (reverse xs) * 10 + x
 where
    (x:xs) = reverse ys

generator1 :: [([Int],[Int],[Int])]
generator1
 = [([a,b,c],[d,e,f],[g,h,i]) | [a,b,c,d,e,f,g,h,i,_] <- permutations [0..9]]

selector1 :: ([Int],[Int],[Int]) -> Bool
selector1 (a,b,c)
 =  validDigits a && validDigits b && validDigits c &&
    isPrime x && isPrime y && isPrime z &&
    (z - y) == (y - x)
 where
    x = number a
    y = number b
    z = number c

validDigits :: [Int] -> Bool
validDigits [a, b, c]
 = (a + b + c) /= 2 && isPrime (a + b + c)

isPrime :: Int -> Bool
isPrime n
    | n < 2 = False
    | otherwise = not (factorisable n 2)
 where
    factorisable :: Int-> Int-> Bool
    factorisable n i
        | i * i > n = False
        | otherwise = mod n i == 0 || factorisable n (i + 1)
