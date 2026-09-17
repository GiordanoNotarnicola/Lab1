import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

##Immagine e acquisizione dei punti

def click(evento):
    print(round(evento.xdata), ",", round(evento.ydata))

file_path="C:/Users\Angelo\Desktop\immagine catenaria.jpg"
grafico=plt.figure("catenaria")
img = matplotlib.image.imread(file_path)
plt.xlabel("x [pixels]")
plt.ylabel("y [pixels]")
plt.imshow(img)
plt.show()
cid=grafico.canvas.mpl_connect('button_press_event', click)

x, y=np.loadtxt("C:/Users/Angelo/Desktop/dati catenaria.txt", unpack=True, delimiter=',')
y=1000-y



##Definizione della funzione

def catenaria(x, a, c, x0):
    return c + a*np.cosh((x-x0)/a)


##Incertezze di misura e fit del grafico
sigma_x=np.full(x.shape, 1.)
sigma_y=np.full(y.shape, 1.)

popt, pcov = curve_fit(catenaria, x, y, sigma=sigma_y,  p0=(240.,-84., 518. ), absolute_sigma=True)
a_hat, c_hat, x0_hat=popt
sigma_a, sigma_c, sigma_x0= np.sqrt(pcov.diagonal())

res = y - catenaria(x, a_hat, c_hat, x0_hat)

sigma_eff = np.sqrt(sigma_y**2.0 + (np.sinh((x-x0_hat)/a_hat) * sigma_x)**2.0)
popt, pcov = curve_fit(catenaria, x, y, sigma=sigma_eff, p0=(240, -84, 518))
chisq = sum(((y - catenaria(x, *popt)) / sigma_eff)**2.0)
print(popt, np.sqrt(pcov.diagonal()))
print(chisq)

##plot del grafico

#Definizione del grafico e degli assi
grafico = plt.figure('Grafico della catenaria e dei residui')
ax1, ax2 = grafico.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))
grafico.align_ylabels((ax1, ax2))

#Grafico del fit
ax1.errorbar(x, y, sigma_eff, fmt='.', label='Dati', color='black')
xgrid = np.linspace(80, 950, 1100)
ax1.plot(xgrid, catenaria(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax1.set_ylim(-100, 1100)
ax1.set_xlim(80, 950)
ax1.set_ylabel('y [pixels]')
ax1.grid(color='lightgray', ls='dashed')
ax1.legend()

#Grafico dei residui
ax2.errorbar(x, res, sigma_eff, fmt='.', color='black')
ax2.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
ax2.set_xlabel('x [pixels]')
ax2.set_ylabel('Residui [pixels]')
ax2.grid(color='lightgray', ls='dashed')

plt.show()

##Parabola

def parabola(x, a, b, c):
    return a*x**2+b*x+c

popt, pcov = curve_fit(parabola, x, y, p0=(100, -200, 300))
a_p, b_p, c_p=popt
sigma_a_p, sigma_b_p, sigma_c_p= np.sqrt(pcov.diagonal())

res_p = y -parabola(x, a_p, b_p, c_p)

sigma_eff_p = np.sqrt(sigma_y**2.0 + ((2*a_p*x+b_p) * sigma_x)**2.0)
popt, pcov = curve_fit(parabola, x, y, sigma=sigma_eff_p, p0=(100, -200, 300))
chisq_p = sum(((y - parabola(x, *popt)) / sigma_eff_p)**2.0)
print(popt, np.sqrt(pcov.diagonal()))
print(chisq_p)

grafico_p=plt.figure('Grafico del fit con una parabola')
ax3, ax4=grafico_p.subplots(2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05))
grafico_p.align_ylabels((ax3, ax4))

ax3.errorbar(x, y, sigma_eff_p, fmt='.', label='Dati', color='black')
xgrid = np.linspace(80, 950, 1100)
ax3.plot(xgrid, parabola(xgrid, *popt), label='Modello di best-fit', color='lightgrey')
ax3.set_ylim(-100, 1100)
ax3.set_xlim(80, 950)
ax3.set_ylabel('y [pixels]')
ax3.grid(color='lightgray', ls='dashed')
ax3.legend()

ax4.errorbar(x, res, sigma_eff_p, fmt='.', color='black')
ax4.plot(xgrid, np.full(xgrid.shape, 0.0), color='lightgrey')
ax4.set_xlabel('x [pixels]')
ax4.set_ylabel('Residui [pixels]')
ax4.grid(color='lightgray', ls='dashed')

plt.show()














