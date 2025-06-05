import math
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator
import datetime


def round_sigfig(value, error, digits=2):
    def _round_sig(number, r_digits):
        if r_digits < 0:
            r_digits = 0
        r_number = f"{number:.{r_digits}f}"
        return r_number, r_digits
    if error != 0:
        trunkate = digits - math.ceil(math.log10(abs(error)))
    else:
        trunkate = digits
    r_error, sig_figs = _round_sig(abs(error), trunkate)
    r_value, _ = _round_sig(value, sig_figs)
    return r_value, r_error


def quadratic(x, c, b, a):
    return a*x**2 + b*x + c


class LinReg:
    def __init__(self, _data):
        self.y_data = np.array([(val[0]-1)/50 for val in _data])
        self.x_data = np.array([val[1] for val in _data])

        x = np.column_stack((self.x_data, self.x_data ** 2))
        x = sm.add_constant(x)

        model = sm.OLS(self.y_data, x)
        results = model.fit()
        self.parameters = results.params
        self.errors = results.bse

        self.addons = self._addons()
        self.a1 = round_sigfig(self.parameters[0], self.errors[0])
        self.a2 = round_sigfig(self.parameters[1], self.errors[1])
        self.a3 = round_sigfig(self.parameters[2], self.errors[2])
        self.gravitation_constant = round_sigfig(self.parameters[2]*2, self.errors[2]*2)

        self.output = f"Sum(xi):{self.addons[1]};\tSum(xi^2):{self.addons[2]}\n" \
                      f"Sum(xi^3):{self.addons[3]};\tSum(xi^4):{self.addons[4]}\n" \
                      f"Sum(yi):{self.addons[5]};\tSum(xi*yi):{self.addons[6]}\n" \
                      f"Sum(xi^2*yi):{self.addons[7]}\tDelta:{self.addons[8]}\n" \
                      f"N:{len(self.x_data)};\tst_err:{self.addons[0]}\n" \
                      f"a1:{self.a1[0]}±{self.a1[1]}\t" \
                      f"a2:{self.a2[0]}±{self.a2[1]}\n" \
                      f"a3:{self.a3[0]}±{self.a3[1]}\t" \
                      f"g:{self.gravitation_constant[0]}±{self.gravitation_constant[1]}"

    def _addons(self):
        long_sum = sum((y-self.parameters[0]-self.parameters[1]*x-self.parameters[2]*x**2)**2
                       for x, y in zip(self.x_data, self.y_data))
        standard_err = math.sqrt((1/(len(self.x_data)-3))*long_sum)
        lin_sum = sum(x for x in self.x_data)
        square_sum = sum(x**2 for x in self.x_data)
        cube_sum = sum(x**3 for x in self.x_data)
        quad_sum = sum(x**4 for x in self.x_data)
        y_sum = sum(y for y in self.y_data)
        y_x_sum = sum(x*y for x, y in zip(self.x_data, self.y_data))
        y_xx_sum = sum((x**2)*y for x, y in zip(self.x_data, self.y_data))
        n = len(self.x_data)
        delta = (1/1)*(n*square_sum*quad_sum + 2*lin_sum*cube_sum*square_sum - square_sum**3 - lin_sum**2*quad_sum - n*cube_sum**2)

        return standard_err, lin_sum, square_sum, cube_sum, quad_sum, y_sum, y_x_sum, y_xx_sum, delta


class Plot:
    def __init__(self, _reg):
        self.reg = _reg
        self.boundary = [self.reg.x_data[0], self.reg.x_data[-1]+0.03]


        self._graph = plt

        self._plot_ready()

    def _plot_ready(self):

        self._graph.errorbar(self.reg.x_data, self.reg.y_data, fmt='x', color='black')

        temp_range = np.linspace(self.boundary[0], self.boundary[1], 500)
        regression_line = quadratic(temp_range, *self.reg.parameters)
        label_txt = f"Ausgleichskurve:\n" \
                    f"Ax^2+Bx+C"
        undertitle = f"Werte der Ausgleichskurve betragen:\n" \
                     f"Krümmung A: ({self.reg.a3[0]}±{self.reg.a3[1]})(m/s^2)\n" \
                     f"Steigung B: ({self.reg.a2[0]}±{self.reg.a2[1]})(m/s)\n" \
                     f"Ordinaten-verschiebung C: ({self.reg.a1[0]}±{self.reg.a1[1]})(m)"
        self._graph.plot(temp_range, regression_line, 'r-', label=label_txt)

        self._graph.xlim(left=self.boundary[0]-0.01, right=self.boundary[1])
        self._graph.xlabel("Fallzeit (s)")
        plt.ylim(bottom=-0.01)
        self._graph.ylabel("Fallhöhe (m)")
        self._graph.title("Darstellung Fallhöhe zu Fallzeit", loc='left', y=1.05)

        self._graph.tick_params(axis='both', which="both", direction='in', top=True, right=True)
        self._graph.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
        self._graph.gca().yaxis.set_minor_locator(AutoMinorLocator(5))

        self._graph.figtext(1, 1.05, f"Marius Trabert, {datetime.datetime.now().strftime('%d. %B %Y')}", ha='right', va='top',
                    transform=self._graph.gca().transAxes, fontsize=10)
        self._graph.subplots_adjust(bottom=0.25)
        self._graph.figtext(0.125, 0.04, undertitle)

        self._graph.legend()

    def show_plot(self):
        self._graph.show()

    def save_plot(self):
        self._graph.savefig(f"Graphs/Blatt_4", dpi=600)


if __name__ == '__main__':
    data_66 = [[1, 0], [2, 0.071392], [3, 0.096313], [4, 0.115116], [5, 0.132797], [6, 0.146310],
               [7, 0.159318], [8, 0.171935], [9, 0.183410], [10, 0.194732], [11, 0.204436], [12, 0.214176],
               [13, 0.223948], [14, 0.232436], [15, 0.240200]]
    data_16 = [[1, 0.0], [2, 0.068477], [3, 0.094173], [4, 0.113332], [5, 0.131253], [6, 0.144910], [7, 0.158033],
               [8, 0.170745], [9, 0.182295], [10, 0.193682], [11, 0.203436], [12, 0.213222], [13, 0.223036],
               [14, 0.231557], [15, 0.239350]]
    data_59 = [[1, 0.0], [2, 0.069364], [3, 0.094820], [4, 0.113870], [5, 0.131718], [6, 0.145332], [7, 0.158420],
               [8, 0.171103], [9, 0.182630], [10, 0.193998], [11, 0.203737], [12, 0.213509], [13, 0.223310],
               [14, 0.231821], [15, 0.239606]]
    data_73 = [
    [1, 0.0],
    [2, 0.073364],
    [3, 0.097784],
    [4, 0.116350],
    [5, 0.133867],
    [6, 0.147283],
    [7, 0.160211],
    [8, 0.172763],
    [9, 0.184186],
    [10, 0.195463],
    [11, 0.205133],
    [12, 0.214842],
    [13, 0.224585],
    [14, 0.233049],
    [15, 0.240794]
]
    reg = LinReg(data_66)
    print(reg.output)
    plot = Plot(reg)
    plot.save_plot()


