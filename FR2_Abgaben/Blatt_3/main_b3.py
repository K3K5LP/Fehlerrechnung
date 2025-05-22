import scipy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import datetime
import math


def mean(data):
    s = 0
    for i in data:
        s += i
    s = s/len(data)
    return s


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


def _affine_function(x, m, b):
    return m*x + b


class LinReg:
    def __init__(self, data):
        self.data = data
        self.x_data = [val[0] for val in data]
        self.x_mean = mean([val[0] for val in data])
        self.y_data = [val[1] for val in data]
        self.y_mean = mean([val[1] for val in data])
        # print(self.x_mean, self.y_mean)
        self.covar, self.x_err, self.y_err = self.covariant()

        self.result = scipy.stats.linregress(data)
        self.slope = self.result.slope
        self.intercept = self.result.intercept
        self.r_value = self.result.rvalue
        self.slope_err = self.result.stderr
        self.intercept_err = self.result.intercept_stderr
        print(self. slope, self.intercept, self.r_value, self.slope_err, self.intercept_err)

    def covariant(self):
        cov = x_err = y_err = 0
        for i in self.data:
            x_err_iter = i[0] - self.x_mean
            x_err += x_err_iter**2
            y_err_iter = i[1] - self.y_mean
            y_err += y_err_iter**2
            cov += x_err_iter*y_err_iter
        cov = cov / len(self.data)
        x_err = x_err / len(self.data)
        y_err = y_err / len(self.data)
        return cov, x_err, y_err

    def calc_r(self):
        r = self.covar/(np.sqrt(self.x_err)*np.sqrt(self.y_err))
        return r


class Plot:
    def __init__(self, line):
        self.line = line
        self.boundary = [self.line.x_data[0]-2, self.line.x_data[-1]+2]

        self._graph = plt

        self._plot_ready()

    def _plot_ready(self):

        self._graph.errorbar(self.line.x_data, self.line.y_data, fmt='x', color='black')

        temp_range = np.linspace(self.boundary[0], self.boundary[1], 5)
        regression_line = _affine_function(temp_range, self.line.slope, self.line.intercept)
        slope, slope_err = round_sigfig(self.line.slope, self.line.slope_err)
        intercept, intercept_err = round_sigfig(self.line.intercept, self.line.intercept_err)
        label_txt = f"Ausgleichsgerade:\n{slope} ±{slope_err} "\
                    f"(g/(m³*°C))*x +{intercept} ±{intercept_err}(g/m³)"
        label_txt = f"Ausgleichsgerade:\n" \
                    f"B⋅x + A"
        undertitle = f"Werte der Ausgleichsgeraden betragen:\n" \
                     f"Steigung B: ({slope} ±{slope_err})(g/(°C⋅m³))\n" \
                     f"Ordinaten-verschiebung A: ({intercept} ±{intercept_err})(g/m³)"
        self._graph.plot(temp_range, regression_line, 'r-', label=label_txt)

        self._graph.xlim(left=self.boundary[0], right=self.boundary[1])
        self._graph.xlabel('Temperatur (°C)')
        plt.ylim(bottom=0)
        self._graph.ylabel('Luftfeuchte (g/m³)')
        self._graph.title('Darstellung Korrelation Temperatur zu rel. Luftfeuchte', loc='left', y=1.05)

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
        self._graph.savefig(f"Graphs/Blatt_3", dpi=600)


class PlotTest:

    def __init__(self):
        self.boundary = [-2, 2]
        temp_range = np.linspace(self.boundary[0], self.boundary[1], 5)
        regression_line = _affine_function(temp_range, 1, 2)
        plt.plot(temp_range, regression_line, 'r-', label="label_txt")
        plt.legend()
        plt.show()


if __name__ == '__main__':
    # Meine
    data_set = [[-15, 0.79], [-11, 0.90], [-7, 1.32], [-3, 2.23], [1, 1.91], [5, 2.12], [9, 5.09], [13, 5.03],
                 [17, 5.30], [21, 6.57], [25, 8.48], [29, 12.98], [33, 18.54], [37, 22.57], [41, 35.07]]
    # 16
    _data_set = [[-15, 0.65], [-11, 0.73], [-7, 1.08], [-3, 1.81], [1, 1.55], [5, 1.72], [9, 4.13], [13, 4.09],
                [17, 4.30], [21, 5.33], [25, 6.88], [29, 10.54], [33, 15.05], [37, 18.32], [41, 28.47]]
    # 59
    _data_set = [[-15, 0.87], [-11, 0.99], [-7, 1.45], [-3, 2.43], [1, 2.09], [5, 2.32], [9, 5.56], [13, 5.51],
                [17, 5.80], [21, 7.19], [25, 9.27], [29, 14.2], [33, 20.29], [37, 24.69], [41, 38.37]]

    calc = LinReg(data_set)
    print(calc.covar)

    plot = Plot(calc)
    plot.save_plot()

