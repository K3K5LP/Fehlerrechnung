import numpy as np
from scipy.stats import poisson

# non functional
def _lump_data(data):
    output = []
    iteration = 0
    for i in range(len(data)):
        if iteration == 0:
            summation = data[i][1]
            add = [data[i][0]]
            while summation < 5:
                iteration += 1
                if i + iteration >= len(data):
                    print(output)
                    last = []
                    for u in range(len(output)):
                        last.append(output[u][0])
                        print(last)
                    for u in range(len(add)):
                        last.append(add[u])
                        print(last)
                    add = last
                    print(last)
                    summation = output[-1][1]
                else:
                    add.append(i+iteration)
                    summation += data[i+iteration][1]
            output.append([add, summation])
        else:
            iteration -= 1
    return output
    "out of range fehler beheben"

# not needed
def _calculate_mean(data):
    data = np.array(data)
    x_vals = data[:, 0].astype(int)
    y_vals = data[:, 1]

    # Estimate λ as the weighted mean
    total_counts = np.sum(y_vals)
    lam = np.sum(x_vals * y_vals) / total_counts
    return lam


class Calculate:

    def __init__(self, data, mean):
        self.data = data
        self.samples = self.summate()
        # self.lump = _lump_data()
        self.mean = mean
        self.length = len(data)-1
        self.poisson = self.get_poisson()
        self.chi2 = self.get_chi()

    def summate(self):
        summation = 0
        for i in self.data:
            summation += i[1]
        return summation

    def get_poisson(self):
        probs = poisson.pmf(np.arange(self.length), mu=self.mean)

        tail = poisson.sf(self.length - 1, mu=self.mean)

        scaled_probs = (probs * self.samples).tolist()
        scaled_probs.append(float(tail * self.samples))

        return scaled_probs

    def get_chi(self):
        chi2 = 0
        for [_, o], e in zip(self.data, self.poisson):
            if e == 0:
                continue
            chi2 += (o - e) ** 2 / e
        # chi2 = chi2/self.length
        return chi2


if __name__ == '__main__':
    data_trim = [[0, 40], [1, 85], [2, 92], [3, 62], [4, 25], [5, 19], [6, 13]]
    # data = [[0, 40], [1, 85], [2, 92], [3, 62], [4, 25], [5, 19],[6, 7], [7,4],[8,2]]
    mean = 2.036
    # mean = 2.16
    calc = Calculate(data_trim, mean)

    print(calc.poisson)
    print(calc.chi2)
