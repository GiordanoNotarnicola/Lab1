import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

##Dati raccolti
p= np.array([ 27.7, 27.5, 27.1, 25.8, 24.8, 23.3, 20.9, 15.6, 1.5])
q=np.array([ 67.0, 65.0, 63.0, 61.0, 59.0, 57.0, 55.0, 53.0, 51.0])
p=40-p
q=q-40
sigma_p=np.sqrt(np.array([ 0.2,  0.2, 0.3, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5])**2+0.1**2)
sigma_q=np.full(q.shape, 0.1*np.sqrt(2))
r=27.0/(2*np.pi)
sigma_r= 1/(2*np.pi)

##Definiamo la funzione e i parametri di fit

def retta(p, f):
    return (p*f)/(p-f)


popt, pcov= curve_fit(retta, p, q, sigma=sigma_q, absolute_sigma=True)
f_hat=popt

for i in range(4):
    sigma_eff = np.sqrt(sigma_q**2.0 + (sigma_p*((f_hat/(p-f_hat))**2.0))**2.0)
    popt,pcov= curve_fit(retta, p, q, sigma=sigma_eff, absolute_sigma=True)
    f_hat=popt
    sigma_f=  np.sqrt(pcov.diagonal())
    res=q-retta(p, f_hat)
    chisq= sum((res/sigma_eff)**2)




print("la distanza focale è:",f_hat, sigma_f)
print("il chi quadro è:", chisq)

##Grafico del fit

grafico=plt.figure("grafico della funzione e dei residui")
ax1, ax2 = grafico.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))
grafico.align_ylabels((ax1, ax2))

#Grafico del fit
ax1.errorbar(p, q, sigma_eff, fmt='o', label='Dati', color='black')
xgrid = np.linspace(0, 60, 200)
ax1.plot(xgrid, retta(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax1.set_ylim(10, 35)
ax1.set_xlim(10, 40.0)
ax1.set_ylabel('q [cm]')
ax1.grid(color='lightgray', ls='dashed')
ax1.legend()

#Grafico dei residui
ax2.errorbar(p, res, sigma_eff, fmt='o', color='black')
ax2.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
ax2.set_xlabel('p [cm]')
ax2.set_ylabel('Residui [cm]')
ax2.grid(color='lightgray', ls='dashed')

plt.show()

##Trovare la refrattività
sigma_f=sigma_f

ref=r/(2*f_hat-r)
sigma_ref=2*np.sqrt((r*sigma_f)**2+(f_hat*sigma_r)**2)/((2*f_hat-r)**2)
print(ref, sigma_ref)
