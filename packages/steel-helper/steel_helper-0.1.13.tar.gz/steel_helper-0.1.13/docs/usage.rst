=====
Usage
=====

To use steel-helper in a project::

	import steel_helper
	from steel_helper import Member,Load


Axial Strength
##############

.. image:: img/compression_problem1.png
	:caption: Problem 1

Putting the following into a Jupyter Notebook

.. code-block:: python

	m1_1 = Member('W10X100')
	m = m1_1

	F_y = 50
	F_u = 65
	m.properties(F_y = F_y,F_u = F_u) 

	Lx = Ly = 10
	Kx = Ky = 1
	m.axial_strength(Lx = Lx,Kx = Kx,Ly = Ly,Ky = Ky)
	m.myeqns.markfull("P_n")

Will produce
.. code-block:: markdown

	Ref  | Variable | Equation | Equation_fill | Answer
	:-:|:-:|:-:|:-:|:-:
	E3-2  | Slenderness x | $$\frac{(L_x * K_x)}{r_x}$$ | (10 ft * 1)/4.6 in | 26.087 dimensionless
	E3-2 | <span style='color:blue'>Slenderness y</span> | $$\frac{(L_y * K_y)}{r_y}$$ | (10 ft * 1)/2.65 in | <span style='color:blue'>45.283 dimensionless</span>
	E3-2,E3-3  | Slenderness check | $$4.71 * \sqrt{\frac{E}{F_y}}$$ | 4.71 * sqrt(29000 kip / in ** 2/50 kip / in ** 2) | 113.43
	E3-2,E3-3  | F_e | $$(\frac{(\pi^2 * E)}{Slenderness^2})$$ | ((3.14^2 * 29000 kip / in ** 2)/ 45.283^2) | 139.58 kip / inch ** 2
	E3-2,E3-3  | P_cr | $$(\frac{(\pi^2 * E * A)}{Slenderness^2})$$ | ((3.14^2 * 29000 kip / in ** 2 * 29.3 in ** 2)/ 45.283^2) | 4089.7 kip
	E3-2  | F_cr | $$(0.658^{(\frac{F_y}{F_e})} * F_y)$$ | (0.658 ^(50 kip / in ** 2/139.58 kip / in ** 2) * 50 kip / in ** 2) | 43.038 kip / inch ** 2
	E3-2 | <span style='color:blue'>P_n</span> | $$(F_{cr} * A_g)$$ | 43.038 kip / in ** 2 * 29.3 in ** 2 | <span style='color:blue'>1261 kip</span>
	a  | P_n_LRFD | $$P_n * \phi$$ | 1261 kip * 0.9 | 1134.9 kip
	a  | P_n_ASD | $$\frac{P_n}{\omega}$$ | 1261 kip / 1.67 | 755.1 kip


and
.. code-block:: markdown

	Ref  | Variable | Equation | Equation_fill | Answer
	:-:|:-:|:-:|:-:|:-:
	E3-2  | Slenderness x | $$\frac{(L_x * K_x)}{r_x}$$ | (35 ft * 1)/4.6 in | 91.304 dimensionless
	E3-2 | <span style='color:blue'>Slenderness y</span> | $$\frac{(L_y * K_y)}{r_y}$$ | (35 ft * 1)/2.65 in | <span style='color:blue'>158.49 dimensionless</span>
	E3-2,E3-3  | Slenderness check | $$4.71 * \sqrt{\frac{E}{F_y}}$$ | 4.71 * sqrt(29000 kip / in ** 2/50 kip / in ** 2) | 113.43
	E3-2,E3-3  | F_e | $$(\frac{(\pi^2 * E)}{Slenderness^2})$$ | ((3.14^2 * 29000 kip / in ** 2)/ 158.49^2) | 11.394 kip / inch ** 2
	E3-2,E3-3  | P_cr | $$(\frac{(\pi^2 * E * A)}{Slenderness^2})$$ | ((3.14^2 * 29000 kip / in ** 2 * 29.3 in ** 2)/ 158.49^2) | 333.86 kip
	E3-3  | F_cr | $$0.877 * F_e$$ | 0.877 * 11.394 kip / in ** 2 | 9.9929 kip / inch ** 2
	E3-2 | <span style='color:blue'>P_n</span> | $$(F_{cr} * A_g)$$ | 9.9929 kip / in ** 2 * 29.3 in ** 2 | <span style='color:blue'>292.79 kip</span>
	a  | P_n_LRFD | $$P_n * \phi$$ | 292.79 kip * 0.9 | 263.51 kip
	a  | P_n_ASD | $$\frac{P_n}{\omega}$$ | 292.79 kip / 1.67 | 175.32 kip

Which is then rendered as

.. image: img/compression1_1
	:caption: Solution 1.1
and 

.. image: img/compression1_2
	:caption: Solution 1.2
