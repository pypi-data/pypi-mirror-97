from IPython.display import Math, display, Markdown
from sympy import latex
import pint


class Equations:

    def __init__(self):
        self.items = {"Top": ['Variable', 'Answer', 'Equation']}

    def additem(self, value, equation):
        self.items[(value)] = (equation)

    def adddict(self, mydict):
        for key, value in mydict.items():
            self.items[(key)] = (value)

    def addline(self):
        # I believe the number just needs to be larger than number of variables
        self.items['Line'] = (' ' * 20)

    def delitem(self, value):
        del self.items[(value)]

    def displayinventory(self):
        return self.items

    def printkeys(self, *highs):
        for key, value in self.items.items():
            print(key)

    def displayfancy(self, *highs):
        l = 0
        m = 0
        r = 0
        for key, value in self.items.items():
            for i, item in enumerate(value):
                # print(item)
                if i == 0:
                    if len(str(item)) > l:
                        l = len(str(item)) + 2
                        # print(l)
                if i == 2:
                    if len(str(item)) > m:
                        m = len(str(item)) + 2
                if i == 1:
                    if len(str(item)) > r:
                        r = len(str(item)) + 2
        # print(l, m, r)
        for key, value in self.items.items():
            # if key in ["A_g", "A_n", "A_e"]:

            # Use this to determine keys
            # print(key)
            variable = value[0]
            solution = value[1]
            try:
                equation = value[2]
                try:
                    if key in highs:
                        print(
                            f"{color.YELLOW}{variable:<{l}} | {(equation):<{m}} | {solution:>{r}.3g}{color.END}")
                    else:
                        print(
                            f"{variable:<{l}} | {(equation):<{m}} | {solution:>{r}.3g}")
                except:
                    print(
                        f"{variable:<{l}} | {(equation):<{m}} | {solution:<{r}}\n {'-' * (l + m + r - 5)}")
            except:
                print(f"{variable:<{l}}   {'':<{m}} | {solution:>{r}.3g}")
        print('\n'*3
              )


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


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

    def get_combo_loads(self):
        D = self.D
        L = self.L
        L_r = self.L_r
        S = self.S
        R = self.R
        W = self.W

        omega = 1.67
        phi = 0.9
        mymax = 0

        #     LRFD
        print("LRFD")
        for i in range(1, 6):
            combo_value_LRFD = self.combo_loads("LRFD", i)

            print(f"Combonation {i} = {(combo_value_LRFD):.3g}")
            if combo_value_LRFD > mymax:
                mymax = combo_value_LRFD
        print(f"max = {mymax:.3g}")
        print(f"max / phi = {(mymax / phi):.3g}")

        mymax = 0
        print("")
        print("ASD")
        for i in range(1, 8):
            combo_value_ASD = self.combo_loads("ASD", i)
            print(f"Combonation {i} = {(combo_value_ASD):.3g}")
            if combo_value_ASD > mymax:
                mymax = combo_value_ASD
        print(f"max = {mymax:.3g}")
        print(f"max * omega = {(mymax * omega):.3g}")

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
                    "LRFD Combo " + str(combo), ["LRFD Combo " + str(combo), 1.4 * D,
                                                 f'1.4 * {D}'])
                return 1.4 * D
            elif combo == 2:
                self.myeqns.additem(
                    "LRFD Combo " + str(combo), ["LRFD Combo " + str(combo), 1.2 * D + 1.6 * L + 0.5 * (max(L_r, S, R)),
                                                 f'1.2 * {D} + 1.6 * {L} + 0.5 * {(max(L_r, S, R))}'])
                return 1.2 * D + 1.6 * L + 0.5 * (max(L_r, S, R))
            elif combo == 3:
                self.myeqns.additem(
                    "LRFD Combo " + str(combo), ["LRFD Combo " + str(combo), 1.2 * D + 1.6 * max(L_r, S, R) + max(0.5 * L, 0.5 * W),
                                                 f'1.2 * {D} + 1.6 * {max(L_r, S, R)} + {max(0.5 * L, 0.5 * W)}'])

                # print(f"1.2 * {D} + 1.6 * {max(L_r, S, R)} + {max(0.5*L, 0.5 * W)}")
                return 1.2 * D + 1.6 * max(L_r, S, R) + max(0.5 * L, 0.5 * W)
            elif combo == 4:
                self.myeqns.additem(
                    "LRFD Combo " + str(combo), ["LRFD Combo " + str(combo), 1.2 * D + 1.0 * W + 1.0 * L + 0.5 * max(L_r, S, R),
                                                 f'1.2 * {D} + 1.0 * {W} + 1.0 * {L} + 0.5 * {max(L_r, S, R)}'])

                return 1.2 * D + 1.0 * W + 1.0 * L + 0.5 * max(L_r, S, R)
            elif combo == 5:
                self.myeqns.additem(
                    "LRFD Combo " + str(combo), ["LRFD Combo " + str(combo), 0.9 * D + 1.0 * W,
                                                 f'0.9 * {D} + 1.0 * {W}'])
                self.myeqns.addline()

                return 0.9 * D + 1.0 * W

        if load_type == "ASD":
            if combo == 1:
                self.myeqns.additem(
                    "ASD Combo " + str(combo), ["ASD Combo " + str(combo), D,
                                                f'{D}'])
                return D
            elif combo == 2:
                self.myeqns.additem(
                    "ASD Combo " + str(combo), ["ASD Combo " + str(combo), D + L,
                                                f'{D} + {L}'])
                return D + L
            elif combo == 3:
                self.myeqns.additem(
                    "ASD Combo " + str(combo), ["ASD Combo " + str(combo), D + max(L_r, S, R),
                                                f'{D} + {max(L_r, S, R)}'])
                return D + max(L_r, S, R)
            elif combo == 4:
                self.myeqns.additem(
                    "ASD Combo " + str(combo), ["ASD Combo " + str(combo), D + 0.75 * L + 0.75 * max(L_r, S, R),
                                                f'{D} + 0.75 * {L} + 0.75 * {max(L_r, S, R)}'])
                return D + 0.75 * L + 0.75 * max(L_r, S, R)
            elif combo == 5:
                self.myeqns.additem(
                    "ASD Combo " + str(combo), ["ASD Combo " + str(combo), D + 0.6 * W,
                                                f'{D} + 0.6 * {W}'])
                return D + 0.6 * W
            elif combo == 6:
                self.myeqns.additem(
                    "ASD Combo " + str(combo), ["ASD Combo " + str(combo), D + 0.75 * L + 0.75 * 0.6 * W + 0.75 * max(L_r, S, R),
                                                f'{D} + 0.75 * {L} + 0.75 * 0.6 * {W} + 0.75 * {max(L_r, S, R)}'])
                return D + 0.75 * L + 0.75 * 0.6 * W + 0.75 * max(L_r, S, R)
            elif combo == 7:
                self.myeqns.additem(
                    "ASD Combo " + str(combo), ["ASD Combo " + str(combo), 0.6 * D + 0.6 * W,
                                                f'0.6 * {D} + 0.6 * {W}'])
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

        #     LRFD
        # print("LRFD")
        for i in range(1, 6):
            combo_value_LRFD = self.combo_loads("LRFD", i)
            # print(f"Combonation {i} = {(combo_value_LRFD):.3}")
            if combo_value_LRFD > mymax:
                mymax = combo_value_LRFD
                mymax_combo = i
        self.LRFD_max = mymax
        print("LRFD")
        print(f"Combo {mymax_combo}")
        print(f"max = {mymax:.3}")
        print(f"max / phi = {(mymax / phi):.3}")

        mymax = 0
        # print("")
        # print("ASD")
        for i in range(1, 8):
            combo_value_ASD = self.combo_loads("ASD", i)
            # print(f"Combonation {i} = {(combo_value_ASD):.3}")
            if combo_value_ASD > mymax:
                mymax = combo_value_ASD
                mymax_combo = i
        self.ASD_max = mymax
        print("\nASD")
        print(f"Combo {mymax_combo}")
        print(f"max={mymax}")
        print(f"max * omega = {(mymax / omega):.3}\n")


