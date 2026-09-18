import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


##Dati raccolti
t, T, t_T=np.loadtxt("C:/Users/Angelo/Desktop/aabbcc.txt", unpack=True)
sigma_t=np.full(t.shape, 0.0001)
sigma_T=np.full(T.shape, 0.0001)
sigma_t_T=np.full(t_T.shape, 0.0001)
g=9.805
w=0.01965
sigma_w=0.00005
l=1.115
sigma_l=0.005
d=1.135
sigma_d=0.005
v_0=(w*l)/(t_T*d)
sigma_v_0=np.sqrt((l*sigma_w/(t_T*d))**2+(w*sigma_l/(t_T*d))**2+(w*l*sigma_t_T/(d*t_T**2))**2+(w*l*sigma_d/(t_T*d**2))**2)
theta_0=np.arccos(1-(v_0**2/(2*g*l)))
sigma_theta_0=np.sqrt(1/(1-(1-(v_0**2/(2*g*l)))**2)*((v_0*sigma_v_0/(g*l))**2+(v_0**2*sigma_l/(2*g*l**2))**2))

##Definizione delle funzioni e parametri di fit

#Tempo caratteristico

def exp(t, k, v_1):
    return v_1*np.e**(-k*t)

popt, pcov=curve_fit(exp, t, v_0, p0=(0.0002, 1), sigma=sigma_v_0,  absolute_sigma=True)
k_hat, v_1_hat=popt
sigma_k, sigma_v_1=np.sqrt(pcov.diagonal())
res=v_0-exp(t, k_hat, v_1_hat)
chisq=sum((res/sigma_v_0)**2)
tau=1/k_hat
sigma_tau=sigma_k/k_hat**2
print("il tempo caratteristico é", tau, "la sua incertezza", sigma_tau, "il chi quadro è", chisq)
print('v0', v_1_hat, sigma_v_1)

#Termini superiori al primo del periodo del pendolo

def period(theta_0, T_0):
    return T_0*(1+(theta_0**2)/16+(11/3072)*theta_0**4)

popt1, pcov1=curve_fit(period, theta_0, T, sigma=sigma_T, absolute_sigma=True)
T_0_hat=popt1
sigma_T_0=np.sqrt(pcov1.diagonal())
for i in range(4):
    sigma_eff = np.sqrt(sigma_T**2.0 + ((theta_0/8+(11/768)*theta_0**3)*sigma_theta_0)**2.0)
    popt1,pcov1= curve_fit(period, theta_0, T, sigma=sigma_eff, absolute_sigma=True)
    T_0_hat=popt1
    sigma_T_0=np.sqrt(pcov1.diagonal())
    res1=T-period(theta_0, T_0_hat)
    chisq1= sum((res1/sigma_eff)**2)

print('i parametri t0 sono', T_0_hat, 'le loro incertezze', sigma_T_0, 'il chi quadro è', chisq1)

##Plot dei grafici

# #fit tempo caratteristico
grafico=plt.figure(1)
ax1, ax2 =grafico.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))
grafico.align_ylabels((ax1, ax2))

ax1.errorbar(t, v_0, sigma_v_0, fmt='.', label='Dati', color='black')
xgrid = np.linspace(-1, 1100)
ax1.plot(xgrid, exp(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax1.set_ylim(0, 2.5)
ax1.set_xlim(0, 750)
ax1.set_ylabel("velocità nel punto più basso [m/s]")
ax1.grid(color='lightgray', ls='dashed')

ax2.errorbar(t, res, sigma_v_0, fmt='.', color='black')
ax2.plot(xgrid, np.full(xgrid.shape, 0), color='lightgrey')
ax2.set_xlabel("t[s]")
ax2.set_ylabel('Residui')
ax2.grid(color='lightgray', ls='dashed')

plt.show()

#grafico periodo in funzione del tempo

# figure=plt.figure(2)
# figure.align_ylabels(ax3)
# ax3.errorbar(t, T, yerr=sigma_T, xerr=sigma_t, fmt='o', label='Data', ecolor='blue')
# ax3.set_xlim(0,30)
# ax3.set_ylim(0, 420)
# ax3.set_xlabel('Tempo [s]')
# ax3.set_ylabel('Periodi [s]')
# ax3.grid(color='lightgray', ls='dashed')
# plt.show()

#fit sviluppo in serie del periodo del pendolo

grafico1=plt.figure(3)
ax5, ax6=grafico1.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))
grafico1.align_ylabels((ax5, ax6))

ax5.errorbar(theta_0, T, sigma_eff, fmt='.', label='Dati', color='blue')
xgrid = np.linspace(-1, 1110, 20000)
ax5.plot(xgrid, period(xgrid, *popt1), label='Modello di best-fit', color='black')
ax5.set_ylim(2.095, 2.165)
ax5.set_xlim(0.15, 0.75)
ax5.set_ylabel("T[s]")
ax5.grid(color='lightgray', ls='dashed')

ax6.errorbar(theta_0, res1, sigma_eff, fmt='.', color='black')
ax6.plot(xgrid, np.full(xgrid.shape, 0), color='lightgrey')
ax6.set_xlabel("Ampiezza di oscillazione [rad]")
ax6.set_ylabel('Residui')
ax6.grid(color='lightgray', ls='dashed')

plt.show()


















