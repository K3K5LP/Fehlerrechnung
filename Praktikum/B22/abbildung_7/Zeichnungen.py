import data_file
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import scipy as sp
import math


# Exponentielle Funktion: y = A * exp(B * x)
def _exp_function(x, a, b):
    return a * np.exp(b * x)


def _affine_function(x, m, b):
    return m*x + b


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


def param_string(parameter):
    if float(parameter) < 0:
        return str(f"-{parameter.strip('-')}")
    else:
        return str(f"+{parameter}")


class Plotter:
    def __init__(self, table, y_label, title="", save=False, x_start=0, y_start=0):

        self.data = data_file.data_set[table]

        self.title = title
        self.number = f"Abbildung 7"
        self.save = save
        self.x_start = x_start
        self.y_start = y_start
        self.size = 6

        # Extrahieren der Spannung (volt) und Stromwerte (current)
        self.volt = self.data[:, 0]
        self.volt_err = self.data[:, 1]
        self.current = self.data[:, 2]
        self.current_err = self.data[:, 3]
        self.volt_fit = np.linspace(self.x_start, max(self.volt) * 1.2, 10000)
        self.y_label = y_label
        self.current_fit = []

    def trim_data(self, size_min, size_max):
        volt = np.array([])
        current = np.array([])
        for x in range(len(self.volt_fit)):
            if size_min <= self.volt_fit[x] <= size_max:
                volt = np.append(volt, self.volt_fit[x])
                current = np.append(current, self.current_fit[x])

        return volt, current

    def lin_reg(self, size=None):
        if size is None:
            volt, current = self.volt, self.current
        else:
            volt, current, _, _ = self.trim_data(size)

        output = sp.stats.linregress(volt, current)
        slope = output.slope
        intercept = output.intercept
        slope_err = output.stderr
        intercept_err = output.intercept_stderr
        print(slope, intercept, slope_err, intercept_err)

    def lin_model(self, size=None, end=float('inf')):
        if size is None:
            volt, current = self.volt_fit, self.current_fit
        else:
            volt, current = self.trim_data(size, end)

        [opt, cov] = sp.optimize.curve_fit(_affine_function, volt, current)
        m, b = opt
        m_err, b_err = np.sqrt(np.diag(cov))

        mb_cov = cov[0][1]

        current_fit = _affine_function(self.volt_fit, m, b)

        return current_fit, [m, b, m_err, b_err, mb_cov]


    def plot(self, linear, start, fit, lin_label):
        plt.figure(figsize=(self.size * 1.41, self.size))

        current_fit = []
        label = ""
        # Fit-Kurve vorbereiten

        if type(fit) is int:
            spline = sp.interpolate.make_interp_spline(self.volt, self.current, k=fit)

            self.current_fit = spline(self.volt_fit)
            if fit == 1:
                label = f'Fit mit linearen Splines'
            else:
                label = f'Fit mit kubischen Splines'


        # Plot
        plt.plot(self.volt_fit, self.current_fit, 'r-', label=label)
        if linear:
            plt.errorbar(self.volt, self.current, xerr=self.volt_err, yerr=self.current_err, fmt='x', color='black', label='Messdaten aus Prisma 3', capsize=3)
        else:
            plt.errorbar(self.volt, self.current, xerr=self.volt_err, yerr=self.current_err, fmt='x', color='black', capsize=3)

        if linear:
            # Ausgabe der Ergebnisse
            linear_fit, [slope, intercept, slope_err, intercept_err, slope_intercept_cov] = self.lin_model(start, start+0.2)
            x_intercept = -intercept / slope
            sigma_x_intercept = np.sqrt(
                (intercept_err / slope) ** 2 + ((intercept * slope_err) / slope ** 2) ** 2 -
                2*((1/slope)*(intercept/(slope**2)))*slope_intercept_cov)


            #print(f"Schnittpunkt mit der x-Achse: {x_intercept:.4f} V")
            #print(f"Fehler des Schnittpunkts: {sigma_x_intercept:.4f} V")

            # Plot der Ausgleichsgeraden im linearen Bereich
            round_sigfig(x_intercept, sigma_x_intercept)
            plt.plot(self.volt_fit, linear_fit, '--', label=f'Linearer Fit:  {round_sigfig(slope,slope,3)[0]}(°/nm)x {param_string(round_sigfig(intercept,intercept,3)[0])}(°)')



        points = self.search_values()
        plt.plot(*zip(*points), 'ks', label="Ablesepunkte zur Bestimmung\nder unbekannten Lampe")

        if self.current[-1] == 0:
            height = max(self.current_err) * 1.8
            neg_height = -max(self.current_err) * 1.8
        else:
            height = (self.current[0]-self.y_start)*1.2 + self.y_start
            neg_height = self.y_start
        self.finish_plot((self.volt[-1]-self.x_start)*1.05 + self.x_start, height, y_beginning=neg_height)

    def search_values(self):
        val_arr = []
        for y in data_file.search_values:
            differenzen = np.abs(self.current_fit - y)  # Betrag der Abweichungen
            index_min = np.argmin(differenzen)  # Index der kleinsten Abweichung
            bester_wert = self.current_fit[index_min]
            val_arr.append([self.volt_fit[index_min], y])
            print(f"Zielwert: {self.volt_fit[index_min]}, {y}")
        return val_arr

    def finish_plot(self, x_lim, y_lim, y_beginning=0.0):
        # Achsen und Layout
        plt.xlabel('λ (nm)')
        plt.ylabel(self.y_label)
        plt.ylim(bottom=y_beginning, top=y_lim)
        plt.xlim(left=self.x_start, right=x_lim)
        plt.tick_params(axis='both', which="both", direction='in', top=True, right=True)
        #plt.minorticks_on()
        plt.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
        plt.gca().yaxis.set_minor_locator(AutoMinorLocator(5))
        plt.title(self.title, loc='left', y=1.04)
        plt.figtext(0.98, 0.04, self.number, ha="right")
        plt.get_current_fig_manager().set_window_title(self.number)
        plt.legend()
        plt.tight_layout()
        if self.save:
            plt.savefig(f"Graphs/{self.number}", dpi=600)
            plt.close()
        else:
            plt.show()

