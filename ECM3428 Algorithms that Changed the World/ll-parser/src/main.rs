use std::{
    collections::{HashMap, HashSet},
    env, fmt,
};

#[derive(Copy, Clone, Eq, PartialEq, Hash)]
enum Terminal {
    Empty,
    Id,
    LParen,
    RParen,
    Plus,
    Mult,
    Eos,
}

impl Terminal {
    fn from_char(c: char) -> Option<Terminal> {
        match c {
            '0'..='9' => Some(Terminal::Id),
            'a'..='z' | 'A'..='Z' => Some(Terminal::Id),
            '(' => Some(Terminal::LParen),
            ')' => Some(Terminal::RParen),
            '+' => Some(Terminal::Plus),
            '*' => Some(Terminal::Mult),
            _ => None,
        }
    }
}

impl fmt::Debug for Terminal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Terminal::Empty => write!(f, "ε"),
            Terminal::Id => write!(f, "id"),
            Terminal::LParen => write!(f, "("),
            Terminal::RParen => write!(f, ")"),
            Terminal::Plus => write!(f, "+"),
            Terminal::Mult => write!(f, "*"),
            Terminal::Eos => write!(f, "$"),
        }
    }
}

impl Into<Symbol> for Terminal {
    fn into(self) -> Symbol {
        Symbol::T(self)
    }
}

#[derive(Copy, Clone, Eq, PartialEq, Hash)]
enum Nonterminal {
    E,
    Ep,
    T,
    Tp,
    F,
}

impl fmt::Debug for Nonterminal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Nonterminal::E => write!(f, "E"),
            Nonterminal::Ep => write!(f, "E'"),
            Nonterminal::T => write!(f, "T"),
            Nonterminal::Tp => write!(f, "T'"),
            Nonterminal::F => write!(f, "F"),
        }
    }
}

impl Into<Symbol> for Nonterminal {
    fn into(self) -> Symbol {
        Symbol::NT(self)
    }
}

#[derive(Copy, Clone, Eq, Hash, PartialEq)]
enum Symbol {
    T(Terminal),
    NT(Nonterminal),
}

impl fmt::Debug for Symbol {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Symbol::T(t) => write!(f, "{:?}", t),
            Symbol::NT(nt) => write!(f, "{:?}", nt),
        }
    }
}

impl Symbol {
    fn to_terminal(self) -> Option<Terminal> {
        match self {
            Symbol::T(t) => Some(t),
            _ => None,
        }
    }

    fn to_nonterminal(self) -> Option<Nonterminal> {
        match self {
            Symbol::NT(nt) => Some(nt),
            _ => None,
        }
    }
}

type ProductionBody = Vec<Symbol>;
type Grammar = HashMap<Nonterminal, Vec<ProductionBody>>;

/// Compute the FIRST set for a given symbol in the given grammar
fn first(x: Symbol, grammar: &Grammar) -> HashSet<Terminal> {
    match x {
        Symbol::T(terminal) => return HashSet::from([terminal]), // If X is a terminal, FIRST(X) = { X }
        Symbol::NT(nonterminal) => {
            let mut firsts = HashSet::new();

            for production in grammar.get(&nonterminal).unwrap_or(&Vec::new()) {
                // If X -> 𝜖 is a production, 𝜖 is in FIRST(X)
                if *production == vec![Symbol::T(Terminal::Empty)] {
                    firsts.insert(Terminal::Empty);
                }

                let mut all_empty = true;

                for symbol in production {
                    let sym_first = first(*symbol, grammar);

                    for sym in &sym_first {
                        firsts.insert(*sym);
                    }

                    if !sym_first.contains(&Terminal::Empty) {
                        all_empty = false;
                        break;
                    }
                }

                if all_empty {
                    firsts.insert(Terminal::Empty);
                }
            }

            return firsts;
        }
    }
}

