import numpy as np
import statsmodels.api as sm
import math


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


class Calculations:
    def __init__(self, _data):
        self.data = _data
        self.degree = 2
        self._error = 0.05
        self.test_value = 90

        self.curvature_matrix = np.zeros((self.degree + 1, self.degree + 1))
        self._calculate_matrix()

        self.covar = np.linalg.inv(self.curvature_matrix)

        self.errors = np.sqrt(np.diag(self.covar))

        self.gaus_error = 0
        self.cov_error = 0
        self.parameters = np.array([])
        self._calc_params()

        self.best_value = self.parameters @ np.array([1, self.test_value, self.test_value**2])
        self.out = self._output()

    def _output(self):
        gaus = round_sigfig(self.best_value, self.gaus_error)
        cov = round_sigfig(self.best_value, self.cov_error)
        out = f"Krümmungsmatrix:\n{self.curvature_matrix}\n"\
              f"Kovarianzmatrix:\n{self.covar}\n"\
              f"params:\n{self.parameters}\n"\
              f"errors:\n{self.errors}\n"\
              f"gaus error:\n({gaus[0]} ± {gaus[1]})mV\n"\
              f"covariant error:\n({cov[0]} ± {cov[1]})mV"
        return out

    def _calc_params(self):
        beta = np.array([0.0, 0.0, 0.0])
        for i in range(self.degree + 1):
            for (x, y) in zip(self.data.x_data, self.data.y_data):
                beta[i] += (1 / (self._error ** 2)) * y * (x ** i)
        print(beta)

        self.parameters = self.covar @ beta

        deriv_sum = 0
        for i in range(self.degree + 1):
            deriv_sum += self.test_value ** (2*i) * self.errors[i]**2
        self.gaus_error = np.sqrt(deriv_sum)

        test_vector = np.array([1, self.test_value, self.test_value**2])

        self.cov_error = np.sqrt(test_vector @ self.covar @ test_vector)

    def _calculate_matrix(self):
        for i in range(self.degree+1):
            for j in range(self.degree+1):
                for (x, y) in zip(self.data.x_data, self.data.y_data):
                    self.curvature_matrix[i][j] += (1/(self._error**2))*(x**i)*(x**j)

    @staticmethod
    def quad(x, a, b, c):
        return a * x ** 2 + b * x + c


# Daten:
class Data66:
    def __init__(self):
        self.x_data = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])
        self.y_data = np.array([-0.261, -0.087, -0.071, -0.114, -0.020, 0.114, 0.032, 0.224, 1.297, 1.405, 1.764,
                                1.621, 2.159, 2.287, 2.120, 2.454, 2.979, 3.092, 3.237, 3.096, 3.282])


class Data59:
    def __init__(self):
        self.x_data = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])
        self.y_data = np.array([-0.185, -0.129, 0.004, -0.096, -0.117, 0.096, 0.069, 0.231, 1.265, 1.371, 1.716,
                                1.514, 2.163, 2.535, 2.258, 2.481, 2.942, 3.174, 3.132, 3.127, 3.360])


class Data16:
    def __init__(self):
        self.x_data = np.array(
            [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])
        self.y_data = np.array([
            -0.629, -0.322, -0.183, -0.186, -0.227, 0.186, 0.166, 0.633, 1.023, 1.118,
            1.540, 1.600, 1.836, 2.097, 2.219, 2.445, 2.707, 2.940, 3.267, 3.356, 3.465
        ])


class Data19:
    def __init__(self):
        self.x_data = np.array(
            [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])
        self.y_data = np.array([
    -0.486, -0.250, -0.159, -0.156, -0.140, 0.156, 0.174, 0.488, 0.939, 1.203,
    1.558, 1.622, 1.875, 2.134, 2.239, 2.479, 2.738, 2.895, 3.207, 3.410, 3.450])


class Datavorlesung:
    def __init__(self):
        self.x_data = np.array(
            [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])
        self.y_data = np.array([
    -0.849, -0.738, -0.537, -0.354, -0.196, -0.019, 0.262, 0.413, 0.734, 0.882,
    1.258, 1.305, 1.541, 1.768, 1.935, 2.147, 2.456, 2.676, 2.994, 3.200, 3.318])


class Datakorr:
    def __init__(self):
        self.x_data = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])
        self.y_data = np.array([-0.735, -0.616, -0.394, -0.186, -0.005, 0.198, 0.515, 0.680, 1.015, 1.162, 1.517,
                                1.560, 1.774, 1.981, 2.137, 2.339, 2.646, 2.873, 3.207, 3.422, 3.543])


if __name__ == '__main__':
    data = Data59()
    calc = Calculations(data)
    print(calc.out)
