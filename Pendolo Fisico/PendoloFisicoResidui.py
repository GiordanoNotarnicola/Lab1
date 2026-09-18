import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Misure
d = np.array([3.2, 8.9, 13.2, 18.9, 23.2, 28.9, 33.2, 38.9, 43.2, 48.9])
sigma_d = np.full(d.shape, 0.144)
T = np.array([3.45, 2.12, 1.81, 1.63, 1.56, 1.53, 1.54, 1.56, 1.60, 1.64])
sigma_T = np.array([0.071, 0.024, 0.009, 0.005, 0.004, 0.004, 0.005, 0.006, 0.004, 0.003])

# d = np.array([ 8.9, 13.2, 18.9, 23.2, 28.9, 33.2, 38.9, 43.2, 48.9])
# sigma_d = np.full(d.shape, 0.14)
# T = np.array([ 2.091, 1.803, 1.614, 1.564, 1.551, 1.542, 1.564, 1.604, 1.641])
# sigma_T = np.array([ 0.024, 0.009, 0.005, 0.004, 0.004, 0.005, 0.005, 0.004, 0.003])

d=d/100
sigma_d=sigma_d/100
# Definizione dell’accelerazione di gravita‘
g = 9.81

def period_model(d, l):
    return 2.0 * np.pi * np.sqrt((l**2.0 / 12.0 + d**2.0) / (g * d))


#Fit
popt, pcov = curve_fit(period_model, d, T, sigma=sigma_T)
l_hat = popt[0]
sigma_l = np.sqrt(pcov[0, 0])
print(l_hat, sigma_l)
#Calculate the residuals with respect to the best-fit model.
res = T - period_model(d, *popt)

chi_square=sum((res/sigma_T)**2)
print("il chi quadro è:",chi_square)

#Plot
fig = plt.figure('Grafico del tempo in funzione del tempo e dei residui')
ax1, ax2 = fig.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.1))

# Main plot: the scatter plot of x vs. y, on the top panel.
ax1.errorbar(d, T, sigma_T, sigma_d, fmt='o', label='Dati', color='black')
# Grid and best-fit
xgrid = np.linspace(0.0, 1.0, 100)
ax1.plot(xgrid, period_model(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax1.set_ylim(1.2, 3.6)
# Setup the axes, grids and legend.
ax1.set_ylabel('Periodo [s]')
ax1.grid(color='lightgray', ls='dashed')
ax1.legend()
# And now the residual plot, on the bottom panel.
ax2.errorbar(d, res, sigma_T, sigma_d, fmt='o', color='black')
# This will draw a horizontal line at y=0, which is the equivalent of the best-fit
# model in the residual representation.
ax2.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
# Setup the axes, grids and legend.
ax2.set_xlabel('Distanza [m]')
ax2.set_ylabel('Residui [s]')
ax2.grid(color='lightgray', ls='dashed')

plt.xlim(0.0, 0.52)
fig.align_ylabels((ax1, ax2))

plt.savefig('T(d)senza0.pdf')
plt.show()