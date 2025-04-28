import math
import datetime
import numpy as np
import matplotlib.pyplot as plt

def calculate(raw_data):
    scale = [val[0] for val in raw_data]
    rel = calc_relative(raw_data)
    poisson = calc_poisson(raw_data, rel)

    return scale, rel, poisson

def calc_relative(raw_data):
    data = [val[1] for val in raw_data]
    count = 0
    for i in data:
        count += i
    relative = []
    for i in data:
        relative.append(i/count)
    return relative

def calc_poisson(raw_data, rel):
    repetitions = [val[0] for val in raw_data]
    expected_value = 0
    for i in repetitions:
        expected_value += i*rel[i]
    poisson = []
    for k in repetitions:
        temp = (expected_value**k)/math.factorial(k)*math.exp(-expected_value)
        poisson.append(temp)
    return poisson

def search_index(data, target):
    for i in data:
        if i[0] == target:
            return i

def plot(data):
    x_values, RelHäuf, poisson = data
    #Values = [[0, 11], [1, 80], [2, 74], [3, 71], [4, 48], [5, 28], [6, 13], [7, 9], [8, 2]]
    #RelHäuf = [1,2,3,4,5,6,7,8,9]
    #poisson = [1,2,3,4,5,6,7,8,9]


    bar_width = 1
    x_indexes = np.arange(len(x_values))
    plt.figure(figsize=(8, 4))
    plt.bar(x_indexes, RelHäuf, width=bar_width, label='relative Häufigkeit', hatch='||', alpha=1, edgecolor='black',
            facecolor='none', linewidth=0.8)
    plt.bar(x_indexes, poisson, width=bar_width, label='Poissonwahrscheinlichkeit', hatch='//', alpha=1,
            edgecolor='black', facecolor='none', linewidth=0.8)

    plt.xlabel('Ereignisse')
    plt.ylabel('Wahrscheinlichkeit')
    plt.title('Vergleich Poissonwahrscheinlichkeit mit relativer Häufigkeit', loc='left',y=1.05)
    plt.xticks(x_indexes, x_values)
    plt.legend()
    plt.tick_params(axis='both', direction='in')

    plt.figtext(1, 1.05, f"Marius Trabert, {datetime.datetime.now().strftime("%d. %B %Y")}", ha='right', va='top', transform=plt.gca().transAxes, fontsize=10)
    plt.figtext(0,  1.05, "[Histogramm 1]", fontsize=10, ha="left",va="top",transform=plt.gca().transAxes)
    plt.xlim(-0.5, 8.5)
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = [[0, 11], [1, 80], [2, 74], [3, 71], [4, 48], [5, 28], [6, 13], [7, 9], [8, 2]]
    plot(calculate(data))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
