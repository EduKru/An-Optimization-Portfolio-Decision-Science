# An-Optimization-Portfolio

Project 1 [Warehousing-automated-guided-vehicles-order-picking](https://github.com/DerEddie/An-Optimization-Portfolio-Decision-Science/blob/main/AGV-Routing-Scheduling/Description.md)




I am working on this course: https://www.coursera.org/learn/basic-modeling/home/welcome

This Portfolio will cover some examples of problems

What solvers are out there which one could use to solve an optimization problem?

Tools to build decision support systems:
- GAMS
- Gurobi
- MiniZinc
- OR-Tools (Google)
- ZIMPL


D(X), D(Y)


X ∈ D(X) , Y ∈ D(Y)\
Constraint (stability Diamond): |X| + |Y| = 10


Problem:\
Find the largest D'(x) ⊆ D(X) and D'(Y) ⊆ D(Y)\
X ∈ D'(X), Y ∈ D'(Y)

Σ
θ

Α	α	Alpha	a	
Β	β	Beta	b	
Γ	γ	Gamma	g	
Δ	δ	Delta	d	
Ε	ε	Epsilon	e	
Ζ	ζ	Zeta	z	
Η	η	Eta	h	
Θ	θ	Theta	th	
Ι	ι	Iota	i	
Κ	κ	Kappa	k	
Λ	λ	Lambda	l	
Μ	μ	Mu	m	
Ν	ν	Nu	n	
Ξ	ξ	Xi	x	
Ο	ο	Omicron	o	
Π	π	Pi	p	
Ρ	ρ	Rho	r	
Σ	σ,ς *	Sigma	s	
Τ	τ	Tau	t	
Υ	υ	Upsilon	u	
Φ	φ	Phi	ph	
Χ	χ	Chi	ch	
Ψ	ψ	Psi	ps	
Ω	ω	Omega	o	

Cao Zhi 

![image](https://user-images.githubusercontent.com/29587190/149989811-21c0b3f0-135f-47d1-b432-485fcd397848.png)

MiniZinc:
Order of commands doesnt matter at all.

Declaring variables:
var 0..9: S;

comments:
- %
- /* */

String:
- "thisisastring"
- show(v)
- "\(v)" string literal
- "a" + "b" concat

Constraints:

constraint
- 10000 * S + 1000 * E + 100 * V + 10 * E + 1 * N
- + 10000 * P + 1000 * A + 100 * C + 10 * E + 1 * S
- = 10000 * V + 1000 * E + 100 * R + 10 * S + 1 * E;


Inequality, Equality etc.
- =
- !=
- <
- \>
- <=
- \>=

What is the goal?
- solve satisfy;
- solve maximize *expression*
- solve minimize *arith.expression*

Boolean expression
- b1 /\ b2 : conjunction
- b1 \\/ b2 : disjunction
- b1 -> b1 : implication
- b1 <-> b2: biimplication
- not b1: negation




sets:
- set of type
- union, intersect, subset, superset, diff, symdiff, card
- set of int: ROW = 1..6;
- set of float: RAN = 3.0 .. 5.0;
- set of bool: bs = {PRIME subset ROW, false}
- min(S)
- max(S)
- card(S)

array:
- array[index_set1, index_set2, ....] of type
- arr2d = [| 1,2,3
-                | 4 5 6 |]


set comprehension:
- {expr | generator1, generator2, ... where bool-expr}
- { i + j | i,j in 1..4 where i < j }


  print(ianfoi)

ouput [listofstringexpressions];


enum "口" = { "大","女","日","马"}

examples:

- constraint x > 0 /\ y > 0;
- constraint x > 0; % not reified
- constraint y > 0; % not reified
- 
![image](https://user-images.githubusercontent.com/29587190/150001066-dbb9553d-68dd-4e08-ab15-f6d3ead9db26.png)


b = x[2] < y[2] /\ x[4] < y[4]



