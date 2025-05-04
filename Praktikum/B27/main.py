from Zeichnungen import *
from data_file import *

#plot_list = [0:name, 1:plot style, 2:linear, 3:linear start, 4:fit, 5:table number, 6:y lable]


def fit(number, save = False):
    table = Plotter(plot_list[number][5], number, plot_list[number][6], plot_list[number][0], save=save)
    if plot_list[number][1] == "normal":
        table.plot(linear = plot_list[number][2], start= plot_list[number][3], fit= plot_list[number][4])
    if plot_list[number][1] == "voltage":
        table.plot_voltage()

def fit1(save=False):
    table = Plotter(1, 1,"Durchlassrichtung GE-Diode")
    table.plot(start=0.6, fit="cube")

def fit2(save=False):
    table = Plotter(2,2,"Sperrichtung GE-Diode")
    table.plot(linear = False, fit="lin")

def fit3(save=False):
    table = Plotter(1,3, "Widerstand GE-Diode","Widerstand GE-Diode (Ω)" )
    table.plot_voltage()

def fit4(save=False):
    table = Plotter(3,4,"Durchlassrichtung Si-Diode")
    table.plot(start=0.6)

def fit5(save=False):
    table = Plotter(4,5,"Sperrichtung Si-Diode")
    table.plot(linear = False, fit="lin")

def fit6(save=False):
    table = Plotter(5,6,"Durchlassrichtung Zenerdiode")
    table.plot(start=0.7)

def fit7(save=False):
    table = Plotter(6,7,"Sperrrichtung Zenerdiode")
    table.plot(start=1.8)

def fit8(save=False):
    table = Plotter(7,8, "Spannungsangleichung Zenerdiode")
    table.plot(start=0.7)

def fit9(save=False):
    table = Plotter(8,9,"Durchlassrichtung LED")
    table.plot(start=1.75)

def save_fits():
    for i in range(1,10):
        if i != 8:
            print(i)
            fit(i, True)

if __name__ == '__main__':
    save_fits()
    #fit(2)
