# An-Optimization-Portfolio

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
           10000 * S + 1000 * E + 100 * V + 10 * E + 1 * N
         + 10000 * P + 1000 * A + 100 * C + 10 * E + 1 * S
         = 10000 * V + 1000 * E + 100 * R + 10 * S + 1 * E;

- =
- !=
- <
- \>
- <=
- \>=

ouput [listofstringexpressions];
