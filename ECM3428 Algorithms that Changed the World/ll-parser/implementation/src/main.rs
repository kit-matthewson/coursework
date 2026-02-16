use std::{
    collections::{HashMap, HashSet},
    env, fmt,
};

/// The possible terminals in the grammar. `Eos` is the end of input marker.
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
    /// Converts a `char` to a `Terminal` with basic matching.
    /// Note that at this stage of parsing we do not care about the exact values of identifiers.
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
    /// Convert this `Terminal` to a string.
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
    /// Convert this `Terminal` into a `Symbol`.
    fn into(self) -> Symbol {
        Symbol::T(self)
    }
}

/// The Non-Terminals needed for the grammar.
#[derive(Copy, Clone, Eq, PartialEq, Hash)]
enum Nonterminal {
    E,
    Ep,
    T,
    Tp,
    F,
}

impl fmt::Debug for Nonterminal {
    /// Convert this `Nonterminal` to a string.
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
    /// Convert this `Nonterminal` into a `Symbol`.
    fn into(self) -> Symbol {
        Symbol::NT(self)
    }
}

/// Either a Terminal or Non-Terminal.
#[derive(Copy, Clone, Eq, Hash, PartialEq)]
enum Symbol {
    T(Terminal),
    NT(Nonterminal),
}

impl fmt::Debug for Symbol {
    /// Convert this `Symbol` into a string by converting the underlying `Terminal` or `Nonterminal`.
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Symbol::T(t) => write!(f, "{:?}", t),
            Symbol::NT(nt) => write!(f, "{:?}", nt),
        }
    }
}

impl Symbol {
    /// Try and get the `Terminal` contained in this `Symbol`.
    /// Returns `None` if the symbol is a non-terminal.
    fn to_terminal(self) -> Option<Terminal> {
        match self {
            Symbol::T(t) => Some(t),
            _ => None,
        }
    }

    /// Try and get the `Nonterminal` contained in this `Symbol`.
    /// Returns `None` if the symbol is a terminal.
    fn to_nonterminal(self) -> Option<Nonterminal> {
        match self {
            Symbol::NT(nt) => Some(nt),
            _ => None,
        }
    }
}

// Type definitions for Production Bodies and Grammars
type ProductionBody = Vec<Symbol>;
type Grammar = HashMap<Nonterminal, Vec<ProductionBody>>;

/// Compute the FIRST set for a given symbol in the given grammar
fn first(x: Symbol, grammar: &Grammar) -> HashSet<Terminal> {
    match x {
        Symbol::T(terminal) => return HashSet::from([terminal]), // If X is a terminal, FIRST(X) = { X }
        Symbol::NT(nonterminal) => {
            let mut firsts = HashSet::new();

            for production in grammar.get(&nonterminal).unwrap_or(&Vec::new()) {
                // If X -> empty is a production, empty is in FIRST(X)
                if *production == vec![Symbol::T(Terminal::Empty)] {
                    firsts.insert(Terminal::Empty);
                }

                let mut all_empty = true;

                // If empty is in all the previous production symbol FIRST sets, then the FIRST set of this symbol is in our FIRST set.
                for symbol in production {
                    let sym_first = first(*symbol, grammar);

                    for sym in &sym_first {
                        firsts.insert(*sym);
                    }

                    if !sym_first.contains(&Terminal::Empty) {
                        // We can break when we find any symbol that can't produce empty.
                        all_empty = false;
                        break;
                    }
                }

                // If empty is in all production symbol FIRST sets, empty is in our FIRST set
                if all_empty {
                    firsts.insert(Terminal::Empty);
                }
            }

            return firsts;
        }
    }
}

