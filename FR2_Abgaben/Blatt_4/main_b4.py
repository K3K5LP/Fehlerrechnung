from scipy import odr
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator
import datetime


def quadratic(x, c, b, a):
    return a*x**2 + b*x + c


class LinReg:
    def __init__(self, _data):
        self.y_data = np.array([(val[0]-1)/50 for val in _data])
        print(self.y_data)
        self.x_data = np.array([val[1] for val in _data])
        self.data = odr.Data(self.x_data, self.y_data)
        odr_obj = odr.ODR(self.data, odr.quadratic)
        output = odr_obj.run()
        self.parameters = output.beta
        self.gravitation_constant = self.parameters[0]*2

        X = np.column_stack((self.x_data, self.x_data ** 2))
        X = sm.add_constant(X)

        model = sm.OLS(self.y_data, X)
        results = model.fit()
        self.parameters = results.params

        print(results.summary())


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
        label_txt = f"Ausgleichsgerade:\n" \
                    f"B⋅x + A"
        """undertitle = f"Werte der Ausgleichsgeraden betragen:\n" \
                     f"Steigung B: ({slope} ±{slope_err})(g/(°C⋅m³))\n" \
                     f"Ordinaten-verschiebung A: ({intercept} ±{intercept_err})(g/m³)"""
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
        # self._graph.figtext(0.125, 0.04, undertitle)

        self._graph.legend()

    def show_plot(self):
        self._graph.show()

    def save_plot(self):
        self._graph.savefig(f"Graphs/Blatt_3", dpi=600)


if __name__ == '__main__':
    data = [[1, 0], [2, 0.071392], [3, 0.096313], [4, 0.115116], [5, 0.132797], [6, 0.146310],
            [7, 0.159318], [8, 0.171935], [9, 0.183410], [10, 0.194732], [11, 0.204436], [12, 0.214176],
            [13, 0.223948], [14, 0.232436], [15, 0.240200]]
    reg = LinReg(data)
    print(reg.parameters)
    print(reg.gravitation_constant)
    plot = Plot(reg)
    plot.show_plot()


