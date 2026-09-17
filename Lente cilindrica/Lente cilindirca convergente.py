import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import odr

##Dati raccolti
p= np.array([27.9, 27.7, 27.5, 27.1, 25.8, 24.8, 23.3, 20.9, 15.6, 1.5])
q=np.array([69.0, 67.0, 65.0, 63.0, 61.0, 59.0, 57.0, 55.0, 53.0, 51.0])
p=40-p
q=q-40
sigma_p1=np.array([0.2, 0.2, 0.2, 0.3, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5])
sigma_q1=np.full(q.shape, 0.1)
sigma_p= sigma_p1/p**2
sigma_q= sigma_q1/q**2
r=27.0/(2*np.pi)
sigma_r= 0.2/(2*np.pi)

##Definiamo la funzione e i parametri di fit con sigma eff

def retta(x, m, q):
    return m*x + q


popt, pcov= curve_fit(retta, 1/p, 1/q, sigma=sigma_q, absolute_sigma=True)
m_hat, f_hat=popt

for i in range(1):
    sigma_eff = np.sqrt(sigma_q**2.0 + (m_hat* sigma_p)**2.0)
    popt,pcov= curve_fit(retta, 1/p, 1/q, sigma=sigma_eff, absolute_sigma=True)
    m_hat, f_hat=popt
    sigma_m, sigma_f=  np.sqrt(pcov.diagonal())
    res=1/q-retta(1/p, m_hat, f_hat)
    chisq= sum((res/sigma_eff)**2)

# def hype(p, f):
#     return 1/p - 1/f
#
# popt1, pcov1= curve_fit(hype, p, q, sigma=sigma_q1)


print("il coefficiente angolare è:",m_hat, sigma_m, "l'intercetta è:",f_hat, sigma_f)
print("il chi quadro è:", chisq)

##Definiamo funzione e parametri del fit con odr
def fit_model(pars, x):
    return pars[0]*x+ pars[1]

model=odr.Model(fit_model)
data=odr.RealData(1/p, 1/q, sx=sigma_p, sy= sigma_q)
alg=odr.ODR(data, model, beta0=(1., 1.))
out=alg.run()
n_hat, d_hat= out.beta
sigma_n, sigma_d= np.sqrt(out.cov_beta.diagonal())
chi=out.sum_square
print('odr è:', n_hat, d_hat, sigma_d, sigma_n, chi)
d_hat= 1/d_hat
sigma_d=sigma_d/d_hat**2
ref_odr=r/(2*d_hat-r)



##Grafico del fit

grafico=plt.figure("grafico della funzione e dei residui")
ax1, ax2 = grafico.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))
grafico.align_ylabels((ax1, ax2))

#Grafico del fit
ax1.errorbar(1/p, 1/q, sigma_eff, fmt='o', label='Dati', color='black')
xgrid = np.linspace(0, 2, 10)
ax1.plot(xgrid, retta(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax1.set_ylim(0.025, 0.11)
ax1.set_xlim(0.02, 0.09)
ax1.set_ylabel('q [cm]')
ax1.grid(color='lightgray', ls='dashed')
ax1.legend()

#Grafico dei residui
ax2.errorbar(1/p, res, sigma_eff, fmt='o', color='black')
ax2.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
ax2.set_xlabel('p [cm]')
ax2.set_ylabel('Residui [cm]')
ax2.grid(color='lightgray', ls='dashed')

plt.show()

##Trovare la refrattività
f_hat=1/f_hat
sigma_f=sigma_f/f_hat**2

ref=r/(2*f_hat-r)
sigma_ref=2*np.sqrt((r*sigma_f)**2+(f_hat*sigma_r)**2)/((2*f_hat-r)**2)
print(ref, sigma_ref)


##dati con -1 costante
# refrattività[0.34065139] [0.01691462]
#1/f [0.11826069] [0.00040976]











