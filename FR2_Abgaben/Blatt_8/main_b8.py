import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import AutoMinorLocator
import datetime


class ExponentialFit:
    def __init__(self, x_data, y_data, y_err, fixed_half_life=None, name=""):
        self.name = name

        self.x_data = np.array(x_data)
        self.y_data = np.array(y_data)
        self.y_err = np.array(y_err)
        self.fixed_half_life = fixed_half_life

        self.results = {}

    def model(self, x, A, tau, b):
        return A * np.exp(-x / tau) + b

    def model_no_b(self, x, A, tau):
        return A * np.exp(-x / tau)

    def model_fixed_tau(self, x, A, b, tau_fixed):
        return A * np.exp(-x / tau_fixed) + b

    def model_fixed_tau_no_b(self, x, A, tau_fixed):
        return A * np.exp(-x / tau_fixed)

    # Fit-Funktionen
    def fit_free_tau_free_b(self):
        p0 = [self.y_data[0], (self.x_data[-1]-self.x_data[0])/2, 0]
        popt, pcov = curve_fit(self.model, self.x_data, self.y_data, sigma=self.y_err, p0=p0, absolute_sigma=True)
        red_chi2 = self._reduced_chi2(self.model(self.x_data, *popt))
        self.results['free_tau_free_b'] = (popt, pcov, red_chi2)

    def fit_free_tau_b0(self):
        p0 = [self.y_data[0], (self.x_data[-1]-self.x_data[0])/2]
        popt, pcov = curve_fit(self.model_no_b, self.x_data, self.y_data, sigma=self.y_err, p0=p0, absolute_sigma=True)
        red_chi2 = self._reduced_chi2(self.model_no_b(self.x_data, *popt))
        self.results['free_tau_b0'] = (popt, pcov, red_chi2)

    def fit_fixed_tau_free_b(self):
        if self.fixed_half_life is None:
            print("⚠️ Feste HWZ nicht gesetzt.")
            return
        tau_fixed = self.fixed_half_life / np.log(2)
        p0 = [self.y_data[0], 0]
        popt, pcov = curve_fit(lambda x, A, b: self.model_fixed_tau(x, A, b, tau_fixed),
                               self.x_data, self.y_data, sigma=self.y_err, p0=p0, absolute_sigma=True)
        red_chi2 = self._reduced_chi2(self.model_fixed_tau(self.x_data, *popt, tau_fixed))
        self.results['fixed_tau_free_b'] = (popt, pcov, red_chi2)

    def fit_fixed_tau_b0(self):
        if self.fixed_half_life is None:
            print("⚠️ Feste HWZ nicht gesetzt.")
            return
        tau_fixed = self.fixed_half_life / np.log(2)
        p0 = [self.y_data[0]]
        popt, pcov = curve_fit(lambda x, A: self.model_fixed_tau_no_b(x, A, tau_fixed),
                               self.x_data, self.y_data, sigma=self.y_err, p0=p0, absolute_sigma=True)
        red_chi2 = self._reduced_chi2(self.model_fixed_tau_no_b(self.x_data, *popt, tau_fixed))
        self.results['fixed_tau_b0'] = (popt, pcov, red_chi2)

    def _reduced_chi2(self, y_fit):
        res = (self.y_data - y_fit) / self.y_err
        dof = len(self.y_data) - (len(self.results) + 1)
        return np.sum(res**2) / dof if dof > 0 else np.nan

    def fit_all(self):
        self.fit_free_tau_free_b()
        self.fit_free_tau_b0()
        if self.fixed_half_life is not None:
            self.fit_fixed_tau_free_b()
            self.fit_fixed_tau_b0()
        else:
            print("⚠️ Feste HWZ nicht angegeben – fixe HWZ-Fits werden übersprungen.")

    def _plot(self, mode):
        mode_map = {
            0: ('free_tau_free_b', 'Freie HWZ, freies b'),
            1: ('free_tau_b0', 'Freie HWZ, b=0'),
            2: ('fixed_tau_free_b', f'Feste HWZ={self.fixed_half_life} s, freies b'),
            3: ('fixed_tau_b0', f'Feste HWZ={self.fixed_half_life} s, b=0')
        }

        if mode not in mode_map:
            print("Bitte Modus 0-3 angeben!")
            return

        key, title = mode_map[mode]
        if key not in self.results:
            getattr(self, f"fit_{key}")()


        popt, pcov, red_chi2 = self.results[key]
        perr = np.sqrt(np.diag(pcov))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        fig.suptitle("Plausibilitätsbetrachtung einer Praktikumsauswertung", x=0.1, ha="left")
        fig.text(0.1, 0.90,title, ha='left', fontsize=14)
        fig.text(0.97, 0.90, f"{self.name}, {datetime.datetime.now().strftime('%d. %B %Y')}", ha='right', va='top',
                 fontsize=10)

        ax1.errorbar(self.x_data, self.y_data, yerr=self.y_err, fmt='o', capsize=5, label='Daten')

        x_fit = np.linspace(self.x_data.min(), self.x_data.max(), 500)

        if key == 'free_tau_free_b':
            y_fit = self.model(x_fit, *popt)
            y_model = self.model(self.x_data, *popt)
            tau = popt[1]
            tau_err = perr[1]
        elif key == 'free_tau_b0':
            y_fit = self.model_no_b(x_fit, *popt)
            y_model = self.model_no_b(self.x_data, *popt)
            tau = popt[1]
            tau_err = perr[1]
        elif key == 'fixed_tau_free_b':
            tau = self.fixed_half_life / np.log(2)
            tau_err = 0
            y_fit = self.model_fixed_tau(x_fit, *popt, tau)
            y_model = self.model_fixed_tau(self.x_data, *popt, tau)
        elif key == 'fixed_tau_b0':
            tau = self.fixed_half_life / np.log(2)
            tau_err = 0
            y_fit = self.model_fixed_tau_no_b(x_fit, *popt, tau)
            y_model = self.model_fixed_tau_no_b(self.x_data, *popt, tau)

        ax1.plot(x_fit, y_fit, 'r-', label='Fit')
        ax1.set_ylabel("Zählrate")
        ax1.tick_params(axis='both', which='both', direction='in', top=True, right=True)
        ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax1.yaxis.set_minor_locator(AutoMinorLocator(5))

        res = (self.y_data - y_model) / self.y_err
        ax2.errorbar(self.x_data, res, yerr=np.ones_like(res), fmt='o', capsize=5)
        ax2.axhline(0, color='k', linestyle='--')
        ax2.set_xlabel("Zeit [s]")
        ax2.set_ylabel("Normierte Residuen")
        ax2.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax2.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax2.tick_params(axis='both', which='both', direction='in', top=True, right=True)

        plt.tight_layout(rect=[0, 0, 1, 0.9])

        print(f"Ergebnis für {title}:")
        if 'free_tau' in key:
            hwz = tau * np.log(2)
            hwz_err = tau_err * np.log(2)
            print(f"Tau = {tau:.3f} ± {tau_err:.3f} s")
            print(f"HWZ = {hwz:.3f} ± {hwz_err:.3f} s")
        else:
            print(f"Tau (fest) = {tau:.3f} s, HWZ (fest) = {self.fixed_half_life:.3f} s")

        if 'free_tau_free_b' in key:
            print(f"A = {popt[0]:.3f} ± {perr[0]:.3f}")
            print(f"b = {popt[2]:.3f} ± {perr[2]:.3f}")
        elif 'free_tau_b0' in key:
            print(f"A = {popt[0]:.3f} ± {perr[0]:.3f}")
        elif 'fixed_tau_free_b' in key:
            print(f"A = {popt[0]:.3f} ± {perr[0]:.3f}")
            print(f"b = {popt[1]:.3f} ± {perr[1]:.3f}")
        elif 'fixed_tau_b0' in key:
            print(f"A = {popt[0]:.3f} ± {perr[0]:.3f}")

        print(f"Reduziertes Chi² = {red_chi2:.3f}\n")

    def plot(self, i):
        self._plot(i)
        plt.show()

    def save(self, i):
        self._plot(i)
        plt.savefig(f"Graphs/Blatt_8_graph_{i}", dpi=600)




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

class Data73:
    def __init__(self):
        self.name = ""
        self.x_data = np.array(
            [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400,
             420, 440, 460, 480, 500, 520, 540, 560, 580, 600])

        self.y_data = np.array([
    1978, 1896, 1717, 1505, 1469, 1280, 1162, 1127, 952, 909,
    851, 715, 713, 632, 547, 556, 464, 429, 425, 341,
    341, 317, 255, 272, 231, 198, 213, 165, 159, 162, 119
])

        self.y_err = np.array([
    44.7, 43.77, 41.68, 39.05, 38.59, 36.06, 34.38, 33.87, 31.18, 30.48,
    29.51, 27.11, 27.07, 25.53, 23.81, 24.0, 22.0, 21.19, 21.1, 19.0,
    19.0, 18.36, 16.58, 17.09, 15.84, 14.76, 15.26, 13.6, 13.38, 13.49, 11.79
])

if __name__ == '__main__':
    data = Data66()

    fit = ExponentialFit(data.x_data, data.y_data, data.y_err, 153, data.name)
    for i in range(4):
        fit.save(i)


