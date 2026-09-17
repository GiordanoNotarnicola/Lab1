# Fit oscill.py
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
t, x, t2, x2=np.loadtxt("C:/Users/Angelo/Desktop/Università Fisica/Laboratorio 1/Pendolo accoppiato/2PendControfase.txt", unpack=True)
x-=474
t-=66.379
sigma_t = np.full(t.shape, 0.000001)
sigma_x = np.full(x.shape, 0.289)
def cosine(t, A, w, phi, C, tau):
    return A*np.e**(-t/tau)*np.cos(w*t+phi)+C
popt1, pcov1 = curve_fit(cosine, t, x, p0=(40, 4.45, 100, -0.5, 26),sigma=sigma_x, absolute_sigma = True)#1PendSmorz
A_hat, w_hat, phi_hat, C_hat, tau_hat = popt1
sigma_A, sigma_w, sigma_phi, sigma_C, sigma_tau= np.sqrt(pcov1.diagonal())
for i in range(4):
    sigma_eff = np.sqrt(sigma_x**2.0 +((A_hat*(w_hat*np.sin(w_hat*t+phi_hat)*np.cos(w_hat*t+phi_hat)*sigma_t)**2.0)))
    popt1,pcov1= curve_fit(cosine, t, x, sigma=sigma_eff, absolute_sigma=True)
    A_hat, w_hat, phi_hat, C_hat, tau_hat = popt1
    sigma_A, sigma_w, sigma_phi, sigma_C, sigma_tau= np.sqrt(pcov1.diagonal())
res1=x-cosine(t, *popt1)
chisq1= sum((res1/sigma_eff)**2)
print('#Battimenti \n A: ', f'{A_hat:.4f}', f'{sigma_A:.4f}', 'wp: ', f'{w_hat:.4f}', f'{sigma_w:.4f}', 'phi: ', f'{phi_hat:.4f}', f'{sigma_phi:.4f}', 'C: ',f'{C_hat:.4f}', f'{sigma_C:.4f}','tau' , f'{tau_hat:.4f}', f'{sigma_tau:.4f}' '\n Ilchi quadro è', f'{chisq1:.4f}\n')
##grafico
fig = plt.figure('Grafico')
ax1, ax2 = fig.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1],
hspace=0.05))
ax1.errorbar(t, x, sigma_x, sigma_t, fmt='o', label='Dati', color='black')
xgrid = np.linspace(0.0, 100, 1000000)
ax1.plot(xgrid, cosine(xgrid, *popt1), label='Modello di best-fit',
color='lightgrey')
#plt.ylim(-0.01, 8.2)
plt.xlim(-0.2, 11.8)
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