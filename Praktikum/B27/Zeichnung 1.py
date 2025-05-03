import numpy as np
import matplotlib.pyplot as plt

# Daten mit neuen Spannungswerten

Table3 = np.array([
    [0.004, 0.000500399840127872, 0.0, 0.002],
    [0.1001, 0.000500399840127872, 0.0, 0.002],
    [0.201, 0.000600333240792145, 0.0, 0.002],
    [0.30159, 0.000600333240792145, 0.001, 0.002],
    [0.40034, 0.000600333240792145, 0.016, 0.002],
    [0.49901, 0.000600333240792145, 0.209, 0.002],
    [0.58576, 0.000600333240792145, 1.394, 0.002],
    [0.6487, 0.000701141925718324, 5.18, 0.004],
    [0.68398, 0.000703491293478462, 10.602, 0.007]
])
Table1 = np.array([
    [0.0087,  0.000500399840127872, 0.0,     0.002],
    [0.10688, 0.000500399840127872, 0.022,   0.002],
    [0.19873, 0.000600333240792145, 0.187,   0.002],
    [0.29447, 0.000600333240792145, 0.613,   0.002],
    [0.38771, 0.000600333240792145, 1.229,   0.002],
    [0.48001, 0.000600333240792145, 1.979,   0.002],
    [0.57167, 0.000700642562224134, 2.833,   0.003],
    [0.66302, 0.000700642562224134, 3.768,   0.003],
    [0.75334, 0.000701141925718324, 4.766,   0.004],
    [0.84197, 0.000701141925718324, 5.803,   0.004],
    [0.93181, 0.00080156097709407,  6.909,   0.005],
    [1.01945, 0.000802246844805263, 8.035,   0.006],
    [1.10871, 0.000802246844805263, 9.229,   0.006],
    [1.19626, 0.000803056660516554, 10.444,  0.007],
])

Table5 = np.array([
    [0.0088,  0.000500399840127872, 0.0,    0.002],
    [0.1,     0.000500399840127872, 0.0,    0.002],
    [0.2009,  0.000600333240792145, 0.0,    0.002],
    [0.3016,  0.000600333240792145, 0.0,    0.002],
    [0.399,   0.000600333240792145, 0.0,    0.002],
    [0.49907, 0.000600333240792145, 0.003,  0.002],
    [0.59855, 0.000600333240792145, 0.065,  0.002],
    [0.69204, 0.000700285656000464, 0.886,  0.002],
    [0.75662, 0.000701141925718324, 4.318,  0.004],
    [0.79488, 0.000703491293478462, 10.472, 0.007]
])

data = Table5

# Extrahieren
volt = data[:, 0]
current = data[:, 2]
current_err = data[:, 3]

# Fehlerbalken plotten
plt.errorbar(volt, current, yerr=current_err, fmt='x', ecolor='gray', capsize=3, label='Messwerte', color="black")
# Polynom 3. Ordnung fitten
coeffs = np.polyfit(volt, current, 5)
poly = np.poly1d(coeffs)
# Fitkurve berechnen
volt_fit = np.linspace(min(volt), max(volt), 500)
current_fit = poly(volt_fit)
current_fit = np.clip(current_fit, 0, None)
print(poly)
# Plot
plt.plot(volt_fit, current_fit, 'r-', label=f'Kubischer Fit: {poly}')


# Lineare Regression im quasi-linearen Bereich (ab 0.3 V bis 1.0 V)
mask_linear = (volt >= 0.5) & (volt <= 1.2)
slope, intercept = np.polyfit(volt[mask_linear], current[mask_linear], 1)
linear_fit = slope * volt_fit + intercept
# Verhindert negative Werte bei der linearen Regression
linear_fit = np.clip(linear_fit, 0, None)
# entfernen negativer Werte
linear_fit = np.where(linear_fit > 0, linear_fit, np.nan)
# Plot der Ausgleichsgeraden im linearen Bereich
plt.plot(volt_fit, linear_fit, 'g--', label=f'Linear-Fit: y = {slope:.2f}x + {intercept:.2f}')



plt.xlabel('Spannung (V)')
plt.ylabel('Strom (mA)')
plt.title('Strom-Spannungs-Kennlinie mit kubischem Fit')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
