import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#Misure sfere
m = np.array([44.8150, 21.7430, 11.8830, 8.3620, 3.5260])
sigma_m = np.full(m.shape, 0.0003)
d = np.array([22.230, 17.460, 14.290, 12.700, 9.520])
sigma_d = np.full(d.shape, 0.003)
# Calcolo del volume
r = d / 2.0
sigma_r = sigma_d / 2.0
V = 4.0 / 3.0 * np.pi * r**3.0
sigma_V = V * 3.0 * sigma_d / d

def line(x, m):
    return m * x

def power_law(x, norm, index):
    return norm * (x**index)



# Perform the fit...
popt, pcov = curve_fit(line, m, V, sigma=sigma_V, p0=0)
m_hat = popt
sigma_m = np.sqrt(pcov.diagonal())
print(m_hat, sigma_m)
# ...and calculate the residuals with respect to the best-fit model.
res = V - line(m, *popt)

# Create the main figure...
fig = plt.figure('Grafico della temperatura in funzione del tempo e dei residui')

ax1, ax2 = fig.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))

# Main plot: the scatter plot of x vs. y, on the top panel.
ax1.errorbar(m, V, sigma_V, sigma_m, fmt='o', label='Dati', color='black')
# Plot the best-fit model on a dense grid.
xgrid = np.linspace(0.0, 48.0, 100)
ax1.plot(xgrid, line(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
#ax1.set_ylim(0, 5900)
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
plt.xlim(-0.01, 48)

fig.align_ylabels((ax1, ax2))
plt.savefig('Sfere_V(m).pdf')

plt.show()

plt.figure('Grafico massa-raggio')
plt.errorbar(r, m, sigma_m, sigma_r, fmt='o', color='black')
popt, pcov = curve_fit(power_law, r, m)
norm_hat, index_hat = popt
sigma_norm, sigma_index = np.sqrt(pcov.diagonal())
print(norm_hat, sigma_norm, index_hat, sigma_index)
k=norm_hat*3/4/np.pi
sigma_k=sigma_norm*3/4/np.pi
print(k, sigma_k)
x = np.linspace(4., 20., 100)
plt.plot(x, power_law(x, norm_hat, index_hat), color='lightgrey')

plt.yscale('log')
plt.xscale('log')
plt.xlabel('Raggio [mm]')
plt.ylabel('Massa [g]')
plt.grid(which='both', ls='dashed', color='gray')
plt.savefig('Bilog_m(r).pdf')



plt.show()
