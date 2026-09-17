import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#Misure
x = np.array([0.0, 25.0, 50.0, 75.0, 100.0, 125.0, 150.0, 175.0, 200.0, 225.0, 250.0, 275.0, 300.0, 325.0, 350.0])
sigma_x = np.full(x.shape, 0.3)
T = np.array([48.4, 47.6, 47.3, 46.7, 46.4, 45.5, 43.6, 43.0, 42.4, 42.1, 41.7, 41.3, 41.1, 40.7, 40.4])
sigma_T = np.full(T.shape, 0.2)

x=x/1000
sigma_x=sigma_x/1000

#Funzione per il fit
def line(x, m, q):
    return m * x + q

#Fit
popt, pcov = curve_fit(line, x, T, sigma=sigma_T)
m_hat, q_hat = popt
sigma_m, sigma_q = np.sqrt(pcov.diagonal())
print(m_hat, sigma_m, q_hat, sigma_q)

#Calculate the residuals with respect to the best-fit model.
res = T - line(x, *popt)

chi_quadro=sum((res/sigma_T)**2)
print("il chi quadro è:",chi_quadro )

#Plot
fig = plt.figure('Grafico della temperatura in funzione del tempo e dei residui')
ax1, ax2 = fig.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))

# Main plot: the scatter plot of x vs. y, on the top panel.
ax1.errorbar(x, T, sigma_T, sigma_x, fmt='o', label='Dati', color='black')
# Grid e best-fit
xgrid = np.linspace(0.0, 10.0, 100)
ax1.plot(xgrid, line(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax1.set_ylim(38, 50)
# Setup the axes, grids and legend.
ax1.set_ylabel('Temperatura [°C]')
ax1.grid(color='lightgray', ls='dashed')
ax1.legend()
# And now the residual plot, on the bottom panel.
ax2.errorbar(x, res, sigma_T, sigma_x, fmt='o', color='black')
# model in the residual representation.
ax2.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
# Setup the axes, grids and legend.
ax2.set_xlabel('Posizione [m]')
ax2.set_ylabel('Residui [°C]')
ax2.grid(color='lightgray', ls='dashed')

plt.xlim(-0.01, 0.365)
fig.align_ylabels((ax1, ax2))

plt.savefig('AlluminioT(x).pdf')
plt.show()