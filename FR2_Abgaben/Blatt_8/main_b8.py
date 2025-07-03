import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import AutoMinorLocator
import datetime


class ExponentialFit:
    def __init__(self, x_data, y_data, y_err, fixed_half_life=None, name=""):
        self.x_data = np.array(x_data)
        self.y_data = np.array(y_data)
        self.y_err = np.array(y_err)
        self.fixed_half_life = fixed_half_life
        self.name = name

        self.results_free_hwz = None
        self.results_fixed_hwz = None
        self.results_fixed_hwz_with_b = None  # Neu: mit Verschiebung b

    # Modell ohne Verschiebung
    def model(self, x, a, tau):
        return a * np.exp(-x / tau)

    # Modell mit Verschiebung b
    def model_with_b(self, x, a, b, tau):
        return a * np.exp(-x / tau) + b

    def fit_free_hwz(self):
        p0 = [self.y_data[0], 100]
        popt, pcov = curve_fit(
            self.model,
            self.x_data,
            self.y_data,
            sigma=self.y_err,
            absolute_sigma=True,
            p0=p0
        )
        y_fit = self.model(self.x_data, *popt)
        residuals = (self.y_data - y_fit) / self.y_err
        chi2 = np.sum(residuals**2)
        ndof = len(self.x_data) - len(popt)
        chi2_red = chi2 / ndof

        tau = popt[1]
        tau_err = np.sqrt(pcov[1, 1])
        half_life = tau * np.log(2)
        half_life_err = tau_err * np.log(2)

        self.results_free_hwz = {
            'popt': popt,
            'pcov': pcov,
            'chi2_red': chi2_red,
            'half_life': half_life,
            'half_life_err': half_life_err
        }

    def fit_fixed_hwz(self):
        if self.fixed_half_life is None:
            print("Keine feste Halbwertszeit vorgegeben.")
            return

        tau_fixed = self.fixed_half_life / np.log(2)

        def model_fixed_tau(x, a):
            return a * np.exp(-x / tau_fixed)

        p0 = [self.y_data[0]]
        popt, pcov = curve_fit(
            model_fixed_tau,
            self.x_data,
            self.y_data,
            sigma=self.y_err,
            absolute_sigma=True,
            p0=p0
        )
        y_fit = model_fixed_tau(self.x_data, *popt)
        residuals = (self.y_data - y_fit) / self.y_err
        chi2 = np.sum(residuals**2)
        ndof = len(self.x_data) - len(popt)
        chi2_red = chi2 / ndof

        self.results_fixed_hwz = {
            'popt': popt,
            'pcov': pcov,
            'chi2_red': chi2_red,
            'tau_fixed': tau_fixed
        }

    # Neu: Fit mit fester HWZ und Verschiebung b
    def fit_fixed_hwz_with_b(self):
        if self.fixed_half_life is None:
            print("Keine feste Halbwertszeit vorgegeben.")
            return

        tau_fixed = self.fixed_half_life / np.log(2)

        def model_fixed_tau_b(x, a, b):
            return a * np.exp(-x / tau_fixed) + b

        p0 = [self.y_data[0], 0]
        popt, pcov = curve_fit(
            model_fixed_tau_b,
            self.x_data,
            self.y_data,
            sigma=self.y_err,
            absolute_sigma=True,
            p0=p0
        )
        y_fit = model_fixed_tau_b(self.x_data, *popt)
        residuals = (self.y_data - y_fit) / self.y_err
        chi2 = np.sum(residuals**2)
        ndof = len(self.x_data) - len(popt)
        chi2_red = chi2 / ndof

        self.results_fixed_hwz_with_b = {
            'popt': popt,
            'pcov': pcov,
            'chi2_red': chi2_red,
            'tau_fixed': tau_fixed
        }

    def _plot(self):
        if self.results_free_hwz is None:
            self.fit_free_hwz()
        if self.fixed_half_life is not None and self.results_fixed_hwz is None:
            self.fit_fixed_hwz()
        if self.fixed_half_life is not None and self.results_fixed_hwz_with_b is None:
            self.fit_fixed_hwz_with_b()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        fig.suptitle("Plausibilitätsbetrachtung einer Praktikumsauswertung", x=0.1,  ha="left")
        fig.text(0.97, 0.95, f"{self.name}, {datetime.datetime.now().strftime('%d. %B %Y')}", ha='right', va='top', fontsize=10)
            # (1, 1.05, f"{self.name}, {datetime.datetime.now().strftime('%d. %B %Y')}", fontsize=10)

        ax1.errorbar(self.x_data, self.y_data, yerr=self.y_err, fmt='kx', label='Daten', capsize=5)

        x_fit = np.linspace(min(self.x_data), max(self.x_data), 500)


        # Freie HWZ
        y_fit_free = self.model(x_fit, *self.results_free_hwz['popt'])
        ax1.plot(x_fit, y_fit_free, 'r-', label='Fit (freie HWZ)')

        # Feste HWZ
        if self.results_fixed_hwz is not None:
            tau_fixed = self.results_fixed_hwz['tau_fixed']

            def model_fixed_tau(x, a):
                return a * np.exp(-x / tau_fixed)

            y_fit_fixed = model_fixed_tau(x_fit, *self.results_fixed_hwz['popt'])
            ax1.plot(x_fit, y_fit_fixed, 'b--', label=f'Fit (feste HWZ={self.fixed_half_life:.1f} s)')

        # Plot von fester HWZ mit b NICHT, nur berechnen!

        ax1.set_ylabel('Zählrate')
        ax1.legend()
        ax1.tick_params(axis='both', which="both", direction='in', top=True, right=True)
        ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax1.yaxis.set_minor_locator(AutoMinorLocator(5))





        # Residuen plotten
        y_model_free = self.model(self.x_data, *self.results_free_hwz['popt'])
        res_free = (self.y_data - y_model_free) / self.y_err
        ax2.errorbar(self.x_data, res_free, yerr=np.ones_like(self.y_err), fmt='ro', label='Residuen (frei)', capsize=5)

        if self.results_fixed_hwz is not None:
            tau_fixed = self.results_fixed_hwz['tau_fixed']

            def model_fixed_tau(x, a):
                return a * np.exp(-x / tau_fixed)

            y_model_fixed = model_fixed_tau(self.x_data, *self.results_fixed_hwz['popt'])
            res_fixed = (self.y_data - y_model_fixed) / self.y_err
            ax2.errorbar(self.x_data, res_fixed, yerr=np.ones_like(self.y_err), fmt='bx', label='Residuen (fest)', capsize=5)

        ax2.axhline(0, color='k', linestyle='--')
        ax2.set_xlabel('Zeit [s]')
        ax2.set_ylabel('Normierte Residuen')
        ax2.legend()

        ax2.tick_params(axis='both', which="both", direction='in', top=True, right=True)
        ax2.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax2.yaxis.set_minor_locator(AutoMinorLocator(5))

        plt.tight_layout()

    def plot(self):
        self._plot()
        plt.show()

    def save(self):
        self._plot()
        plt.savefig(f"Graphs/Blatt_8_graph", dpi=600)

        # Ausgabe
        print("\n--- Fit mit freier Halbwertszeit (kein b) ---")
        popt = self.results_free_hwz['popt']
        pcov = self.results_free_hwz['pcov']
        print(f"a = {popt[0]:.2f} ± {np.sqrt(pcov[0, 0]):.2f}")
        print(f"tau = {popt[1]:.2f} ± {np.sqrt(pcov[1, 1]):.2f}")
        print(f"Halbwertszeit = {self.results_free_hwz['half_life']:.2f} ± {self.results_free_hwz['half_life_err']:.2f} s")
        print(f"Reduziertes Chi² = {self.results_free_hwz['chi2_red']:.2f}")

        if self.results_fixed_hwz is not None:
            print("\n--- Fit mit fester Halbwertszeit (kein b) ---")
            popt = self.results_fixed_hwz['popt']
            pcov = self.results_fixed_hwz['pcov']
            print(f"a = {popt[0]:.2f} ± {np.sqrt(pcov[0, 0]):.2f}")
            print(f"Feste Halbwertszeit (vorgegeben): {self.fixed_half_life:.2f} s")
            print(f"Reduziertes Chi² = {self.results_fixed_hwz['chi2_red']:.2f}")

        if self.results_fixed_hwz_with_b is not None:
            print("\n--- Fit mit fester Halbwertszeit und Verschiebung b ---")
            popt = self.results_fixed_hwz_with_b['popt']
            pcov = self.results_fixed_hwz_with_b['pcov']
            print(f"a = {popt[0]:.2f} ± {np.sqrt(pcov[0, 0]):.2f}")
            print(f"b = {popt[1]:.2f} ± {np.sqrt(pcov[1, 1]):.2f}")
            print(f"Feste Halbwertszeit (vorgegeben): {self.fixed_half_life:.2f} s")
            print(f"Reduziertes Chi² = {self.results_fixed_hwz_with_b['chi2_red']:.2f}")


