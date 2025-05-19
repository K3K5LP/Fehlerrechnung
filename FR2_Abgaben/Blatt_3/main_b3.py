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
        print(self.x_mean, self.y_mean)
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
            x_erriter = i[0] - self.x_mean
            x_err += x_erriter**2
            y_erriter = i[1] - self.y_mean
            y_err += y_erriter**2
            cov += x_erriter*y_erriter
        cov = cov / len(self.data)
        x_err = x_err / len(self.data)
        y_err = y_err / len(self.data)
        return cov, x_err, y_err

    def calc_r(self):
        r = self.covar/(np.sqrt(self.x_err)*np.sqrt(self.y_err))
        return r


def plot(line):
    plt.errorbar(line.x_data, line.y_data, fmt='x', color='black')

    fit = [_affine_function(x, line.slope, line.intercept) for x in line.x_data]
    slope, slope_err = round_sigfig(line.slope, line.slope_err)
    intercept, intercept_err = round_sigfig(line.intercept, line.intercept_err)
    label = f"Ausgleichsgerade:\n{slope} ±{slope_err} "\
            f"[g/(m³*°C)]*x +{slope} ±{slope_err}[g/m³]"

    plt.plot(line.x_data, fit, 'r-', label=label)

    plt.xlabel('Temperatur [°C]')
    plt.ylabel('Luftfeuchte [g/m³]')
    plt.title('Darstellung Korrelation Temperatur zu rel. Luftfeuchtigkeit', loc='left', y=1.04)
    plt.legend()
    plt.tick_params(axis='both', which="both", direction='in', top=True, right=True)
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(5))

    plt.figtext(1, 1.04, f"Marius Trabert, {datetime.datetime.now().strftime('%d. %B %Y')}", ha='right', va='top',
                transform=plt.gca().transAxes, fontsize=10)
    plt.show()


if __name__ == '__main__':

    data_set = [[-15, 0.79], [-11, 0.90], [-7, 1.32],[-3, 2.23],[1, 1.91],[5, 2.12],[9,5.09],[13, 5.03],[17, 5.30], [21, 6.57],[25, 8.48],
                [29, 12.98], [33, 18.54], [37, 22.57], [41, 35.07]]
    calc = LinReg(data_set)
    print(calc.r_value)

    plot(calc)
