import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2

##Indice di rifrazione del plexigas


r=8.10
sigma_r=0.05/np.sqrt(12)
sin_i=np.array([1.0, 2.3, 3.5, 4.5, 5.4, 6.0, 6.7, 7.3, 7.6, 7.7])/r
sin_r=np.array([0.8, 1.6, 2.3, 3.1, 3.7, 4.1, 4.5, 4.9, 5.1, 5.2])/r
sigma_l=0.2/np.sqrt(12)
sigma_r=np.sqrt((r*sigma_l)**2+(sin_r*sigma_r)**2)/r**2
sigma_i=np.sqrt((r*sigma_l)**2+(sin_i*sigma_r)**2)/r**2
def line(sin_r, m):
    return m*sin_r

popt,pcov=curve_fit(line, sin_r, sin_i, sigma=sigma_i, absolute_sigma=True)
n_hat=popt
df=sin_i.size-popt.size
for i in range(1):
    sigma_eff=np.sqrt(sigma_i**2+(n_hat*sigma_r)**2)
    popt,pcov=curve_fit(line, sin_r, sin_i, sigma=sigma_eff, absolute_sigma=True)
    n_hat=popt
    sigma_n=np.sqrt(pcov.diagonal())
    res=sin_i-line(sin_r, n_hat)
    chisq=sum((res/sigma_eff)**2)
    p_value=chi2.cdf(chisq, df)-chi2.cdf(0, df)
    if p_value>0.5:
        p_value=1-p_value
    else:
        p_value=p_value

print("La refrattività del vetro è", n_hat-1,'±',sigma_n)
print(chisq)
print(p_value)
grafico=plt.figure(1)
ax1, ax2 =grafico.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))
grafico.align_ylabels((ax1, ax2))

#Grafico del fit
ax1.errorbar(sin_r, sin_i, sigma_eff, fmt='o', label='Dati', color='black')
xgrid = np.linspace(-1, 1)
ax1.plot(xgrid, line(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax1.set_ylim(0, 1)
ax1.set_xlim(0, 0.7)
ax1.set_ylabel(r'$\sin\theta_i$')
ax1.grid(color='lightgray', ls='dashed')


#Grafico dei residui
ax2.errorbar(sin_r, res, sigma_eff, fmt='o', color='black')
ax2.plot(xgrid, np.full(xgrid.shape, 0), color='lightgrey')
ax2.set_xlabel(r'$\sin\theta_r$')
ax2.set_ylabel('Residui')
ax2.grid(color='lightgray', ls='dashed')

plt.show()

##Lunghezza focale lente divergente

p=np.array([34.5, 37.5, 28.3, 30.2, 29.0, 31.5, 33.0, 37.0, 27.5, 30.5])
p=p-48.5
q=np.array([20.0, 16.0, 46.0, 37., 47.5, 35., 27., 17., 54.5, 34.5])
sigma_p=np.full(p.shape, 0.51)
sigma_q=np.full(q.shape, 0.50)
sigma_p= sigma_p/p**2
sigma_q= sigma_q/q**2

def retta(x, m, q):
    return m*x + q


popt1, pcov1= curve_fit(retta, 1/p, 1/q, sigma=sigma_q, absolute_sigma=True)
m_hat, f_hat=popt1
df1=7
for i in range(1):
    sigma_eff1 = np.sqrt(sigma_q**2.0 + (m_hat* sigma_p)**2.0)
    popt1,pcov1= curve_fit(retta, 1/p, 1/q, sigma=sigma_eff1, absolute_sigma=True)
    m_hat, f_hat=popt1
    sigma_m, sigma_f=  np.sqrt(pcov1.diagonal())
    res=1/q-retta(1/p, m_hat, f_hat)
    chisq= sum((res/sigma_eff1)**2)
    p_value1=chi2.cdf(chisq, df1)-chi2.cdf(0, df1)
    if p_value1>0.5:
        p_value1=1-p_value1
    else:
        p_value1=p_value1


print("il coefficiente angolare è:",m_hat, sigma_m, "l'intercetta è:",f_hat, sigma_f)
print("il chi quadro è:", chisq)


##Grafico del fit

figure=plt.figure(2)
ax3, ax4 = figure.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))
figure.align_ylabels((ax3, ax4))

#Grafico del fit
ax3.errorbar(1/p, 1/q, yerr=sigma_eff1, fmt='o', label='Dati', color='black')
xgrid = np.linspace(-3, 2, 10)
ax3.plot(xgrid, retta(xgrid, *popt1), label='Modello di best-fit', color='lightgrey')
ax3.set_ylim(0.01, 0.08)
ax3.set_xlim(-0.1, -0.04)
ax3.set_ylabel('1/q [cm$^{-1}$]')
ax3.grid(color='lightgray', ls='dashed')
ax3.legend()

#Grafico dei residui
ax4.errorbar(1/p, res, sigma_eff1, fmt='o', color='black')
ax4.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
ax4.set_xlabel('1/p [cm$^{-1}$]')
ax4.set_ylabel('Residui [cm$^{-1}$]')
ax4.grid(color='lightgray', ls='dashed')

plt.show()



















