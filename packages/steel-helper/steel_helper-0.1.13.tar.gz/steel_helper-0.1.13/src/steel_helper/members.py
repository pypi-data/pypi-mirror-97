import pandas as pd
from IPython.display import Math, display, Markdown
from sympy import latex
from math import sqrt, pi
import pint
import os
import re

u = pint.UnitRegistry()
u.default_format = "~H.5g"


class Equations:
    def __init__(self):
        self.items = {"Top": ["Variable", "Answer", "Equation_fill", "Equation", "Ref"]}
        self.maxes = []
        self.greens = []
        self.reds = []

    def additem(self, value, equation):
        self.items[(value)] = equation

    def adddict(self, mydict):
        for key, value in mydict.items():
            self.items[(key)] = value

    def addline(self):
        # I believe the number just needs to be larger than number of variables
        self.items["Line"] = " " * 20

    def delitem(self, value):
        del self.items[(value)]

    def displayinventory(self):
        return self.items

    def printkeys(self, *highs):
        for key, value in self.items.items():
            print(key)

    def markfull(self, *highs):
        mymarkdown = ""
        a, b, c, d, e = 0, 0, 0, 0, 0
        for max in self.maxes:
            highs += (max,)

        spacing = 1
        for key, value in self.items.items():
            for i, item in enumerate(value):
                # print(item)
                if i == 0:
                    if len(str(item)) > a:
                        a = len(str(item)) + spacing
                        # print(l)
                if i == 1:
                    if len(str(item)) > b:
                        b = len(str(item)) + spacing
                if i == 2:
                    if len(str(item)) > c:
                        c = len(str(item)) + spacing
                if i == 3:
                    if len(str(item)) > d:
                        d = len(str(item)) + spacing
                if i == 4:
                    if len(str(item)) > e:
                        e = len(str(item)) + spacing
        # print(a,b,c,d,e)
        a, b, c, d, e = e, a, d, c, b
        for key, value in self.items.items():
            # if key in ["A_g", "A_n", "A_e"]:

            # Use this to determine keys
            # print(key)
            variable = value[0]
            solution = value[1]
            equation_fill = value[2]
            equation = value[3]
            ref = value[4]

            try:
                if key in highs:
                    mymarkdown += f"\n{ref} | <span style='color:blue'>{variable}</span> | {(equation)} | {(equation_fill)} | <span style='color:blue'>{solution:.5g}</span>"
                elif key in self.reds:
                    mymarkdown += f"\n{ref} | <span style='color:red'>{variable}</span> | {(equation)} | {(equation_fill)} | <span style='color:red'>{solution:.5g}</span>"
                elif key in self.greens:
                    mymarkdown += f"\n{ref} | <span style='color:green'>{variable}</span> | {(equation)} | {(equation_fill)} | <span style='color:green'>{solution:.5g}</span>"
                else:
                    mymarkdown += f"\n{ref}  | {variable} | {(equation)} | {(equation_fill)} | {solution:.5g}"
            except:
                mymarkdown += (
                    # f"{ref:<{a}}  | {variable:<{b}} | {(equation):<{c}} | {(equation_fill):<{d}} | {solution:<{e}}\n{'-' * (a + b + c + d + e + 6)}"
                    f"{ref}  | {variable} | {(equation)} | {(equation_fill)} | {solution}\n:-:|:-:|:-:|:-:|:-:"
                )

            # except:
            #     print(f"{ref}{variable:<{a}}   {'':<{b}} | {solution:>{c}.3g}")
        display(Markdown(mymarkdown))
        # print(mymarkdown)
        print("\n" * 3)

    def markans(self, *highs):
        mymarkdown = ""
        a, b, c, d, e = 0, 0, 0, 0, 0
        for max in self.maxes:
            highs += (max,)
        spacing = 1
        for key, value in self.items.items():
            for i, item in enumerate(value):
                # print(item)
                if i == 0:
                    if len(str(item)) > a:
                        a = len(str(item)) + spacing
                        # print(l)
                if i == 1:
                    if len(str(item)) > b:
                        b = len(str(item)) + spacing
                if i == 2:
                    if len(str(item)) > c:
                        c = len(str(item)) + spacing
                if i == 3:
                    if len(str(item)) > d:
                        d = len(str(item)) + spacing
                if i == 4:
                    if len(str(item)) > e:
                        e = len(str(item)) + spacing
        # print(a,b,c,d,e)
        a, b, c, d, e = e, a, d, c, b
        for key, value in self.items.items():
            # if key in ["A_g", "A_n", "A_e"]:

            # Use this to determine keys
            # print(key)
            variable = value[0]
            solution = value[1]
            equation_fill = value[2]
            equation = value[3]
            ref = value[4]

            try:
                if key in highs:
                    mymarkdown += f"\n**{variable}** | **{solution:.5g}**"
                else:
                    mymarkdown += f"\n{variable} | {solution:.5g}"
            except:
                mymarkdown += (
                    # f"{ref:<{a}}  | {variable:<{b}} | {(equation):<{c}} | {(equation_fill):<{d}} | {solution:<{e}}\n{'-' * (a + b + c + d + e + 6)}"
                    f"{variable} | {solution}\n:-:|:-:"
                )

            # except:
            #     print(f"{ref}{variable:<{a}}   {'':<{b}} | {solution:>{c}.3g}")
        display(Markdown(mymarkdown))
        # print(mymarkdown)
        print("\n" * 3)

    def displayfull(self, *highs):
        a, b, c, d, e = 0, 0, 0, 0, 0
        for max in self.maxes:
            highs += (max,)
        spacing = 1
        for key, value in self.items.items():
            for i, item in enumerate(value):
                # print(item)
                if i == 0:
                    if len(str(item)) > a:
                        a = len(str(item)) + spacing
                        # print(l)
                if i == 1:
                    if len(str(item)) > b:
                        b = len(str(item)) + spacing
                if i == 2:
                    if len(str(item)) > c:
                        c = len(str(item)) + spacing
                if i == 3:
                    if len(str(item)) > d:
                        d = len(str(item)) + spacing
                if i == 4:
                    if len(str(item)) > e:
                        e = len(str(item)) + spacing
        # print(a,b,c,d,e)
        a, b, c, d, e = e, a, d, c, b
        for key, value in self.items.items():
            # if key in ["A_g", "A_n", "A_e"]:

            # Use this to determine keys
            # print(key)
            variable = value[0]
            solution = value[1]
            equation_fill = value[2]
            equation = value[3]
            ref = value[4]

            try:
                if key in highs:
                    print(
                        f"{color.YELLOW}{color.BOLD}{ref:<{a}}  | {variable:<{b}} | {(equation):<{c}} | {(equation_fill):<{d}} | {solution:>{e}.5g}{color.END}"
                    )
                else:
                    print(
                        f"{ref:<{a}}  | {variable:<{b}} | {(equation):<{c}} | {(equation_fill):<{d}} | {solution:>{e}.5g}"
                    )
            except:
                print(
                    # f"{ref:<{a}}  | {variable:<{b}} | {(equation):<{c}} | {(equation_fill):<{d}} | {solution:<{e}}\n{'-' * (a + b + c + d + e + 6)}"
                    f"{ref:<{a}}  | {variable:<{b}} | {(equation):<{c}} | {(equation_fill):<{d}} | {solution:<{e}}\n{'-'*a}|{'-'*b}|{'-'*c}|{'-'*d}|{'-'*e}"
                )

            # except:
            #     print(f"{ref}{variable:<{a}}   {'':<{b}} | {solution:>{c}.3g}")
        print("\n" * 3)

    def displayans(self, *highs):
        # only prints Variable(b) and Answer(e)
        a, b, c, d, e = 0, 0, 0, 0, 0
        for max in self.maxes:
            highs += (max,)
        spacing = 1
        for key, value in self.items.items():
            for i, item in enumerate(value):
                # print(item)
                if i == 0:
                    if len(str(item)) > a:
                        a = len(str(item)) + spacing
                        # print(l)
                if i == 1:
                    if len(str(item)) > b:
                        b = len(str(item)) + spacing
                if i == 2:
                    if len(str(item)) > c:
                        c = len(str(item)) + spacing
                if i == 3:
                    if len(str(item)) > d:
                        d = len(str(item)) + spacing
                if i == 4:
                    if len(str(item)) > e:
                        e = len(str(item)) + spacing
        # print(a,b,c,d,e)
        a, b, c, d, e = e, a, d, c, b
        for key, value in self.items.items():
            # if key in ["A_g", "A_n", "A_e"]:

            # Use this to determine keys
            # print(key)
            variable = value[0]
            solution = value[1]
            equation_fill = value[2]
            equation = value[3]
            ref = value[4]

            try:
                if key in highs:
                    print(
                        f"{color.YELLOW}{color.BOLD}{variable:<{b}} | {solution:>{e}.5g}{color.END}"
                    )
                else:
                    print(f"{variable:<{b}} | {solution:>{e}.5g}")
            except:
                print(f"{variable:<{b}} | {solution:<{e}}\n{'-' * b} | {'-'*e}")
            # except:
            #     print(f"{ref}{variable:<{a}}   {'':<{b}} | {solution:>{c}.3g}")
        print("\n" * 3)


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class Bracers:
    def __init__(self):

        self.myeqns = Equations()

    def add_loads(self, load):
        self.loads = self.loads + load

    def combine_loads(self):
        myloads = [self.windward, self.leeward, self.seismic]


