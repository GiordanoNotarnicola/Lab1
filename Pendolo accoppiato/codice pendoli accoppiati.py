# Fit Battimenti.py

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
t, x, t2, x2=np.loadtxt("C:/Users/Angelo/Desktop/Università Fisica/Laboratorio 1/Pendolo accoppiato/Battimenti3.txt", unpack=True)
x-=471
t-=15.436
#p0=(82, 4.54, 0.09, 0, 1.52, 0.025)
sigma_t = np.full(t.shape, 0.001)
sigma_x = np.full(x.shape, 0.289)
def cosine(t, A, wp, wb, phip, phib, tau):
    return 2*A*np.cos(wp*t+phip)*np.cos(wb*t+phib)*np.e**(-t*tau)
popt1, pcov1 = curve_fit(cosine, t, x, p0=(64.17, 4.5, 0.09, 4.33, 1.56, 0.0116), sigma=sigma_x, absolute_sigma = True)
A_hat, wp_hat, wb_hat, phip_hat, phib_hat, tau_hat = popt1
sigma_A, sigma_wp, sigma_wb, sigma_phip, sigma_phib, sigma_tau = np.sqrt(pcov1.diagonal())
popt1,pcov1= curve_fit(cosine, t, x, sigma=sigma_x, absolute_sigma=True)
res1=x-cosine(t, *popt1)
chisq1= sum((res1/sigma_x)**2)
print('#Battimenti \n A:', f'{A_hat:.4f}', f'{sigma_A:.4f}', 'wp: ', f'{wp_hat:.4f}', f'{sigma_wp:.4f}', 'wb: ', f'{wb_hat:.4f}', f'{sigma_wb:.4f}', 'phip: ',f'{phip_hat:.4f}', f'{sigma_phip:.4f}', 'phib: ', f'{phib_hat:.4f}', f'{sigma_phib:.4f}','tau: ', f'{tau_hat:.4f}', f'{sigma_tau:.4f}' '\n Il chi quadro è',f'{chisq1:.4f}\n')
##grafico
fig = plt.figure('Grafico')
ax1, ax2 = fig.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1],
hspace=0.05))
ax1.errorbar(t, x, sigma_x, sigma_t, fmt='o', label='Dati', color='black')
xgrid = np.linspace(0.0, 100, 1000000)
ax1.plot(xgrid, cosine(xgrid, 64.17, 4.53, 0.09, 4.33, 1.564, 0.0116),
label='Modello di best-fit', color='lightgrey')
#plt.ylim(-0.01, 8.2)
plt.xlim(-0.01, 37.5)
ax1.set_ylabel('Ampiezza di oscillazione [u]')
ax1.grid(color='lightgray', ls='dashed')
#ax1.legend()
ax2.errorbar(t, res1, sigma_x, sigma_t, fmt='o', label='Dati', color='black')
ax2.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
ax2.set_xlabel('Tempi [s]')
ax2.set_ylabel('Residui [u]')
ax2.grid(color='lightgray', ls='dashed')
plt.show()
#plt.savefig('Smorzamento.pdf')