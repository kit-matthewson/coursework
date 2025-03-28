 main :-
    generator3(X), selector3(X), write(X).

number([], 0).
number([X|XS], N) :-
    number(XS, N1),
    length(XS, L),
    N is X * 10^L + N1.

generator3([AS, BS]) :-
    permutation([1, 2, 3, 4, 5, 6, 7, 8, 9], XS),
    cut(XS, AS, BS).

cut([A, B], [A], [B]).
cut([H|T], [H|AS], BS) :-
    cut(T, AS, BS).
cut([H|T], AS, [H|BS]) :-
    cut(T, AS, BS).

selector3([AS, BS]) :-
    number(AS, A),
    number(BS, B),

    Product is A * B,
    palindrome(Product),
    Product mod 10 =:= 4,

    min(A, B, Min),
    Min mod 10 =:= 3,

    Sum is A + B + 100,
    palindrome(Sum).

palindrome(N) :-
    number_codes(N, Digits), % number(N, Digits) does not work. This function was suggested by GenAI.
    reverse(Digits, Digits).

min(X, Y, X) :- X =< Y.
min(X, Y, Y) :- X > Y.