class Load:
    def __init__(self, Dead=0, Live=0, Live_roof=0, Snow=0, Rain=0, Wind=0):
        # self.D = Dead * u.kips / (u.inch ** 2)
        self.D = Dead * u.kips
        self.L = Live * u.kips
        self.L_r = Live_roof * u.kips
        self.S = Snow * u.kips
        self.R = Rain * u.kips
        self.W = Wind * u.kips
        self.myeqns = Equations()

    def combo_loads(self, load_type, combo):
        D = self.D
        L = self.L
        L_r = self.L_r
        S = self.S
        R = self.R
        W = self.W
        if load_type == "LRFD":
            if combo == 1:
                self.myeqns.additem(
                    "LRFD Combo " + str(combo),
                    [
                        "LRFD Combo " + str(combo),
                        1.4 * D,
                        f"1.4 * {D}",
                        "1.4 * D",
                        "ASCE 7",
                    ],
                )
                return 1.4 * D
            elif combo == 2:
                self.myeqns.additem(
                    "LRFD Combo " + str(combo),
                    [
                        "LRFD Combo " + str(combo),
                        1.2 * D + 1.6 * L + 0.5 * (max(L_r, S, R)),
                        f"1.2 * {D} + 1.6 * {L} + 0.5 * {(max(L_r, S, R))}",
                        "1.2 * D + 1.6 * L + 0.5 * (max(L_r, S, R))",
                        "ASCE 7",
                    ],
                )
                return 1.2 * D + 1.6 * L + 0.5 * (max(L_r, S, R))
            elif combo == 3:
                self.myeqns.additem(
                    "LRFD Combo " + str(combo),
                    [
                        "LRFD Combo " + str(combo),
                        1.2 * D + 1.6 * max(L_r, S, R) + max(0.5 * L, 0.5 * W),
                        f"1.2 * {D} + 1.6 * {max(L_r, S, R)} + {max(0.5 * L, 0.5 * W)}",
                        "1.2 * D + 1.6 * max(L_r, S, R) + max(0.5 * L, 0.5 * W)",
                        "ASCE 7",
                    ],
                )

                # print(f"1.2 * {D} + 1.6 * {max(L_r, S, R)} + {max(0.5*L, 0.5 * W)}")
                return 1.2 * D + 1.6 * max(L_r, S, R) + max(0.5 * L, 0.5 * W)
            elif combo == 4:
                self.myeqns.additem(
                    "LRFD Combo " + str(combo),
                    [
                        "LRFD Combo " + str(combo),
                        1.2 * D + 1.0 * W + 1.0 * L + 0.5 * max(L_r, S, R),
                        f"1.2 * {D} + 1.0 * {W} + 1.0 * {L} + 0.5 * {max(L_r, S, R)}",
                        "1.2 * D + 1.0 * W + 1.0 * L + 0.5 * max(L_r, S, R)",
                        "ASCE 7",
                    ],
                )

                return 1.2 * D + 1.0 * W + 1.0 * L + 0.5 * max(L_r, S, R)
            elif combo == 5:
                self.myeqns.additem(
                    "LRFD Combo " + str(combo),
                    [
                        "LRFD Combo " + str(combo),
                        0.9 * D + 1.0 * W,
                        f"0.9 * {D} + 1.0 * {W}",
                        "0.9 * D + 1.0 * W",
                        "ASCE 7",
                    ],
                )
                self.myeqns.addline()

                return 0.9 * D + 1.0 * W

        if load_type == "ASD":
            if combo == 1:
                self.myeqns.additem(
                    "ASD Combo " + str(combo),
                    [
                        "ASD Combo " + str(combo),
                        D,
                        f"{D}",
                        "D",
                        "ASCE 7",
                    ],
                )
                return D
            elif combo == 2:
                self.myeqns.additem(
                    "ASD Combo " + str(combo),
                    [
                        "ASD Combo " + str(combo),
                        D + L,
                        f"{D} + {L}",
                        "D + L",
                        "ASCE 7",
                    ],
                )
                return D + L
            elif combo == 3:
                self.myeqns.additem(
                    "ASD Combo " + str(combo),
                    [
                        "ASD Combo " + str(combo),
                        D + max(L_r, S, R),
                        f"{D} + {max(L_r, S, R)}",
                        "D + max(L_r, S, R)",
                        "ASCE 7",
                    ],
                )
                return D + max(L_r, S, R)
            elif combo == 4:
                self.myeqns.additem(
                    "ASD Combo " + str(combo),
                    [
                        "ASD Combo " + str(combo),
                        D + 0.75 * L + 0.75 * max(L_r, S, R),
                        f"{D} + 0.75 * {L} + 0.75 * {max(L_r, S, R)}",
                        "D + 0.75 * L + 0.75 * max(L_r, S, R)",
                        "ASCE 7",
                    ],
                )
                return D + 0.75 * L + 0.75 * max(L_r, S, R)
            elif combo == 5:
                self.myeqns.additem(
                    "ASD Combo " + str(combo),
                    [
                        "ASD Combo " + str(combo),
                        D + 0.6 * W,
                        f"{D} + 0.6 * {W}",
                        "D + 0.6 * W",
                        "ASCE 7",
                    ],
                )
                return D + 0.6 * W
            elif combo == 6:
                self.myeqns.additem(
                    "ASD Combo " + str(combo),
                    [
                        "ASD Combo " + str(combo),
                        D + 0.75 * L + 0.75 * 0.6 * W + 0.75 * max(L_r, S, R),
                        f"{D} + 0.75 * {L} + 0.75 * 0.6 * {W} + 0.75 * {max(L_r, S, R)}",
                        "D + 0.75 * L + 0.75 * 0.6 * W + 0.75 * max(L_r, S, R)",
                        "ASCE 7",
                    ],
                )
                return D + 0.75 * L + 0.75 * 0.6 * W + 0.75 * max(L_r, S, R)
            elif combo == 7:
                self.myeqns.additem(
                    "ASD Combo " + str(combo),
                    [
                        "ASD Combo " + str(combo),
                        0.6 * D + 0.6 * W,
                        f"0.6 * {D} + 0.6 * {W}",
                        "0.6 * D + 0.6 * W",
                        "ASCE 7",
                    ],
                )
                return 0.6 * D + 0.6 * W

    def get_max_loads(self):

        D = self.D
        L = self.L
        L_r = self.L_r
        S = self.S
        R = self.R
        W = self.W

        omega = 1.67
        phi = 0.9
        mymax = 0

        for i in range(1, 6):
            combo_value_LRFD = self.combo_loads("LRFD", i)
            # print(f"Combonation {i} = {(combo_value_LRFD):.3}")
            if combo_value_LRFD > mymax:
                mymax = combo_value_LRFD
                mymax_combo = i
        self.LRFD_max = mymax

        self.myeqns.maxes.append(f"LRFD Combo {mymax_combo}")

        mymax = 0

        for i in range(1, 8):
            combo_value_ASD = self.combo_loads("ASD", i)

            if combo_value_ASD > mymax:
                mymax = combo_value_ASD
                mymax_combo = i
        self.ASD_max = mymax
        self.myeqns.maxes.append(f"ASD Combo {mymax_combo}")


