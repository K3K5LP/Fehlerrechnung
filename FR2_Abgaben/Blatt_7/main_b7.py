import numpy as np

class Calculations:
    def __init__(self, data):
        self.data = data
        self.degree = 2
        self.error = 0.05

        self.curvature_matrix = np.zeros((self.degree + 1, self.degree + 1))
        self._calculate_matrix()

        self.covar = np.linalg.inv(self.curvature_matrix)

    def _calculate_matrix(self):
        for i in range(self.degree+1):
            for j in range(self.degree+1):
                for (x, y) in zip(self.data.x_data, self.data.y_data):
                    self.curvature_matrix[i, j] += (1/(self.error**2))*(x**i)*(x**j)


class Data66:
    def __init__(self):
        self.x_data = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        self.y_data = [-0.261, -0.087, -0.071, -0.114, -0.020, 0.114, 0.032, 0.224, 1.297, 1.405, 1.764,
                       1.621, 2.159, 2.287, 2.120, 2.454, 2.979, 3.092, 3.237, 3.096, 3.282]


class Data59:
    def __init__(self):
        self.x_data = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        self.y_data = [-0.185, -0.129, 0.004, -0.096, -0.117, 0.096, 0.069, 0.231, 1.265, 1.371, 1.716,
                       1.514, 2.163, 2.535, 2.258, 2.481, 2.942, 3.174, 3.132, 3.127, 3.360]

class Datakorr:
    def __init__(self):
        self.x_data = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        self.y_data = [-0.735, -0.616, -0.394, -0.186, -0.005, 0.198, 0.515, 0.680, 1.015, 1.162, 1.517,
     1.560, 1.774, 1.981, 2.137, 2.339, 2.646, 2.873, 3.207, 3.422, 3.543]

if __name__ == '__main__':
    data = Datakorr()
    calc = Calculations(data)
    print(calc.curvature_matrix)
    print(calc.covar)
