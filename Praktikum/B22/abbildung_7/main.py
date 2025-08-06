from Zeichnungen import *
from data_file import *

#plot_list = [0:name, 1:plot style, 2:linear, 3:linear start, 4:fit, 5:table number, 6:y lable, 7:x start, 8:show label,9:y_start]


def fit(number, save = False):
    table = Plotter(plot_list[number][5], plot_list[number][6], plot_list[number][0], save=save, x_start=plot_list[number][7], y_start=plot_list[number][9])
    if plot_list[number][1] == "normal":
        table.plot(linear=plot_list[number][2], start=plot_list[number][3], fit=plot_list[number][4], lin_label=plot_list[number][8])
    if plot_list[number][1] == "voltage":
        table.plot_voltage()


def save_fits():
    for i in range(1, 10):
        print(i)
        fit(i, True)



if __name__ == '__main__':
    #save_fits()
    fit(1, True)