# ---------------------------------------------------------------
# try:
#   import pint
# except:
#   !pip install pint
#   import pint


u = pint.UnitRegistry()
Q = u.Quantity


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


class Tension_Member:
    def __init__(self):
        # Default is A36
        self.F_y = 36 * u.kips / (u.inch ** 2)
        self.F_u = 58 * u.kips / (u.inch ** 2)
        self.myeqns = Equations()

    # def __enter__(self):
    #     pass

    # def __exit__(self):
    #     pass

    def dimensions(self, l_plate, w_plate, t_plate, A_g):
        self.l_plate = convert_to_float(l_plate) * u.inch
        self.w_plate = convert_to_float(w_plate) * u.inch
        self.t_plate = convert_to_float(t_plate) * u.inch
        if A_g == 0:
            self.A_g = self.w_plate * self.t_plate
            # print(f"A_g = {self.w_plate} * {self.t_plate}\n\t= {self.A_g}")
            self.myeqns.additem(
                "A_g", ['A_g', self.A_g, f'{self.w_plate} * {self.t_plate}'])
        else:
            self.A_g = A_g * u.inch ** 2

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
                "hole_size", ['hole_size', self.hole_size, f'{self.bolt_size} + 1 / 8 * u.inch'])
        else:
            self.hole_size = self.bolt_size + 3 / 16 * u.inch
            self.myeqns.additem(
                "hole_size", ['hole_size', self.hole_size, f'{self.bolt_size} + 3 / 16 * u.inch'])

        self.A_hole = self.t_plate * self.hole_size
        self.A_holes = self.A_hole * self.holes
        A_holes = self.A_holes

        if len(stagger) > 0:
            stagger_factors = 0
            stagger_equations = ""
            for diag_hole in stagger:
                s, g, diagonals = diag_hole[0] * \
                    u.inch, diag_hole[1] * u.inch, diag_hole[2]

                stagger_factors += t * diagonals * ((s**2)/(4*g))
                stagger_equations += f" + {t} * {diagonals} diagonals * (({s}**2)/(4*{g}))"

            A_n = (A_g - A_holes + stagger_factors) * load_transfer
            self.A_n = A_n

            self.myeqns.additem(
                "A_n", ["A_n from stagger", A_n, f"({A_g: .3} - {A_holes: .3}{stagger_equations}) * {load_transfer})"])
        else:

            A_n = (A_g - A_holes) * load_transfer
            self.A_n = A_n
            self.myeqns.additem(
                "A_n", ["A_n", A_n, f"({A_g: .3} - {A_holes: .3} * {load_transfer})"])

    def design_strength(self):
        P_n_gross = self.P_n_gross
        P_n_net = self.P_n_net
        # print(P_n_gross)
        # print(P_n_gross)
        self.myeqns.additem("LRFD Yield strength", [
                            "LRFD Yield strength", 0.9 * P_n_gross, f'0.9 * {P_n_gross:.3g}'])
        self.myeqns.additem("LRFD Rupture strength", [
                            "LRFD Rupture strength", 0.75 * P_n_net, f'0.75 * {P_n_net:.3g}'])

        self.myeqns.additem("ASD Yield strength", [
                            "ASD Yield strength", P_n_gross / 1.67, f'{P_n_gross:.3g} / 1.67'])
        self.myeqns.additem("ASD Rupture strength", [
                            "ASD Rupture strength", P_n_net / 2, f'{P_n_net:.3g} / 2'])

    def reduction_factor(self, shape_type, x_bar=0, l_plate=0, w_plate=0, fasteners=0):
        l = l_plate
        w = w_plate
        x = x_bar
        if fasteners >= 4:
            self.myeqns.additem("U",
                                ['U from more than 4 fasteners',
                                 0.8, f'0.8'])
            return 0.80
        elif fasteners == 3:
            self.myeqns.additem("U",
                                ['U from 3 fasteners',
                                 0.6, f'0.6'])
            return 0.60
        elif shape_type == "other":
            self.myeqns.additem("U",
                                ['U from other',
                                 1 - (x_bar / l_plate), f'1 - ({x_bar} / {l_plate})'])

            return 1 - (x_bar / l_plate)

        elif shape_type == "bolted_plate":
            self.myeqns.additem("U",
                                ['U from bolted plate',
                                 1, f'1'])
            return 1
        elif shape_type == "welded_member":
            # print(l, w, x)
            # print(((3*l**2)/(3*l**2 + w**2))*(1 - (x/l)))
            self.myeqns.additem("U",
                                ['U from welded member',
                                 ((3*l**2)/(3*l**2 + w**2))*(1 - (x/l)),
                                 f'(((3*{l}**2)/(3*{l}**2 + {w}**2))*(1 - ({x}/{l})))'])
            return(((3*l**2)/(3*l**2 + w**2))*(1 - (x/l)))
        elif shape_type == "large_hss":
            self.myeqns.additem("U",
                                ['U from large hss',
                                 1, f'1'])
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
            "A_e", ["A_e", A_e, f'{A_n:.3g} * {effective_factor:.3g}'])

        P_n_gross = F_y * A_g
        # print(P_n_gross)
        self.P_n_gross = P_n_gross
        self.myeqns.additem("Nominal strength gross", [
                            "Nominal strength gross", P_n_gross, f"{F_y:.3} * {A_g:.3}"])

        P_n_net = F_u * A_e
        # print(P_n_gross)
        self.P_n_net = P_n_net
        self.myeqns.additem("Nominal strength net", [
                            "Nominal strength net", P_n_net, f"{F_u:.3} * {A_e:.3}"])

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
        self.myeqns.additem("Gross_area_in_shear",
                            ['Gross area in shear',
                             A_g, f'{x_bolts} * {t_plate}'])
        A_nv = t_plate * ((x_bolts) - (holes - 0.5 * rows) * (d_hole))
        A_nt = t_plate * ((y_bolts) - (0.5 * rows) * (d_hole))
        R_n = 0.6 * F_u * A_nv + effective_factor * F_u * A_nt
        R_n_u = 0.6 * F_y * A_g + effective_factor * F_u * A_nt

        nominal_strength = min([R_n, R_n_u])
        # this is for design strength calculation which needs both
        self.P_n_net = nominal_strength
        self.P_n_gross = 0

        self.myeqns.additem("Net_area_in_shear",
                            ['Net area in shear',
                             A_nv, f'{t_plate} * (({x_bolts}) - ({holes} - 0.5 * {rows}) * ({d_hole}))'])
        self.myeqns.additem("Net_area_in_tension",
                            ['Net area in tension',
                             A_nt, f'{t_plate} * (({y_bolts}) - (0.5 * {rows}) * ({d_hole}))'])
        self.myeqns.additem("R_n",
                            ['R_n',
                             R_n, f'0.6 * {F_u} * {A_nv:.3g} + {effective_factor} * {F_u} * {A_nt:.3g}'])
        self.myeqns.additem("R_n_u",
                            ['R_n_u',
                             R_n_u, f'0.6 * {F_y} * {A_g:.3g} + {effective_factor} * {F_u} * {A_nt:.3g}'])
        self.myeqns.additem("nominal_strength",
                            ['nominal_strength',
                             nominal_strength, f'min([{R_n}, {R_n_u}])'])


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
