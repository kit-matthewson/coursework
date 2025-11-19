
# Setting up Rust
Rust can be installed from https://rust-lang.org/tools/install/.

# Running the program
The parsing program will work on any grammar, but I have only provided a grammar definition for arithmetic expressions that contain the multiplication or addition of identifiers, possibly with brackets. Identifiers can be any number or letter.

For example:
- `2+2`
- `(a+b)*3`
- `x+(x*(x+(x+x)))`

## Running the tests
Run `cargo test` to execute the provided tests.

## Running on your own input
To run from the command line, execute:
`cargo run "<expression>"`
For example:
- `cargo run "2+2"`
- `cargo run "(a+b)*3"`
- `cargo run "x+(x*(x+(x+x)))"`
This will produce an output showing how the input has been tokenised:
```
Tokenised:
 '2+2' => [id, +, id, $]  
```
And a table showing the execution of the parser:
```
 stack                          | input                          | action
 $E                             |                         id+id$ | E -> TE'
 $E'T                           |                         id+id$ | T -> FT'
 $E'T'F                         |                         id+id$ | F -> id
 $E'T'id                        |                         id+id$ |
 $E'T'                          |                           +id$ | T' -> ε
 $E'ε                           |                           +id$ |
 $E'                            |                           +id$ | E' -> +TE'
 $E'T+                          |                           +id$ |
 $E'T                           |                            id$ | T -> FT'
 $E'T'F                         |                            id$ | F -> id
 $E'T'id                        |                            id$ |
 $E'T'                          |                              $ | T' -> ε
 $E'ε                           |                              $ |
 $E'                            |                              $ | E' -> ε
 $ε                             |                              $ |
 $                              |                              $ |
```
Followed by an error message if one occurs and a statement as to whether the input was valid.
