import data_file
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import scipy as sp


# Exponentielle Funktion: y = A * exp(B * x)
def _exp_function(x, a, b):
    return a * np.exp(b * x)


def _affine_function(x, m, b):
    return m*x + b


def param_string(parameter, accuracy=2):
    if parameter < 0:
        return str(f"-{abs(parameter):.{accuracy}}")
    else:
        return str(f"+{parameter:.{accuracy}}")


class Plotter:
    def __init__(self, table, number, y_label, title="", save=False, x_start=0):

        self.data = data_file.data_set[table]

        self.title = title
        self.number = f"[Graph {number}]"
        self.save = save
        self.x_start = x_start

        # Extrahieren der Spannung (volt) und Stromwerte (current)
        self.volt = self.data[:, 0]
        self.volt_err = self.data[:, 1]
        self.current = self.data[:, 2]
        self.current_err = self.data[:, 3]
        self.volt_fit = np.linspace(self.x_start, max(self.volt) * 1.2, 500)
        self.y_label = y_label

    def trim_data(self, size_min):
        volt = np.array([])
        current = np.array([])
        volt_err = np.array([])
        current_err = np.array([])
        for x in range(len(self.volt)):
            if size_min <= self.volt[x]:
                volt = np.append(volt, self.volt[x])
                current = np.append(current, self.current[x])
                volt_err = np.append(volt_err, self.volt_err[x])
                current_err = np.append(current_err, self.current_err[x])
        return volt, current, volt_err, current_err

    def lin_reg(self, size=None):
        if size is None:
            size = [0, 30]
        volt = []
        current = []
        volt_err = []
        current_err = []
        for x in range(len(self.volt)):
            if size[0] <= self.volt[x] <= size[1]:
                volt.append(self.volt[x])
                current.append(self.current[x])
                volt_err.append(self.volt_err[x])
                current_err.append(self.current_err[x])

        data = sp.odr.RealData(volt, current, volt_err, current_err)
        output = sp.odr.ODR(data, sp.odr.polynomial(1)).run()
        lin_fit = np.poly1d(output.beta[::-1])
        current_fit = lin_fit(self.volt_fit)
        return current_fit

    def lin_model(self, size=None):
        if size is None:
            volt, current, volt_err, current_err = self.volt, self.current, self.volt_err, self.current_err
        else:
            volt, current, volt_err, current_err = self.trim_data(size)
        [opt, cov] = sp.optimize.curve_fit(_affine_function, volt, current, sigma = current_err, absolute_sigma=True)
        m, b = opt
        m_err, b_err = np.sqrt(np.diag(cov))
        print(cov)
        mb_cov = cov[0][1]
        print(cov[0][1])

        current_fit = _affine_function(self.volt_fit, m, b)

        return current_fit, [m,b,m_err,b_err, mb_cov]

    def plot_voltage(self):
        volt, current, volt_err, current_err = self.trim_data(0.3)
        resistance = volt / current
        res_err = np.sqrt((volt_err/volt)**2+(current_err/current)**2)*resistance

        delta = []
        delta_err = []
        new_volt = []
        for i in range(1,len(volt)-1):
            res_now = (float(volt[i-1])-float(volt[i+1]))/(float(current[i-1])-float(current[i+1]))
            delta.append(res_now)
            new_volt.append(volt[i])

            delta_err.append(np.sqrt(
                (np.sqrt(float(volt_err[i-1])**2+float(volt_err[i+1])**2)/(float(volt[i-1])-float(volt[i+1])))**2+
                (np.sqrt(float(current_err[i-1])**2+float(current_err[i+1])**2)/(float(current[i-1])-float(current[i+1])))**2)
                *res_now)

        spline_res = sp.interpolate.CubicSpline(volt, resistance)
        resistance_fit = spline_res(self.volt_fit)
        label_res = f'Fit mit kubischen Splines des Widerstands'
        plt.plot(self.volt_fit, resistance_fit, '-', label=label_res)
        plt.errorbar(volt, resistance, yerr=res_err, fmt='x', color='black', capsize=3)
        print(f"Widerstand: {resistance}, {res_err}")

        spline_delta = sp.interpolate.CubicSpline(new_volt, delta)
        delta_fit = spline_delta(self.volt_fit)
        label_delta = f'Fit mit kubischen Splines des differentiellen Widerstands'

        plt.plot(self.volt_fit, delta_fit, '--', label=label_delta)
        plt.errorbar(new_volt, delta, yerr=delta_err, fmt='x', color='black', capsize=3)
        print(f"delta Widerstand: {delta}, {delta_err}")



        self.finish_plot(max(volt)*1.1, max(resistance)*1.05)

    def plot(self, linear, start, fit, error_bar):
        current_fit = []
        label = ""
        # Fit-Kurve vorbereiten

        if type(fit) is int:
            #spline = sp.interpolate.CubicSpline(self.volt, self.current)
            spline = sp.interpolate.make_interp_spline(self.volt, self.current, k=fit)
            #spline = sp.interpolate.UnivariateSpline(self.volt, self.current, k=3)
            current_fit = spline(self.volt_fit)
            if fit == 1:
                label = f'Fit mit linearen Splines'
            else:
                label = f'Fit mit kubischen Splines'

        elif fit == "exp":
            # Fit der exponentiellen Funktion
            initial_guess = [0, 10]
            [params, _] = sp.optimize.curve_fit(_exp_function, self.volt, self.current, sigma=self.current_err,
                                                absolute_sigma=True, p0=initial_guess, maxfev=100000)
            # print(params)
            current_fit = _exp_function(self.volt_fit, *params)
            label = f'Exponentieller Fit: {params[0]:.4e}(mA) * exp[{params[1]:.2f}(1/V) * x]'

        elif fit == "lin":

            current_fit, [m, b, _, _, _] = self.lin_model()
            """if m != 0:
                pot_m = int(np.log10(abs(m))-1)
            else:
                pot_m = 0
            if b != 0:
                pot_b = int(np.log10(abs(b))-1)
            else:
                pot_b = 0

            if pot_m != 0:
                a = f"e{pot_m}"
            else:
                a=""
            if pot_b != 0:
                c = f"e{pot_b}"
            else:
                c=""

            label = f'Linearer Fit:  ({m/(10**pot_m):.2f}±{m_err/(10**pot_m):.2f}){a}*x + ({b/(10**pot_b):.2f}±{b_err/(10**pot_b):.2f}){c}'

            pot = max(pot_m, pot_b)

            if pot != 0:
                a = f"e{pot}"
            else:
                a = "" """

            label = f'Linearer Fit:  {param_string(m, 2)}(mA/V)x {param_string(b, 2)}(mA)'

        # Plot
        plt.plot(self.volt_fit, current_fit, 'r-', label=label)
        if linear:
            plt.errorbar(self.volt, self.current, yerr=self.current_err, fmt='x', color='black', label='Messdaten', capsize=3)
        else:
            plt.errorbar(self.volt, self.current, yerr=self.current_err, fmt='x', color='black', capsize=3)

        if linear:
            """mask_linear = (self.volt >= start) & (self.volt <= end)
            slope, intercept = np.polyfit(self.volt[mask_linear], self.current[mask_linear], 1, full=True)[0]

            x_intercept = -intercept / slope

            # Fehler der Steigung und des y-Achsenabschnitts
            slope_err = np.sqrt(np.diag(np.cov(self.volt, self.current)))[0]
            intercept_err = np.sqrt(np.diag(np.cov(self.volt, self.current)))[1]

            # Fehler des Schnittpunkts
            sigma_x_intercept = np.sqrt((intercept / slope ** 2 * slope_err) ** 2 + (1 / slope * intercept_err) ** 2)
            """
            # Ausgabe der Ergebnisse
            linear_fit, [slope, intercept, slope_err, intercept_err, slope_intercept_cov] = self.lin_model(start)
            x_intercept = -intercept / slope
            sigma_x_intercept = np.sqrt(
                (intercept_err / slope) ** 2 + ((intercept * slope_err) / slope ** 2) ** 2 -
                2*((1/slope)*(intercept/(slope**2)))*slope_intercept_cov)


            #print(f"Schnittpunkt mit der x-Achse: {x_intercept:.4f} V")
            #print(f"Fehler des Schnittpunkts: {sigma_x_intercept:.4f} V")

            # Plot der Ausgleichsgeraden im linearen Bereich
            plt.plot(self.volt_fit, linear_fit, '--', label=f'Linearer Fit:  {param_string(slope,4)}(mA/V)x {param_string(intercept,4)}(mA)')

            plt.errorbar(x_intercept, 0, xerr=sigma_x_intercept, fmt='.', color='black', label=f"Kniespannung: ({param_string(x_intercept,4)} ± {sigma_x_intercept:.4f})V",
                         capsize=3)

        if self.current[-1] == 0:
            height = max(self.current_err) * 1.8
            neg_height = -max(self.current_err) * 1.8
        else:
            height = self.current[-1]*1.2
            neg_height = 0
        self.finish_plot((self.volt[-1]-self.x_start)*1.05 + self.x_start, height, y_beginning=neg_height)

    def finish_plot(self, x_lim, y_lim, y_beginning = 0.0):
        # Achsen und Layout
        plt.xlabel('Spannung (V)')
        plt.ylabel(self.y_label)
        plt.ylim(bottom=y_beginning, top=y_lim)
        plt.xlim(left=self.x_start, right=x_lim)
        plt.tick_params(axis='both', which="both", direction='in', top=True, right=True)
        #plt.minorticks_on()
        plt.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
        plt.gca().yaxis.set_minor_locator(AutoMinorLocator(5))
        plt.title(self.title, loc='left', y=1.04)
        plt.figtext(1, 1.04, f"Marius Trabert, {datetime.datetime.now().strftime('%d. %B %Y')}", ha='right', va='top',
                    transform=plt.gca().transAxes, fontsize=10)
        plt.figtext(0.98,0.04,self.number, ha="right")
        plt.get_current_fig_manager().set_window_title(self.number)
        plt.legend()
        plt.tight_layout()
        if self.save:
            plt.savefig(f"Graphs/{self.number}", dpi=600)
            plt.close()
        else:
            plt.show()