/// Compute the FOLLOW sets for all nonterminals in the given grammar with the given start symbol
fn follow_sets(
    grammar: &Grammar,
    start_symbol: Nonterminal,
) -> HashMap<Nonterminal, HashSet<Terminal>> {
    let mut follows: HashMap<Nonterminal, HashSet<Terminal>> = HashMap::new();

    // Initialise the follow sets
    for nonterminal in grammar.keys() {
        follows.insert(*nonterminal, HashSet::new());
    }

    // Add $ to FOLLOW(S)
    follows
        .get_mut(&start_symbol)
        .unwrap()
        .insert(Terminal::Eos);

    let mut changed = true;

    while changed {
        changed = false;

        for (a, productions) in grammar.iter() {
            for production in productions.iter() {
                for i in 0..production.len() {
                    if let Some(b) = production[i].to_nonterminal() {
                        let mut beta_first: HashSet<Terminal> = HashSet::new();
                        let mut can_be_empty = true;

                        for j in (i + 1)..production.len() {
                            let sym_first = first(production[j], grammar);

                            for &t in &sym_first {
                                if t != Terminal::Empty {
                                    beta_first.insert(t);
                                }
                            }

                            if !sym_first.contains(&Terminal::Empty) {
                                can_be_empty = false;
                                break;
                            }
                        }

                        for t in beta_first {
                            if follows.get_mut(&b).unwrap().insert(t) {
                                changed = true;
                            }
                        }

                        if can_be_empty {
                            let follow_a = follows.get(a).unwrap().clone();

                            for &t in &follow_a {
                                if follows.get_mut(&b).unwrap().insert(t) {
                                    changed = true;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    follows
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        println!("Correct usage: {} <input string>", args[0]);
        return;
    }

    // Define the grammar
    // A production is an entry in this Hash Map, with the key as the head and the value as the body.
    // The body is a vec, where each entry is one of the possible derivations.
    // Each derivation is itself a vec of the symbols in the derivation.

    // This grammar produces arithmetic expressions, from example 4.11 in Compilers: Principles, Techniques, and Tools
    // We have to use this more verbose syntax to eliminate left recursion
    let grammar: Grammar = HashMap::from([
        (
            // E -> TE'
            Nonterminal::E,
            vec![vec![Nonterminal::T.into(), Nonterminal::Ep.into()]],
        ),
        (
            // E' -> +TE' | e
            Nonterminal::Ep,
            vec![
                vec![
                    Terminal::Plus.into(),
                    Nonterminal::T.into(),
                    Nonterminal::Ep.into(),
                ],
                vec![Terminal::Empty.into()],
            ],
        ),
        (
            // T -> FT'
            (
                Nonterminal::T,
                vec![vec![Nonterminal::F.into(), Nonterminal::Tp.into()]],
            )
        ),
        (
            // T' -> *FT' | e
            Nonterminal::Tp,
            vec![
                vec![
                    Terminal::Mult.into(),
                    Nonterminal::F.into(),
                    Nonterminal::Tp.into(),
                ],
                vec![Terminal::Empty.into()],
            ],
        ),
        (
            // F -> (E) | id
            Nonterminal::F,
            vec![
                vec![
                    Terminal::LParen.into(),
                    Nonterminal::E.into(),
                    Terminal::RParen.into(),
                ],
                vec![Terminal::Id.into()],
            ],
        ),
    ]);

    let start_symbol = Nonterminal::E;

    // Construct the parsing table
    let follows = follow_sets(&grammar, start_symbol);

    let mut table: HashMap<(Nonterminal, Terminal), ProductionBody> = HashMap::new();
    for (head, productions) in &grammar {
        for production in productions {
            let mut production_firsts = HashSet::new();
            let mut can_derive_empty = true;

            // Compute FIRST set of the production
            for symbol in production {
                let sym_first = first(*symbol, &grammar);
                for &t in &sym_first {
                    if t != Terminal::Empty {
                        production_firsts.insert(t);
                    }
                }
                if !sym_first.contains(&Terminal::Empty) {
                    can_derive_empty = false;
                    break;
                }
            }

            // Add production to table for terminals in FIRST set
            for &terminal in &production_firsts {
                if terminal != Terminal::Empty {
                    table.insert((*head, terminal), production.clone());
                }
            }

            // If production can derive ε, add it for terminals in FOLLOW set
            if can_derive_empty || *production == vec![Symbol::T(Terminal::Empty)] {
                let follow_set = follows.get(head).unwrap();
                for &terminal in follow_set {
                    table.insert((*head, terminal), production.clone());
                }
            }
        }
    }

    // Initialise the stack
    // A rust Vec can function as a stack
    let mut stack: Vec<Symbol> = vec![Terminal::Eos.into(), start_symbol.into()];

    println!();

    // Initialise the input string
    let input = args[1]
        .chars()
        .map(|c| {
            Terminal::from_char(c)
                .expect(&format!("Input contains symbol not in alphabet: '{}'", c))
        })
        .chain(std::iter::once(Terminal::Eos)) // Append $ to the end of the input
        .collect::<Vec<Terminal>>();
    println!("{} => {:?}", args[1], input);

    let mut p = 0; // Input pointer

    // The parsing loop
    println!("\n {: <10} | {: <10} | {: <20} ", "stack", "input", "action");
    while !stack.is_empty() {

        // Print the current stack and input
        let stack_str = stack
            .iter()
            .map(|s| format!("{:?}", s))
            .collect::<Vec<String>>()
            .join("");

        let input_str = input[p..]
            .iter()
            .map(|t| format!("{:?}", t))
            .collect::<Vec<String>>()
            .join("");

        print!(" {: <10} | {: >10} | ", stack_str, input_str);

        if let Some(top) = stack.last() {
            if let Some(t) = top.to_terminal() {
                if t == input[p] {
                    p += 1;
                    stack.pop();
                } else if t == Terminal::Empty {
                    stack.pop();
                } else {
                    println!("Syntax error: Expected {:?}, found {:?}", t, input[p]);
                    return;
                }
            } else if let Some(nt) = top.to_nonterminal() {
                if let Some(production) = table.get(&(nt, input[p])) {
                    stack.pop();
                    let mut production = production.clone();

                    // Print the production used
                    print!("{} -> ", format!("{:?}", nt));
                    for sym in &production {
                        print!("{:?}", sym);
                    }

                    production.reverse();
                    stack.append(&mut production);
                } else {
                    println!("Syntax error: No production for ({:?}, {:?})", nt, input[p]);
                    return;
                }
            }
        }

        println!();
    }

    println!("\nFinished parsing");
}