class Data1:
    def __init__(self):
        self.name = ""
        self.x_data = np.array([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400,
                  420, 440, 460, 480, 500, 520, 540, 560, 580, 600])

        self.y_data = np.array([1938, 1859, 1684, 1475, 1441, 1255, 1139, 1105, 933, 891, 835, 701, 700, 620, 536, 545, 455, 420, 417,
                  334, 335, 311, 250, 267, 226, 194, 209, 162, 156, 159, 117])

        self.y_err = np.array([44.25, 43.35, 41.28, 38.67, 38.22, 35.71, 34.04, 33.54, 30.87, 30.18, 29.24, 26.85, 26.83, 25.3, 23.58,
                 23.77, 21.79, 20.98, 20.9, 18.81, 18.84, 18.19, 16.43, 16.94, 15.68, 14.63, 15.13, 13.49, 13.27, 13.38,
                 11.7])

class Data66:
    def __init__(self):
        self.name = "Marius Trabert"
        self.x_data = np.array([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400,
                  420, 440, 460, 480, 500, 520, 540, 560, 580, 600])

        self.y_data = np.array([
    2165, 2075, 1885, 1660, 1618, 1418, 1293, 1253, 1069, 1021,
    959, 816, 811, 725, 636, 643, 546, 508, 504, 415,
    414, 389, 324, 340, 296, 262, 277, 227, 220, 222, 178
])

        self.y_err = np.array([
    46.53, 45.55, 43.42, 40.74, 40.22, 37.66, 35.96, 35.4, 32.7, 31.95,
    30.97, 28.57, 28.48, 26.93, 25.22, 25.36, 23.37, 22.54, 22.45, 20.37,
    20.35, 19.72, 18, 18.44, 17.2, 16.19, 16.64, 15.07, 14.83, 14.9, 13.34
])

class Data59:
    def __init__(self):
        self.name = ""
        self.x_data = np.array([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400,
                  420, 440, 460, 480, 500, 520, 540, 560, 580, 600])

        self.y_data = np.array([
    2293, 2191, 1985, 1746, 1696, 1482, 1346, 1300, 1105, 1051,
    983, 830, 823, 731, 635, 641, 538, 497, 490, 396,
    394, 366, 297, 313, 267, 230, 245, 192, 184, 186, 139
])

        self.y_err = np.array([
    48.09, 47.02, 44.78, 42.02, 41.42, 38.76, 36.96, 36.33, 33.54, 32.73,
    31.67, 29.15, 29.03, 27.4, 25.59, 25.71, 23.62, 22.74, 22.58, 20.4,
    20.35, 19.65, 17.8, 18.25, 16.94, 15.81, 16.28, 14.56, 14.28, 14.35, 12.61
])


data = Data66()

fit = ExponentialFit(data.x_data, data.y_data, data.y_err, 153, data.name)
fit.save()

