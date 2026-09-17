import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#Misure sfere
m = np.array([10.5800,16.41, 24.6150, 34.8450])
sigma_m = np.full(m.shape, 0.0003)
V = np.array([1249.44,1945.70, 2898.31, 4114.88])
sigma_V = np.array([3.06, 1.69, 7.03, 1.78])

def line(x, m):
    return m * x

# Perform the fit...
popt, pcov = curve_fit(line, m, V, sigma=sigma_V)
m_hat= popt
sigma_m= np.sqrt(pcov.diagonal())
rho=1/m_hat
sigma_rho=1/m_hat**2*sigma_m
print(rho, sigma_rho)
# ...and calculate the residuals with respect to the best-fit model.
res = V - line(m, *popt)

# Create the main figure...
fig = plt.figure('Grafico del volume in funzione della massa e dei residui')

ax1, ax2 = fig.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))

# Main plot: the scatter plot of x vs. y, on the top panel.
ax1.errorbar(m, V, sigma_V, sigma_m, fmt='o', label='Dati', color='black')
# Plot the best-fit model on a dense grid.
xgrid = np.linspace(0.0, 48.0, 100)
ax1.plot(xgrid, line(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax1.set_ylim(0, 6300)
# Setup the axes, grids and legend.
ax1.set_ylabel('Volume [mm$^3$]')
ax1.grid(color='lightgray', ls='dashed')
ax1.legend()
# And now the residual plot, on the bottom panel.
ax2.errorbar(m, res, sigma_V, sigma_m, fmt='o', color='black')
# This will draw a horizontal line at y=0, which is the equivalent of the best-fit
# model in the residual representation.
ax2.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
# Setup the axes, grids and legend.
ax2.set_xlabel('Massa [g]')
ax2.set_ylabel('Residui [mm$^3$]')
ax2.grid(color='lightgray', ls='dashed')

# The final touch to main canvas :-)
plt.xlim(-0.01, 40)

fig.align_ylabels((ax1, ax2))
plt.savefig('CilindriePrismiOttone_V(m).pdf')



plt.show()