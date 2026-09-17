import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Misure dirette---mettete i vostri numeri!
# Qui potete anche leggere i dati da file, usando il metodo np.loadtxt(),
# se lo trovate comodo.
t = np.array([0.0, 0.0333, 0.0666, 0.1, 0.1333, 0.1666, 0.2, 0.2333, 0.2666, 0.3,
0.3333, 0.3666, 0.4, 0.4333, 0.4666, 0.5, 0.5333, 0.5666])
sigma_t=np.full(t.shape, 0.0001 )
h = np.array([198.5, 196.5, 192, 186.5, 179.5, 172.0, 163.5, 152.5,
141.0, 129.5, 117.0, 102.5, 86.5, 69.5, 51.5, 32.5, 11.5, -7])
sigma_h = np.array([0.29, 0.34, 0.39, 0.44, 0.49, 0.54, 0.59, 0.64, 0.69, 0.74, 0.79, 0.84, 0.89, 0.94, 0.99, 1.0, 1.1, 1.1])
# Conversione in m.
h = h / 100.0
sigma_h = sigma_h / 100.0

def parabola(t, a, v0, h0):
    return 0.5 * a * t**2.0 + v0 * t + h0

# Perform the fit...
popt, pcov = curve_fit(parabola, t, h, sigma=sigma_h)
a_hat, v0_hat, h0_hat = popt
sigma_a, sigma_v0, sigma_h0 = np.sqrt(np.diagonal(pcov))
print(a_hat, sigma_a, v0_hat, sigma_v0, h0_hat, sigma_h0)

# ...and calculate the residuals with respect to the best-fit model.
res = h - parabola(t, *popt)

# Create the main figure...
fig = plt.figure('Un grafico dei residui')
# ...and make space for the two plots. Note that `gridspec_kw` and `hspace`
# control the arrangements of the two sub-panels within the figure, see
# https://matplotlib.org/stable/api/_as_gen/matplotlib.gridspec.GridSpec.html
ax1, ax2 = fig.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))

# Main plot: the scatter plot of x vs. y, on the top panel.
ax1.errorbar(t, h, sigma_h, fmt='o', label='Dati', color='black')
# Plot the best-fit model on a dense grid.
xgrid = np.linspace(-1.0, 10.0, 100)
ax1.plot(xgrid, parabola(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax1.set_ylim(-0.3, 2.2)
# Setup the axes, grids and legend.
ax1.set_ylabel('h [m]')
ax1.grid(color='lightgray', ls='dashed')
ax1.legend()

# And now the residual plot, on the bottom panel.
ax2.errorbar(t, res, sigma_h, fmt='o', color='black')
# This will draw a horizontal line at y=0, which is the equivalent of the best-fit
# model in the residual representation.
ax2.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
# Setup the axes, grids and legend.
ax2.set_xlabel('t [s]')
ax2.set_ylabel('Residui [m]')
ax2.grid(color='lightgray', ls='dashed')

# The final touch to main canvas :-)
plt.xlim(-0.01, 0.6)
fig.align_ylabels((ax1, ax2))


plt.show()
