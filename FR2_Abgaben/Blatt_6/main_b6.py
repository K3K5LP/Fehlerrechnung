import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import AutoMinorLocator


class ChiSquared:
    def __init__(self, data):
        self.x = np.array(data.x_data)
        self.y = np.array(data.y_data)
        self.name = data.name
        self.sigma = np.sqrt(self.y)
        self._graph = plt

        self.A, self.B, self.Z = self.berechne_chi2_grid(*data.boundary)
        self._plot_ready()

    def chi_squared(self, a, b):
        y_theo = a * np.exp(-b * self.x)
        return np.sum(((self.y - y_theo) / self.sigma) ** 2)

    def berechne_chi2_grid(self, a_range, b_range, a_steps=200, b_steps=200):
        a_vals = np.linspace(*a_range, a_steps)
        b_vals = np.linspace(*b_range, b_steps)
        A, B = np.meshgrid(a_vals, b_vals)
        Z = np.zeros_like(A)

        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                Z[i, j] = self.chi_squared(A[i, j], B[i, j])
        return A, B, Z

    def _plot_ready(self):
        self._graph.figure(figsize=(10, 8))
        contour = self._graph.contourf(self.A, self.B, np.log10(self.Z), levels=100, cmap="turbo")
        contour_lines = plt.contour(self.A, self.B, np.log10(self.Z), levels=10, colors='black', linewidths=0.8)
        self._graph.clabel(contour_lines, inline=True, fontsize=8)
        self._graph.xlabel("Parameter: a")
        self._graph.ylabel("Parameter: b")
        self._graph.title("Logarithmierter Chi²-Hyperraum", loc="left", y=1.05)
        cbar = self._graph.colorbar(contour)
        cbar.set_label('Log10[Chi²-Wert]')

        self._graph.tick_params(axis='both', which="both", direction='in', top=True, right=True)
        self._graph.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
        self._graph.gca().yaxis.set_minor_locator(AutoMinorLocator(5))

        self._graph.figtext(1, 1.05, f"{self.name}, {datetime.datetime.now().strftime('%d. %B %Y')}", ha='right',
                            va='top',
                            transform=self._graph.gca().transAxes, fontsize=10)
        plot_name = "(Abbildung 1)"
        self._graph.figtext(0.75, 0.06, plot_name)

    def show_plot(self):
        self._graph.show()

    def save_plot(self):
        self._graph.savefig(f"Graphs/Blatt_6_chi", dpi=600)


class Data66:
    def __init__(self):
        self.name = "Marius Trabert"
        self.x_data = np.array([20, 40, 60, 80, 100, 120, 140, 160, 180, 200])
        self.y_data = np.array([1567, 1277, 923, 803, 546, 498, 332, 299, 210, 172])
        # self.boundary = [[500, 3000], [0.01, 0.02]]
        self.boundary = [[0, 10000], [0, 0.05]]


class Data59:
    def __init__(self):
        self.name = ""
        self.x_data = np.array([20, 40, 60, 80, 100, 120, 140, 160, 180, 200])
        self.y_data = np.array([4429, 3217, 2165, 1647, 1056, 838, 523, 417, 269, 198])
        # self.boundary =[[0, 7000], [0, 0.02]]
        self.boundary = [[0, 10000], [0, 0.05]]
        # self.boundary = [[5000, 7000], [0.015, 0.02]]


if __name__ == '__main__':
    data = Data66()
    chi = ChiSquared(data)
    chi.save_plot()
    chi.show_plot()
