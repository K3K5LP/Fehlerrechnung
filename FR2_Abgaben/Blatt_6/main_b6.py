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
        self.start = data.start
        self.window = [200, 0.002]

        self.reg_param = []
        self.A, self.B, self.Z = self.berechne_chi2_grid(*data.boundary)

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

    def _plot_ready(self, big_plot = True):
        print("plot")
        #self._graph.clf()
        if big_plot:
            plot_number = 1
            h, j, k = self.A, self.B, np.log10(self.Z)
        else:
            plot_number = 2
            if not self.reg_param:
                self.optimize()

            a_range = [self.reg_param[0] - self.window[0], self.reg_param[0] + self.window[0]]
            b_range = [self.reg_param[1] - self.window[1], self.reg_param[1] + self.window[1]]
            h, j, o = self.berechne_chi2_grid(a_range, b_range)
            k = np.log10(o)
        self._graph.figure(figsize=(10, 8))
        contour = self._graph.contourf(h, j, k, levels=100, cmap="turbo")
        contour_lines = plt.contour(h, j, k, levels=10, colors='black', linewidths=0.8)
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
        plot_name = f"(Abbildung {plot_number})"
        self._graph.figtext(0.75, 0.06, plot_name)

    def show_big_plot(self):
        print("show")
        self._plot_ready()
        self._graph.show()

    def show_small_plot(self):
        self._plot_ready(False)
        self._graph.show()


    def save_big_plot(self):
        self._plot_ready()
        self._graph.savefig(f"Graphs/Blatt_6_chi", dpi=600)

    def save_small_plot(self):
        self._plot_ready(False)
        self._graph.savefig(f"Graphs/Blatt_6_chi_small", dpi=600)


    @staticmethod
    def parabolisches_minimum(x1, x2, x3, y1, y2, y3):
        denom = (x1 - x2)*(x1 - x3)*(x2 - x3)
        A = (x3*(y2 - y1) + x2*(y1 - y3) + x1*(y3 - y2)) / denom
        B = (x3**2*(y1 - y2) + x2**2*(y3 - y1) + x1**2*(y2 - y3)) / denom
        x_min = -B / (2*A)
        return x_min

    def optimize(self, delta_a=50, delta_b=0.002, tol=1e-10, max_iter=2000, second=False, start=None):
        if start is None:
            a, b = self.start
        else:
            a, b = start
        # print(f"Startwerte: a = {a:.2f}, b = {b:.5f}")
        chi2_new = self.chi_squared(a, b)
        for iteration in range(max_iter):
            prev_chi2 = self.chi_squared(a, b)

            prev_chi2_a = prev_chi2
            chi2_down_a = self.chi_squared(a - delta_a, b)
            chi2_up_a = self.chi_squared(a + delta_a, b)
            while chi2_down_a < prev_chi2_a:
                a= a - delta_a
                prev_chi2_a = chi2_down_a
                chi2_down_a = self.chi_squared(a - delta_a, b)
            while chi2_up_a < prev_chi2_a:
                a = a + delta_a
                prev_chi2_a = chi2_up_a
                chi2_up_a = self.chi_squared(a + delta_a, b)

            a_candidates = [a - delta_a, a, a + delta_a]
            chi2_a = [self.chi_squared(a_cand, b) for a_cand in a_candidates]
            a_opt = self.parabolisches_minimum(*a_candidates, *chi2_a)

            prev_chi2_b = prev_chi2
            chi2_down_b = self.chi_squared(a, b - delta_b)
            chi2_up_b = self.chi_squared(a, b + delta_b)
            while chi2_down_b < prev_chi2_b:
                b = b - delta_b
                prev_chi2_b = chi2_down_a
                chi2_down_b = self.chi_squared(b, b - delta_b)
            while chi2_up_b < prev_chi2_b:
                b = b + delta_b
                prev_chi2_b = chi2_up_b
                chi2_up_b = self.chi_squared(a, b + delta_a)

            b_candidates = [b - delta_b, b, b + delta_b]
            chi2_b = [self.chi_squared(a_opt, b_cand) for b_cand in b_candidates]
            b_opt = self.parabolisches_minimum(*b_candidates, *chi2_b)

            chi2_new = self.chi_squared(a_opt, b_opt)
            if chi2_new > prev_chi2:
                print("smaller")
                delta_a = delta_a/10
                delta_b = delta_b/10

            else:
                print(f"Iter {iteration+1}: a = {a_opt}, b = {b_opt}, chi² = {chi2_new}")

                if abs(chi2_new - prev_chi2) < tol:
                    print("test ende")
                    if second or abs(self.optimize(delta_a/10, delta_b/10, tol, second=True, start=[a_opt, b_opt])[2]-chi2_new) < tol:
                        print("Konvergenz erreicht.")
                        break
                    else:
                        delta_a = delta_a / 100
                        delta_b = delta_b / 100

            a, b = a_opt, b_opt

        self.reg_param = [a, b, chi2_new]

        return [a, b, chi2_new]


class Data66:
    def __init__(self):
        self.name = "Marius Trabert"
        self.x_data = np.array([20, 40, 60, 80, 100, 120, 140, 160, 180, 200])
        self.y_data = np.array([1567, 1277, 923, 803, 546, 498, 332, 299, 210, 172])
        self.boundary = [[0, 10000], [0, 0.05]]
        self.start = [3000, 0.015]


class Data59:
    def __init__(self):
        self.name = ""
        self.x_data = np.array([20, 40, 60, 80, 100, 120, 140, 160, 180, 200])
        self.y_data = np.array([4429, 3217, 2165, 1647, 1056, 838, 523, 417, 269, 198])
        self.boundary = [[0, 10000], [0, 0.05]]
        self.start = [6300, 0.017]



if __name__ == '__main__':
    data = Data66()
    chi = ChiSquared(data)
    reg_par = chi.optimize()
    print(*reg_par)
    print(np.log(2)/reg_par[1])
    # chi.save_big_plot()
    # chi.save_small_plot()
    # chi.show_big_plot()
    #chi.show_small_plot()
