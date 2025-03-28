 main :-
    generator4(X), selector4(X), write(X).

selector4([[M1, D1, S1], [M2, D2, S2]]) :-
    T1 is D1,
    U1 is D2,

    letters(M1, T2),
    letters(M2, U2),

    primes(M1, T3),
    primes(M2, U3),

    mondays(D1, S1, MS1),
    length(MS1, T4),
    mondays(D2, S2, MS2),
    length(MS2, U4),

    prime_sats(D1, S1, SS1),
    length(SS1, T5),
    prime_sats(D2, S2, SS2),
    length(SS2, U5),

    prime(T1 + T2 + T3 + T4 + T5),
    prime(U1 + U2 + U3 + U4 + U5),

    T1 =\= U1,
    T2 =\= U2,
    T3 =\= U3,
    T4 =\= U4,
    T5 =\= U5.

% letters/2 was generated with GenAI
letters(1, 7).  % January
letters(2, 8).  % February
letters(3, 5).  % March
letters(4, 5).  % April
letters(5, 3).  % May
letters(6, 4).  % June
letters(7, 4).  % July
letters(8, 6).  % August
letters(9, 9).  % Septembe
letters(10, 7)  % October
letters(11, 8)  % November
letters(12, 8)  % December

prime_sats(D, S, SS) :-
    findall(X, prime_saturday(D, S, X), SS).

prime_saturday(D, S, X) :-
    saturday(D, S, X),
    prime(X).

primes(M, N) :-
    month_length(M, DS),
    findall(D, (between(1, DS, D), prime(D)), PDS),
    length(PDS, N).

prime(N)
  :- N > 1, \+ factorisable(2, N).

factorisable(F, N)
  :- F * F =< N,
     0 is N mod F.
factorisable(F, N)
  :- F * F =< N,
     F1 is F + 1,
     factorisable(F1, N).

generator4([[M1, D1, S1], [M2, D2, S2]]) :-
    between(1, 12, M1),
    successor(M1, M2, 12),
    month_length(M1, D1),
    month_length(M2, D2),
    between(1, 7, S1),
    SX is (S1 + (D1 mod 7)) mod 7,
	day_fix(SX, S2).

day_fix(0, 7).
day_fix(X, X).

successor(X1, X2, Max) :-
    X1 < Max,
    X2 is X1 + 1.
successor(Max, 1, Max).

saturday(D, S, X) :-
    between(0, D, N),
    O is (8 - S) mod 7,
    X is (7 * N) + O - 1,
    X =< D.

mondays(D, S, MS) :-
    findall(M, monday(D, S, M), MS).

monday(D, S, M) :-
    between(0, D, N),
    O is (8 - S) mod 7,
    M is 1 + (7 * N) + O,
    M =< D.

% month_length/2 was generated with GenAI
month_length(M, D) :-
    member(M, [1, 3, 5, 7, 8, 10, 12]),
    D is 31.
month_length(M, D) :-
    member(M, [4, 6, 9, 11]),
    D is 30.
month_length(2, D) :-
    D is 28.
month_length(2, D) :-
    D is 29.
