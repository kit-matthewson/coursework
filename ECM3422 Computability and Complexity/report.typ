#let project(title: "", authors: (), body) = {
  // Set the document's basic properties.
  set document(author: authors, title: title)
  set page(numbering: "1", number-align: center)
  set text(font: "New Computer Modern", lang: "en")
  show math.equation: set text(weight: 400)
  set heading(numbering: "1.1.")

  // Set run-in subheadings, starting at level 3.
  show heading: it => {
    if it.level > 2 {
      parbreak()
      text(11pt, style: "italic", weight: "regular", it.body + ".")
    } else {
      it
    }
  }


  // Title row.
  align(center)[
    #block(text(weight: 700, 1.75em, title))
  ]

  // Author information.
  pad(
    top: 0.5em,
    bottom: 0.5em,
    x: 2em,
    grid(
      columns: (1fr,) * calc.min(3, authors.len()),
      gutter: 1em,
      ..authors.map(author => align(center, strong(author))),
    ),
  )

  // Main body.
  set par(justify: true)

  body
}

#show: project.with(title: "ECM3422: Computability and Complexity", authors: ("730002704",))

No AI was used to produce this assignment.

= Simple Solver
For my simple solver I first implemented classes for an abstract 'expression', a literal, and the two types of clauses. These make the solver implementation simpler by providing `evaluate` and `get_vars` functions to evaluate the expression (that is, determine its truth value given some assignment) and get the set of variables used in the expression respectively. These classes are also used in the optimised solver.

The solver works by recursively calling `solve_with_assignment`, which takes an expression and an assignment. If this function is called with a complete assignment of variables then it evaluates the expression given the assignment and returns its truth value. If called with an incomplete assignment it picks a variable to assign (the 'choice variable') and recursively calls with this variable assigned true and then false. If neither assignment leads to the expression being satisfied, the solve function returns false.

In the worst case this algorithm will have to assign every variable twice, first to true and then to false. With $n$ variables this leads to a complexity of $O(2^n)$. A formula which is only satisfied when all variables are assigned false would lead to this scenario.

Some simple optimisations that could be made might include early-exiting from an assignment, for instance if one side of a conjunction is known to be false. This would decrease the complexity for some formulae, but still retain the same worst case.

= Optimised Solver

= Comparison
The simple solver can find an actual satisfying assignment, whereas the optimised solver only shows if one exists.
