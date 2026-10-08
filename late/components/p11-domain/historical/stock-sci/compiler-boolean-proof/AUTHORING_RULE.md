# Boolean value operands in SCI1.1 conditions

With the pinned SCICompanion compiler, never place a raw logical `and` or `or` value inside a comparison operand in an `if`, `while`, or other conditional expression. The compiler can inherit the outer branch context, skip the comparison, or leave/pop unrelated stack words. Written source semantics and source-only tests do not detect this defect.

Unsafe:

```
(if (!= ready (and (!= padding 0) (!= approved 0))) (return 0))
(if (!= (or (!= introHi 0) (!= introLo 0)) observedIntro) (return 0))
```

Safe when the expression can be evaluated at that exact location:

```
(= requirementsMet (and (!= padding 0) (!= approved 0)))
(if (!= ready requirementsMet) (return 0))
```

Safe local isolation, preserving the surrounding guards and evaluation order:

```
(if (!= ready (not (not (and (!= padding 0) (!= approved 0))))) (return 0))
```

The standalone assignment and double-negation forms are proven by the original stock-runtime fixture and a 256-case compiled-bytecode truth table with stack-balance checks. Keep side effects, bounds checks and guarded accesses in their original order. Do not hoist a calculation across a guard merely to satisfy this rule.

For an existing accepted component, retain a frozen original snapshot and record that this is a compiler-safe lowering with unchanged domain semantics. Regenerate through the owner’s source-generation path so a later rebuild cannot restore unsafe expressions. Cover future adapters with the source hazard scanner plus compiled-bytecode or native behavioral tests; do not use recompilation identity or source-VM passes as proof of correct native execution.

The rule is specific to the current compiler. Changing or removing it requires a compiler regression fixture proving correct semantics and balanced stack behavior across the complete test matrix.
