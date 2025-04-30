import math
import datetime
import numpy as np
import matplotlib.pyplot as plt


def calculate(raw_data):
    scale = [val[0] for val in raw_data]
    rel = calc_relative(raw_data)
    poisson, info = calc_poisson(raw_data, rel)

    return scale, rel, poisson, info


def calc_relative(raw_data):
    _data = [val[1] for val in raw_data]
    count = 0
    for _ in _data:
        count += _
    relative = []
    for _ in _data:
        relative.append(_/count)
    return relative


def calc_poisson(raw_data, rel):
    repetitions = [val[0] for val in raw_data]
    expected_value = 0
    n = 0
    for _ in repetitions:
        expected_value += _*rel[_]
        n += raw_data[_][1]
    poisson = []
    for k in repetitions:
        temp = (expected_value**k)/math.factorial(k)*math.exp(-expected_value)
        poisson.append(temp)
        info = [expected_value, (expected_value/n)**0.5, n]
    return poisson, info


def search_index(_data, target):
    for _ in _data:
        if _[0] == target:
            return i


def plot(_data):
    x_values, rel_occurrence, poisson, junk = _data

    bar_width = 1
    x_indexes = np.arange(len(x_values))
    plt.figure(figsize=(7, 7))
    plt.bar(x_indexes, rel_occurrence, width=bar_width, label='relative Häufigkeit', hatch='||', alpha=1,
            edgecolor='black', facecolor='none', linewidth=0.8)
    plt.bar(x_indexes, poisson, width=bar_width, label='Poisson-Wahrscheinlichkeit', hatch='//', alpha=1,
            edgecolor='black', facecolor='none', linewidth=0.8)

    plt.xlabel('Ereignisse')
    plt.ylabel('Wahrscheinlichkeit')
    plt.title('Vergleich Poisson-Wahrscheinlichkeit mit relativer Häufigkeit', loc='left', y=1.04)
    plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(0.0125))
    plt.yticks(np.arange(0, max(max(rel_occurrence), max(poisson)), 0.025))
    plt.xticks(x_indexes, x_values)
    plt.legend()
    plt.tick_params(axis='both', which="both", direction='in', top=True, right=True)

    plt.figtext(1, 1.035, f"Marius Trabert, {datetime.datetime.now().strftime('%d. %B %Y')}", ha='right', va='top',
                transform=plt.gca().transAxes, fontsize=10)
    plt.xlim(-0.5, 8.5)
    plt.show()


if __name__ == '__main__':
    legend = ["Ereignisse:\t\t\t\t\t", "Relative Häufigkeit:\t\t", "Poisson Wahrscheinlichkeit:\t", "µ,σ,n:\t\t\t\t\t\t"]
    data = [[0, 23], [1, 83], [2, 71], [3, 74], [4, 45], [5, 19], [6, 16], [7, 3], [8, 2]]
    calc = calculate(data)
    for i in range(len(calc)):
        print(legend[i], calc[i])
    plot(calc)
