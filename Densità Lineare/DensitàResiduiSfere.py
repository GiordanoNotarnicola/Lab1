import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#Misure
ms = np.array([44.8150, 21.7430, 11.8830, 8.3620, 3.5260])
sigma_ms = np.full(ms.shape, 0.0003)
d = np.array([22.230, 17.460, 14.290, 12.700, 9.520])
sigma_d = np.full(d.shape, 0.003)

V = np.array([5751.98, 2786.96, 1527.90, 1072.53, 451.76])
sigma_V = V * 3.0 * sigma_d / d

#Funzione per il fit
def line(x, m):
    return m * x

#Fit
popt, pcov = curve_fit(line, ms, V, sigma=sigma_V, p0=0.0)
m_hat = popt
sigma_m, = np.sqrt(pcov.diagonal())
rho=1/m_hat
sigma_rho=1/m_hat**2*sigma_m
print(rho, sigma_rho)
#Calculate the residuals with respect to the best-fit model.
res = V - line(ms, *popt)

#Plot
fig = plt.figure('Grafico della temperatura in funzione del tempo e dei residui')
ax1, ax2 = fig.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))

# Main plot: the scatter plot of x vs. y, on the top panel.
ax1.errorbar(ms, V, sigma_V, sigma_ms, fmt='o', label='Dati', color='black')
# Grid and best-fit
xgrid = np.linspace(0.0, 50.0, 100)
ax1.plot(xgrid, line(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
#ax1.set_ylim(0, 5900)
# Setup the axes, grids and legend.
ax1.set_ylabel('Volume [mm$^3$]')
ax1.grid(color='lightgray', ls='dashed')
ax1.legend()
# And now the residual plot, on the bottom panel.
ax2.errorbar(ms, res, sigma_V, sigma_ms, fmt='o', color='black')
# This will draw a horizontal line at y=0, which is the equivalent of the best-fit
# model in the residual representation.
ax2.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
# Setup the axes, grids and legend.
ax2.set_xlabel('Massa [g]')
ax2.set_ylabel('Residui [mm$^3$]')
ax2.grid(color='lightgray', ls='dashed')

plt.xlim(-0.01, 47)
fig.align_ylabels((ax1, ax2))


plt.show()