def convert_to_float(frac_str):
    # This takes the inputed string like ("2", "5/8","2 5/8" and converts those to in)
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split("/")
        try:
            leading, num = num.split(" ")
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


class Member:
    def __init__(self, designation):

        # Default is A36
        self.F_y = 36 * u.kips / (u.inch ** 2)
        self.F_u = 58 * u.kips / (u.inch ** 2)
        self.E = 29_000 * u.kips / (u.inch ** 2)
        self.myeqns = Equations()
        if designation != "none":
            try:
                shapes = pd.read_excel(
                    "aisc-shapes-14.xlsx", sheet_name="Database v15.0H"
                )
                df = shapes
            except:
                # Used for module usage (Able to access file downloaded with module)
                init_location = __file__
                # print(init_location)
                shapes_location = (
                    init_location.replace("members.py", "") + "aisc-shapes-14.xlsx"
                )
                shapes = pd.read_excel(shapes_location, sheet_name="Database v15.0H")
                df = shapes

            myedition = shapes["Edition"] == "14th"
            mydesignation = shapes["Designation"] == designation
            myshape = shapes.loc[myedition & mydesignation]
            # This adds all of the attributes from the table as attributes of member
            for column in myshape.columns:
                try:
                    exec(f"self.{column} = float(myshape[column])")
                #                 print(f"'{column}' = {float(myshape[column])}")
                except:
                    pass

            # print(designation)
            # Space is necessary
            designation = re.sub("[^X0-9/. ]", "", designation)

            mydimensions = designation.split("X")

            if len(mydimensions) == 3:
                self.w_plate = convert_to_float(mydimensions[1]) * u.inch
                self.t_plate = convert_to_float(mydimensions[2]) * u.inch
            else:
                self.w_plate = convert_to_float(mydimensions[0]) * u.inch
                self.t_plate = convert_to_float(mydimensions[1]) * u.inch

            try:

                self.A_g = self.A_g * u.inch ** 2
            except:
                self.A_g = self.w_plate * self.t_plate

                self.myeqns.additem(
                    "A_g",
                    [
                        "A_g",
                        self.A_g,
                        f"{self.w_plate} * {self.t_plate}",
                        "w_plate * t_plate",
                        "Gross area",
                    ],
                )

    def properties(self, F_y, F_u):
        # steel = "A36"
        # from steel bible
        self.F_y = F_y * u.kips / (u.inch ** 2)
        self.F_u = F_u * u.kips / (u.inch ** 2)

    def bolts(self, bolt_size, holes, load_transfer=1, *stagger):
        self.bolt_size = convert_to_float(bolt_size) * u.inch
        self.holes = holes
        t = self.t_plate
        A_g = self.A_g
        # print(stagger)
        if self.bolt_size < 1 * u.inch:
            self.hole_size = self.bolt_size + 1 / 8 * u.inch
            self.myeqns.additem(
                "hole_size",
                [
                    "hole_size",
                    self.hole_size,
                    f"{self.bolt_size} + 1 / 8 * u.inch",
                    "bolt_size + 1 / 8 * u.inch",
                    "Table J3.3 and b4.36 (16.1-130,16.1-20)",
                ],
            )
        else:
            self.hole_size = self.bolt_size + 3 / 16 * u.inch
            self.myeqns.additem(
                "hole_size",
                [
                    "hole_size",
                    self.hole_size,
                    f"{self.bolt_size} + 3 / 16 * u.inch",
                    "bolt_size + 3 / 16 * u.inch",
                    "Table J3.3 and b4.36 (16.1-130,16.1-20)",
                ],
            )

        self.A_hole = self.t_plate * self.hole_size
        self.A_holes = self.A_hole * self.holes

        self.myeqns.additem(
            "Area of holes",
            [
                "Area of holes",
                self.A_holes,
                f"{self.t_plate} * {self.hole_size} * {self.holes}",
                "t_plate * hole_size * holes",
                "",
            ],
        )

        A_holes = self.A_holes

        if len(stagger) > 0:
            stagger_factors = 0
            stagger_equations = ""
            for diag_hole in stagger:
                s, g, diagonals = (
                    diag_hole[0] * u.inch,
                    diag_hole[1] * u.inch,
                    diag_hole[2],
                )

                stagger_factors += t * diagonals * ((s ** 2) / (4 * g))
                stagger_equations += (
                    f" + {t} * {diagonals} diagonals * (({s}**2)/(4*{g}))"
                )

            A_n = (A_g - A_holes + stagger_factors) * load_transfer
            self.A_n = A_n

            self.myeqns.additem(
                "A_n",
                [
                    "A_n from stagger",
                    A_n,
                    f"({A_g: .3} - {A_holes: .3}{stagger_equations}) * {load_transfer})",
                    "(A_g - A_holes + stagger_equations) * load_transfer)",
                    "Stagger factor from Eq 3.2",
                ],
            )
        else:

            A_n = (A_g - A_holes) * load_transfer
            self.A_n = A_n
            self.myeqns.additem(
                "A_n",
                [
                    "A_n",
                    A_n,
                    f"({A_g: .3} - {A_holes: .3} * {load_transfer})",
                    "(A_g - A_holes * load transfer)",
                    "Net area accounting for load transfer",
                ],
            )

    def design_strength(self):
        P_n_gross = self.P_n_gross
        P_n_net = self.P_n_net
        # print(P_n_gross)
        # print(P_n_gross)
        self.myeqns.additem(
            "LRFD Yield strength",
            [
                "LRFD Yield strength",
                0.9 * P_n_gross,
                f"0.9 * {P_n_gross:.3g}",
                "0.9 * {P_n_gross:.3g}",
                "D2-1",
            ],
        )
        self.myeqns.additem(
            "LRFD Rupture strength",
            [
                "LRFD Rupture strength",
                0.75 * P_n_net,
                f"0.75 * {P_n_net:.3g}",
                "0.75 * {P_n_net:.3g}",
                "D2-2",
            ],
        )

        self.myeqns.additem(
            "ASD Yield strength",
            [
                "ASD Yield strength",
                P_n_gross / 1.67,
                f"{P_n_gross:.3g} / 1.67",
                "{P_n_gross:.3g} / 1.67",
                "D2-1",
            ],
        )
        self.myeqns.additem(
            "ASD Rupture strength",
            [
                "ASD Rupture strength",
                P_n_net / 2,
                f"{P_n_net:.3g} / 2",
                "P_n_net / 2",
                "D2-2",
            ],
        )

    def reduction_factor(self, shape_type, x_bar=0, l_plate=0, w_plate=0, fasteners=0):
        l = l_plate
        w = w_plate
        x = x_bar
        if fasteners >= 4:
            self.myeqns.additem(
                "U",
                [
                    "U from more than 4 fasteners",
                    0.8,
                    f"0.8",
                    "0.8",
                    "Table D3.1",
                ],
            )
            return 0.80
        elif fasteners == 3:
            self.myeqns.additem(
                "U",
                [
                    "U from 3 fasteners",
                    0.6,
                    f"0.6",
                    "0.6",
                    "Table D3.1",
                ],
            )
            return 0.60
        elif shape_type == "other":
            self.myeqns.additem(
                "U",
                [
                    "U from other",
                    1 - (x_bar / l_plate),
                    f"1 - ({x_bar} / {l_plate})",
                    "1 - (x_bar / l_plate)",
                    "Table D3.1",
                ],
            )

            return 1 - (x_bar / l_plate)

        elif shape_type == "bolted_plate":
            self.myeqns.additem(
                "U",
                [
                    "U from bolted plate",
                    1,
                    f"1",
                    "1",
                    "Table D3.1",
                ],
            )
            return 1
        elif shape_type == "welded_member":
            # print(l, w, x)
            # print(((3*l**2)/(3*l**2 + w**2))*(1 - (x/l)))
            self.myeqns.additem(
                "U",
                [
                    "U from welded member",
                    ((3 * l ** 2) / (3 * l ** 2 + w ** 2)) * (1 - (x / l)),
                    f"(((3*{l}**2)/(3*{l}**2 + {w}**2))*(1 - ({x}/{l})))",
                    "(((3*l**2)/(3*l**2 + w**2))*(1 - (x/l)))",
                    "Table D3.1",
                ],
            )
            return ((3 * l ** 2) / (3 * l ** 2 + w ** 2)) * (1 - (x / l))
        elif shape_type == "large_hss":
            self.myeqns.additem(
                "U",
                [
                    "U from large hss",
                    1,
                    f"1",
                    "1",
                    "Table D3.1",
                ],
            )
            return 1

    def nominal_strength(self, effective_factor):
        self.effective_factor = effective_factor
        F_y = self.F_y
        F_u = self.F_u
        A_g = self.A_g
        A_n = self.A_n
        A_holes = self.A_holes
        t = self.t_plate

        A_e = A_n * effective_factor
        self.myeqns.additem(
            "A_e",
            [
                "A_e",
                A_e,
                f"{A_n:.3g} * {effective_factor:.3g}",
                "A_n * effective_factor",
                "D3-1",
            ],
        )

        P_n_gross = F_y * A_g
        # print(P_n_gross)
        self.P_n_gross = P_n_gross
        self.myeqns.additem(
            "Nominal strength gross",
            [
                "Nominal strength gross",
                P_n_gross,
                f"{F_y:.3} * {A_g:.3}",
                "F_y * A_g",
                "D2-1",
            ],
        )

        P_n_net = F_u * A_e
        # print(P_n_gross)
        self.P_n_net = P_n_net
        self.myeqns.additem(
            "Nominal strength net",
            [
                "Nominal strength net",
                P_n_net,
                f"{F_u:.3} * {A_e:.3}",
                "F_u * A_e",
                "D2-2",
            ],
        )

    def block_shear(self, x_bolts, y_bolts, rows=1, effective_factor=1):
        # l_plate = self.l_plate
        # w_plate = self.w_plate
        t_plate = self.t_plate
        y_bolts = convert_to_float(y_bolts) * u.inch
        x_bolts = convert_to_float(x_bolts) * u.inch

        F_y = self.F_y
        F_u = self.F_u

        d_hole = self.hole_size
        A_hole = self.A_hole
        holes = self.holes

        A_g = x_bolts * t_plate
        self.myeqns.additem(
            "Gross_area_in_shear",
            [
                "Gross area in shear",
                A_g,
                f"{x_bolts} * {t_plate}",
                "x_bolts * t_plate",
                "J4-5",
            ],
        )
        A_nv = t_plate * ((x_bolts) - (holes - 0.5 * rows) * (d_hole))
        A_nt = t_plate * ((y_bolts) - (0.5 * rows) * (d_hole))
        R_n = 0.6 * F_u * A_nv + effective_factor * F_u * A_nt
        R_n_u = 0.6 * F_y * A_g + effective_factor * F_u * A_nt

        nominal_strength = min([R_n, R_n_u])
        # this is for design strength calculation which needs both
        self.P_n_net = nominal_strength
        self.P_n_gross = 0

        self.myeqns.additem(
            "Net_area_in_shear",
            [
                "Net area in shear",
                A_nv,
                f"{t_plate} * (({x_bolts}) - ({holes} - 0.5 * {rows}) * ({d_hole}))",
                "t_plate * ((x_bolts) - (holes - 0.5 * rows) * (d_hole))",
                "J4-5",
            ],
        )
        self.myeqns.additem(
            "Net_area_in_tension",
            [
                "Net area in tension",
                A_nt,
                f"{t_plate} * (({y_bolts}) - (0.5 * {rows}) * ({d_hole}))",
                "t_plate * ((y_bolts) - (0.5 * rows) * (d_hole))",
                "J4-5",
            ],
        )
        self.myeqns.additem(
            "R_n",
            [
                "R_n",
                R_n,
                f"0.6 * {F_u} * {A_nv:.3g} + {effective_factor} * {F_u} * {A_nt:.3g}",
                "0.6 * F_u * A_nv + effective_factor * F_u * A_nt",
                "Eq 3.3",
            ],
        )
        self.myeqns.additem(
            "R_n_u",
            [
                "R_n_u",
                R_n_u,
                f"0.6 * {F_y} * {A_g:.3g} + {effective_factor} * {F_u} * {A_nt:.3g}",
                "0.6 * F_y * A_g + effective_factor * F_u * A_nt",
                "Eq 3.4",
            ],
        )
        self.myeqns.additem(
            "nominal_strength",
            [
                "nominal_strength",
                nominal_strength,
                f"min([{R_n}, {R_n_u}])",
                "min([R_n, R_n_u])",
                "D2-1 and D2-2",
            ],
        )

    # Compression

    def axial_strength(self, Lx, Kx, Ly, Ky):

        Lx = Lx * u.foot
        Ly = Ly * u.foot
        r_x = self.rx * u.inch
        r_y = self.ry * u.inch
        F_y = self.F_y
        E = self.E
        A_g = self.A_g
        self.slenderness_x = (Kx * Lx.to(u.inch)) / r_x
        self.slenderness_y = (Ky * Ly.to(u.inch)) / r_y
        # if Ly != 0 and Ky != 0:

        self.myeqns.additem(
            "Slenderness x",
            [
                "Slenderness x",
                self.slenderness_x,
                f"({Lx} * {Kx})/{r_x}",
                r"$$\frac{(L_x * K_x)}{r_x}$$",
                "E3-2",
            ],
        )

        self.myeqns.additem(
            "Slenderness y",
            [
                "Slenderness y",
                self.slenderness_y,
                f"({Ly} * {Ky})/{r_y}",
                r"$$\frac{(L_y * K_y)}{r_y}$$",
                "E3-2",
            ],
        )
        if self.slenderness_y > self.slenderness_x:
            self.r_min = r_y
            self.L = Ly
            self.K = Ky
            self.myeqns.maxes.append("Slenderness y")
        else:
            self.r_min = r_x
            self.L = Lx
            self.K = Kx
            self.myeqns.maxes.append("Slenderness x")

        self.slenderness = max(self.slenderness_x, self.slenderness_y)

        Slenderness_check = 4.71 * sqrt(E / F_y)
        self.myeqns.additem(
            "Slenderness check",
            [
                "Slenderness check",
                Slenderness_check,
                f"4.71 * sqrt({E}/{F_y})",
                r"$$4.71 * \sqrt{\frac{E}{F_y}}$$",
                "E3-2,E3-3",
            ],
        )

        from math import pi

        F_e = (pi ** 2 * E) / self.slenderness ** 2
        self.myeqns.additem(
            "F_e",
            [
                "F_e",
                F_e,
                f"(({pi:.3}^2 * {E})/ {self.slenderness}^2)",
                r"$$(\frac{(\pi^2 * E)}{Slenderness^2})$$",
                "E3-2,E3-3",
            ],
        )
        # Added as check
        # self.myeqns.greens.append("F_e")

        P_cr = (pi ** 2 * E * A_g) / self.slenderness ** 2
        self.P_cr = P_cr
        self.myeqns.additem(
            "P_cr",
            [
                "P_cr",
                P_cr,
                f"(({pi:.3}^2 * {E} * {A_g})/ {self.slenderness}^2)",
                r"$$(\frac{(\pi^2 * E * A)}{Slenderness^2})$$",
                "E3-2,E3-3",
            ],
        )

        if self.slenderness > Slenderness_check:
            F_cr = 0.877 * F_e
            self.myeqns.additem(
                "F_cr",
                [
                    "F_cr",
                    F_cr,
                    f"0.877 * {F_e}",
                    "$$0.877 * F_e$$",
                    "E3-3",
                ],
            )
        else:
            F_cr = 0.658 ** (F_y / F_e) * F_y
            self.myeqns.additem(
                "F_cr",
                [
                    "F_cr",
                    F_cr,
                    f"(0.658 ^({F_y}/{F_e}) * {F_y})",
                    r"$$(0.658^{(\frac{F_y}{F_e})} * F_y)$$",
                    "E3-2",
                ],
            )

        P_n = F_cr * A_g
        self.P_n = P_n
        self.myeqns.additem(
            "P_n",
            [
                "P_n",
                P_n,
                f"{F_cr} * {A_g}",
                r"$$(F_{cr} * A_g)$$",
                "E3-2",
            ],
        )

        phi = 0.9
        P_n_LRFD = P_n * phi
        self.myeqns.additem(
            "P_n_LRFD",
            [
                "P_n_LRFD",
                P_n_LRFD,
                f"{P_n} * {phi}",
                r"$$P_n * \phi$$",
                "a",
            ],
        )
        try:
            if P_n_LRFD > self.LRFD_max:
                self.myeqns.greens.append("P_n_LRFD")
            else:
                self.myeqns.reds.append("P_n_LRFD")
        except:
            print("theres none")

        omega = 1.67
        P_n_ASD = P_n / omega
        self.myeqns.additem(
            "P_n_ASD",
            [
                "P_n_ASD",
                P_n_ASD,
                f"{P_n} / {omega}",
                r"$$\frac{P_n}{\omega}$$",
                "a",
            ],
        )
        try:
            if P_n_ASD > self.ASD_max:
                self.myeqns.greens.append("P_n_ASD")
            else:
                self.myeqns.reds.append("P_n_ASD")
        except:
            pass

    def available_strength(self, L1, L2, K1, K2):
        r_x = self.rx
        r_y = self.ry
        L1_cr = L1 * K1
        L2_cr = L2 * K2
        return L1_cr / (r_x / r_y)

    def factor_of_safety(self, myload):
        myload = myload * u.kips
        P_cr = self.P_cr
        factor_of_safety = P_cr / myload
        self.myeqns.additem(
            "factor of safety",
            [
                "factor of safety",
                factor_of_safety,
                f"({P_cr} / {myload})",
                r"$\frac({P_{cr}}{myload})$",
                "a",
            ],
        )

    def slenderness_hss(self):
        print(self.b__tdes)
        print(1.4 * sqrt(self.E / self.F_y))
        if self.b__tdes <= 1.4 * sqrt(self.E / self.F_y):

            print("Not slender")
        else:
            print("Slender")

    def local_stability(self):
        E = self.E
        F_y = self.F_y
        bf = self.bf
        tf = self.tf
        # h = self.h
        tw = self.tw

        first = bf / (2 * tf)
        second = 0.56 * sqrt(E / F_y)
        third = (self.ddet - 2 * self.kdes) / tw
        print(first, second, third)

    def add_loads(self, loads):
        self.LRFD_max = loads.LRFD_max
        self.ASD_max = loads.ASD_max


class purlin:
    def __init__(self, weight, count):
        self.weight = weight * u.pound_force / u.foot
        self.count = count
        # print(self.x)


class truss:
    def __init__(self, x, y, length, spacing):
        self.x = convert_to_float(x) * u.foot
        self.y = convert_to_float(y) * u.foot
        self.length = convert_to_float(length) * u.foot
        self.spacing = spacing * u.feet


class Frame:
    def __init__(self, H, L):
        self.H = H * u.foot
        self.L = L * u.foot

    def find_g(self, A, B):
        H = self.H
        L = self.L

        if A == "Pin":
            g_a = 10
        elif A == "Fixed":
            g_a = 1
        else:
            g_a = (A[0] / H) / (A[1] / L)

        if B == "Pin":
            g_b = 10
        elif B == "Fixed":
            g_b = 1
        else:
            g_b = (B[0] / H) / (B[1] / L)

        print(f"g_a = {g_a}")
        print(f"g_b = {g_b}")
