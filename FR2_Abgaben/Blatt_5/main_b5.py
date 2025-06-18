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


def legendre(x, num):
    if num == 0:
        return 1
    if num == 1:
        return x
    if num == 2:
        return 0.5 * (3 * x ** 2 - 1)


class Legendre_Reg:
    def __init__(self, data):
        self.angle_data = np.asarray(data[0])
        self.y_data = np.asarray(data[1])
        self.x_data = math.cos(self.angle_data)

        self.result = self._calc()
        print(self.result)

    def _calc(self):

        x_leg = np.vstack([
            np.ones_like(self.x_data),
            self.x_data,
            0.5 * (3 * self.x_data ** 2 - 1)
        ]).T

        model = sm.OLS(self.y_data, x_leg)
        model_fit = model.fit()

        y_pred = model_fit.predict(x_leg)

        return model, y_pred, model.coef_


class Plot:
    def __init__(self, _reg):

        self.name = "Marius Trabert"

        self.reg = _reg
        self.boundary = [self.reg.x_data[0]-0.1, self.reg.x_data[-1]+0.1]
        self.a1 = round_sigfig(self.reg.parameters[0], self.reg.errors[0])
        self.a2 = round_sigfig(self.reg.parameters[1], self.reg.errors[1])
        self.a3 = round_sigfig(self.reg.parameters[2], self.reg.errors[2])

        self._graph = plt

    def _regression(self, x):
        y = 0
        for i in range(3):
            y += self.reg.parameters[i]*legendre(np.cos(x*(2*math.pi)/360), i)
        return y

    def _plot_ready(self):
        self._graph.clf()

        self._graph.errorbar(self.reg.x_data, self.reg.y_data, yerr=self.reg.y_err, fmt='x', color='black', capsize=3,
                             label="um Hintergrund bereinigte Zählereignisse")

        temp_range = np.linspace(0, 180, 500)
        regression_line = self._regression(temp_range)

        label_txt = f"Ausgleichskurve:\n" \
                    f"Bestwert Legendre Polynome 2. Grades"
        undertitle = f"Werte der Ausgleichskurve betragen:\n" \
                     f"Legendre Faktor a0: ({self.a1[0]}±{self.a1[1]})\n" \
                     f"Legendre Faktor a1: ({self.a2[0]}±{self.a2[1]})\n" \
                     f"Legendre Faktor a2: ({self.a3[0]}±{self.a3[1]})"
        plot_name = "(Abbildung 2)"
        self._graph.plot(temp_range, regression_line, 'r-', label=label_txt)

        self._graph.xlim(left=10, right=170)
        self._graph.xlabel("Winkel (deg)")
        plt.ylim(bottom=-0.01)
        self._graph.ylabel("Residuen")
        self._graph.title("Streuung von Antiprotonen an flüssigem Wasserstoff", loc='left', y=1.05)

        self._graph.tick_params(axis='both', which="both", direction='in', top=True, right=True)
        self._graph.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
        self._graph.gca().yaxis.set_minor_locator(AutoMinorLocator(5))


        self._graph.figtext(1, 1.05, f"{self.name}, {datetime.datetime.now().strftime('%d. %B %Y')}", ha='right', va='top',
                    transform=self._graph.gca().transAxes, fontsize=10)
        self._graph.subplots_adjust(bottom=0.25)
        self._graph.figtext(0.125, 0.04, undertitle)
        self._graph.figtext(0.75, 0.14, plot_name)

        self._graph.legend()

    def _residuals_ready(self):
        self._graph.clf()
        self._graph.errorbar(self.reg.x_data, self.reg.residuals, fmt='x', color='black', capsize=3,
                             label="Residuen")

        self._graph.axhline(y=0)

        self._graph.xlim(left=10, right=170)
        self._graph.xlabel("Winkel (deg)")

        self._graph.ylabel("Erfasste Zählereignisse")
        self._graph.title("Residuen der Legendreregression", loc='left', y=1.05)

        self._graph.tick_params(axis='both', which="both", direction='in', top=True, right=True)
        self._graph.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
        self._graph.gca().yaxis.set_minor_locator(AutoMinorLocator(5))

        self._graph.figtext(1, 1.05, f"{self.name}, {datetime.datetime.now().strftime('%d. %B %Y')}", ha='right',
                            va='top',
                            transform=self._graph.gca().transAxes, fontsize=10)
        plot_name = "(Abbildung 1)"
        self._graph.figtext(0.75, 0.14, plot_name)

        self._graph.legend()

    def show_plot(self):
        self._plot_ready()
        self._graph.show()

    def show_residuals(self):
        self._residuals_ready()
        self._graph.show()

    def save_plot(self):
        self._plot_ready()
        self._graph.savefig(f"Graphs/Blatt_5_graph", dpi=600)

    def save_residuals(self):
        self._residuals_ready()
        self._graph.savefig(f"Graphs/Blatt_5_residuen", dpi=600)


class Data66:
    def __init__(self):
        self.x_data_ = [-0.906307787,
-0.707106781,
-0.5,
-0.173648178,
0,
0.258819045,
0.422618262,
0.573576436,
0.766044443,
0.939692621]  # cos
        self.x_data = [155, 135, 120, 100, 90, 75, 65, 55, 40, 20]  # winkel
        self.y_data = [174, 116,
91,
47,
47,
53,
62,
67,
120,
202]
        self.y_err = [14,
12,
11,
7,
8,
8,
9,
11,
13,
16]
        self.parameters = [93.1, -7.4, 104]
        self.errors = [3.4, 6.6, 8.0]
        self.residuals = [-2, -8, 7, 0, 6, 3, -4, -21, -7, 30]


class Data59:
    def __init__(self):
        self.x_data = [155, 135, 120, 100, 90, 75, 65, 55, 40, 20]
        self.y_data = [174, 120, 91, 47, 41, 53, 62, 63, 120, 207]
        self.y_err = [14, 12, 11, 7, 8, 8, 9, 11, 13, 16]
        self.parameters = [92.9, -8.5, 107.6]
        self.errors = [3.4, 6.6, 8]
        self.residuals = [-5, -6, 7, 2, 2, 5, -2, -24, -7, 33]


if __name__ == '__main__':
    data = Data66()
    plot = Plot(data)
    plot.save_plot()
    plot.save_residuals()

