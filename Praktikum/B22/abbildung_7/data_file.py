import numpy as np

_table1 = np.array([
    [435.4, 3.3, 63.6, 0.2],
    [469.4, 3.4, 62.2, 0.2],
    [481.6, 3.5, 61.8, 0.2],
    [509.3, 3.6, 61.0, 0.2],
    [546.5, 3.7, 60.2, 0.2],
    [577.6, 3.8, 59.7, 0.2],
    [644.8, 4, 58.8, 0.2]
])

search_values = np.array([59.7, 60.2, 60.4, 61.6, 61.9, 62.7, 62.9, 63.1])

data_set = [[], _table1]

# [0:name, 1:plot style, 2:linear, 3:linear start, 4:fit, 5:table number, 6:y lable, 7:x start, 8:show label]
plot_list = [
    [],
    ["Winkeldispersionskurve von Prisma 3", "normal",  True,   577.5,     3,      1,  "δmin (°)", 430, "δmin (°)", 58]
]