/// Compute the FOLLOW sets for all nonterminals in the given grammar with the given start symbol.
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

    // We repeat this until nothing else is added
    let mut changed = true;
    while changed {
        changed = false;

        // For every production...
        for (a, productions) in grammar.iter() {
            for production in productions.iter() {
                // For every symbol in the RHS...
                for i in 0..production.len() {
                    // For each production a -> ... b ...
                    // We call the suffix of b 'beta'
                    // Everything is FIRST(beta) (except empty) is in FOLLOW(b)
                    if let Some(b) = production[i].to_nonterminal() {
                        let mut beta_first: HashSet<Terminal> = HashSet::new(); // FIRST(beta)
                        let mut can_be_empty = true; // True if beta can produce empty

                        // For each symbol of beta (beta[i], beta[i+1], ...), we add FIRST(beta[j]) to FOLLOW(b) until we find a FIRST(beta[j]) that does not contain empty
                        for j in (i + 1)..production.len() {
                            // Find FIRST(beta[j])
                            let sym_first = first(production[j], grammar);

                            // Add all non-empty terminals
                            for &t in &sym_first {
                                if t != Terminal::Empty {
                                    beta_first.insert(t);
                                }
                            }

                            // beta contains a terminal where FIRST(beta[i]) does not contain empty
                            // This means we can stop collecting the FIRSTs, and the suffix cannot produce empty
                            if !sym_first.contains(&Terminal::Empty) {
                                can_be_empty = false;
                                break;
                            }
                        }

                        for t in beta_first {
                            // Inserting to a `HashMap` returns `true` if the element was not already present
                            if follows.get_mut(&b).unwrap().insert(t) {
                                changed = true;
                            }
                        }

                        if can_be_empty {
                            // If the suffix can be empty, then everything in FOLLOW(a) is in FOLLOW(b)
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

fn construct_table(
    grammar: Grammar,
    start_symbol: Nonterminal,
) -> HashMap<(Nonterminal, Terminal), ProductionBody> {
    let follows = follow_sets(&grammar, start_symbol);

    let mut table = HashMap::new();
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
                    let mut production = production.clone();
                    production.reverse(); // The table expects productions in the reverse order for the stack
                    table.insert((*head, terminal), production);
                }
            }

            // If production can derive empty, add it for terminals in FOLLOW set
            if can_derive_empty || *production == vec![Symbol::T(Terminal::Empty)] {
                let follow_set = follows.get(head).unwrap();
                for &terminal in follow_set {
                    let mut production = production.clone();
                    production.reverse(); // The table expects productions in the reverse order for the stack
                    table.insert((*head, terminal), production);
                }
            }
        }
    }

    table
}

/// Perform the LL(1) parsing.
fn parse(
    table: HashMap<(Nonterminal, Terminal), ProductionBody>,
    start_symbol: Nonterminal,
    input: Vec<Terminal>,
    silent: bool,
) -> bool {
    if !silent {
        println!(
            "\n {: <20} | {: <20} | {: <20} ",
            "stack", "input", "action"
        );
    }

    // Initialise the stack
    // A `Vec` can function as a stack (it has pop and push methods)
    let mut stack: Vec<Symbol> = vec![Terminal::Eos.into(), start_symbol.into()];

    let mut p = 0; // Input pointer

    // The parsing loop
    while !stack.is_empty() {
        // Print the curent stack and input
        if !silent {
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

            print!(" {: <20} | {: >20} | ", stack_str, input_str);
        }

        if let Some(top) = stack.last() {
            if let Some(t) = top.to_terminal() {
                if t == input[p] {
                    p += 1;
                    stack.pop();
                } else if t == Terminal::Empty {
                    stack.pop();
                } else {
                    if !silent {
                        println!("Syntax Error: Expected '{:?}', found '{:?}'", t, input[p])
                    }
                    return false;
                }

                if !silent {
                    println!("'{:?}'", t);
                }
            } else if let Some(nt) = top.to_nonterminal() {
                if let Some(production) = table.get(&(nt, input[p])) {
                    if !silent {
                        // Print the production used
                        print!("{} -> ", format!("{:?}", nt));
                        for sym in production.iter().rev() {
                            print!("{:?}", sym);
                        }
                        println!()
                    }

                    stack.pop();
                    stack.append(&mut production.clone());
                } else {
                    if !silent {
                        println!("Syntax Error: No production for ({:?}, {:?})", nt, input[p])
                    }
                    return false;
                }
            }
        }
    }

    return true;
}

fn produce_arithmetic_grammar() -> Grammar {
    // Define the grammar
    // A production is an entry in this Hash Map, with the key as the head and the value as the body.
    // The body is a vec, where each entry is one of the possible derivations.
    // Each derivation is itself a vec of the symbols in the derivation.

    // This grammar produces arithmetic expressions, from example 4.11 in Compilers: Principles, Techniques, and Tools
    // We have to use this more verbose syntax to eliminate left recursion

    HashMap::from([
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
    ])
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        println!("Correct usage: {} <input string>", args[0]);
        return;
    }

    let grammar = produce_arithmetic_grammar();

    // Initialise the input string
    let input = args[1]
        .chars()
        .filter(|c| *c != ' ') // Remove spaces from the input
        .map(|c| {
            Terminal::from_char(c)
                .expect(&format!("Input contains symbol not in alphabet: '{}'", c))
        })
        .chain(std::iter::once(Terminal::Eos)) // Append $ to the end of the input
        .collect::<Vec<Terminal>>();

    println!("Tokenised:\n '{}' => {:?}", args[1], input);

    let start_symbol = Nonterminal::E;
    let table = construct_table(grammar, start_symbol);
    let valid = parse(table, start_symbol, input, false);

    println!("Valid input: {}", valid);
}

#[cfg(test)]
mod tests {
    use super::*;

    fn parses(input: &str) -> bool {
        let grammar = produce_arithmetic_grammar();

        let input = input
            .chars()
            .map(|c| Terminal::from_char(c).expect(&format!("Invalid char in test input: '{}'", c)))
            .chain(std::iter::once(Terminal::Eos)) // Append $ to the end of the input
            .collect::<Vec<Terminal>>();

        let start_symbol = Nonterminal::E;
        let table = construct_table(grammar, start_symbol);

        parse(table, start_symbol, input, true)
    }

    #[test]
    fn test_simple_addition() {
        assert!(parses("2+2"));
    }

    #[test]
    fn test_multiplication_and_parentheses() {
        assert!(parses("(a+b)*3"));
    }

    #[test]
    fn test_nested_expressions() {
        assert!(parses("x+(x*(x+(x+x)))"));
    }

    #[test]
    fn test_precedence_multiplication_over_addition() {
        assert!(parses("a+b*c"));
        assert!(parses("a*b+c"));
    }

    #[test]
    fn test_multiple_operators() {
        assert!(parses("a+b+c+d"));
        assert!(parses("a*b*c*d"));
    }

    #[test]
    fn test_mixed_operators_and_parens() {
        assert!(parses("(x+y)*(z+w)"));
        assert!(parses("a+(b*(c+d))"));
    }
    #[test]
    fn test_unbalanced_paren_left() {
        assert!(!parses("(a+b"));
    }

    #[test]
    fn test_unbalanced_paren_right() {
        assert!(!parses("a+b)"));
    }

    #[test]
    fn test_missing_operand() {
        assert!(!parses("a+"));
        assert!(!parses("*b"));
    }

    #[test]
    fn test_consecutive_operators() {
        assert!(!parses("a++b"));
        assert!(!parses("a*b+"));
    }
}
